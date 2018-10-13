"""Digest tests."""
import unittest
from ocfl.disposition import get_dispositor


class TestAll(unittest.TestCase):
    """TestAll class to run tests."""

    def test_everything(self):
        """Test everything, just a little."""
        d = get_dispositor('pairtree')
        self.assertEqual(d.identifier_to_path('abcd'), 'ab/cd/abcd')
        d = get_dispositor('tripletree')
        self.assertEqual(d.identifier_to_path('abcd'), 'abc/d/abcd')
        d = get_dispositor('quadtree')
        self.assertEqual(d.identifier_to_path('abcde'), 'abcd/e/abcde')
        d = get_dispositor('uuid_quadtree')
        self.assertEqual(d.identifier_to_path('urn:uuid:6ba7b810-9dad-11d1-80b4-00c04fd430c8'),
                         '6ba7/b810/9dad/11d1/80b4/00c0/4fd4/30c8')
        # Errors
        self.assertRaises(Exception, get_dispositor)
        self.assertRaises(Exception, get_dispositor, None)
        self.assertRaises(Exception, get_dispositor, 'unknown')
