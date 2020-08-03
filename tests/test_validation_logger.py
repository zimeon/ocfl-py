"""Version tests."""
import argparse
import unittest
from ocfl.validation_logger import ValidationLogger


class TestAll(unittest.TestCase):
    """TestAll class to run tests."""

    def test_init(self):
        """Test init method."""
        vl = ValidationLogger()
        self.assertEqual(vl.num_errors, 0)
        self.assertEqual(vl.num_warnings, 0)

    def test_error_or_warning(self):
        """Test error_or_warning method."""
        vc = {
            "E999": {
                "params": ["param1"],
                "description": {
                    "en": "It is all broken, %s - whoaaa!",
                    "zz": "No params here"
                }
            },
            "W998": {
                "description": {}
            },
            "W999": {
                "description": {
                    "ab": "999 warning",
                    "xy": "Warning 999"
                }
            }}
        vl = ValidationLogger(lang='zz', validation_codes=vc)
        vl.error_or_warning("E111")
        self.assertEqual(len(vl.messages), 1)
        self.assertIn("Unknown error: E111 - params ({})", vl.messages[-1])
        vl.error_or_warning("E222", one="two", three="four")
        self.assertEqual(len(vl.messages), 2)
        self.assertIn("Unknown error: E222 - params ({'one': 'two', 'three': 'four'})", vl.messages[-1])
        vl.error_or_warning("E999")
        self.assertEqual(len(vl.messages), 3)
        self.assertIn("[E999] No params here {}", vl.messages[-1])
        vl.lang = 'yy'
        vl.error_or_warning("E999", param1="THAT")
        self.assertEqual(len(vl.messages), 4)
        self.assertIn("[E999] It is all broken, THAT - whoaaa!", vl.messages[-1])
        # Warning with warnings not show
        vl.error_or_warning("W999", severity="warning")
        self.assertEqual(len(vl.messages), 4)
        # Now show warnings and try again
        vl.show_warnings = True
        vl.error_or_warning("W999", severity="warning")
        self.assertEqual(len(vl.messages), 5)
        # No language match, not en, so show first alphabetically
        self.assertIn("[W999] 999 warning", vl.messages[-1])
        # Now with other match
        vl.lang = "xy"
        vl.error_or_warning("W999", severity="warning")
        self.assertEqual(len(vl.messages), 6)
        self.assertIn("[W999] Warning 999", vl.messages[-1])
        # No description
        vl.error_or_warning("W998", severity="warning")
        self.assertEqual(len(vl.messages), 7)
        self.assertIn("[W998] Unknown warning without a description", vl.messages[-1])

    def test_error(self):
        """Test error method."""
        vl = ValidationLogger()
        vl.error("E111")
        self.assertEqual(vl.num_errors, 1)
        self.assertIn("Unknown error: E111 - params ({})", vl.messages[-1])

    def test_warning(self):
        """Test warning method."""
        vl = ValidationLogger(show_warnings=True)
        vl.warning("W333")
        self.assertEqual(vl.num_warnings, 1)
        self.assertIn("Unknown warning: W333 - params ({})", vl.messages[-1])
