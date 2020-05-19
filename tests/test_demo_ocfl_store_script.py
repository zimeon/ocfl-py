# -*- coding: utf-8 -*-
"""Tests/demo of ocfl-store.py client."""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

from testlib import DemoTestCase


class TestAll(DemoTestCase):
    """TestAll class to run tests."""

    def test00_version(self):
        """Test showing version number."""
        out = self.run_script("Show version number",
                              ["python", "ocfl-store.py",
                               "--version",
                               "--root=TMPDIR/root",
                               "--list"],
                              text="The `--version` argument will show version number and exit (but we still tave to specify a root and an action)")
        self.assertIn("ocfl-store.py is part of ocfl-py version", out)

    def test01_create_add(self):
        """Test store initialization and object addition."""
        out = self.run_script("Create new store",
                              ["python", "ocfl-store.py",
                               "--root=TMPDIR/root",
                               "--init",
                               "-v"])
        self.assertIn("Created OCFL storage root", out)
        out = self.run_script("List empty store",
                              ["python", "ocfl-store.py",
                               "--root=TMPDIR/root",
                               "--list", "-v"])
        self.assertIn("Found 0 OCFL Objects under root", out)
        out = self.run_script("Add object",
                              ["python", "ocfl-store.py",
                               "--root=TMPDIR/root",
                               "--add",
                               "--src", "fixtures/1.0/good-objects/minimal_one_version_one_file",
                               "--disposition", "identity",
                               "-v"])
        self.assertIn("Copying from fixtures/1.0/good-objects/minimal_one_version_one_file to", out)
        self.assertIn("root/ark%3A123%2Fabc", out)

    def test02_errors(self):
        """Test error cases."""
        out = self.run_script("Create new store",
                              ["python", "ocfl-store.py",
                               "--root=TMPDIR/root",
                               "--init",
                               "-v"])
        self.assertIn("Created OCFL storage root", out)
        out = self.run_script("Add object",
                              ["python", "ocfl-store.py",
                               "--root=TMPDIR/root",
                               "--add",
                               "-v"])
        self.assertIn("Must specify object path with --src", out)


if __name__ == "__main__":
    # Run in demo mode if run directly instead of through py.test
    TestAll.run_as_demo(title="OCFL Object Root Store manipulation script")
