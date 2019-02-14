"""Version tests."""
import argparse
import unittest
from ocfl.version import add_version_metadata_args, VersionMetadata


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

    def test02_VersionMetedata_init(self):
        """Test VersionMetadata class."""
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
        m = VersionMetadata(inventory_file='tests/testdata/inventories/inv_1_good.json')
        self.assertEqual(m.version, 'v1')

    def test03_VersionMetedata_from_inventory_file(self):
        """Test VersionMetadata from_inventory_file."""
        m = VersionMetadata()
        m.from_inventory_file('tests/testdata/inventories/inv_1_good.json')
        self.assertEqual(m.created, '2018-10-02T12:00:00Z')
        # Failures
        m = VersionMetadata()
        self.assertRaises(Exception, m.from_inventory,
                          inventory={})
        self.assertRaises(Exception, m.from_inventory,
                          inventory={'versions': {}})
        self.assertRaises(Exception, m.from_inventory,
                          inventory={'versions': {}}, vdir='v1')
        self.assertRaises(Exception, m.from_inventory,
                          inventory={'head': 'v1', 'versions': {}}, vdir='v1')
