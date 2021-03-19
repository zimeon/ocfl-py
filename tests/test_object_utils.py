# -*- coding: utf-8 -*-
"""Object tests."""
import argparse
import unittest
from ocfl.object_utils import remove_first_directory, make_unused_filepath, next_version, add_object_args, find_path_type


class TestAll(unittest.TestCase):
    """TestAll class to run tests."""

    def test_remove_first_directory(self):
        """Test remove_first_directory function."""
        self.assertEqual(remove_first_directory(''), '')
        self.assertEqual(remove_first_directory('a'), '')
        self.assertEqual(remove_first_directory('a/b'), 'b')
        self.assertEqual(remove_first_directory('a/b/'), 'b')
        self.assertEqual(remove_first_directory('a/b/c'), 'b/c')

    def test_make_unused_filepath(self):
        """Test make_unused_filepath function."""
        self.assertEqual(make_unused_filepath('x/y', []), 'x/y__2')
        self.assertEqual(make_unused_filepath('x/y', {'x/y__2': 1}), 'x/y__3')
        self.assertEqual(make_unused_filepath('x/y', {'x/y': 1}, ''), 'x/y2')
        self.assertEqual(make_unused_filepath('x/y', ['x/y', 'x/y2', 'x/y3'], ''), 'x/y4')

    def test_next_version(self):
        """Test next_version function."""
        self.assertRaises(Exception, next_version, '1')
        self.assertRaises(Exception, next_version, 1)
        self.assertRaises(Exception, next_version, 'v1v')
        # good non-zero padded
        self.assertEqual(next_version('v1'), 'v2')
        self.assertEqual(next_version('v99'), 'v100')
        self.assertEqual(next_version('v1234'), 'v1235')
        # good zero-padded
        self.assertEqual(next_version('v01'), 'v02')
        self.assertEqual(next_version('v00001'), 'v00002')
        self.assertEqual(next_version('v00999'), 'v01000')
        self.assertEqual(next_version('v0998'), 'v0999')
        # overflow
        self.assertRaises(Exception, next_version, 'v09')
        self.assertRaises(Exception, next_version, 'v0999')

    def test_add_object_args(self):
        """Test (kinda) adding object args."""
        parser = argparse.ArgumentParser()
        add_object_args(parser)
        args = parser.parse_args(['--skip', 'aa'])
        self.assertIn('aa', args.skip)

    def test_find_path_type(self):
        """Test find_path_type function."""
        self.assertEqual(find_path_type("extra_fixtures/good-storage-roots/fedora-root"), "root")
        self.assertEqual(find_path_type("fixtures/1.0/good-objects/minimal_one_version_one_file"), "object")
        self.assertEqual(find_path_type("README"), "file")
        self.assertIn("does not exist", find_path_type("this_path_does_not_exist"))
        self.assertEqual(find_path_type("ocfl"), "no 0= declaration file")
        self.assertIn("more than one 0= declaration file", find_path_type("extra_fixtures/misc/multiple_declarations"))
        self.assertIn("unrecognized", find_path_type("extra_fixtures/misc/unknown_declaration"))
