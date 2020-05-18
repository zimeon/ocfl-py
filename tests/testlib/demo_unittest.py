# -*- coding: utf-8 -*-
"""Modified version of unittest.TestCase that includes demo support."""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import __main__ as main


class DemoTestCase(unittest.TestCase):
    """Modified unittest.TestCase to support demos."""

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
        if self.demo:
            print("\n## %d. %s" % (self.n, self.shortDescription()))

    def tearDown(self):
        """Teardown for each test."""
        if self.tmpdir is not None and not self.keep_tmpdirs:
            shutil.rmtree(self.tmpdir)

    def run_script(self, desc, options, text=None, treedir=None):
        """Run the ocfl-store.py script."""
        self.m += 1
        if self.demo:
            print("\n### %d.%d %s\n" % (self.n, self.m, desc))
        if text:
            print(text + '\n')
        cmd = ['python']
        for option in options:
            cmd.append(option.replace('TMPDIR', self.tmpdir))
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
        else:
            return out
        if code == 0 and treedir:
            tree = subprocess.check_output('cd %s; tree -a %s' % (self.tmpdir, treedir),
                                           stderr=subprocess.STDOUT,
                                           shell=True).decode('utf-8')
            print("```\n" + tree + "```\n")
        else:
            print("Exited with code %d" % (code))
        return out

    @classmethod
    def run_as_demo(cls, title="Demo output"):
        """Run tests in demo mode."""
        cls.demo = True
        print("# " + title + "\n")
        print("_Output from `" + main.__file__ + "`._")
        unittest.main(verbosity=0)  # No dots added while running
