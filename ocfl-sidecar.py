#!/usr/bin/env python
"""OCFL inventory sidecar generator and updater."""
import argparse
import logging
import os.path

import ocfl
from ocfl.command_line_utils import add_version_arg, check_version_arg, add_verbosity_args, check_verbosity_args


def parse_arguments():
    """Parse command line arguments.

    Will display message and exit if --help/-h or --version arguments are
    supplied.

    Returns Namespace object from argparse parsing of command line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Update OCFL inventory sidecar file for each inventory "
        "path specified. Usually used without the --digest argument and the "
        "digest algorithm is extracted from the inventory. However, if "
        "given, the --digest parameter will force use of the specified "
        "digest algorithm.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("path", type=str, nargs="*",
                        help="OCFL inventory file or directory containing one, repeatable")
    parser.add_argument("--digest", default=None,
                        help="digest algorithm to use overriding any in inventory")
    add_version_arg(parser)
    add_verbosity_args(parser)
    args = parser.parse_args()
    check_version_arg(args)
    check_verbosity_args(args)
    return args


def create_sidecar(args, directory):
    """Create sidecar for inventory in dir."""
    inventory_path = os.path.join(directory, ocfl.INVENTORY_FILENAME)
    if not os.path.isfile(inventory_path):
        logging.error("Ignoring path %s because there is no inventory file %s.", directory, inventory_path)
    else:
        obj = ocfl.Object(path=directory)
        if args.digest is not None:
            obj.digest_algorithm = args.digest
        else:  # Read inventory in the hope of setting digest_algoritm
            try:
                obj.parse_inventory()
            except ocfl.ObjectException as e:
                logging.warning("Failed to read inventory in directory %s (%s)", directory, e)
        sidecar = obj.write_inventory_sidecar()
        print("Written sidecar file %s" % (os.path.join(directory, sidecar)))


def main():
    """Run from command line."""
    args = parse_arguments()
    paths = ["."] if len(args.path) == 0 else args.path
    for path in paths:
        logging.debug("Looking at path %s", path)
        if os.path.isdir(path):
            create_sidecar(args, path)
        else:
            (directory, filename) = os.path.split(path)
            if filename == ocfl.INVENTORY_FILENAME:
                create_sidecar(args, directory)
            else:
                logging.error("Ignoring path %s with filename that is not inventory.json")


if __name__ == "__main__":
    main()
