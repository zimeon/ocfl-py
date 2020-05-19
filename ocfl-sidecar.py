#!/usr/bin/env python
"""OCFL inventory sidecar generator and updater."""
import argparse
import logging
import ocfl
import os.path

INVENTORY_NAME = "inventory.json"


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Update OCFL inventory sidecar file",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("path", type=str, nargs="*",
                        help="OCFL inventory files or directories containing them")
    parser.add_argument("--digest", default=None,
                        help="Digest algorithm to use overriding any in inventory")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Be more verbose")
    args = parser.parse_args()
    return args


def create_sidecar(dir):
    """Create sidecar for inventory in dir."""
    inventory_path = os.path.join(dir, INVENTORY_NAME)
    if not os.path.isfile(inventory_path):
        logging.error("Ignoring path %s because there is not file %s." % (dir, inventory_path))
    else:
        object = ocfl.Object()
        if args.digest is not None:
            object.digest_algorithm = args.digest
        else:  # Read inventory in the hope of setting digest_algoritm
            try:
                object.parse_inventory(dir)
            except ocfl.ObjectException as e:
                logging.warning("Failed to read inventory in directory %s (%s)" % (dir, str(e)))
        sidecar = object.write_inventory_sidecar(dir)
        logging.info("Written sidecar file %s" % (sidecar))


if __name__ == "__main__":
    args = parse_arguments()
    logging.basicConfig(level=logging.INFO if args.verbose else logging.WARN)
    paths = ["."] if len(args.path) == 0 else args.path
    for path in paths:
        logging.info("Looking at path %s" % (path))
        if os.path.isdir(path):
            create_sidecar(path)
        else:
            (dir, filename) = os.path.split(path)
            if filename == INVENTORY_NAME:
                create_sidecar(dir)
            else:
                logging.error("Ignoring path %s with filename that is not inventory.json")
    print("Done.")
