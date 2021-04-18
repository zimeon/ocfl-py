"""Metadata for a specific version of OCFL Object's content."""
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


class VersionMetadataException(Exception):
    """Exception class for OCFL Object."""


class VersionMetadata():
    """Class for metadata for a specific version of an OCFL Object."""

    def __init__(self, args=None, inventory=None, version=None,
                 identifier=None, created=None, message=None, name=None, address=None):
        """Initialize by various means, including command line arguments from argparse."""
        self.id = identifier
        self.created = created
        self.message = message
        self.name = name
        self.address = address
        if args is not None:
            self.created = args.created
            self.message = args.message
            self.name = args.name
            self.address = args.address
        elif inventory is not None:
            self.from_inventory(inventory, version)

    def from_inventory(self, inventory, version=None):
        """Initialize from an inventory object.

        Look for specific version directory version if specified, else
        return the head version.

        Parameters:
            inventory - inventory object (dict)
            version - explicit version name, else taken from inventory head
        """
        self.id = inventory.get('id', None)
        if 'versions' not in inventory:
            raise VersionMetadataException("No versions object in inventory")
        if version is None:
            if 'head' not in inventory:
                raise VersionMetadataException("No head version specified in inventory")
            version = inventory['head']
        # Now find version metadata
        if version not in inventory['versions']:
            raise VersionMetadataException("No version block for %s in inventory")
        inv_version = inventory['versions'][version]
        self.version = version
        if 'created' in inv_version:
            self.created = inv_version['created']
        if 'message' in inv_version:
            self.message = inv_version['message']
        if 'user' in inv_version:
            if 'name' in inv_version['user']:
                self.name = inv_version['user']['name']
            if 'address' in inv_version['user']:
                self.address = inv_version['user']['address']

    def as_dict(self, **kwargs):
        """Return dictionary object with version metedata."""
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
