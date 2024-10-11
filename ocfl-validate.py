#!/usr/bin/env python
"""Command line tool to validate an OCFL Storage Root, Object or Inventory.

Validation functions are provided by both the ocfl.py and ocfl-object.py
tools, but these also have features for manipulations. This tool is designed
for validation only, with no options that manipulate stores, objectes or files.
"""
import argparse
import logging
import sys

import ocfl
from ocfl.command_line_utils import add_version_arg, check_version_arg, add_verbosity_args, check_verbosity_args, validate_object, validate_object_inventory


def parse_arguments():
    """Parse command line arguments.

    Will display message and exit if --help/-h or --version arguments are
    supplied.

    Returns Namespace object from argparse parsing of command line arguments.
    """
    parser = argparse.ArgumentParser(
        description='Validate one or more OCFL objects, storage roots or standalone '
        'inventory files. By default shows any errors or warnings, and final '
        'validation status. Use -q to show only errors, -Q to show only validation '
        'status. HAS NO OPTIONS TO MAKE CHANGES TO THE STORAGE ROOT OR OBJECT.')
    parser.add_argument('path', type=str, nargs='*',
                        help='OCFL storage root, object or inventory path(s) to validate')
    parser.add_argument('--very-quiet', '-Q', action='store_true',
                        help="be very quiet, show only validation status not warnings or errors (implies -q)")
    parser.add_argument('--lax-digests', action='store_true',
                        help='allow use of any known digest')
    parser.add_argument('--no-check-digests', action='store_true',
                        help='do not check digest values')

    add_version_arg(parser)
    add_verbosity_args(parser)
    args = parser.parse_args()
    check_version_arg(args)
    check_verbosity_args(args)
    return args


def do_validation(args):
    """Set up and do the validation.

    Arguments:
        args: Namespace object with command line arguments from argparse.

    Returns True if all OK, else False.
    """
    if len(args.path) == 0:
        print("No OCFL paths specified, nothing to do! (Use -h for help)")

    num = 0
    num_good = 0
    num_paths = len(args.path)
    show_warnings = not args.quiet and not args.very_quiet
    show_errors = not args.very_quiet
    for path in args.path:
        num += 1
        path_type = ocfl.find_path_type(path)
        if path_type == 'object':
            logging.debug("Validating OCFL Object at %s", path)
            obj = ocfl.Object(lax_digests=args.lax_digests)
            if validate_object(obj, path,
                               show_warnings=show_warnings,
                               show_errors=show_errors,
                               check_digests=not args.no_check_digests):
                num_good += 1
        elif path_type == 'root':
            logging.debug("Validating OCFL Storage Root at %s", path)
            store = ocfl.StorageRoot(root=path,
                                     lax_digests=args.lax_digests)
            if store.validate(show_warnings=show_warnings,
                              show_errors=show_errors,
                              check_digests=not args.no_check_digests):
                num_good += 1
        elif path_type == 'file':
            logging.debug("Validating separate OCFL Inventory at %s", path)
            obj = ocfl.Object(lax_digests=args.lax_digests)
            if validate_object_inventory(obj, path,
                                         show_warnings=show_warnings,
                                         show_errors=show_errors):
                num_good += 1
        else:
            print("Bad path %s (%s)", path, path_type)
        if num_paths > 1:
            logging.debug(" [%d / %d paths validated, %d / %d VALID]\n", num, num_paths, num_good, num)
    return num_good == num


if __name__ == "__main__":
    aargs = parse_arguments()
    ok = do_validation(aargs)
    if not ok:
        sys.exit(1)
