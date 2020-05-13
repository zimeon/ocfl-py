#!/usr/bin/env python
"""Validate an OCFL Object."""
import argparse
import ocfl
import sys

parser = argparse.ArgumentParser(
    description='Validate one or more OCFL objects. By default shows any '
    'errors or warnings, and final validation status. Use -q to show only errors, '
    '-Q to show only validation status.')
parser.add_argument('objdir', type=str, nargs='*',
                    help='OCFL object path(s) of objects to validate')
parser.add_argument('--quiet', '-q', action='store_true',
                    help="be quiet, do not show warnings")
parser.add_argument('--very-quiet', '-Q', action='store_true',
                    help="be very quiet, show only validation status (implies -q)")
parser.add_argument('--lax-digests', action='store_true',
                    help='allow use of any known digest')
parser.add_argument('--no-check-digests', action='store_true',
                    help='do not check digest values')

ocfl.add_shared_args(parser)
args = parser.parse_args()
ocfl.check_shared_args(args)

if len(args.objdir) == 0:
    print("No OCFL bject paths specified, nothing to do! (Use -h for help)")
ocfl = ocfl.Object(lax_digests=args.lax_digests)
num_bad = 0
for objdir in args.objdir:
    if not ocfl.validate(objdir,
                         show_warnings=not args.quiet and not args.very_quiet,
                         show_errors=not args.very_quiet,
                         check_digests=not args.no_check_digests):
        num_bad += 1
if num_bad > 0:
    sys.exit(1)
