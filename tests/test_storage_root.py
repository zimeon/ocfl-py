# -*- coding: utf-8 -*-
"""Storage root tests."""
import io
import logging
import os
import tempfile
import unittest

from ocfl.storage_root import StorageRoot, StorageRootException
from ocfl.layout_registry import get_layout
from ocfl.layout_0002_flat_direct import Layout_0002_Flat_Direct
from ocfl.validation_logger import ValidationLogger


class TestAll(unittest.TestCase):
    """TestAll class to run tests."""

    def test_get_layout(self):
        """Test everything, just a little."""
        d = get_layout("0002-flat-direct-storage-layout")
        self.assertEqual(d.identifier_to_path("ab cd"), "ab cd")
        d = get_layout("nnnn-tuple-tree")
        self.assertEqual(d.identifier_to_path("abcd"), "ab/cd/abcd")
        d = get_layout("nnnn-uuid-quadtree")
        self.assertEqual(d.identifier_to_path("urn:uuid:6ba7b810-9dad-11d1-80b4-00c04fd430c8"),
                         "6ba7/b810/9dad/11d1/80b4/00c0/4fd4/30c8")
        # Errors
        self.assertRaises(Exception, get_layout)
        self.assertRaises(Exception, get_layout, None)
        self.assertRaises(Exception, get_layout, "unknown")

    def test_init(self):
        """Test StorageRoot init."""
        s = StorageRoot()
        self.assertEqual(s.root, None)
        self.assertEqual(s.layout_name, None)
        s = StorageRoot(root="a", layout_name="b")
        self.assertEqual(s.root, "a")
        self.assertEqual(s.layout_name, "b")

    def test_open_root_fs(self):
        """Test open_root_fs method."""
        s = StorageRoot()
        self.assertIs(s.root_fs, None)
        tempdir = tempfile.mkdtemp(prefix="test_open_root_fs")
        print(tempdir)
        s.root = tempdir
        s.open_root_fs()
        self.assertIsNot(s.root_fs, None)
        # Error - open without create, then succeed with create
        rootdir = os.path.join(tempdir, "xyz")
        s = StorageRoot()
        s.root = rootdir
        self.assertRaises(StorageRootException, s.open_root_fs)
        s.open_root_fs(create=True)
        self.assertIsNot(s.root_fs, None)

    def test_layout(self):
        """Test layout property."""
        s = StorageRoot(root="x", layout_name="0002-flat-direct-storage-layout")
        self.assertTrue(isinstance(s.layout, Layout_0002_Flat_Direct))

    def test_traversal_error(self):
        """Test traversal_error method."""
        s = StorageRoot()
        self.assertEqual(s.num_traversal_errors, 0)
        s.traversal_error("oops")
        self.assertEqual(s.num_traversal_errors, 1)

    def test_object_path(self):
        """Test object_path method."""
        s = StorageRoot(root="x/y", layout_name="0002-flat-direct-storage-layout")
        self.assertEqual(s.object_path("id1"), "id1")
        s = StorageRoot(root="z/a", layout_name="nnnn-uuid-quadtree")
        self.assertEqual(s.object_path("urn:uuid:6ba7b810-9dad-11d1-80b4-00c04fd430c8"), "6ba7/b810/9dad/11d1/80b4/00c0/4fd4/30c8")

    def test_initialize(self):
        """Test initialize method."""
        tempdir = tempfile.mkdtemp(prefix="test_init_1")
        s = StorageRoot(root=tempdir, layout_name="0002-flat-direct-storage-layout")
        self.assertRaises(StorageRootException, s.initialize)
        tempdir2 = os.path.join(tempdir, "aaa")
        s = StorageRoot(root=tempdir2, layout_name="0002-flat-direct-storage-layout")
        s.initialize(spec_version="1.0")
        self.assertTrue(os.path.isfile(os.path.join(tempdir2, "0=ocfl_1.0")))
        tempdir2 = os.path.join(tempdir, "bbb")
        s = StorageRoot(root=tempdir2, layout_name="0002-flat-direct-storage-layout")
        s.initialize()
        self.assertTrue(os.path.isfile(os.path.join(tempdir2, "0=ocfl_1.1")))

    def test_check_root_structure(self):
        """Test check_root_structure method."""
        tempdir = os.path.join(tempfile.mkdtemp(prefix="test_root"), "rrr")
        s = StorageRoot(root=tempdir, layout_name="0002-flat-direct-storage-layout")
        # No declaration
        os.mkdir(tempdir)
        s.open_root_fs()
        self.assertRaises(StorageRootException, s.check_root_structure)
        # Wrong declaration
        decl = os.path.join(tempdir, "0=something_else")
        with open(decl, "w", encoding="utf-8") as fh:
            fh.close()
        self.assertRaises(StorageRootException, s.check_root_structure)
        # Two declarations
        decl2 = os.path.join(tempdir, "0=ocfl_1.0")
        with open(decl2, "w", encoding="utf-8") as fh:
            fh.write("not correct")
            fh.close()
        self.assertRaises(StorageRootException, s.check_root_structure)
        os.remove(decl)
        # Right file, wrong content
        self.assertRaises(StorageRootException, s.check_root_structure)
        os.remove(decl2)
        # All good
        with open(decl2, "w", encoding="utf-8") as fh:
            fh.write("ocfl_1.0\n")
            fh.close()
        self.assertTrue(s.check_root_structure())

    def test_parse_layout_file(self):
        """Test parse_layout_file method."""
        s = StorageRoot(root="mem://")
        s.open_root_fs(create=True)
        s.root_fs.writetext("ocfl_layout.json", '{"extension": "aa", "description": "bb"}')
        self.assertEqual(s.parse_layout_file(), ("aa", "bb"))
        s.root_fs.writetext("ocfl_layout.json", '["aa", "bb"]')
        self.assertRaises(StorageRootException, s.parse_layout_file)
        s.root_fs.writetext("ocfl_layout.json", '{"extension": "yy", "description": ["zz"]}')
        self.assertRaises(StorageRootException, s.parse_layout_file)
        s.root_fs.remove("ocfl_layout.json")
        s.root_fs.makedir("ocfl_layout.json")
        self.assertRaises(StorageRootException, s.parse_layout_file)

    def test_object_paths(self):
        """Test object_paths generator."""
        s = StorageRoot(root="extra_fixtures/good-storage-roots/fedora-root")
        s.open_root_fs()
        paths = list(s.object_paths())
        self.assertEqual(len(paths), 176)
        self.assertIn("61/38/37/3fede0e4-d168-475a-9b51-edbed6f0d972", paths)
        # Error cases
        log_io = io.StringIO()
        logger = logging.getLogger()
        logger.addHandler(logging.StreamHandler(log_io))
        s = StorageRoot(root="zip://extra_fixtures/bad-storage-roots/simple-bad-root.zip")  # Using ZipFS
        s.open_root_fs()
        paths = list(s.object_paths())
        self.assertEqual(len(paths), 2)
        self.assertEqual(s.num_traversal_errors, 5)
        log_out = log_io.getvalue()
        self.assertIn("E073 - path='/empty_dir'", log_out)
        self.assertIn("E003d - path='/object_multiple_declarations'", log_out)
        self.assertIn("E004a - path='/object_unknown_version', version='0.9'", log_out)
        self.assertIn("E004b - path='/object_unrecognized_declaration', declaration='0=special_object_yeah'", log_out)
        self.assertIn("E072 - path='/dir_with_file_but_no_declaration'", log_out)
        # Specific error cases
        s = StorageRoot(root="extra_fixtures/bad-storage-roots/E072_root_with_file_not_in_object")
        s.open_root_fs()
        s.log = ValidationLogger()
        self.assertEqual(list(s.object_paths()), ["dir2/minimal_no_content"])
        self.assertEqual(s.num_traversal_errors, 1)
        self.assertIn("E072", s.log.codes)
        #
        s = StorageRoot(root="zip://extra_fixtures/bad-storage-roots/E073_root_with_empty_dir.zip")
        s.open_root_fs()
        s.log = ValidationLogger()
        self.assertEqual(list(s.object_paths()), [])
        self.assertEqual(s.num_traversal_errors, 1)
        self.assertIn("E073", s.log.codes)

    def test_validate(self):
        """Test validate method."""
        s = StorageRoot(root="extra_fixtures/good-storage-roots/fedora-root")
        self.assertTrue(s.validate())
        self.assertEqual(s.num_objects, 176)
        self.assertEqual(s.good_objects, 176)
        # Simple case of three objects
        s = StorageRoot(root="extra_fixtures/good-storage-roots/simple-root")
        self.assertTrue(s.validate())
        self.assertEqual(s.num_objects, 3)
        self.assertEqual(s.good_objects, 3)
        # Reg extension will not give warning
        s = StorageRoot(root="extra_fixtures/good-storage-roots/reg-extension-dir-root")
        self.assertTrue(s.validate())
        self.assertEqual(s.num_objects, 1)
        self.assertEqual(s.good_objects, 1)
        self.assertNotIn("W901", s.log.codes)
        # Unreg extension will give warning
        s = StorageRoot(root="extra_fixtures/good-storage-roots/unreg-extension-dir-root")
        self.assertTrue(s.validate())
        self.assertEqual(s.num_objects, 1)
        self.assertEqual(s.good_objects, 1)
        self.assertIn("W901", s.log.codes)
