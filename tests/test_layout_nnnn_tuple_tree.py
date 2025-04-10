"""Layout_NNNN_Tuple_Tree layout tests."""
import unittest
from ocfl.layout import LayoutException
from ocfl.layout_nnnn_tuple_tree import Layout_NNNN_Tuple_Tree


class TestAll(unittest.TestCase):
    """TestAll class to run tests."""

    def test_encode(self):
        """Test encode."""
        layout = Layout_NNNN_Tuple_Tree()
        self.assertEqual(layout.encode(""), "")
        self.assertEqual(layout.encode("a"), "a")
        self.assertEqual(layout.encode("a/b:?"), "a=b+^3f")

    def test_decode(self):
        """Test decode."""
        layout = Layout_NNNN_Tuple_Tree()
        self.assertEqual(layout.decode(""), "")
        self.assertEqual(layout.decode("a"), "a")
        self.assertEqual(layout.decode("a=b+^3f"), "a/b:?")

    def test_config(self):
        """Test config property."""
        layout = Layout_NNNN_Tuple_Tree()
        self.assertEqual(set(layout.config.keys()), set(("extensionName", "tupleSize")))

    def test_check_tuple_size(self):
        """Test check_tuple_size method."""
        layout = Layout_NNNN_Tuple_Tree()
        self.assertRaises(LayoutException, layout.check_tuple_size, None)
        self.assertRaises(LayoutException, layout.check_tuple_size, "string-not-num")
        self.assertRaises(LayoutException, layout.check_tuple_size, 1)
        self.assertRaises(LayoutException, layout.check_tuple_size, 7)
        self.assertEqual(layout.check_tuple_size(4), None)
        self.assertEqual(layout.tuple_size, 4)

    def test_identifier_to_path(self):
        """Test path creation."""
        layout = Layout_NNNN_Tuple_Tree(tuple_size=2)
        self.assertRaises(LayoutException, layout.identifier_to_path, "")
        self.assertEqual(layout.identifier_to_path("a"), "a/a")
        self.assertEqual(layout.identifier_to_path("ab"), "ab/ab")
        self.assertEqual(layout.identifier_to_path("abc"), "ab/c/abc")
        self.assertEqual(layout.identifier_to_path("abcde"), "ab/cd/e/abcde")
        layout = Layout_NNNN_Tuple_Tree(tuple_size=3)
        self.assertEqual(layout.identifier_to_path("abcdefg"), "abc/def/g/abcdefg")
        self.assertEqual(layout.identifier_to_path("abcdefgh"), "abc/def/gh/abcdefgh")
        self.assertEqual(layout.identifier_to_path("abcdefghi"), "abc/def/ghi/abcdefghi")
