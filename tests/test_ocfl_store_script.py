# -*- coding: utf-8 -*-
"""Tests/demo of ocfl-store.py client."""
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

    tmpdir = None
    n = 0
    m = 0
    demo = False
    keep_tmpdirs = False

    def setUp(self):
        """Setup for each test."""
        type(self).n += 1  # access class variable not copy
        self.m = 0
        self.tmpdir = tempfile.mkdtemp(prefix='test' + str(self.n) + '_')
        print("\n## %d. %s\n" % (self.n, self.shortDescription()))

    def tearDown(self):
        """Teardown for each test."""
        if self.tmpdir is not None and not self.keep_tmpdirs:
            shutil.rmtree(self.tmpdir)

    def run_ocfl_store(self, desc, options, treedir='store'):
        """Run the ocfl-store.py script."""
        self.m += 1
        print("\n### %d.%d %s\n" % (self.n, self.m, desc))
        cmd = ['python', 'ocfl-store.py',
               '--root', os.path.join(self.tmpdir, treedir)] + options
        code = 0
        try:
            out = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode('utf-8')
        except subprocess.CalledProcessError as e:
            out = e.output.decode('utf-8')
            code = e.returncode
        out = "```\n> " + ' '.join(cmd) + "\n" + out + "```\n"
        if self.demo:
            out = re.sub(self.tmpdir, 'tmp', out)
        print(out)
        if code == 0:
            tree = subprocess.check_output('cd %s; tree -a %s' % (self.tmpdir, treedir),
                                           stderr=subprocess.STDOUT,
                                           shell=True).decode('utf-8')
            print("```\n" + tree + "```\n")
        else:
            print("Exited with code %d" % (code))
        return out

    def test01_create_add(self):
        """Test store initialization and object addition."""
        out = self.run_ocfl_store("Create new store",
                                  ['--init', '-v'])
        self.assertIn('Created OCFL storage root', out)
        out = self.run_ocfl_store("List empty store",
                                  ['--list', '-v'])
        self.assertIn('Found 0 OCFL Objects under root', out)
        out = self.run_ocfl_store("Add object",
                                  ['--add', '--src', 'fixtures/objects/of1', '--disposition', 'identity', '-v'])

    def test02_errors(self):
        """Test error cases."""
        out = self.run_ocfl_store("Create new store",
                                  ['--init', '-v'])
        self.assertIn('Created OCFL storage root', out)
        out = self.run_ocfl_store("Add object",
                                  ['--add', '-v'])
        self.assertIn('Must specify object path with --src', out)

if __name__ == '__main__':
    # Run in demo mode if run directly instead of through py.test
    TestAll.demo = True
    print("# Demo output from " + __file__)
    unittest.main()
