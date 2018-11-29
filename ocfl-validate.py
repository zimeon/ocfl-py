#!/usr/bin/env python
"""Validate an OCFL Object."""
import argparse
import ocfl

parser = argparse.ArgumentParser(description='Validate one or more OCFL objects.')
parser.add_argument('objdir', type=str, nargs=1,
                    help='OCFL object path')
args = parser.parse_args()

ocfl = ocfl.Object()
for objdir in args.objdir:
    ocfl.validate(objdir)
