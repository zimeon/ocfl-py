# -*- coding: utf-8 -*-
"""Tests for ocfl.object_utils module."""
import unittest
from ocfl.object_utils import ObjectException, remove_first_directory, \
    make_unused_filepath, first_version_directory, next_version_directory, \
    find_path_type, parse_version_directory


class TestAll(unittest.TestCase):
    """TestAll class to run tests."""

    def test_remove_first_directory(self):
        """Test remove_first_directory function."""
        self.assertEqual(remove_first_directory(""), "")
        self.assertEqual(remove_first_directory("a"), "")
        self.assertEqual(remove_first_directory("a/b"), "b")
        self.assertEqual(remove_first_directory("a/b/"), "b")
        self.assertEqual(remove_first_directory("a/b/c"), "b/c")

    def test_make_unused_filepath(self):
        """Test make_unused_filepath function."""
        self.assertEqual(make_unused_filepath("x/y", []), "x/y")
        self.assertEqual(make_unused_filepath("x/y", set(["x/y", "x/y__2"])), "x/y__3")
        self.assertEqual(make_unused_filepath("x/y", {"x/y": 1}, ""), "x/y2")
        self.assertEqual(make_unused_filepath("x/y", ["x/y", "x/y2", "x/y3"], ""), "x/y4")

    def test_first_version_directory(self):
        """Test first_version_directory function."""
        # trivial non zero-padded
        self.assertEqual(first_version_directory(), "v1")
        # good zero-padded
        self.assertEqual(first_version_directory(4), "v0001")
        self.assertEqual(first_version_directory(zero_padded_width=5), "v00001")
        # errors
        self.assertRaises(ObjectException, first_version_directory, zero_padded_width=1)
        self.assertRaises(ObjectException, first_version_directory, zero_padded_width=6)
        self.assertRaises(Exception, first_version_directory, zero_padded_width="a")

    def test_next_version_directory(self):
        """Test next_version_directory function."""
        self.assertRaises(ObjectException, next_version_directory, "1")
        self.assertRaises(ObjectException, next_version_directory, "v1v")
        self.assertRaises(Exception, next_version_directory, 1)
        # good non-zero padded
        self.assertEqual(next_version_directory("v1"), "v2")
        self.assertEqual(next_version_directory("v99"), "v100")
        self.assertEqual(next_version_directory(vdir="v1234"), "v1235")
        # good zero-padded
        self.assertEqual(next_version_directory("v01"), "v02")
        self.assertEqual(next_version_directory("v00001"), "v00002")
        self.assertEqual(next_version_directory("v00999"), "v01000")
        self.assertEqual(next_version_directory("v0998"), "v0999")
        # overflow
        self.assertRaises(ObjectException, next_version_directory, "v09")
        self.assertRaises(ObjectException, next_version_directory, "v0999")

    def test_find_path_type(self):
        """Test find_path_type function."""
        self.assertEqual(find_path_type("extra_fixtures/good-storage-roots/fedora-root"), "root")
        self.assertEqual(find_path_type("fixtures/1.0/good-objects/minimal_one_version_one_file"), "object")
        self.assertEqual(find_path_type("README"), "file")
        self.assertIn("does not exist", find_path_type("this_path_does_not_exist"))
        self.assertIn("nor can parent", find_path_type("still_nope/nope_doesnt_exist"))
        self.assertEqual(find_path_type("ocfl"), "no 0= declaration file")
        self.assertEqual(find_path_type("extra_fixtures/misc/multiple_declarations"), "root")
        self.assertIn("unrecognized", find_path_type("extra_fixtures/misc/unknown_declaration"))

    def test_parse_version_directory(self):
        """Test parse_version_directory function."""
        self.assertEqual(parse_version_directory("v1"), 1)
        self.assertEqual(parse_version_directory("v00001"), 1)
        self.assertEqual(parse_version_directory("v99999"), 99999)
        # Bad
        self.assertRaises(Exception, parse_version_directory, None)
        self.assertRaises(ObjectException, parse_version_directory, "")
        self.assertRaises(ObjectException, parse_version_directory, "1")
        self.assertRaises(ObjectException, parse_version_directory, "v0")
        self.assertRaises(ObjectException, parse_version_directory, "v-1")
        self.assertRaises(ObjectException, parse_version_directory, "v0000")
        self.assertRaises(ObjectException, parse_version_directory, "vv")
        self.assertRaises(ObjectException, parse_version_directory, "v000001")
