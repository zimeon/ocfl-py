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
        """Test creation of a sidecar file."""
        out = self.run_script("Set up directory as object root",
                              ["mkdir", "-v", "TMPDIR/obj"])
        out = self.run_script("Copy in an inventory from an example",
                              ["cp", "-v", "fixtures/1.0/good-objects/minimal_one_version_one_file/inventory.json", "TMPDIR/obj"])
        self.assertIn("obj/inventory.json", out)
        out = self.run_script("Create sidecar for inventory in specified object",
                              ["python", "ocfl-sidecar.py", "TMPDIR/obj"],
                              text="The digest type will be set by reading the inventory (in this case, sha512)")
        self.assertIn("Written sidecar file", out)
        self.assertIn("obj/inventory.json.sha512", out)
        out = self.run_script("Create sidecar for specified inventory",
                              ["python", "ocfl-sidecar.py", "TMPDIR/obj/inventory.json"],
                              text="The digest type will be set by reading the inventory (in this case, sha512)")
        self.assertIn("obj/inventory.json.sha512", out)
        out = self.run_script("Create a new sidecar with a different digest",
                              ["python", "ocfl-sidecar.py", "--digest", "sha256", "TMPDIR/obj"],
                              text="The digest type is set with the --digest parameter")
        self.assertIn("obj/inventory.json.sha256", out)

    def test02_create_multiple(self):
        """Test creation of multiple sidecar files."""
        out = self.run_script("Set up directory as object 1 root",
                              ["mkdir", "-v", "TMPDIR/obj1"])
        out = self.run_script("Set up directory as object 2 root",
                              ["mkdir", "-v", "TMPDIR/obj2"])
        out = self.run_script("Set up directory as object 3 root",
                              ["mkdir", "-v", "TMPDIR/obj3"])
        out = self.run_script("Copy in an inventory from an example for object 1",
                              ["cp", "-v", "fixtures/1.1/good-objects/minimal_uppercase_digests/inventory.json", "TMPDIR/obj1"])
        self.assertIn("obj1/inventory.json", out)
        out = self.run_script("Copy in an inventory from an example for object 2",
                              ["cp", "-v", "fixtures/1.1/good-objects/minimal_mixed_digests/inventory.json", "TMPDIR/obj2"])
        self.assertIn("obj2/inventory.json", out)
        out = self.run_script("Copy in an inventory from an example for object 3",
                              ["cp", "-v", "fixtures/1.1/good-objects/minimal_no_content/inventory.json", "TMPDIR/obj3"])
        self.assertIn("obj3/inventory.json", out)
        out = self.run_script("Create sidecars for all 3 inventory files",
                              ["python", "ocfl-sidecar.py",
                               "TMPDIR/obj1", "TMPDIR/obj2", "TMPDIR/obj3"])
        self.assertIn("Written sidecar file ", out)
        self.assertIn("obj1/inventory.json.sha512", out)
        self.assertIn("obj2/inventory.json.sha512", out)
        self.assertIn("obj3/inventory.json.sha512", out)


if __name__ == "__main__":
    # Run in demo mode if run directly instead of through py.test
    TestAll.run_as_demo(title="OCFL Sidecar creation and update script")
