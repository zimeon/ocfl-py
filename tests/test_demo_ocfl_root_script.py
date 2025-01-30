# -*- coding: utf-8 -*-
"""Tests/demo of ocfl-root.py client."""
from testlib import DemoTestCase


class TestAll(DemoTestCase):
    """TestAll class to run tests."""

    def test00_version(self):
        """Test showing version number."""
        out = self.run_script("Show version number",
                              ["python", "ocfl-root.py",
                               "--version"],
                              text="The `--version` argument will show version number and exit (but we still tave to specify a root and an action)")
        self.assertIn("ocfl-root.py is part of ocfl-py version", out)

    def test01_create_add(self):
        """Test store creation and object addition."""
        out = self.run_script("Create new store",
                              ["python", "ocfl-root.py", "create",
                               "--root=TMPDIR/root",
                               "--layout=nnnn-flat-quoted-storage-layout",
                               "-v"])
        self.assertIn("Created OCFL storage root", out)
        out = self.run_script("List empty store",
                              ["python", "ocfl-root.py", "list",
                               "--root=TMPDIR/root",
                               "-v"])
        self.assertIn("Found 0 OCFL Objects under root", out)
        out = self.run_script("Add object",
                              ["python", "ocfl-root.py", "add",
                               "--root=TMPDIR/root",
                               "--src", "fixtures/1.0/good-objects/minimal_one_version_one_file",
                               "-v"])
        self.assertIn("Added object ark:123/abc", out)
        self.assertIn("path ark%3A123%2Fabc", out)
        out = self.run_script("Error if we try to add the same object again",
                              ["python", "ocfl-root.py", "add",
                               "--root=TMPDIR/root",
                               "--src", "fixtures/1.0/good-objects/minimal_one_version_one_file",
                               "-v"])
        self.assertIn("Add object failed because path ark%3A123%2Fabc exists", out)

    def test02_explore_simple_root(self):
        """Test exploration of a simple OCFL object root."""
        out = self.run_script("List objects",
                              ["python", "ocfl-root.py", "list",
                               "--root=extra_fixtures/good-storage-roots/simple-root"])
        self.assertIn("ark%3A%2F12345%2Fbcd987 -- id=ark:/12345/bcd987", out)
        self.assertIn("ark%3A123%2Fabc -- id=ark:123/abc", out)
        self.assertIn("http%3A%2F%2Fexample.org%2Fminimal_mixed_digests -- id=http://example.org/minimal_mixed_digests", out)
        self.assertIn("Found 3 OCFL Objects under root extra_fixtures/good-storage-roots/simple-root", out)

    def test03_errors(self):
        """Test error cases."""
        out = self.run_script("Create new store",
                              ["python", "ocfl-root.py", "create",
                               "--root=TMPDIR/root",
                               "--layout=0002-flat-direct-storage-layout",
                               "-v"])
        self.assertIn("Created OCFL storage root", out)
        out = self.run_script("Add object",
                              ["python", "ocfl-root.py", "add",
                               "--root=TMPDIR/root",
                               "-v"])
        self.assertIn("Must specify object path with --src", out)

    def test04_build_ext0003_examples(self):
        """Build examples from storage root extension 0003."""
        # Example 2
        out = self.run_script("Create new store",
                              ["python", "ocfl-root.py", "create",
                               "--root=TMPDIR/ex2",
                               "--spec-version=1.0",
                               "--layout=0003-hash-and-id-n-tuple-storage-layout",
                               "--layout-params={\"digestAlgorithm\":\"md5\", \"tupleSize\":2, \"numberOfTuples\":15}",
                               "-v"])
        self.assertIn("Created OCFL storage root", out)
        out = self.run_script("Create add object-01",
                              ["python", "ocfl-root.py", "add",
                               "--root=TMPDIR/ex2",
                               "--src=extra_fixtures/1.0/good-objects/root_ext0003_object-01"])
        self.assertIn("Added object object-01", out)
        self.assertIn("ff/75/53/44/92/48/5e/ab/b3/9f/86/35/67/28/88/object-01", out)
        out = self.run_script("Create add horrible-obj",
                              ["python", "ocfl-root.py", "add",
                               "--root=TMPDIR/ex2",
                               "--src=extra_fixtures/1.0/good-objects/root_ext0003_horrible-obj"])
        self.assertIn("Added object ..hor/rib:le-$id", out)
        self.assertIn("08/31/97/66/fb/6c/29/35/dd/17/5b/94/26/77/17/%2e%2ehor%2frib%3ale-%24id", out)

    def test99_errors(self):
        """Test error conditions."""
        out = self.run_script("No valid command argument",
                              ["python", "ocfl-root.py"],
                              text="With no argument and error and suggections are shown.")
        self.assertIn("No command, nothing to do ", out)
        out = self.run_script("No source directory (--srcdir)",
                              ["python", "ocfl-root.py", "create"],
                              text="The `create` command requires a root to be specifed.")
        self.assertIn("The storage root must be set", out)
        out = self.run_script("No identifier",
                              ["python", "ocfl-root.py", "show",
                               "--root", "tmp"],
                              text="The `show` command requires an identifier.")
        self.assertIn("Must specify id", out)


if __name__ == "__main__":
    # Run in demo mode if run directly instead of through py.test
    TestAll.run_as_demo(title="OCFL Object Root Store manipulation script")
