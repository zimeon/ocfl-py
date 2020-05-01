# -*- coding: utf-8 -*-
"""Tests/demo of ocfl-validate.py client."""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest


class TestAll(unittest.TestCase):
    """TestAll class to run tests."""

    n = 0
    m = 0
    demo = False

    def setUp(self):
        """Setup for each test."""
        type(self).n += 1  # access class variable not copy
        self.m = 0
        if self.demo:
            print("\n## %d. %s\n" % (self.n, self.shortDescription()))

    def run_ocfl_validate(self, desc, options):
        """Run the ocfl-validate.py script."""
        self.m += 1
        if self.demo:
            print("\n### %d.%d %s\n" % (self.n, self.m, desc))
        cmd = ['python', 'ocfl-validate.py'] + options
        code = 0
        try:
            out = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode('utf-8')
        except subprocess.CalledProcessError as e:
            out = e.output.decode('utf-8')
            code = e.returncode
        if self.demo:
            print("```\n> " + ' '.join(cmd) + "\n" + out + "```\n")
        return out

    def test01_good(self):
        """Test simple good case."""
        out = self.run_ocfl_validate("Good test", ['fixtures/1.0/good-objects/minimal_uppercase_digests'])
        self.assertIn('fixtures/1.0/good-objects/minimal_uppercase_digests is VALID', out)

    def test02_warnings(self):
        """Test warning cases."""
        out = self.run_ocfl_validate("Warning test without -v", ['fixtures/1.0/warn-objects/W004_uses_sha256'])
        self.assertIn('fixtures/1.0/warn-objects/W004_uses_sha256 is VALID', out)
        self.assertNotIn('[W004]', out)
        out = self.run_ocfl_validate("Warning test with -v", ['-v', 'fixtures/1.0/warn-objects/W004_uses_sha256'])
        self.assertIn('fixtures/1.0/warn-objects/W004_uses_sha256 is VALID', out)
        self.assertIn('[W004]', out)


if __name__ == '__main__':
    # Run in demo mode if run directly instead of through py.test
    TestAll.demo = True
    print("# Demo output from " + __file__)
    unittest.main()
