# -*- coding: utf-8 -*-
"""Object tests."""
import argparse
import logging
import unittest
from ocfl.command_line_utils import add_version_arg, check_version_arg, add_version_metadata_args, add_object_args, add_verbosity_args, check_verbosity_args


class TestAll(unittest.TestCase):
    """TestAll class to run tests."""

    def test_add_version_metadata_args(self):
        """Test addition of argparse args for version metadata."""
        p = argparse.ArgumentParser(description="Hello!")
        add_version_metadata_args(p)
        args = p.parse_args(["--created=a", "--message=b", "--name=c", "--address=d"])
        self.assertEqual(args.created, "a")
        self.assertEqual(args.message, "b")
        self.assertEqual(args.name, "c")
        self.assertEqual(args.address, "d")

    def test_add_object_args(self):
        """Test (kinda) adding object args."""
        parser = argparse.ArgumentParser()
        add_object_args(parser)
        args = parser.parse_args(["--skip", "aa"])
        self.assertIn("aa", args.skip)

    def test_add_version_arg(self):
        """Test (kinda) adding version arg."""
        parser = argparse.ArgumentParser()
        add_version_arg(parser)
        args = parser.parse_args(["--version"])
        self.assertTrue(args.version)

    def test_check_version_arg(self):
        """Test check of version arg which prints version and exits."""
        parser = argparse.ArgumentParser()
        add_version_arg(parser)
        self.assertRaises(SystemExit, check_version_arg, parser.parse_args(["--version"]))

    def test_add_verbosity_args(self):
        """Test (kinda) adding shared args."""
        parser = argparse.ArgumentParser()
        add_verbosity_args(parser)
        args = parser.parse_args(["--debug"])
        self.assertTrue(args.debug)
        self.assertFalse(args.verbose)
        self.assertFalse(args.quiet)

    def test_check_verbosity_args(self):
        """Test check of shared args."""
        parser = argparse.ArgumentParser()
        add_verbosity_args(parser)
        check_verbosity_args(parser.parse_args(["-v"]))
        self.assertEqual(logging.getLogger().getEffectiveLevel(), logging.WARN)
