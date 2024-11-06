"""Metadata for a specific version of OCFL Object's content."""
from .inventory import Inventory, InventoryException
from .w3c_datetime import datetime_to_str


class VersionMetadata():
    """Class for metadata for a specific version of an OCFL Object.

    Instance variables:
        id: identifier of object
        created: string of creation time
        message: string explaining version creation
        name: name string for author or agent creating version
        address: URI for author or agent creating version
    """

    def __init__(self, *,
                 created=None, message=None, name=None, address=None,
                 inventory=None, version=None):
        """Initialize with direct arguments or via an inventory.

        Arguments:
            created: string of creation time
            message: string explaining version creation
            name: name string for author or agent creating version
            address: URI for author or agent creating version
            inventory: an Inventory object to initialize from, default None
            version: the version directory name from which to extract the
                appropropriate version metadata from the inventory, else None.
                If not specified then the latest/head version metadata will
                be take from the inventory
        """
        self.id = None
        self.created = created
        self.message = message
        self.name = name
        self.address = address
        if inventory is not None:
            self.from_inventory(inventory, version)

    def from_inventory(self, inventory, version=None):
        """Initialize from an inventory dict or Inventory object.

        Arguments:
            inventory: Inventory object or data dict
            version: explicit version name to extract metadata from, else
                extract from the inventory head version

        Look for specific version directory version if specified, else
        return the head version if none specified. Will extract object id,
        created, message, and user data. Will not extract the any state
        information.
        """
        inv = inventory
        if isinstance(inventory, Inventory):
            inv = inventory.data
        self.id = inv.get("id", None)
        if "versions" not in inv:
            raise InventoryException("No versions object in inventory")
        if version is None:
            if "head" not in inv:
                raise InventoryException("No head version specified in inventory")
            version = inv["head"]
        # Now find version metadata
        if version not in inv["versions"]:
            raise InventoryException("No version block for %s in inventory")
        inv_version = inv["versions"][version]
        self.version = version
        if "created" in inv_version:
            self.created = inv_version["created"]
        if "message" in inv_version:
            self.message = inv_version["message"]
        if "user" in inv_version:
            if "name" in inv_version["user"]:
                self.name = inv_version["user"]["name"]
            if "address" in inv_version["user"]:
                self.address = inv_version["user"]["address"]

    def as_dict(self):
        """Return dictionary object with version metedata.

        Returns dict() created according to the inventory structure for
        information about a single version. If created is not set then will
        add the current datatime string.
        """
        m = {}
        m["created"] = self.created if self.created else datetime_to_str()
        if self.message is not None:
            m["message"] = self.message
        if self.name is not None or self.address is not None:
            m["user"] = {}
            if self.name is not None:
                m["user"]["name"] = self.name
            if self.address is not None:
                m["user"]["address"] = self.address
        return m
