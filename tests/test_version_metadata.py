"""Version tests."""
import argparse
import json
import unittest
from ocfl.version_metadata import add_version_metadata_args, VersionMetadata, VersionMetadataException


class TestAll(unittest.TestCase):
    """TestAll class to run tests."""

    def test01_add_args(self):
        """Test addition of argparse args."""
        p = argparse.ArgumentParser(description='Hello!')
        add_version_metadata_args(p)
        args = p.parse_args(['--created=a', '--message=b', '--name=c', '--address=d'])
        self.assertEqual(args.created, 'a')
        self.assertEqual(args.message, 'b')
        self.assertEqual(args.name, 'c')
        self.assertEqual(args.address, 'd')

    def test02_init(self):
        """Test VersionMetadata init method."""
        args = argparse.Namespace(created='a',
                                  message='b',
                                  name='c',
                                  address='d')
        m = VersionMetadata(args=args)
        d = m.as_dict(extra='x')
        self.assertEqual(d['created'], 'a')
        self.assertEqual(d['message'], 'b')
        self.assertEqual(d['user'], {'name': 'c', 'address': 'd'})
        self.assertEqual(d['extra'], 'x')
        # with load from file
        with open('tests/testdata/inventories/inv_1_good.json', 'r', encoding="utf-8") as fh:
            inventory = json.load(fh)
        m = VersionMetadata(inventory=inventory, version='v1')
        self.assertEqual(m.version, 'v1')
        self.assertEqual(m.created, '2018-10-02T12:00:00Z')

    def test03_from_inventory(self):
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
        # Error cases
        m = VersionMetadata()
        self.assertRaises(VersionMetadataException, m.from_inventory, inventory={"no versions": 1})
        self.assertRaises(VersionMetadataException, m.from_inventory, inventory={"versions": {}, "no head": 1})
        self.assertRaises(VersionMetadataException, m.from_inventory, inventory={"versions": {"no v1": {}}, "head": "v1"})
