#!/usr/bin/env python
"""OCFL Object and Inventory Builder."""
import argparse
import ocfl

parser = argparse.ArgumentParser(description='Build an OCFL inventory.')
parser.add_argument('path', type=str, nargs=1,
                    help='base directory path with a set of version directories')
parser.add_argument('--digest', default='sha512',
                    help='digest type to use')
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
args = parser.parse_args()

srcdir = args.path[0]
ocfl = ocfl.OCFL(digest_type=args.digest, skips=args.skip)

ocfl.write_ocfl_object(srcdir=srcdir,
                       forward_delta=not args.no_forward_delta,
                       dedupe=not args.no_dedupe,
                       rename=not args.no_rename,
                       dstdir=args.dstdir)
