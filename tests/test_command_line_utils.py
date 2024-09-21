# -*- coding: utf-8 -*-
"""Object tests."""
import argparse
import unittest
from ocfl.command_line_utils import add_version_metadata_args, add_object_args, add_shared_args, check_shared_args


class TestAll(unittest.TestCase):
    """TestAll class to run tests."""

    def test_add_version_metadata_args(self):
        """Test addition of argparse args for version metadata."""
        p = argparse.ArgumentParser(description='Hello!')
        add_version_metadata_args(p)
        args = p.parse_args(['--created=a', '--message=b', '--name=c', '--address=d'])
        self.assertEqual(args.created, 'a')
        self.assertEqual(args.message, 'b')
        self.assertEqual(args.name, 'c')
        self.assertEqual(args.address, 'd')

    def test_add_object_args(self):
        """Test (kinda) adding object args."""
        parser = argparse.ArgumentParser()
        add_object_args(parser)
        args = parser.parse_args(['--skip', 'aa'])
        self.assertIn('aa', args.skip)

    def test_add_shared_args(self):
        """Test (kinda) adding shared args."""
        parser = argparse.ArgumentParser()
        add_shared_args(parser)
        args = parser.parse_args(['--version', '-v'])
        self.assertTrue(args.version)
        self.assertTrue(args.verbose)

    def test_check_shared_args(self):
        """Test check of shared args."""
        parser = argparse.ArgumentParser()
        add_shared_args(parser)
        parser.parse_args(['--version', '-v'])
        check_shared_args(parser.parse_args(['-v']))
        self.assertRaises(SystemExit, check_shared_args, parser.parse_args(['--version']))
