#!/usr/bin/env python
"""OCFL Object and Inventory Builder."""
import argparse
import logging
import ocfl
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
                          help='Create a new object with version 1 files in srcdir')
    commands.add_argument('--build', action='store_true',
                          help='Build a new object from version directories in srcdir')
    commands.add_argument('--update', action='store_true',
                          help='Update but adding a new version to an OCFL object')
    commands.add_argument('--show', action='store_true',
                          help='Show versions and files in an OCFL object')
    commands.add_argument('--validate', action='store_true',
                          help='Validate an OCFL object')
    commands.add_argument('--extract', action='store', default=None,
                          help='Extract a specific version (or "head") into dstdir')

    src_params = parser.add_argument_group(title="Source files")
    src_params.add_argument('--srcdir', '--src', action='store',
                            help='source directory path')

    obj_params = parser.add_argument_group(title="OCFL object parameters")
    obj_params.add_argument('--digest', default='sha512',
                            help='digest type to use')
    obj_params.add_argument('--fixity', action='append',
                            help='add fixity type to add')
    obj_params.add_argument('--id', default=None,
                            help='identifier of object')
    obj_params.add_argument('--dstdir', '--dst', action='store', default='/tmp',
                            help='destination directory path')

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
    return args


def do_object_operation(args):
    """Implement object operations in a way that can be reused by ocfl-store.py."""
    obj = ocfl.Object(identifier=args.id,
                      digest_algorithm=args.digest,
                      filepath_normalization=args.normalization,
                      skips=args.skip,
                      forward_delta=not args.no_forward_delta,
                      dedupe=not args.no_dedupe,
                      ocfl_version=args.ocfl_version,
                      fixity=args.fixity)
    if args.create:
        if args.srcdir is None:
            raise FatalError("Must specify --srcdir containing v1 files when creating an OCFL object!")
        metadata = ocfl.VersionMetadata(args)
        obj.create(srcdir=args.srcdir,
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
        obj.extract(objdir=args.objdir,
                    version=args.extract,
                    dstdir=args.dstdir)
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
