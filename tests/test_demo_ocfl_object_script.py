# -*- coding: utf-8 -*-
"""Tests/demo of ocfl-object.py client."""
import os.path

from testlib import DemoTestCase


class TestAll(DemoTestCase):
    """TestAll class to run tests."""

    def test00_version(self):
        """Test showing version number."""
        out = self.run_script("Show version number",
                              ["python", "ocfl-object.py", "--version"],
                              text="The `--version` argument will show version number and exit")
        self.assertIn("ocfl-object.py is part of ocfl-py version", out)

    def test01_create_inventory_dryrun(self):
        """Test object inventory creation with output to stdout."""
        out = self.run_script("Inventory for new object with just v1",
                              ["python", "ocfl-object.py",
                               "--create",
                               "--id", "http://example.org/obj1",
                               "--src", "fixtures/1.0/content/cf1/v1"],
                              text="Without an `--objdir` argument the script just writes out the inventory for the object that would have been created.")
        self.assertIn('"id": "http://example.org/obj1"', out)
        self.assertIn("### Inventory for v1", out)
        out = self.run_script("Inventory for new object with three versions",
                              ["python", "ocfl-object.py",
                               "--build",
                               "--id", "http://example.org/obj2",
                               "--src", "fixtures/1.0/content/cf3"],
                              text="Without an `--objdir` argument the script just writes out the inventory for each version in the object that would have been created.")
        self.assertIn('"id": "http://example.org/obj2"', out)
        self.assertIn("### Inventory for v1", out)
        self.assertIn("### Inventory for v2", out)
        self.assertIn("### Inventory for v3", out)

    def test02_create_v1(self):
        """Test object creation with just v1."""
        out = self.run_script("New object with just v1",
                              ["python", "ocfl-object.py",
                               "--create",
                               "--id", "http://example.org/obj1",
                               "--src", "fixtures/1.0/content/cf1/v1",
                               "--objdir", "TMPDIR/obj1",
                               "-v"])
        self.assertIn("Created OCFL object http://example.org/obj1", out)

    def test03_create_multi(self):
        """Test object build with three versions."""
        out = self.run_script("New object with three versions",
                              ["python", "ocfl-object.py",
                               "--build",
                               "--id", "http://example.org/obj2",
                               "--src", "fixtures/1.0/content/cf3",
                               "--objdir", "TMPDIR/obj2",
                               "-v"])
        self.assertIn("Built object http://example.org/obj2 with 3 versions", out)

    def test04_extract(self):
        """Test extract of version."""
        out = self.run_script("Extract v1 of an OCFL v1.0 object",
                              ["python", "ocfl-object.py",
                               "--extract", "v1",
                               "--objdir", "fixtures/1.0/good-objects/spec-ex-full",
                               "--dstdir", "TMPDIR/v1",
                               "-v"])
        # Expect:
        # v1
        # ├── [          0]  empty.txt
        # ├── [        102]  foo
        # │   └── [        272]  bar.xml
        # └── [       2021]  image.tiff
        self.assertIn('Extracted content for v1 in', out)
        self.assertEqual(os.path.getsize(os.path.join(self.tmpdir, "v1/empty.txt")), 0)
        self.assertFalse(os.path.exists(os.path.join(self.tmpdir, "v1/empty2.txt")))
        self.assertEqual(os.path.getsize(os.path.join(self.tmpdir, "v1/foo/bar.xml")), 272)
        self.assertEqual(os.path.getsize(os.path.join(self.tmpdir, "v1/image.tiff")), 2021)
        out = self.run_script("Extract v2 of content in the same OCFL v1.1 object",
                              ["python", "ocfl-object.py",
                               "--extract", "v2",
                               "--objdir", "fixtures/1.1/good-objects/spec-ex-full",
                               "--dstdir", "TMPDIR/v2",
                               "-v"])
        # Expect:
        # v2
        # ├── [          0]  empty.txt
        # ├── [          0]  empty2.txt
        # └── [        102]  foo
        #    └── [        272]  bar.xml
        self.assertIn('Extracted content for v2 in', out)
        self.assertEqual(os.path.getsize(os.path.join(self.tmpdir, "v2/empty.txt")), 0)
        self.assertEqual(os.path.getsize(os.path.join(self.tmpdir, "v2/empty2.txt")), 0)
        self.assertEqual(os.path.getsize(os.path.join(self.tmpdir, "v2/foo/bar.xml")), 272)
        self.assertFalse(os.path.exists(os.path.join(self.tmpdir, "v2/image.tiff")))

    def test20_errors(self):
        """Test error conditions."""
        out = self.run_script("No valid command argument",
                              ["python", "ocfl-object.py"],
                              text="With no argument and error and suggections are shown.")
        self.assertIn("Exactly one command ", out)
        out = self.run_script("No source directory (--srcdir)",
                              ["python", "ocfl-object.py", "--create"],
                              text="The `--create` action requires a source.")
        self.assertIn("Must specify either --srcdir", out)
        out = self.run_script("No identifier",
                              ["python", "ocfl-object.py", "--create", "--srcdir", "tmp"],
                              text="The `--create` action requires an identifier.")
        self.assertIn("Identifier is not set!", out)


if __name__ == "__main__":
    # Run in demo mode if run directly instead of through py.test
    TestAll.run_as_demo(title="OCFL Object manipulation script")
