"""Metadata for a version of OCFL Object's content."""
import json
import logging
from .w3c_datetime import datetime_to_str


def add_version_metadata_args(parser):
    """Add version metadata settings to argparse instance parser."""
    parser.add_argument('--created', default=None,
                        help='creation time to be used with version(s) added, else '
                             'current time will be recorded')
    parser.add_argument('--message', default=None,
                        help='message to be recorded with version(s) added')
    parser.add_argument('--name', default=None,
                        help='name of user adding version(s) to object')
    parser.add_argument('--address', default=None,
                        help='address of user adding version(s) to object')


class VersionMetadata(object):
    """Class for metadata for a version of OCFL Object's content."""

    def __init__(self, args=None, inventory_file=None, inventory=None, vdir=None):
        """Initialize from command line arguments from argparse."""
        self.id = None
        self.created = None
        self.message = None
        self.name = None
        self.address = None
        if args is not None:
            self.created = args.created
            self.message = args.message
            self.name = args.name
            self.address = args.address
        elif inventory_file is not None:
            self.from_inventory_file(inventory_file, vdir)
        elif inventory is not None:
            self.from_inventory(inventory, vdir)

    def from_inventory_file(self, inventory_file, vdir=None):
        """Initialize from an inventory file."""
        logging.info("Reading metadata for %s from %s" % (vdir, inventory_file))
        with open(inventory_file, 'r') as fh:
            inventory = json.load(fh)
        return self.from_inventory(inventory, vdir, inventory_file)

    def from_inventory(self, inventory, vdir=None, inventory_file=''):
        """Initialize from an inventory object.

        Look for specific version directory vdir if specified, else
        return the head version.

        Parameters:
            inventory - inventory object (dict)
            vdir - explicit version directory, else taken from inventory head
            inventory_file - file name used in error reporting (else '')
        """
        self.id = inventory.get('id', None)
        if 'versions' not in inventory:
            raise Exception("No versions object in inventory %s" % (inventory_file))
        version = None
        if vdir is None:
            if 'head' not in inventory:
                raise Exception("No head version specified in inventory %s" % (inventory_file))
            vdir = inventory['head']
        # Now find version metadata
        if vdir not in inventory['versions']:
            raise Exception("No version block for %s in inventory %s" % (vdir, inventory_file))
        version = inventory['versions'][vdir]
        self.version = vdir
        if 'created' in version:
            self.created = version['created']
        if 'message' in version:
            self.message = version['message']
        if 'user' in version:
            if 'name' in version['user']:
                self.name = version['user']['name']
            if 'address' in version['user']:
                self.address = version['user']['address']

    def as_dict(self, **kwargs):
        """Dictionary object with version metedata."""
        m = {}
        self.add_to_dict(m, **kwargs)
        return m

    def add_to_dict(self, m, **kwargs):
        """Add metadata to dictionary m."""
        m['created'] = self.created if self.created else datetime_to_str()
        if self.message is not None:
            m['message'] = self.message
        if self.name is not None or self.address is not None:
            m['user'] = {'name': self.name}
            if self.address is not None:
                m['user']['address'] = self.address
        # Add any extra values, and they will override instance variables
        for (key, value) in kwargs.items():
            m[key] = value
