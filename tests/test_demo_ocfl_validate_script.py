# -*- coding: utf-8 -*-
"""Tests/demo of ocfl-validate.py client."""
from testlib import DemoTestCase


class TestAll(DemoTestCase):
    """TestAll class to run tests."""

    def test00_version(self):
        """Test showing version number."""
        out = self.run_script("Show version number",
                              ["python", "ocfl-validate.py", "--version"],
                              text="The `--version` argument will show version number and exit")
        self.assertIn("ocfl-validate.py is part of ocfl-py version", out)

    def test01_good(self):
        """Test simple good case."""
        out = self.run_script("Good test",
                              ["python", "ocfl-validate.py",
                               "fixtures/1.0/good-objects/minimal_uppercase_digests"])
        self.assertIn("fixtures/1.0/good-objects/minimal_uppercase_digests is VALID", out)

    def test02_warnings(self):
        """Test warning cases."""
        out = self.run_script("Warning test with -q",
                              ["python", "ocfl-validate.py",
                               "-q", "fixtures/1.0/warn-objects/W004_uses_sha256"])
        self.assertIn("fixtures/1.0/warn-objects/W004_uses_sha256 is VALID", out)
        self.assertNotIn("[W004]", out)
        out = self.run_script("Warning test without -q",
                              ["python", "ocfl-validate.py",
                               "fixtures/1.0/warn-objects/W004_uses_sha256"])
        self.assertIn("fixtures/1.0/warn-objects/W004_uses_sha256 is VALID", out)
        self.assertIn("[W004]", out)


if __name__ == "__main__":
    # Run in demo mode if run directly instead of through py.test
    TestAll.run_as_demo(title="OCFL Object and Storage Root validation script")
