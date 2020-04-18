#!/usr/bin/env python
"""OCFL Object and Inventory Builder."""
import argparse
import logging
import ocfl
import bagit
import os.path
import sys


class FatalError(Exception):
    """Exception class for conditions that should abort with message."""

    pass


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Manipulate an OCFL object or inventory.',
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
                          help='Validate an OCFL object')
    commands.add_argument('--extract', action='store', default=None,
                          help='Extract a specific version (or "head") into --dstdir')

    src_params = parser.add_argument_group(title="Source files")
    src_params.add_argument('--srcdir', '--src', action='store',
                            help='Source directory path')
    src_params.add_argument('--srcbag', action='store',
                            help='Source Bagit bag path (alternative to --srcdir)')

    obj_params = parser.add_argument_group(title="OCFL object parameters")
    obj_params.add_argument('--digest', default='sha512',
                            help='digest type to use')
    obj_params.add_argument('--fixity', action='append',
                            help='add fixity type to add')
    obj_params.add_argument('--id', default=None,
                            help='identifier of object')
    obj_params.add_argument('--dstdir', '--dst', action='store', default='/tmp/ocfl-out',
                            help='destination directory path')
    obj_params.add_argument('--dstbag', action='store',
                            help='destination Bagit bag path (alternative to --dstdir)')

    # Version metadata and object settings
    ocfl.add_version_metadata_args(obj_params)
    ocfl.add_object_args(obj_params)
    parser.add_argument('--verbose', '-v', action='store_true',
                        help="be more verbose")
    args = parser.parse_args()

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
                      skips=args.skip,
                      forward_delta=not args.no_forward_delta,
                      dedupe=not args.no_dedupe,
                      lax_digests=args.lax_digests,
                      ocfl_version=args.ocfl_version,
                      fixity=args.fixity)
    if args.create:
        srcdir = args.srcdir
        metadata = ocfl.VersionMetadata(args)
        if args.srcbag:
            bag = bagit.Bag(args.srcbag)
            if not bag.is_valid():
                raise Fatalerror("Source Bagit bag at %s is not valid" % (args.srcbag))
            num_fetch = len(list(bag.fetch_entries()))
            if num_fetch > 0:
                raise Fatalerror("Source Bagit bag at %s includes fetch.txt with %d entries, only locally complete bags supported" % (args.srcbag, num_fetch))
            srcdir = os.path.join(args.srcbag, 'data')
            # Local arguments override but otherwise take metadata from bag-info.txt
            if not args.id and 'External-Identifier' in bag.info:
                obj.identifier = bag.info['External-Identifier']
            if not metadata.created and 'Bagging-Date' in bag.info:
                metadata.created = bag.info['Bagging-Date'] + 'T00:00:00Z'  # FIXME - timezone fudge
            if not metadata.message and 'External-Description' in bag.info:
                metadata.message = bag.info['External-Description']
            if not metadata.name and 'Contact-Name' in bag.info:
                metadata.name = bag.info['Contact-Name']
            if not metadata.address and 'Contact-Email' in bag.info:
                metadata.address = 'mailto:' + bag.info['Contact-Email']
        elif args.srcdir:
            srcdir = args.srcdir
        else:
            raise FatalError("Must specify either --srcdir or --srcbag containing v1 files when creating an OCFL object!")
        obj.create(srcdir=srcdir,
                   metadata=metadata,
                   objdir=args.objdir)
    elif args.build:
        if args.srcdir is None:
            raise FatalError("Must specify --srcdir containing version directories when building an OCFL object!")
        metadata = ocfl.VersionMetadata(args)
        obj.build(srcdir=args.srcdir,
                  metadata=metadata,
                  objdir=args.objdir)
    elif args.update:
        metadata = ocfl.VersionMetadata(args)
        obj.update(objdir=args.objdir,
                   metadata=metadata)
    elif args.show:
        obj.show(objdir=args.objdir)
    elif args.validate:
        obj.validate(objdir=args.objdir)
    elif args.extract:
        if args.dstdir and args.dstbag:
            args.dstdir = None  # Override dstdir if dstbag specified
        version = args.extract
        dst = os.path.join(args.dstdir or args.dstbag)
        version_metadata = obj.extract(objdir=args.objdir,
                                       version=version,
                                       dstdir=dst)
        if args.dstdir:
            print("Extracted content for %s in %s" % (version, dst))
        else: # args.dstbag
            tags = {}
            if version_metadata.id:
                tags['External-Identifier'] = version_metadata.id
            if version_metadata.message:
                tags['External-Description'] = version_metadata.message
            if version_metadata.name:
                tags['Contact-Name'] = version_metadata.name
            if version_metadata.address and version_metadata.address.startswith('mailto:'):
                tags['Contact-Email'] = version_metadata.address[7:]
            bag = bagit.make_bag(dst, bag_info=tags, checksums=['sha512'])
            print("Extracted content for %s saved as Bagit bag in %s" % (version, dst))
    else:
        raise FatalError("Command argument not supported!")


if __name__ == "__main__":
    try:
        args = parse_arguments()
        logging.basicConfig(level=logging.INFO if args.verbose else logging.WARN)
        do_object_operation(args)
    except FatalError as e:
        # Show message but otherwise exit quietly
        print('Error - ' + str(e))
        sys.exit(1)
