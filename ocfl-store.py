#!/usr/bin/env python
"""OCFL Storage Root Command Line Tool."""
import argparse
import logging
import sys

import ocfl
from ocfl.command_line_utils import add_version_arg, check_version_arg, check_shared_args, get_storage_root


def add_common_args(parser):
    """Add argparse arguments that are common to many commands."""
    parser.add_argument('--root',
                        help='OCFL Storage Root path (must be supplied either via --root or $OCFL_ROOT). The "zip://" prefix can be used with zipped roots.')
    parser.add_argument('--layout', default=None,
                        help='Layout of objects under storage root')
    parser.add_argument('--lax-digests', action='store_true',
                        help='allow use of any known digest')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help="be more verbose")
    parser.add_argument('--quiet', '-q', action='store_true',
                        help="be quiet, do not show warnings")


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Manpulate or validate an OCFL Storage Root.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    add_version_arg(parser)
    subparsers = parser.add_subparsers(dest='cmd',
                                       help='Show sub-command help with command -h')

    # Separate sub-parsers for each command
    init_parser = subparsers.add_parser('init',
                                        help='Initialize/create storage root')
    add_common_args(init_parser)

    list_parser = subparsers.add_parser('list', help='List contents of storage root')
    add_common_args(list_parser)

    validate_parser = subparsers.add_parser('validate', help='Validate a storage root and optioally its contents')
    add_common_args(validate_parser)
    validate_parser.add_argument('--validate-objects', default=False,
                                 help='validate each object in the storage root (MAY TAKE TIME)')
    validate_parser.add_argument('--check-digests', default=False,
                                 help='if validating each object, also check all digest (MAY TAKE LOTS OF TIME)')
    validate_parser.add_argument('--max_errors', default=100,
                                 help='maximum number of errors to record/show')

    add_parser = subparsers.add_parser('add', help='Add object at --src to the storage root')
    add_common_args(add_parser)
    add_parser.add_argument('--src', default=None,
                            help='source path of object or version')

    purge_parser = subparsers.add_parser('purge', help='Purge (delete) an object --id from the storage root')
    add_common_args(purge_parser)
    purge_parser.add_argument('--id', default=None,
                              help='identifier of object')

    show_parser = subparsers.add_parser('show', help='Show versions and files in an OCFL object')
    add_common_args(show_parser)
    show_parser.add_argument('--id', default=None,
                             help='identifier of object')

    validate_object_parser = subparsers.add_parser('validate-object', help='Validate an OCFL object')
    validate_object_parser.add_argument('--id', default=None,
                                        help='identifier of object')

    args = parser.parse_args()
    check_version_arg(args)
    check_shared_args(args)
    return args


def validate(store, args):
    """Validate storage root with various outputs.

    args - dictionary of options including:
      quiet - do not show warnings if True
      validate_objects - True to validate each object in tree
      check_digests - True to check all digests for each object
      max_error - Maximum number of error to show
    """
    valid = store.validate(show_warnings=not args.quiet,
                           validate_objects=args.validate_objects,
                           check_digests=args.check_digests,
                           max_errors=args.max_errors)
    if store.structure_error is not None:
        print(store.structure_error)
    for (dirpath, messages) in store.errors:
        print(dirpath)
        print(messages)
    print(str(store.log))
    if args.validate_objects:
        if store.good_objects == store.num_objects:
            print("Objects checked: %d / %d are VALID" % (store.good_objects, store.num_objects))
        else:
            valid = False
            print("Objects checked: %d / %d are INVALID" % (store.num_objects - store.good_objects, store.num_objects))
    else:
        print("Did not check OCFL objects")
    if valid:
        print("Storage root %s is VALID" % (store.root))
    else:
        print("Storage root %s is INVALID" % (store.root))


def do_store_operation(args):
    """Do operation on store based on args."""
    store = ocfl.StorageRoot(root=get_storage_root(args),
                             layout_name=args.layout,
                             lax_digests=args.lax_digests)
    if args.cmd == 'init':
        store.initialize()
    elif args.cmd == 'list':
        for (dirpath, identifier) in store.list_objects():
            print("%s -- id=%s" % (dirpath, identifier))
        print("Found %d OCFL Objects under root %s" % (store.num_objects, store.root))
    elif args.cmd == 'validate':
        validate(store, args)
    elif args.cmd == 'add':
        if not args.src:
            raise ocfl.StorageRootException("Must specify object path with --src")
        store.add(object_path=args.src)
    elif args.cmd == 'purge':
        logging.error("purge not implemented")
    elif args.cmd in ('show', 'validate_object'):
        if not args.id:
            raise ocfl.StorageRootException("Must specify id to act on an object in the store")
        objdir = store.object_path(args.id)
        obj = ocfl.Object(identifier=args.id)
        if args.cmd == 'show':
            logging.warning("Object tree\n%s", obj.tree(objdir=objdir))
        else:
            logging.error("validate not implemented")
    else:
        logging.warning("No command, nothing to do.")


if __name__ == "__main__":
    try:
        aargs = parse_arguments()
        do_store_operation(aargs)
    except (ocfl.StorageRootException, ocfl.ObjectException) as e:
        logging.error(str(e))
        sys.exit(1)
