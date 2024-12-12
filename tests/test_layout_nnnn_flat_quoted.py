"""Layout_NNNN_Flat_Quoted layout tests."""
import unittest
from ocfl.layout import LayoutException
from ocfl.layout_nnnn_flat_quoted import Layout_NNNN_Flat_Quoted


class TestAll(unittest.TestCase):
    """TestAll class to run tests."""

    def test_identifier_to_path(self):
        """Test identifier_to_path."""
        layout = Layout_NNNN_Flat_Quoted()
        self.assertRaises(LayoutException, layout.identifier_to_path, "")
        self.assertEqual(layout.identifier_to_path("abc"), "abc")
        self.assertEqual(layout.identifier_to_path("this n that"), "this+n+that")
