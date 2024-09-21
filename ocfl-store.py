#!/usr/bin/env python
"""OCFL Storage Root Command Line Tool."""
import argparse
import logging
import sys

import ocfl
from ocfl.command_line_utils import add_version_metadata_args, add_object_args, add_shared_args, check_shared_args, get_storage_root

parser = argparse.ArgumentParser(description='Manpulate or validate an OCFL Storage Root.',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--root',
                    help='OCFL Storage Root path (must be supplied either via --root or $OCFL_ROOT)')
parser.add_argument('--disposition', '-d', default=None,
                    help='Disposition of objects under root')
parser.add_argument('--quiet', '-q', action='store_true',
                    help="be quiet, do not show warnings")

commands = parser.add_mutually_exclusive_group(required=True)
# These commands are actions on the storage root
commands.add_argument('--init', action='store_true',
                      help='Initialize specified storage root')
commands.add_argument('--list', action='store_true',
                      help='List contents specified storage root')
commands.add_argument('--validate', action='store_true',
                      help='Validate a storage root and all of its contents')
commands.add_argument('--add', action='store_true',
                      help='Add object at --src from the storage root')
commands.add_argument('--purge', action='store_true',
                      help='Purge (delete) an object --id from the storage root')
# and these commands act on an object in the store
commands.add_argument('--create-object', action='store_true',
                      help='Create an new object with version 1 from objdir')
commands.add_argument('--show-object', action='store_true',
                      help='Show versions and files in an OCFL object')
commands.add_argument('--validate-object', action='store_true',
                      help='Validate an OCFL object')

# Object property settings
parser.add_argument('--id', default=None,
                    help='identifier of object')
parser.add_argument('--src', default=None,
                    help='source path of object or version')
parser.add_argument('--digest', default='sha512',
                    help='digest type to use')
parser.add_argument('--fixity', action='append',
                    help='add fixity type to add')

# Version metadata and object settings
add_version_metadata_args(parser)
add_object_args(parser)
add_shared_args(parser)
args = parser.parse_args()
check_shared_args(args)

try:
    store = ocfl.Store(root=get_storage_root(args),
                       disposition=args.disposition,
                       lax_digests=args.lax_digests)
    if args.init:
        store.initialize()
    elif args.list:
        store.list()
    elif args.validate:
        store.validate(show_warnings=not args.quiet)
    elif args.add:
        if not args.src:
            raise ocfl.StoreException("Must specify object path with --src")
        store.add(object_path=args.src)
    elif args.purge:
        logging.error("purge not implemented")
    elif args.show_object or args.validate_object:
        if not args.id:
            raise ocfl.StoreException("Must specify id to act on an object in the store")
        objdir = store.object_path(args.id)
        obj = ocfl.Object(identifier=args.id,
                          digest_algorithm=args.digest,
                          forward_delta=not args.no_forward_delta,
                          dedupe=not args.no_dedupe,
                          fixity=args.fixity)
        if args.show_object:
            logging.warning("Object tree\n%s", obj.tree(objdir=args.objdir))
        else:
            logging.error("create/build/validate not implemented")
    else:
        logging.warning("No command, nothing to do.")
except (ocfl.StoreException, ocfl.ObjectException) as e:
    logging.error(str(e))
    sys.exit(1)
