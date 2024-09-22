"""Layout_NNNN_Flat_Quoted layout tests."""
import os.path
import unittest
from ocfl.layout_nnnn_flat_quoted import Layout_NNNN_Flat_Quoted


class TestAll(unittest.TestCase):
    """TestAll class to run tests."""

    def test_identifier_to_path(self):
        """Test identifier_to_path."""
        d = Layout_NNNN_Flat_Quoted()
        self.assertEqual(d.identifier_to_path(''), '')
        self.assertEqual(d.identifier_to_path('abc'), 'abc')
        self.assertEqual(d.identifier_to_path('this n that'), 'this+n+that')
