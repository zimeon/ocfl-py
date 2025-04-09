# -*- coding: utf-8 -*-
"""Modified version of unittest.TestCase that includes demo support."""
import os
import re
import shutil
import subprocess
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
        """Do setup for each test."""
        type(self).n += 1  # access class variable not copy
        self.m = 0
        self.tmpdir = tempfile.mkdtemp(prefix="test" + str(self.n) + "_")
        if self.demo:
            print("\n## %d. %s" % (self.n, self.shortDescription()))

    def tearDown(self):
        """Teardown for each test."""
        if self.tmpdir is not None and not self.keep_tmpdirs:
            shutil.rmtree(self.tmpdir)

    def run_script(self, desc, options, text=None):
        """Run the ocfl-root.py script.

        Usually desc will be a section heading for this test. However, if desc
        is None then we do note create a new section. This is useful for follow
        ons to a test such as showing a directory.
        """
        if desc:
            self.m += 1
            if self.demo:
                print("\n### %d.%d %s\n" % (self.n, self.m, desc))
        if text:
            text = re.sub("TMPDIR", "tmp", text)
            print(text + "\n")
        cmd = []
        for option in options:
            cmd.append(option.replace("TMPDIR", self.tmpdir))
        code = 0
        try:
            out = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode("utf-8")
        except subprocess.CalledProcessError as e:
            out = e.output.decode("utf-8")
            code = e.returncode
        out = "```\n> " + " ".join(cmd) + "\n" + out + "```\n"
        if self.demo:
            out = re.sub(self.tmpdir, "tmp", out)
            print(out)
            if code != 0:
                print("(last command exited with return code %d)\n" % (code))
        return out

    def demo_tree(self, treedir, text=None):
        """Show directory tree from treedir under TMPDIR if in demo mode."""
        if self.demo:
            if text is not None:
                print(text + "\n")
            cmd = ["find", "-s", os.path.join(self.tmpdir, treedir), "-print"]
            out = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode("utf-8")
            out = "```\n> " + " ".join(cmd) + "\n" + out + "```\n"
            out = re.sub(self.tmpdir, "tmp", out)
            print(out)

    def demo_text(self, text=None):
        """Show text if in demo mode."""
        if self.demo:
            if text is not None:
                print(text + "\n")

    def demo_file_exists(self, file, size=None):
        """Test file exists under tmpdir, size if specified."""
        self.assertTrue(os.path.exists(os.path.join(self.tmpdir, file)))
        if size is not None:
            self.assertEqual(os.path.getsize(os.path.join(self.tmpdir, file)), size)
        if self.demo:
            if size is not None:
                print("File `tmp/%s` exists with size %d\n" % (file, size))
            else:
                print("File `tmp/%s` exists\n" % (file))

    def demo_file_does_not_exist(self, file):
        """Test file does not exist under tmpdir."""
        self.assertFalse(os.path.exists(os.path.join(self.tmpdir, file)))
        if self.demo:
            print("File `tmp/%s` does not exist\n" % (file))

    @classmethod
    def run_as_demo(cls, title="Demo output"):
        """Run tests in demo mode."""
        cls.demo = True
        print("# " + title + "\n")
        script_name = re.sub(r"""^.*/tests/""", "tests/", main.__file__)
        print("_Output from `" + script_name + "`._")
        unittest.main(verbosity=0)  # No dots added while running
