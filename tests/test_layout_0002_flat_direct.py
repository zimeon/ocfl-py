"""Layout_0002_Flat_Direct layout tests."""
import os.path
import unittest
from ocfl.layout_0002_flat_direct import Layout_0002_Flat_Direct


class TestAll(unittest.TestCase):
    """TestAll class to run tests."""

    def test_name(self):
        """Test canonical name."""
        self.assertEqual(Layout_0002_Flat_Direct().name, '0002-flat-direct-storage-layout')

    def test_identifier_to_path(self):
        """Test identifier_to_path."""
        d = Layout_0002_Flat_Direct()
        self.assertEqual(d.identifier_to_path('abc'), 'abc')
        self.assertEqual(d.identifier_to_path('this n that'), 'this n that')
        # From the extension
        self.assertEqual(d.identifier_to_path('object-01'), 'object-01')
        self.assertEqual(d.identifier_to_path('..hor_rib:lé-$id'), '..hor_rib:lé-$id')
        # Exception cases
        for bad_id in ('', '.', os.path.join('a', 'b')):
            self.assertRaises(Exception, d.identifier_to_path, bad_id)
