#!/usr/bin/env python
"""OCFL Object Store Tool."""
import argparse
import logging
import ocfl
import sys

parser = argparse.ArgumentParser(description='Manpulate an OCFL Object Store.',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--root', required=True,
                    help='OCFL Storage Root for this object store')
parser.add_argument('--disposition', '-d', default=None,
                    help='disposition of objects under root')

commands = parser.add_mutually_exclusive_group(required=True)
# These commands are actions on the store
commands.add_argument('--init', action='store_true',
                      help='Initialize an object store at specified --root')
commands.add_argument('--list', action='store_true',
                      help='List contents of object store')
commands.add_argument('--add', action='store_true',
                      help='Add object to object store')
commands.add_argument('--purge', action='store_true',
                      help='Purge (delete) an object from object store')
# and these commands act on an object in the store
commands.add_argument('--create', action='store_true',
                      help='Create an new object with version 1 from objdir')
commands.add_argument('--build', action='store_true',
                      help='Build an new object from version directories in objdir')
commands.add_argument('--show', action='store_true',
                      help='Show versions and files in an OCFL object')
commands.add_argument('--validate', action='store_true',
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
ocfl.add_version_metadata_args(parser)
ocfl.add_object_args(parser)

parser.add_argument('--verbose', '-v', action='store_true',
                    help="be more verbose")

args = parser.parse_args()

logging.basicConfig(level=logging.INFO if args.verbose else logging.WARN)

try:
    store = ocfl.Store(root=args.root, disposition=args.disposition)
    if args.init:
        store.initialize()
    elif args.list:
        store.list()
    elif args.add:
        if not args.src:
            raise ocfl.StoreException("Must specify object path with --src")
        store.add(object_path=args.src)
    elif args.purge:
        logging.error("purge not implemented")
    elif args.create or args.build or args.show or args.validate:
        if not args.id:
            raise ocfl.StoreException("Must specify id to act on an object in the store")
        objdir = store.object_path(args.id)
        obj = ocfl.Object(identifier=args.id,
                          digest_algorithm=args.digest,
                          forward_delta=not args.no_forward_delta,
                          dedupe=not args.no_dedupe,
                          skips=args.skip,
                          ocfl_version=args.ocfl_version,
                          fixity=args.fixity)
        if args.show:
            obj.show(objdir)
        else:
            logging.error("create/build/validate not implemented")
    else:
        logging.warn("Nuttin' happenin' 'round 'ere.")
except (ocfl.StoreException, ocfl.ObjectException) as e:
    logging.error(str(e))
    sys.exit(1)
