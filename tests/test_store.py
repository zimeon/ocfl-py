# -*- coding: utf-8 -*-
"""Store tests."""
import fs
import io
import json
import logging
import os
import sys
import tempfile
import unittest
from ocfl.store import Store, StoreException
from ocfl.identity import Identity


class TestAll(unittest.TestCase):
    """TestAll class to run tests."""

    def test_init(self):
        """Test Store init."""
        s = Store()
        self.assertEqual(s.root, None)
        self.assertEqual(s.disposition, None)
        s = Store(root='a', disposition='b')
        self.assertEqual(s.root, 'a')
        self.assertEqual(s.disposition, 'b')

    def test_open_root_fs(self):
        """Test open_root_fs method."""
        s = Store()
        self.assertIs(s.root_fs, None)
        tempdir = tempfile.mkdtemp(prefix='test_open_root_fs')
        print(tempdir)
        s.root = tempdir
        s.open_root_fs()
        self.assertIsNot(s.root_fs, None)
        # Error - open without create, then succeed with create
        rootdir = os.path.join(tempdir, 'xyz')
        s = Store()
        s.root = rootdir
        self.assertRaises(StoreException, s.open_root_fs)
        s.open_root_fs(create=True)
        self.assertIsNot(s.root_fs, None)

    def test_dispositor(self):
        """Test dispositor property."""
        s = Store(root='x', disposition='identity')
        self.assertTrue(isinstance(s.dispositor, Identity))

    def test_traversal_error(self):
        """Test traversal_error method."""
        s = Store()
        self.assertEqual(s.num_traversal_errors, 0)
        s.traversal_error("oops")
        self.assertEqual(s.num_traversal_errors, 1)

    def test_object_path(self):
        """Test object_path method."""
        s = Store(root='x/y', disposition='identity')
        self.assertEqual(s.object_path('id1'), 'id1')
        s = Store(root='z/a', disposition='uuid_quadtree')
        self.assertEqual(s.object_path('urn:uuid:6ba7b810-9dad-11d1-80b4-00c04fd430c8'), '6ba7/b810/9dad/11d1/80b4/00c0/4fd4/30c8')

    def test_initialize(self):
        """Test initialize method."""
        tempdir = tempfile.mkdtemp(prefix='test_init')
        s = Store(root=tempdir, disposition='identity')
        self.assertRaises(StoreException, s.initialize)
        tempdir = os.path.join(tempdir, 'aaa')
        s = Store(root=tempdir, disposition='identity')
        s.initialize()
        self.assertTrue(os.path.isfile(os.path.join(tempdir, '0=ocfl_1.0')))

    def test_check_root_structure(self):
        """Test check_root_structure method."""
        tempdir = os.path.join(tempfile.mkdtemp(prefix='test_root'), 'rrr')
        s = Store(root=tempdir, disposition='identity')
        # No declaration
        os.mkdir(tempdir)
        s.open_root_fs()
        self.assertRaises(StoreException, s.check_root_structure)
        # Wrong declaration
        decl = os.path.join(tempdir, '0=something_else')
        with open(decl, 'w') as fh:
            fh.close()
        self.assertRaises(StoreException, s.check_root_structure)
        # Two declarations
        decl2 = os.path.join(tempdir, '0=ocfl_1.0')
        with open(decl2, 'w') as fh:
            fh.write("not correct")
            fh.close()
        self.assertRaises(StoreException, s.check_root_structure)
        os.remove(decl)
        # Right file, wrong content
        self.assertRaises(StoreException, s.check_root_structure)
        os.remove(decl2)
        # All good
        with open(decl2, 'w') as fh:
            fh.write("ocfl_1.0\n")
            fh.close()
        self.assertTrue(s.check_root_structure())
        # Spec "file" a directory
        spec = os.mkdir(os.path.join(tempdir, "ocfl_1.0.txt"))
        self.assertRaises(StoreException, s.check_root_structure)

    def test_parse_layout_file(self):
        """Test parse_layout_file method."""
        s = Store(root="mem://")
        s.open_root_fs(create=True)
        self.assertEqual(s.parse_layout_file(), (None, None))
        s.root_fs.writetext('ocfl_layout.json', '{"extension": "aa", "description": "bb"}')
        self.assertEqual(s.parse_layout_file(), ("aa", "bb"))
        s.root_fs.writetext('ocfl_layout.json', '["aa", "bb"]')
        self.assertRaises(StoreException, s.parse_layout_file)
        s.root_fs.writetext('ocfl_layout.json', '{"extension": "yy", "description": ["zz"]}')
        self.assertRaises(StoreException, s.parse_layout_file)
        s.root_fs.remove('ocfl_layout.json')
        s.root_fs.makedir('ocfl_layout.json')
        self.assertRaises(StoreException, s.parse_layout_file)

    def test_object_paths(self):
        """Test object_paths generator."""
        s = Store(root='extra_fixtures/good-storage-roots/fedora-root')
        s.open_root_fs()
        paths = list(s.object_paths())
        self.assertEqual(len(paths), 176)
        self.assertIn('61/38/37/3fede0e4-d168-475a-9b51-edbed6f0d972', paths)
        # Error cases
        log_io = io.StringIO()
        logger = logging.getLogger()
        logger.addHandler(logging.StreamHandler(log_io))
        s = Store(root='zip://extra_fixtures/bad-storage-roots/simple-bad-root.zip')  # Using ZipFS
        s.open_root_fs()
        paths = list(s.object_paths())
        self.assertEqual(len(paths), 2)
        self.assertEqual(s.num_traversal_errors, 5)
        log_out = log_io.getvalue()
        self.assertIn('Empty directory /empty_dir', log_out)
        self.assertIn('Multiple 0= declaration files in /object_multiple_declarations', log_out)
        self.assertIn('Object with unknown version 0.9 in /object_unknown_version', log_out)
        self.assertIn('Object with unrecognized declaration 0=special_object_yeah in /object_unrecognized_declaration', log_out)
        self.assertIn('Directory /dir_with_file_but_no_declaration has file but not object declaration', log_out)

    def test_validate(self):
        """Test validate method."""
        for root in ['extra_fixtures/good-storage-roots/fedora-root',
                     'extra_fixtures/good-storage-roots/simple-root']:
            s = Store(root=root)
            self.assertTrue(s.validate())
