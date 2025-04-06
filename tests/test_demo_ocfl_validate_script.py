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
        out = self.run_script("Warning test for a v1.0 object",
                              ["python", "ocfl-validate.py",
                               "fixtures/1.0/warn-objects/W004_uses_sha256"],
                              text="The test shows warning W004 with a link to the v1.0 specification")
        self.assertIn("fixtures/1.0/warn-objects/W004_uses_sha256 is VALID", out)
        self.assertIn("[W004]", out)
        self.assertIn("https://ocfl.io/1.0/spec/#W004", out)
        #
        out = self.run_script("Warning test with -q (--quiet) flag",
                              ["python", "ocfl-validate.py",
                               "-q", "fixtures/1.0/warn-objects/W004_uses_sha256"],
                              text="The -q or --quiet flag will silence any warning messages")
        self.assertIn("fixtures/1.0/warn-objects/W004_uses_sha256 is VALID", out)
        self.assertNotIn("[W004]", out)
        #
        out = self.run_script("Warning test for a v1.1 object with several warnings",
                              ["python", "ocfl-validate.py",
                               "fixtures/1.1/warn-objects/W001_W004_W005_zero_padded_versions"],
                              text="The test shows warning W004 with a link to the v1.0 specification")
        self.assertIn("fixtures/1.1/warn-objects/W001_W004_W005_zero_padded_versions is VALID", out)
        self.assertIn("[W001]", out)
        self.assertIn("[W004]", out)
        self.assertIn("[W005]", out)
        self.assertIn("https://ocfl.io/1.1/spec/#W001", out)


if __name__ == "__main__":
    # Run in demo mode if run directly instead of through py.test
    TestAll.run_as_demo(title="Demonstration of OCFL Object and Storage Root validation script")
