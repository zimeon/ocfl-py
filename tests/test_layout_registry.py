"""Layout registry tests."""
import unittest
from ocfl.layout import Layout
from ocfl.layout_registry import add_layout, get_layout, layout_is_supported


class TestAll(unittest.TestCase):
    """TestAll class to run tests."""

    def test_defaults(self):
        """Test default settings supported."""
        # Supported
        self.assertTrue(layout_is_supported("0002-flat-direct-storage-layout"))
        self.assertTrue(isinstance(get_layout("0002-flat-direct-storage-layout"), Layout))
        self.assertTrue(layout_is_supported("flat-direct"))  # alias set up
        self.assertTrue(isinstance(get_layout("flat-direct"), Layout))
        # Unknown
        self.assertFalse(layout_is_supported("unknown"))
        self.assertRaises(Exception, get_layout, "unknown")

    def test_add_layout(self):
        """Test addition of new Layout class."""
        self.assertFalse(layout_is_supported("mylayout"))
        add_layout("mylayout", Layout)
        self.assertTrue(layout_is_supported("mylayout"))
        self.assertTrue(isinstance(get_layout("mylayout"), Layout))
