"""Metadata for a version of OCFL Object's content."""
import json
import logging
from .w3c_datetime import datetime_to_str


def add_version_metadata_args(parser):
    """Add version metadata settings to argarse instance."""
    parser.add_argument('--created', default=None,
                        help='creation time to be used with version(s) added, else '
                             'current time will be recorded')
    parser.add_argument('--message', default='',
                        help='message to be recorded with version(s) added')
    parser.add_argument('--name', default='someone',
                        help='name of user adding version(s) to object')
    parser.add_argument('--address', default='somewhere',
                        help='address of user adding version(s) to object')


class VersionMetadata(object):
    """Class for metadata for a version of OCFL Object's content."""

    def __init__(self, args=None, inventory_file=None, vdir=None):
        """Initialize from command line arguments from argparse."""
        self.created = None
        self.message = None
        self.name = None
        self.address = None
        if args is not None:
            self.created = args.created
            self.message = args.message
            self.name = args.name
            self.address = args.address
        elif inventory_filename is not None:
            self.init_from_inventory(inventory_file, vdir)

    def init_from_inventory(self, inventory_file, vdir):
        """Initialize from an inventory file."""
        logging.info("Reading metadata for %s from %s" % (vdir, inventory_file))
        with open(inventory_file, 'r') as fh:
            inventory = json.load(fh)
        if 'versions' not in inventory:
            raise Exception("No versions object in inventory %s" % (inventory_file))
        version = None
        for v in inventory['versions']:
            if 'version' in v and v['version'] == vdir:
                version = v
                break
        if version is None:
            raise Exception("No version block for %s in inventory %s" % (vdir, inventory_file))
        print(str(version))
        if 'created' in version:
            self.created = version['created']
        if 'message' in version:
            self.message= version['message']
        if 'user' in version:
            if 'name' in version['user']:
                self.name = version['user']['name']
            if 'address' in version['user']:
                self.address = version['user']['address']

    def as_dict(self, **kwargs):
        """Dictionary object with versin metedata."""
        m = {}
        self.add_to_dict(m, **kwargs)
        return m

    def add_to_dict(self, m, **kwargs):
        """Add metadata to dictionary m."""
        m['type'] = 'Version'
        m['created'] = self.created if self.created else datetime_to_str()
        m['message'] = self.message
        m['user'] = {'name': self.name, 'address': self.address}
        # Add any extra values, and they will override instance variables
        for (key, value) in kwargs.items():
            m[key] = value
