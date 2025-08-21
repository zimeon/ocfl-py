"""ValidationLogger tests."""
import unittest
from ocfl.validation_logger import ValidationLogger


class TestAll(unittest.TestCase):
    """TestAll class to run tests."""

    def test_init(self):
        """Test init method."""
        vl = ValidationLogger()
        self.assertEqual(vl.num_errors, 0)
        self.assertEqual(vl.num_warnings, 0)

    def test_log(self):
        """Test log method."""
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
        vl = ValidationLogger(lang="zz", validation_codes=vc)
        vl.log("E333", is_error=True)
        self.assertEqual(len(vl.messages), 1)
        self.assertIn("Unknown error: E333 - params ({})", vl.messages[-1])
        vl.log("E222", is_error=True, one="two", three="four")
        self.assertEqual(len(vl.messages), 2)
        self.assertIn("Unknown error: E222 - params ({'one': 'two', 'three': 'four'})", vl.messages[-1])
        vl.log("E999", is_error=True)
        self.assertEqual(len(vl.messages), 3)
        self.assertIn("[E999] No params here {}", vl.messages[-1])
        vl.lang = "yy"
        vl.log("E999", is_error=True, param1="THAT")
        self.assertEqual(len(vl.messages), 4)
        self.assertIn("[E999] It is all broken, THAT - whoaaa!", vl.messages[-1])
        # Warning with warnings not show
        vl.log("W999", is_error=False)
        self.assertEqual(len(vl.messages), 4)
        # Now show warnings and try again
        vl.log_warnings = True
        vl.log("W999", is_error=False)
        self.assertEqual(len(vl.messages), 5)
        # No language match, not en, so show first alphabetically
        self.assertIn("[W999] 999 warning", vl.messages[-1])
        # Now with other match
        vl.lang = "xy"
        vl.log("W999", is_error=False)
        self.assertEqual(len(vl.messages), 6)
        self.assertIn("[W999] Warning 999", vl.messages[-1])
        # No description
        vl.log("W998", is_error=False)
        self.assertEqual(len(vl.messages), 7)
        self.assertIn("[W998] Unknown warning without a description", vl.messages[-1])

    def test_error(self):
        """Test error method."""
        vl = ValidationLogger()
        vl.error("E333")
        self.assertEqual(vl.num_errors, 1)
        self.assertIn("Unknown error: E333 - params ({})", vl.messages[-1])

    def test_warning(self):
        """Test warning method."""
        vl = ValidationLogger(log_warnings=True)
        vl.warning("W333")
        self.assertEqual(vl.num_warnings, 1)
        self.assertIn("Unknown warning: W333 - params ({})", vl.messages[-1])

    def test_status_str_and_str(self):
        """Test status_str method and __str__."""
        vl = ValidationLogger()
        self.assertEqual(vl.status_str(), "")
        vl.error("E991")
        vl.error("E992")
        self.assertEqual(vl.status_str(),
                         "Unknown error: E991 - params ({})\nUnknown error: E992 - params ({})")
        # str(vl) is just a call to vl.status_str()
        self.assertEqual(vl.status_str(), str(vl))
