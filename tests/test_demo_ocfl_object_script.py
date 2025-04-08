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
                              ["python", "ocfl-object.py", "create",
                               "--id", "http://example.org/obj1",
                               "--src", "fixtures/1.0/content/cf1/v1",
                               "--created", "2024-10-24T18:30:01Z"],
                              text="Without an `--objdir` argument the script just writes out the inventory for the object that would have been created.")
        self.assertIn('"id": "http://example.org/obj1"', out)
        self.assertIn("### Inventory for v1", out)
        out = self.run_script("Inventory for new object with three versions",
                              ["python", "ocfl-object.py", "build",
                               "--id", "http://example.org/obj2",
                               "--src", "fixtures/1.0/content/cf3",
                               "--metadata", "extra_fixtures/1.0/content/spec-ex-full-metadata.json"],
                              text="Without an `--objdir` argument the script just writes out the inventory for each version in the object that would have been created.")
        self.assertIn('"id": "http://example.org/obj2"', out)
        self.assertIn("### Inventory for v3", out)

    def test02_create_v1(self):
        """Test object creation with just v1."""
        out = self.run_script("New object with just v1",
                              ["python", "ocfl-object.py", "create",
                               "--id", "http://example.org/obj1",
                               "--src", "fixtures/1.0/content/cf1/v1",
                               "--objdir", "TMPDIR/obj1",
                               "--created", "2024-10-24T18:30:03Z",
                               "-v"])
        self.assertIn("Created OCFL object http://example.org/obj1", out)
        out = self.run_script("New object with two identical files",
                              ["python", "ocfl-object.py", "create",
                               "--id", "http://example.org/obj_dedupe",
                               "--src", "extra_fixtures/content/dupe-files",
                               "--objdir", "TMPDIR/obj_dedupe",
                               "--created", "2025-04-08T14:00:01Z",
                               "-v"],
                              text="The two identical files are deduped, only one copy being stored and using the first name of the dupes by alphanumeric sort")
        self.assertIn("Created OCFL object http://example.org/obj_dedupe", out)
        self.demo_tree("obj_dedupe",
                       text="Object tree shows v1 with content:")
        self.demo_file_exists("obj_dedupe/v1/content/file1.txt", 10)
        self.demo_file_does_not_exist("obj_dedupe/v1/content/file1_dupe.txt")
        out = self.run_script("New object with two identical files not deduped",
                              ["python", "ocfl-object.py", "create",
                               "--id", "http://example.org/obj_no_dedupe",
                               "--src", "extra_fixtures/content/dupe-files",
                               "--objdir", "TMPDIR/obj_no_dedupe",
                               "--created", "2025-04-08T14:00:02Z",
                               "--no-dedupe",
                               "-v"],
                              text="The identical file are not deduped because the --no-dedupe flag is given")
        self.assertIn("Created OCFL object http://example.org/obj_no_dedupe", out)
        self.demo_tree("obj_no_dedupe",
                       text="Object tree shows v1 with content:")
        self.demo_file_exists("obj_no_dedupe/v1/content/file1.txt", 10)
        self.demo_file_exists("obj_no_dedupe/v1/content/file1_dupe.txt", 10)

    def test03_create_multi(self):
        """Test object build with three versions."""
        out = self.run_script("New object with three versions",
                              ["python", "ocfl-object.py", "build",
                               "--id", "http://example.org/obj2",
                               "--src", "fixtures/1.0/content/cf3",
                               "--objdir", "TMPDIR/obj2",
                               "-v"])
        self.assertIn("Built object http://example.org/obj2", out)
        self.assertIn("with 3 versions", out)

    def test04_extract(self):
        """Test extract of version."""
        out = self.run_script("Extract v1 of content in an OCFL v1.0 object",
                              ["python", "ocfl-object.py", "extract",
                               "--objdir", "fixtures/1.0/good-objects/spec-ex-full",
                               "--objver", "v1",
                               "--dstdir", "TMPDIR/v1",
                               "-v"],
                              text="Version 1 object with location specified in `--objdir` and the first version specified in `--objver`, extract into TMPDIR/v1:")
        self.assertIn("Extracted content for v1 in", out)
        out = self.run_script(None,
                              ["find", "-s", "TMPDIR/v1", "-print"],
                              text="and the extracted files are:")
        self.assertEqual(os.path.getsize(os.path.join(self.tmpdir, "v1/empty.txt")), 0)
        self.assertFalse(os.path.exists(os.path.join(self.tmpdir, "v1/empty2.txt")))
        self.assertEqual(os.path.getsize(os.path.join(self.tmpdir, "v1/foo/bar.xml")), 272)
        self.assertEqual(os.path.getsize(os.path.join(self.tmpdir, "v1/image.tiff")), 2021)
        #
        # Now in v1.1 object
        out = self.run_script("Extract v2 of content in an OCFL v1.1 object",
                              ["python", "ocfl-object.py", "extract",
                               "--objver", "v2",
                               "--objdir", "fixtures/1.1/good-objects/spec-ex-full",
                               "--dstdir", "TMPDIR/v2",
                               "-v"])
        self.assertIn("Extracted content for v2 in", out)
        out = self.run_script(None,
                              ["find", "-s", "TMPDIR/v2", "-print"],
                              text="and the extracted files are:")
        self.assertEqual(os.path.getsize(os.path.join(self.tmpdir, "v2/empty.txt")), 0)
        self.assertEqual(os.path.getsize(os.path.join(self.tmpdir, "v2/empty2.txt")), 0)
        self.assertEqual(os.path.getsize(os.path.join(self.tmpdir, "v2/foo/bar.xml")), 272)
        self.assertFalse(os.path.exists(os.path.join(self.tmpdir, "v2/image.tiff")))
        #
        # And "head" should extract v3
        out = self.run_script("Extract head version (v3) of content in the same OCFL v1.1 object",
                              ["python", "ocfl-object.py", "extract",
                               "--objver", "head",
                               "--objdir", "fixtures/1.1/good-objects/spec-ex-full",
                               "--dstdir", "TMPDIR/head",
                               "-v"])
        self.assertIn("Extracted content for v3 in", out)
        out = self.run_script(None,
                              ["find", "-s", "TMPDIR/v3", "-print"],
                              text="and the extracted files are:")
        self.assertEqual(os.path.getsize(os.path.join(self.tmpdir, "v2/empty.txt")), 0)
        self.assertEqual(os.path.getsize(os.path.join(self.tmpdir, "v2/empty2.txt")), 0)
        self.assertEqual(os.path.getsize(os.path.join(self.tmpdir, "v2/foo/bar.xml")), 272)
        self.assertFalse(os.path.exists(os.path.join(self.tmpdir, "v2/image.tiff")))
        #
        # Extract individual files
        out = self.run_script("Extract foo/bar.xml of v3 into a new directory",
                              ["python", "ocfl-object.py", "extract",
                               "--objver", "v3",
                               "--objdir", "fixtures/1.1/good-objects/spec-ex-full",
                               "--logical-path", "foo/bar.xml",
                               "--dstdir", "TMPDIR/files",
                               "-v"])
        self.assertIn("Extracted foo/bar.xml in v3", out)
        out = self.run_script(None,
                              ["find", "-s", "TMPDIR/files", "-print"],
                              text="and the extracted file is:")
        self.assertEqual(os.path.getsize(os.path.join(self.tmpdir, "files/bar.xml")), 272)
        # Extract individual file into dir that exists
        out = self.run_script("Extract image.tiff of v3 (default) into the same directory",
                              ["python", "ocfl-object.py", "extract",
                               "--objdir", "fixtures/1.1/good-objects/spec-ex-full",
                               "--logical-path", "image.tiff",
                               "--dstdir", "TMPDIR/files",
                               "-v"])
        self.assertIn("Extracted image.tiff in v3", out)
        out = self.run_script(None,
                              ["find", "-s", "TMPDIR/files", "-print"],
                              text="and the directory now contains two extracted files:")
        self.assertEqual(os.path.getsize(os.path.join(self.tmpdir, "files/image.tiff")), 2021)

    def test20_errors(self):
        """Test error conditions."""
        out = self.run_script("No valid command argument",
                              ["python", "ocfl-object.py"],
                              text="With no argument and error and suggections are shown.")
        self.assertIn("No command, nothing to do", out)
        out = self.run_script("No source directory (--srcdir)",
                              ["python", "ocfl-object.py", "create",
                               "--objdir", "TMP/v1"],
                              text="The `create` command requires a source.")
        self.assertIn("Must specify either --srcdir", out)
        out = self.run_script("No identifier",
                              ["python", "ocfl-object.py", "show",
                               "--srcdir", "tmp"],
                              text="The `show` command requires --objdir.")
        self.assertIn("the following arguments are required: --objdir", out)


if __name__ == "__main__":
    # Run in demo mode if run directly instead of through py.test
    TestAll.run_as_demo(title="Demonstration of OCFL Object manipulation script")
