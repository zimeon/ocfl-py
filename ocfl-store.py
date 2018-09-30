#!/usr/bin/env python
"""OCFL Object Store Tool."""
import argparse
import logging
import ocfl

parser = argparse.ArgumentParser(description='Manpulate an OCFL Object Store.',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--root', required=True,
                    help='OCFL Storage Root for this object store')
parser.add_argument('--disposition', '-d', default=None,
                    help='Disposition of objects under roor')
commands = parser.add_mutually_exclusive_group(required=True)
commands.add_argument('--create', action='store_true',
                      help='Create and initialize an object store')
commands.add_argument('--list', action='store_true',
                      help='List contents of object store')
commands.add_argument('--add', action='store_true',
                      help='Add object to object store')
commands.add_argument('--purge', action='store_true',
                      help='Purge (delete) an object from object store')

# Object property settings
parser.add_argument('--id', default=None,
                    help='identifier of object')
parser.add_argument('--src', default=None,
                    help='source path of object or version')
parser.add_argument('--digest', default='sha512',
                    help='digest type to use')
parser.add_argument('--fixity', action='append',
                    help='add fixity type to add')

# Version metadata settings
parser.add_argument('--created', default=None,
                    help='creation time to be used with version(s) added, else '
                         'current time will be recorded')
parser.add_argument('--message', default='',
                    help='message to be recorded with version(s) added')
parser.add_argument('--name', default='someone',
                    help='name of user adding version(s) to object')
parser.add_argument('--address', default='somewhere',
                    help='address of user adding version(s) to object')


parser.add_argument('--default-disposition', '--dd', default='pairtree',
                    help='default disposiion of objects')
parser.add_argument('--skip', action='append', default=['README.md'],
                    help='directories and files to ignore')
parser.add_argument('--no-forward-delta', action='store_true',
                    help='do not use forward deltas')
parser.add_argument('--no-dedupe', '--no-dedup', action='store_true',
                    help='do not use deduplicate files within a version')
parser.add_argument('--no-rename', action='store_true',
                    help='include files in new version if they did not exist with '
                         'same path in previous version')
parser.add_argument('--dstdir', '--dst',
                    help='write OCFL object to a new directory dst')
parser.add_argument('--verbose', '-v', action='store_true',
                    help="be more verbose")
# parser.add_argument('path', type=str, nargs=1,
#                     help='base directory path with a set of version directories')
args = parser.parse_args()

logging.basicConfig(level=logging.INFO if args.verbose else logging.WARN)

try:
    store = ocfl.Store(root=args.root, disposition=args.disposition,
                       default_disposition=args.default_disposition)
    if args.create:
        store.create()
    elif args.list:
        store.list()
    elif args.add:
        store.add(object_path=args.src)
    else:
        logging.warn("Nuttin' happenin' 'round ere.")
except (ocfl.StoreException, ocfl.ObjectException) as e:
    logging.error(str(e))
