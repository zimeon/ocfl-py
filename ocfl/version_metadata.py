"""Metadata for a specific version of OCFL Object's content."""
from .w3c_datetime import datetime_to_str

from .inventory import Inventory


class VersionMetadataException(Exception):
    """Exception class for OCFL Object."""


class VersionMetadata():
    """Class for metadata for a specific version of an OCFL Object."""

    def __init__(self, *, args=None, inventory=None, version=None,
                 created=None, message=None, name=None, address=None):
        """Initialize by various means, including command line arguments from argparse."""
        self.id = None
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
        """Initialize from an inventory dict or object.

        Look for specific version directory version if specified, else
        return the head version if none specified.

        Arguments:
            inventory - Inventory object or data dict.
            version - explicit version name to extract metadata from, else
                extract from the inventory head version.
        """
        inv = inventory
        if isinstance(inventory, Inventory):
            inv = inventory.data
        self.id = inv.get('id', None)
        if 'versions' not in inv:
            raise VersionMetadataException("No versions object in inventory")
        if version is None:
            if 'head' not in inv:
                raise VersionMetadataException("No head version specified in inventory")
            version = inv['head']
        # Now find version metadata
        if version not in inv['versions']:
            raise VersionMetadataException("No version block for %s in inventory")
        inv_version = inv['versions'][version]
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
        """Return dictionary object with version metedata.

        Arguments:
            **kwargs: keyword=value pairs that are used to add the corresponding
                key and value to the dictionary. If none are specified then
                no additional data will be added.

        Returns dict() created according to the inventory structure for
        information about a single version. Adds data from this object and
        then any additional data in **kwargs.
        """
        m = {}
        m['created'] = self.created if self.created else datetime_to_str()
        if self.message is not None:
            m['message'] = self.message
        if self.name is not None or self.address is not None:
            m['user'] = {'name': self.name}
            if self.address is not None:
                m['user']['address'] = self.address
        # Add any extra values, and they will override instance variables
        for key, value in kwargs.items():
            m[key] = value
        return m
