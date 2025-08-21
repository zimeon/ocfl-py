"""Layout_NNNN_UUID_Quadtree tests."""
import unittest
from ocfl.layout import LayoutException
from ocfl.layout_nnnn_uuid_quadtree import Layout_NNNN_UUID_Quadtree


class TestAll(unittest.TestCase):
    """TestAll class to run tests."""

    def test_config(self):
        """Test config property."""
        layout = Layout_NNNN_UUID_Quadtree()
        self.assertEqual(set(layout.config.keys()), set(("extensionName", "prefix")))

    def test_check_prefix(self):
        """Test check_prefix method."""
        layout = Layout_NNNN_UUID_Quadtree()
        self.assertRaises(LayoutException, layout.check_prefix, None)
        self.assertRaises(LayoutException, layout.check_prefix, 53)
        self.assertRaises(LayoutException, layout.check_prefix, "")  # stil not!
        self.assertEqual(layout.check_prefix("Pref"), None)
        self.assertEqual(layout.prefix, "Pref")

    def test_encode(self):
        """Test NOOP encode."""
        uuqt = Layout_NNNN_UUID_Quadtree()
        self.assertEqual(uuqt.encode(""), "")
        self.assertEqual(uuqt.encode("a"), "a")
        self.assertEqual(uuqt.encode("a/b:?"), "a/b:?")

    def test_decode(self):
        """Test NOOP decode."""
        uuqt = Layout_NNNN_UUID_Quadtree()
        self.assertEqual(uuqt.decode(""), "")
        self.assertEqual(uuqt.decode("a"), "a")
        self.assertEqual(uuqt.decode("a/b:?"), "a/b:?")

    def test03_identifier_to_path(self):
        """Test path creation."""
        uuqt = Layout_NNNN_UUID_Quadtree()
        self.assertEqual(uuqt.identifier_to_path("urn:uuid:6ba7b810-9dad-11d1-80b4-00c04fd430c8"),
                         "6ba7/b810/9dad/11d1/80b4/00c0/4fd4/30c8")
        # Bad ones
        self.assertRaises(Exception, uuqt.identifier_to_path, "")
        self.assertRaises(Exception, uuqt.identifier_to_path, "6ba7b810-9dad-11d1-80b4-00c04fd430c8")
        self.assertRaises(Exception, uuqt.identifier_to_path, "uuid:6ba7b810-9dad-11d1-80b4-00c04fd430c8")
        self.assertRaises(Exception, uuqt.identifier_to_path, "urn:uuid:6ba7b810-9dad-11d1-80b4-00c04fd430cX")
