#!/usr/bin/env python
"""OCFL Object and Inventory Builder."""
import argparse
import logging
import sys

import ocfl


class FatalError(Exception):
    """Exception class for conditions that should abort with message."""


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Manipulate or validate an OCFL object or inventory.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # This should really be done with add_mutually_exclusive_group() but
    # the current argparse doesn't support grouping and a title for that
    # so use a plain group instead and will check later
    commands = parser.add_argument_group(title="Commands (exactly one required)")
    commands.add_argument('--create', action='store_true',
                          help='Create a new object with version 1 files in --srcdir or from --srcbag')
    commands.add_argument('--build', action='store_true',
                          help='Build a new object from version directories in --srcdir')
    commands.add_argument('--update', action='store_true',
                          help='Update an object by adding a new version from files in --srcdir or from --srcbag')
    commands.add_argument('--show', action='store_true',
                          help='Show versions and files in an OCFL object')
    commands.add_argument('--validate', action='store_true',
                          help='Validate an OCFL object (use ocfl-validate.py for more control)')
    commands.add_argument('--extract', action='store', default=None,
                          help='Extract a specific version (or "head") into --dstdir')

    src_params = parser.add_argument_group(title="Source files")
    src_params.add_argument('--srcdir', '--src', action='store',
                            help='Source directory path')
    src_params.add_argument('--srcbag', action='store',
                            help='Source Bagit bag path (alternative to --srcdir)')

    obj_params = parser.add_argument_group(title="OCFL object parameters")
    obj_params.add_argument('--digest', default='sha512',
                            help='Digest algorithm to use')
    obj_params.add_argument('--fixity', action='append',
                            help='Add fixity type to add')
    obj_params.add_argument('--id', default=None,
                            help='Identifier of object')
    obj_params.add_argument('--dstdir', '--dst', action='store', default='/tmp/ocfl-out',
                            help='Destination directory path')
    obj_params.add_argument('--dstbag', action='store',
                            help='Destination Bagit bag path (alternative to --dstdir)')

    # Version metadata and object settings
    ocfl.add_version_metadata_args(obj_params)
    ocfl.add_object_args(obj_params)
    ocfl.add_shared_args(parser)
    args = parser.parse_args()
    ocfl.check_shared_args(args)

    # Require command and only one command
    cmds = ['create', 'build', 'update', 'show', 'validate', 'extract']
    num_cmds = 0
    for cmd in cmds:
        if getattr(args, cmd):
            num_cmds += 1
    if num_cmds != 1:
        raise FatalError("Exactly one command (%s) must be specified" % ', '.join(cmds))

    # Must not specify both srcdir and srcbag
    if args.srcdir and args.srcbag:
        raise FatalError("Must not specify both --srcdir and --srcbag")

    return args


def do_object_operation(args):
    """Implement object operations in a way that can be reused by ocfl-store.py."""
    obj = ocfl.Object(identifier=args.id,
                      digest_algorithm=args.digest,
                      filepath_normalization=args.normalization,
                      forward_delta=not args.no_forward_delta,
                      dedupe=not args.no_dedupe,
                      lax_digests=args.lax_digests,
                      fixity=args.fixity)
    if args.create:
        srcdir = args.srcdir
        metadata = ocfl.VersionMetadata(args=args)
        if args.srcbag is not None:
            srcdir = ocfl.bag_as_source(args.srcbag, metadata)
            if metadata.id is not None:
                if obj.id:
                    if obj.id != metadata.id:
                        raise FatalError("Identifier specified (%s) and identifier from Bagit bag (%s) do not match!" % (obj.id, metadata.id))
                else:
                    obj.id = metadata.id
        elif args.srcdir is None:
            raise FatalError("Must specify either --srcdir or --srcbag containing v1 files when creating an OCFL object!")
        obj.create(srcdir=srcdir,
                   metadata=metadata,
                   objdir=args.objdir)
    elif args.build:
        if args.srcdir is None:
            raise FatalError("Must specify --srcdir containing version directories when building an OCFL object!")
        metadata = ocfl.VersionMetadata(args=args)
        obj.build(srcdir=args.srcdir,
                  metadata=metadata,
                  objdir=args.objdir)
    elif args.update:
        srcdir = args.srcdir
        metadata = ocfl.VersionMetadata(args=args)
        if args.srcbag is not None:
            srcdir = ocfl.bag_as_source(args.srcbag, metadata)
        elif args.srcdir is None:
            raise FatalError("Must specify either --srcdir or --srcbag containing new version files when updating an OCFL object!")
        obj.update(objdir=args.objdir,
                   srcdir=srcdir,
                   metadata=metadata)
    elif args.show:
        obj.show(objdir=args.objdir)
    elif args.validate:
        obj.validate(objdir=args.objdir)
    elif args.extract:
        if args.dstdir and args.dstbag:
            args.dstdir = None  # Override dstdir if dstbag specified
        version = args.extract
        dst = args.dstdir or args.dstbag
        metadata = obj.extract(objdir=args.objdir,
                               version=version,
                               dstdir=dst)
        if args.dstdir:
            print("Extracted content for %s in %s" % (version, dst))
        else:  # args.dstbag
            ocfl.bag_extracted_version(dst, metadata)
            print("Extracted content for %s saved as Bagit bag in %s" % (version, dst))
    else:
        raise FatalError("Command argument not supported!")


if __name__ == "__main__":
    try:
        aargs = parse_arguments()
        logging.basicConfig(level=logging.INFO if aargs.verbose else logging.WARN)
        do_object_operation(aargs)
    except (FatalError, ocfl.ObjectException) as e:
        # Show message but otherwise exit quietly
        print('Error - ' + str(e))
        sys.exit(1)
