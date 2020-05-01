#!/usr/bin/env python
"""Validate an OCFL Object."""
import argparse
import ocfl
import sys

parser = argparse.ArgumentParser(description='Validate one or more OCFL objects. By default shows any errors and final validation status. Use -v for show warnings, -q to show only validation status.')
parser.add_argument('objdir', type=str, nargs='+',
                    help='OCFL object path(s)')
parser.add_argument('--verbose', '-v', action='store_true',
                    help="be more verbose by including warnings")
parser.add_argument('--quiet', '-q', action='store_true',
                    help="be quiet, show only validation status")
parser.add_argument('--lax-digests', action='store_true',
                    help='allow use of any known digest')
parser.add_argument('--no-check-digests', action='store_true',
                    help='do not check digest values')

args = parser.parse_args()

ocfl = ocfl.Object(lax_digests=args.lax_digests)
num_bad = 0
for objdir in args.objdir:
    if not ocfl.validate(objdir,
                         show_warnings=args.verbose and not args.quiet,
                         show_errors=not args.quiet,
                         check_digests=not args.no_check_digests):
        num_bad += 1
if num_bad > 0:
    sys.exit(1)
