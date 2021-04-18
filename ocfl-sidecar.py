#!/usr/bin/env python
"""OCFL inventory sidecar generator and updater."""
import argparse
import logging
import os.path

import ocfl

INVENTORY_NAME = "inventory.json"


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Update OCFL inventory sidecar file",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("path", type=str, nargs="*",
                        help="OCFL inventory files or directories containing them")
    parser.add_argument("--digest", default=None,
                        help="Digest algorithm to use overriding any in inventory")
    ocfl.add_shared_args(parser)
    args = parser.parse_args()
    ocfl.check_shared_args(args)
    return args


def create_sidecar(args, directory):
    """Create sidecar for inventory in dir."""
    inventory_path = os.path.join(directory, INVENTORY_NAME)
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
        logging.info("Written sidecar file %s", sidecar)


def main():
    """Run from command line."""
    args = parse_arguments()
    logging.basicConfig(level=logging.INFO if args.verbose else logging.WARN)
    paths = ["."] if len(args.path) == 0 else args.path
    for path in paths:
        logging.info("Looking at path %s", path)
        if os.path.isdir(path):
            create_sidecar(args, path)
        else:
            (directory, filename) = os.path.split(path)
            if filename == INVENTORY_NAME:
                create_sidecar(args, directory)
            else:
                logging.error("Ignoring path %s with filename that is not inventory.json")


if __name__ == "__main__":
    main()
    print("Done.")
