# -*- coding: utf-8 -*-
"""Tests/demo of ocfl-sidecar.py client."""
from testlib import DemoTestCase


class TestAll(DemoTestCase):
    """TestAll class to run tests."""

    def test00_version(self):
        """Test showing version number."""
        out = self.run_script("Show version number",
                              ["python", "ocfl-sidecar.py", "--version"],
                              text="The `--version` argument will show version number and exit")
        self.assertIn("ocfl-sidecar.py is part of ocfl-py version", out)

    def test01_create(self):
        """Test creation of sidecar file."""
        out = self.run_script("Set up directory as object root",
                              ["mkdir", "-v", "TMPDIR/obj"])
        self.assertIn("created directory", out)
        out = self.run_script("Copy in an inventory from an example",
                              ["cp", "-v", "fixtures/1.0/good-objects/minimal_one_version_one_file/inventory.json", "TMPDIR/obj"])
        self.assertIn("obj/inventory.json", out)
        out = self.run_script("Create sidecar",
                              ["python", "ocfl-sidecar.py", "TMPDIR/obj"],
                              text="The digest type will be set by reading the inventory (in this case, sha512)")
        self.assertIn("INFO:root:Written sidecar file inventory.json.sha512", out)
        out = self.run_script("Create a new sidecar with a different digest",
                              ["python", "ocfl-sidecar.py", "--digest", "sha256", "TMPDIR/obj"],
                              text="The digest type is set with the --digest parameter")
        self.assertIn("INFO:root:Written sidecar file inventory.json.sha256", out)


if __name__ == "__main__":
    # Run in demo mode if run directly instead of through py.test
    TestAll.run_as_demo(title="OCFL Sidecar creation and update script")
