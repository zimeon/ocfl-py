"""Identity dispositor tests."""
import os.path
import unittest
from ocfl.identity import Identity


class TestAll(unittest.TestCase):
    """TestAll class to run tests."""

    def test01_identifier_to_path(self):
        """Test identifier_to_path."""
        d = Identity()
        self.assertEqual(d.identifier_to_path(''), '')
        self.assertEqual(d.identifier_to_path('abc'), 'abc')
        self.assertEqual(d.identifier_to_path('this n that'), 'this+n+that')

    def test02_relative_path_to_identifier(self):
        """Test relative_path_to_identifier."""
        d = Identity()
        self.assertEqual(d.relative_path_to_identifier(''), '')
        self.assertEqual(d.relative_path_to_identifier('abc'), 'abc')
        self.assertEqual(d.relative_path_to_identifier('this+n+that'), 'this n that')
        self.assertRaises(Exception, d.relative_path_to_identifier, os.path.join('a', 'b'))
