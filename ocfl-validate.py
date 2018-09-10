#!/usr/bin/env python
"""Validate an OCFL Object."""
import argparse
import ocfl

parser = argparse.ArgumentParser(description='Build an OCFL inventory.')
parser.add_argument('path', type=str, nargs=1,
                    help='OCFL object path')
args = parser.parse_args()

ocfl = ocfl.OCFL()
for path in args.path:
    ocfl.validate(path)
