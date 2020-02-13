#!/usr/bin/env python
"""Validate an OCFL Object."""
import argparse
import ocfl

parser = argparse.ArgumentParser(description='Validate one or more OCFL objects.')
parser.add_argument('objdir', type=str, nargs=1,
                    help='OCFL object path')
parser.add_argument('--verbose', '-v', action='store_true',
                    help="be more verbose by including warnings")

args = parser.parse_args()

ocfl = ocfl.Object()
for objdir in args.objdir:
    ocfl.validate(objdir, warnings=args.verbose)
