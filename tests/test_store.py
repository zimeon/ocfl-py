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

    def test01_init(self):
        """Test Store init."""
        s = Store()
        self.assertEqual(s.root, None)
        self.assertEqual(s.disposition, None)
        s = Store(root='a', disposition='b')
        self.assertEqual(s.root, 'a')
        self.assertEqual(s.disposition, 'b')

    def test02_declaration_file(self):
        """Test declaration_file property."""
        s = Store(root='')
        self.assertEqual(s.declaration_file, '0=ocfl_1.0')
        s.root = 'a/b/c'
        self.assertEqual(s.declaration_file, 'a/b/c/0=ocfl_1.0')

    def test03_disposition_file(self):
        """Test disposition_file property."""
        s = Store(root='x', disposition='y')
        self.assertEqual(s.disposition_file, 'x/1=y')

    def test04_dispositor(self):
        """Test dispositor property."""
        s = Store(root='x', disposition='identity')
        self.assertTrue(isinstance(s.dispositor, Identity))

    def test05_object_path(self):
        """Test object_path method."""
        s = Store(root='x/y', disposition='identity')
        self.assertEqual(s.object_path('id1'), 'x/y/id1')
