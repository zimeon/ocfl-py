# -*- coding: utf-8 -*-
"""Tests/demo building spec examples."""
from testlib import DemoTestCase


class TestAll(DemoTestCase):
    """TestAll class to run tests."""

    def test00_minimal_example(self):
        """Test for minumal example."""
        text = "The digest type sha512-spec-ex is sha512 with most of the content " \
               "stripped out and replaced with an ellipsis. This is inventory should " \
               "match the example in <https://ocfl.io/1.1/spec/#example-minimal-object>."
        out = self.run_script("Minimal example",
                              ["python", "ocfl-object.py", "build",
                               "--src", "fixtures/1.1/content/spec-ex-minimal",
                               "--id", "http://example.org/minimal",
                               "--spec-version", "1.1",
                               "--digest", "sha512-spec-ex",
                               "--created", "2018-10-02T12:00:00Z",
                               "--message", "One file",
                               "--name", "Alice",
                               "--address", "alice@example.org",
                               "-v"],
                              text=text)
        self.assertIn("20a60123...f67", out)

    def test01_versioned_example(self):
        """Test for versioned example."""
        text = "This is inventory should match the example with 3 versions in " \
               "<https://ocfl.io/1.1/spec/#example-versioned-object>."
        out = self.run_script("Versioned example",
                              ["python", "ocfl-object.py", "build",
                               "--src", "fixtures/1.1/content/spec-ex-full",
                               "--spec-version", "1.1",
                               "--id", "ark:/12345/bcd987",
                               "--fixity", "md5",
                               "--fixity", "sha1",
                               "--digest", "sha512-spec-ex",
                               "-v"],
                              text=text)
        self.assertIn("4d27c86b026ff70...b53", out)

    def test02_different_paths_example(self):
        """Test for different paths example."""
        text = "This is inventory should match the example showing how content " \
               "paths may differ from logical paths in " \
               "<https://ocfl.io/1.1/spec/#example-object-diff-paths>."
        out = self.run_script("Versioned example",
                              ["python", "ocfl-object.py", "build",
                               "--src", "fixtures/1.1/content/spec-ex-diff-paths",
                               "--id", "http://example.org/diff-paths",
                               "--spec-version", "1.1",
                               "--digest", "sha512-spec-ex",
                               "--normalization", "md5",
                               "--created", "2019-03-14T20:31:00Z",
                               "-v"],
                              text=text)
        # Content paths
        self.assertIn("v1/content/3bacb119a98a15c5", out)
        self.assertIn("v1/content/9f2bab8ef869947d", out)


if __name__ == "__main__":
    # Run in demo mode if run directly instead of through py.test
    TestAll.run_as_demo(title="Build the v1.1 specification examples")
