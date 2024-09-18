#!/usr/bin/env python
"""Validate an OCFL Object."""
import argparse
import logging
import sys

import ocfl

parser = argparse.ArgumentParser(
    description='Validate one or more OCFL objects, storage roots or standalone '
    'inventory files. By default shows any errors or warnings, and final '
    'validation status. Use -q to show only errors, -Q to show only validation '
    'status.')
parser.add_argument('path', type=str, nargs='*',
                    help='OCFL object, storage root or inventory path(s) to validate')
parser.add_argument('--quiet', '-q', action='store_true',
                    help="Be quiet, do not show warnings")
parser.add_argument('--very-quiet', '-Q', action='store_true',
                    help="Be very quiet, show only validation status (implies -q)")
parser.add_argument('--lax-digests', action='store_true',
                    help='Allow use of any known digest')
parser.add_argument('--no-check-digests', action='store_true',
                    help='Do not check digest values')

ocfl.add_shared_args(parser)
args = parser.parse_args()
ocfl.check_shared_args(args)

logging.basicConfig(level=logging.INFO if args.verbose else logging.WARN)
log = logging.getLogger(name="ocfl-validate")
log.setLevel(level=logging.INFO if args.verbose else logging.WARN)

if len(args.path) == 0:
    print("No OCFL paths specified, nothing to do! (Use -h for help)")

num = 0
num_good = 0
num_paths = len(args.path)
show_warnings = not args.quiet and not args.very_quiet
for path in args.path:
    num += 1
    path_type = ocfl.find_path_type(path)
    if path_type == 'object':
        log.info("Validating OCFL Object at %s", path)
        obj = ocfl.Object(lax_digests=args.lax_digests)
        if obj.validate(path,
                        show_warnings=show_warnings,
                        show_errors=not args.very_quiet,
                        check_digests=not args.no_check_digests):
            num_good += 1
    elif path_type == 'root':
        log.info("Validating OCFL Storage Root at %s", path)
        store = ocfl.Store(root=path,
                           lax_digests=args.lax_digests)
        if store.validate(show_warnings=show_warnings,
                          show_errors=not args.very_quiet,
                          check_digests=not args.no_check_digests):
            num_good += 1
    elif path_type == 'file':
        log.info("Validating separate OCFL Inventory at %s", path)
        obj = ocfl.Object(lax_digests=args.lax_digests)
        if obj.validate_inventory(path,
                                  show_warnings=show_warnings,
                                  show_errors=not args.very_quiet):
            num_good += 1
    else:
        log.error("Bad path %s (%s)", path, path_type)
    if num_paths > 1:
        log.info(" [%d / %d paths validated, %d / %d VALID]\n", num, num_paths, num_good, num)
if num_good != num:
    sys.exit(1)
