# -*- coding: utf-8 -*-
"""Store tests."""
import io
import json
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

    def test_spec_file(self):
        """Test spec_file property."""
        s = Store(root='thingy')
        self.assertEqual(s.spec_file, 'thingy/ocfl_1.0.txt')

    def test_dispositor(self):
        """Test dispositor property."""
        s = Store(root='x', disposition='identity')
        self.assertTrue(isinstance(s.dispositor, Identity))

    def test_object_path(self):
        """Test object_path method."""
        s = Store(root='x/y', disposition='identity')
        self.assertEqual(s.object_path('id1'), 'x/y/id1')

    def test_initialize(self):
        """Test initialize method."""
        tempdir = tempfile.mkdtemp(prefix='test_init')
        s = Store(root=tempdir, disposition='identity')
        self.assertRaises(StoreException, s.initialize)
        tempdir = os.path.join(tempdir, 'aaa')
        s = Store(root=tempdir, disposition='identity')
        s.initialize()
        self.assertTrue(os.path.isfile(os.path.join(tempdir,'0=ocfl_1.0')))

    def test_check_root_structure(self):
        """Test check_root_structure method."""
        tempdir = os.path.join(tempfile.mkdtemp(prefix='test_root'), 'rrr')
        s = Store(root=tempdir, disposition='identity')
        # Not present
        self.assertRaises(StoreException, s.check_root_structure)
        # File not dir
        with open(tempdir, 'w') as fh:
            fh.close()
        self.assertRaises(StoreException, s.check_root_structure)
        os.remove(tempdir)
        # No declaration
        os.mkdir(tempdir)
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
        # Finally, all good
        with open(decl2, 'w') as fh:
            fh.write("ocfl_1.0\n")
            fh.close()
        self.assertTrue(s.check_root_structure())

    def test_object_paths(self):
        """Test object_paths generator."""
        s = Store(root='extra_fixtures/good-storage-roots/fedora-root')
        paths = list(s.object_paths())
        self.assertEqual(len(paths), 176)

    def test_validate(self):
        """Test validate method."""
        s = Store(root='extra_fixtures/good-storage-roots/fedora-root')
        self.assertTrue(s.validate())
