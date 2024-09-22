"""Digest tests."""
import unittest
from ocfl.uuid_quadtree import UUIDQuadtree


class TestAll(unittest.TestCase):
    """TestAll class to run tests."""

    def test01_encode(self):
        """Test NOOP encode."""
        uuqt = UUIDQuadtree()
        self.assertEqual(uuqt.encode(''), '')
        self.assertEqual(uuqt.encode('a'), 'a')
        self.assertEqual(uuqt.encode('a/b:?'), 'a/b:?')

    def test02_decode(self):
        """Test NOOP decode."""
        uuqt = UUIDQuadtree()
        self.assertEqual(uuqt.decode(''), '')
        self.assertEqual(uuqt.decode('a'), 'a')
        self.assertEqual(uuqt.decode('a/b:?'), 'a/b:?')

    def test03_identifier_to_path(self):
        """Test path creation."""
        uuqt = UUIDQuadtree()
        self.assertEqual(uuqt.identifier_to_path('urn:uuid:6ba7b810-9dad-11d1-80b4-00c04fd430c8'),
                         '6ba7/b810/9dad/11d1/80b4/00c0/4fd4/30c8')
        # Bad ones
        self.assertRaises(Exception, uuqt.identifier_to_path, '')
        self.assertRaises(Exception, uuqt.identifier_to_path, '6ba7b810-9dad-11d1-80b4-00c04fd430c8')
        self.assertRaises(Exception, uuqt.identifier_to_path, 'uuid:6ba7b810-9dad-11d1-80b4-00c04fd430c8')
        self.assertRaises(Exception, uuqt.identifier_to_path, 'urn:uuid:6ba7b810-9dad-11d1-80b4-00c04fd430cX')
