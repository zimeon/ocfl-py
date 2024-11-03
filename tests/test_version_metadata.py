"""VersionMetadata tests."""
import json
import unittest
from ocfl.version_metadata import VersionMetadata, VersionMetadataException
from ocfl.inventory import Inventory


class TestAll(unittest.TestCase):
    """TestAll class to run tests."""

    def test01_init(self):
        """Test VersionMetadata init method."""
        m = VersionMetadata(created="a",
                            message="b",
                            name="c",
                            address="d")
        d = m.as_dict()
        self.assertEqual(d["created"], "a")
        self.assertEqual(d["message"], "b")
        self.assertEqual(d["user"], {"name": "c", "address": "d"})
        # with load from file
        with open("tests/testdata/inventories/inv_1_good.json", "r", encoding="utf-8") as fh:
            inventory = json.load(fh)
        m = VersionMetadata(inventory=inventory, version="v1")
        self.assertEqual(m.version, "v1")
        self.assertEqual(m.created, "2018-10-02T12:00:00Z")

    def test02_from_inventory(self):
        """Test from_inventory method."""
        m = VersionMetadata()
        m.from_inventory(inventory={
            "id": "III",
            "head": "v1",
            "versions": {
                "v1": {
                    "created": "2020-01-02T03:04:05",
                    "message": "text",
                    "user": {"address": "mailto:alice@example.org", "name": "Alice"}
                }
            }})
        self.assertEqual(m.id, "III")
        self.assertEqual(m.created, "2020-01-02T03:04:05")
        self.assertEqual(m.message, "text")
        self.assertEqual(m.address, "mailto:alice@example.org")
        self.assertEqual(m.name, "Alice")
        # And now from an Inventory object
        inv = Inventory()
        inv.id = "info:a/b/c/99"
        v = inv.add_version()
        v.message = "Hello"
        v.user_name = "Teresa"
        m = VersionMetadata()
        m.from_inventory(inventory=inv, version="v1")
        self.assertEqual(m.id, "info:a/b/c/99")
        self.assertEqual(m.created, None)
        self.assertEqual(m.message, "Hello")
        self.assertEqual(m.name, "Teresa")
        # Error cases
        m = VersionMetadata()
        self.assertRaises(VersionMetadataException, m.from_inventory, inventory={"no versions": 1})
        self.assertRaises(VersionMetadataException, m.from_inventory, inventory={"versions": {}, "no head": 1})
        self.assertRaises(VersionMetadataException, m.from_inventory, inventory={"versions": {"no v1": {}}, "head": "v1"})
