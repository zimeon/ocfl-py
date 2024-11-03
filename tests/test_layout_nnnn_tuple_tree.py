"""Digest tests."""
import unittest
from ocfl.layout_nnnn_tuple_tree import Layout_NNNN_Tuple_Tree


class TestAll(unittest.TestCase):
    """TestAll class to run tests."""

    def test01_encode(self):
        """Test encode."""
        tt = Layout_NNNN_Tuple_Tree()
        self.assertEqual(tt.encode(""), "")
        self.assertEqual(tt.encode("a"), "a")
        self.assertEqual(tt.encode("a/b:?"), "a=b+^3f")

    def test02_decode(self):
        """Test decode."""
        tt = Layout_NNNN_Tuple_Tree()
        self.assertEqual(tt.decode(""), "")
        self.assertEqual(tt.decode("a"), "a")
        self.assertEqual(tt.decode("a=b+^3f"), "a/b:?")

    def test03_identifier_to_path(self):
        """Test path creation."""
        tt = Layout_NNNN_Tuple_Tree(tuple_size=2)
        self.assertEqual(tt.identifier_to_path(""), "")
        self.assertEqual(tt.identifier_to_path("a"), "a/a")
        self.assertEqual(tt.identifier_to_path("ab"), "ab/ab")
        self.assertEqual(tt.identifier_to_path("abc"), "ab/c/abc")
        self.assertEqual(tt.identifier_to_path("abcde"), "ab/cd/e/abcde")
        tt = Layout_NNNN_Tuple_Tree(tuple_size=3)
        self.assertEqual(tt.identifier_to_path("abcdefg"), "abc/def/g/abcdefg")
        self.assertEqual(tt.identifier_to_path("abcdefgh"), "abc/def/gh/abcdefgh")
        self.assertEqual(tt.identifier_to_path("abcdefghi"), "abc/def/ghi/abcdefghi")
