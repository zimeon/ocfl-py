"""Digest tests."""
import unittest
from ocfl.object import Object, remove_first_directory


class TestAll(unittest.TestCase):
    """TestAll class to run tests."""

    def test01_remove_first_directory(self):
        """Test encode."""
        self.assertEqual(remove_first_directory(''), '')
        self.assertEqual(remove_first_directory('a'), '')
        self.assertEqual(remove_first_directory('a/b'), 'b')
        self.assertEqual(remove_first_directory('a/b/'), 'b')
        self.assertEqual(remove_first_directory('a/b/c'), 'b/c')
