#!/usr/bin/env python
"""OCFL Object and Inventory Builder."""
import argparse
import ocfl

parser = argparse.ArgumentParser(description='Build an OCFL inventory.',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('path', type=str, nargs=1,
                    help='base directory path with a set of version directories')
parser.add_argument('--digest', default='sha512',
                    help='digest type to use')
parser.add_argument('--fixity', action='append',
                    help='add fixity type to add')
parser.add_argument('--id', default=None,
                    help='identifier of object')
parser.add_argument('--created', default=None,
                    help='creation time to be used with version(s) added, else '
                         'current time will be recorded')
parser.add_argument('--message', default='',
                    help='message to be recorded with version(s) added')
parser.add_argument('--name', default='someone',
                    help='name of user adding version(s) to object')
parser.add_argument('--address', default='somewhere',
                    help='address of user adding version(s) to object')
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
parser.add_argument('--ocfl-version', default='draft',
                    help='OCFL specification version')
args = parser.parse_args()

srcdir = args.path[0]

ocfl = ocfl.Object(identifier=args.id,
                   digest_type=args.digest,
                   skips=args.skip,
                   ocfl_version=args.ocfl_version)

ocfl.write_ocfl_object(srcdir=srcdir,
                       created=args.created,
                       message=args.message,
                       name=args.name,
                       address=args.address,
                       forward_delta=not args.no_forward_delta,
                       dedupe=not args.no_dedupe,
                       rename=not args.no_rename,
                       fixity=args.fixity,
                       dstdir=args.dstdir)
