# -*- coding: utf-8 -*-
"""Tests/demo of ocfl-store.py client."""
from testlib import DemoTestCase


class TestAll(DemoTestCase):
    """TestAll class to run tests."""

    def test00_version(self):
        """Test showing version number."""
        out = self.run_script("Show version number",
                              ["python", "ocfl-store.py",
                               "--version"],
                              text="The `--version` argument will show version number and exit (but we still tave to specify a root and an action)")
        self.assertIn("ocfl-store.py is part of ocfl-py version", out)

    def test01_create_add(self):
        """Test store initialization and object addition."""
        out = self.run_script("Create new store",
                              ["python", "ocfl-store.py", "init",
                               "--root=TMPDIR/root",
                               "--layout=nnnn-flat-quoted-storage-layout",
                               "-v"])
        self.assertIn("Created OCFL storage root", out)
        out = self.run_script("List empty store",
                              ["python", "ocfl-store.py", "list",
                               "--root=TMPDIR/root",
                               "-v"])
        self.assertIn("Found 0 OCFL Objects under root", out)
        out = self.run_script("Add object",
                              ["python", "ocfl-store.py", "add",
                               "--root=TMPDIR/root",
                               "--src", "fixtures/1.0/good-objects/minimal_one_version_one_file",
                               "-v"])
        self.assertIn("Copying from fixtures/1.0/good-objects/minimal_one_version_one_file to", out)
        self.assertIn("root/ark%3A123%2Fabc", out)
        self.assertIn("Copied", out)

    def test02_explore_simple_root(self):
        """Test exploration of a simple OCFL object root."""
        out = self.run_script("List objects",
                              ["python", "ocfl-store.py", "list",
                               "--root=extra_fixtures/good-storage-roots/simple-root"])
        self.assertIn("ark%3A%2F12345%2Fbcd987 -- id=ark:/12345/bcd987", out)
        self.assertIn("ark%3A123%2Fabc -- id=ark:123/abc", out)
        self.assertIn("http%3A%2F%2Fexample.org%2Fminimal_mixed_digests -- id=http://example.org/minimal_mixed_digests", out)
        self.assertIn("Found 3 OCFL Objects under root extra_fixtures/good-storage-roots/simple-root", out)

    def test03_errors(self):
        """Test error cases."""
        out = self.run_script("Create new store",
                              ["python", "ocfl-store.py", "init",
                               "--root=TMPDIR/root",
                               "--layout=0002-flat-direct-storage-layout",
                               "-v"])
        self.assertIn("Created OCFL storage root", out)
        out = self.run_script("Add object",
                              ["python", "ocfl-store.py", "add",
                               "--root=TMPDIR/root",
                               "-v"])
        self.assertIn("Must specify object path with --src", out)


if __name__ == "__main__":
    # Run in demo mode if run directly instead of through py.test
    TestAll.run_as_demo(title="OCFL Object Root Store manipulation script")
