#!/usr/bin/env python
"""OCFL Object and Inventory Builder."""
import argparse
import logging
import ocfl


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Build an OCFL inventory.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--srcdir', '--src', action='store',
                        help='source directory path')
    parser.add_argument('--digest', default='sha512',
                        help='digest type to use')
    parser.add_argument('--fixity', action='append',
                        help='add fixity type to add')
    parser.add_argument('--id', default=None,
                        help='identifier of object')
    parser.add_argument('--dstdir', '--dst', action='store', default='/tmp',
                        help='destination directory path')

    commands = parser.add_mutually_exclusive_group(required=True)
    commands.add_argument('--create', action='store_true',
                          help='Create an new object with version 1 from objdir')
    commands.add_argument('--build', action='store_true',
                          help='Build an new object from version directories in objdir')
    commands.add_argument('--show', action='store_true',
                          help='Show versions and files in an OCFL object')
    commands.add_argument('--validate', action='store_true',
                          help='Validate an OCFL object')
    commands.add_argument('--extract', action='store', default=None,
                          help='Extract a specific version (or "head") into dstdir')
    # Version metadata and object settings
    ocfl.add_version_metadata_args(parser)
    ocfl.add_object_args(parser)
    parser.add_argument('--verbose', '-v', action='store_true',
                        help="be more verbose")
    return parser.parse_args()


def do_object_operation(args):
    """Implement object operations in a way that can be reused by ocff-store.py."""
    obj = ocfl.Object(identifier=args.id,
                      digest_algorithm=args.digest,
                      skips=args.skip,
                      forward_delta=not args.no_forward_delta,
                      dedupe=not args.no_dedupe,
                      ocfl_version=args.ocfl_version,
                      fixity=args.fixity)
    if args.create:
        metadata = ocfl.VersionMetadata(args)
        obj.create(srcdir=args.srcdir,
                   metadata=metadata,
                   objdir=args.objdir)
    elif args.build:
        metadata = ocfl.VersionMetadata(args)
        obj.build(srcdir=args.srcdir,
                  metadata=metadata,
                  objdir=args.objdir)
    elif args.show:
        obj.show(path=args.objdir)
    elif args.validate:
        obj.validate(path=args.objdir)
    elif args.extract:
        obj.extract(objdir=args.objdir,
                    version=args.extract,
                    dstdir=args.dstdir)
    else:
        raise Exception("Command argument not supported!")


if __name__ == "__main__":
    args = parse_arguments()
    logging.basicConfig(level=logging.INFO if args.verbose else logging.WARN)
    do_object_operation(args)
