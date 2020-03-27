#!/usr/bin/env python
"""Validate an OCFL Object."""
import argparse
import ocfl

parser = argparse.ArgumentParser(description='Validate one or more OCFL objects.')
parser.add_argument('objdir', type=str, nargs=1,
                    help='OCFL object path')
parser.add_argument('--verbose', '-v', action='store_true',
                    help="be more verbose by including warnings")
parser.add_argument('--lax-digests', action='store_true',
                    help='allow use of any known digest')
parser.add_argument('--no-check-digests', action='store_true',
                    help='do not check digest values')

args = parser.parse_args()

ocfl = ocfl.Object(lax_digests=args.lax_digests)
for objdir in args.objdir:
    ocfl.validate(objdir, warnings=args.verbose,
                  check_digests=not args.no_check_digests)
