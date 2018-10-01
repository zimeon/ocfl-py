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

    def test02_VersionMetedata(self):
        """Test VersionMetadata class."""
        args = argparse.Namespace(created='a',
                                  message='b',
                                  name='c',
                                  address='d')
        m = VersionMetadata(args=args)
        d = m.as_dict(extra='x')
        self.assertEqual(d['type'], 'Version')
        self.assertEqual(d['created'], 'a')
        self.assertEqual(d['message'], 'b')
        self.assertEqual(d['user'], {'name': 'c', 'address': 'd'})
        self.assertEqual(d['extra'], 'x')
