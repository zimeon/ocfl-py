# -*- coding: utf-8 -*-
"""Tests/demo of ocfl-object.py client."""
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
        if self.demo:
            print("\n## %d. %s" % (self.n, self.shortDescription()))

    def tearDown(self):
        """Teardown for each test."""
        if self.tmpdir is not None and not self.keep_tmpdirs:
            shutil.rmtree(self.tmpdir)

    def run_ocfl_store(self, desc, options, text=None, treedir='object',
                       include_objdir=True, include_dstdir=False):
        """Run the ocfl-store.py script."""
        self.m += 1
        if self.demo:
            print("\n### %d.%d %s\n" % (self.n, self.m, desc))
        if text:
            print(text + '\n')
        cmd = ['python', 'ocfl-object.py']
        if include_objdir:
            cmd += ['--objdir', os.path.join(self.tmpdir, treedir)]
        elif include_dstdir:
            cmd += ['--dstdir', self.tmpdir]
        cmd += options
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
        if code == 0 and include_objdir:
            tree = subprocess.check_output('cd %s; tree -a %s' % (self.tmpdir, treedir),
                                           stderr=subprocess.STDOUT,
                                           shell=True).decode('utf-8')
            print("```\n" + tree + "```\n")
        elif code == 0 and include_dstdir:
            tree = subprocess.check_output('cd %s; tree -a .' % (self.tmpdir),
                                           stderr=subprocess.STDOUT,
                                           shell=True).decode('utf-8')
            print("```\n" + tree + "```\n")
        else:
            print("Exited with code %d" % (code))
        return out

    def test01_create_inventory_dryrun(self):
        """Test object inventory creation with output to stdout."""
        out = self.run_ocfl_store("Inventory for new object with just v1",
                                  ['--create', '--id', 'http://example.org/obj1', '--src', 'fixtures/1.0/content/cf1/v1'],
                                  text="Without an `--objdir` argument the script just writes out the inventory for the object that would have been created.",
                                  include_objdir=False)
        self.assertIn('"id": "http://example.org/obj1"', out)
        self.assertIn('### Inventory for v1', out)
        out = self.run_ocfl_store("Inventory for new object with three versions",
                                  ['--build', '--id', 'http://example.org/obj2', '--src', 'fixtures/1.0/content/cf3'],
                                  text="Without an `--objdir` argument the script just writes out the inventory for each version in the object that would have been created.",
                                  include_objdir=False)
        self.assertIn('"id": "http://example.org/obj2"', out)
        self.assertIn('### Inventory for v1', out)
        self.assertIn('### Inventory for v2', out)
        self.assertIn('### Inventory for v3', out)

    def test02_create_v1(self):
        """Test object creation with just v1."""
        out = self.run_ocfl_store("New object with just v1",
                                  ['--create', '--id', 'http://example.org/obj1', '--src', 'fixtures/1.0/content/cf1/v1', '-v'])
        self.assertIn('Created object http://example.org/obj1', out)

    def test03_create_multi(self):
        """Test object build with three versions."""
        out = self.run_ocfl_store("New object with three versions",
                                  ['--build', '--id', 'http://example.org/obj2', '--src', 'fixtures/1.0/content/cf3', '-v'])
        self.assertIn('Built object http://example.org/obj2 with 3 versions', out)

    def test04_extract(self):
        """Test extract of version."""
        out = self.run_ocfl_store("Extract v1",
                                  ['--extract', 'v1', '--objdir', 'fixtures/1.0/good-objects/spec-ex-full', '-v'],
                                  include_objdir=False,
                                  include_dstdir=True)
        # Excpect:
        # v1
        # ├── [          0]  empty.txt
        # ├── [        102]  foo
        # │   └── [        272]  bar.xml
        # └── [       2021]  image.tiff
        self.assertEqual(os.path.getsize(os.path.join(self.tmpdir, 'v1/empty.txt')), 0)
        self.assertFalse(os.path.exists(os.path.join(self.tmpdir, 'v1/empty2.txt')))
        self.assertEqual(os.path.getsize(os.path.join(self.tmpdir, 'v1/foo/bar.xml')), 272)
        self.assertEqual(os.path.getsize(os.path.join(self.tmpdir, 'v1/image.tiff')), 2021)
        out = self.run_ocfl_store("Extract v2",
                                  ['--extract', 'v2', '--objdir', 'fixtures/1.0/good-objects/spec-ex-full', '-v'],
                                  include_objdir=False,
                                  include_dstdir=True)
        # Expect:
        # v2
        # ├── [          0]  empty.txt
        # ├── [          0]  empty2.txt
        # └── [        102]  foo
        #    └── [        272]  bar.xml
        self.assertEqual(os.path.getsize(os.path.join(self.tmpdir, 'v2/empty.txt')), 0)
        self.assertEqual(os.path.getsize(os.path.join(self.tmpdir, 'v2/empty2.txt')), 0)
        self.assertEqual(os.path.getsize(os.path.join(self.tmpdir, 'v2/foo/bar.xml')), 272)
        self.assertFalse(os.path.exists(os.path.join(self.tmpdir, 'v2/image.tiff')))

    def test20_errors(self):
        """Test error conditions."""
        out = self.run_ocfl_store("No valid command argument",
                                  [],
                                  include_objdir=False)
        self.assertIn('Exactly one command ', out)
        out = self.run_ocfl_store("No identifier",
                                  ['--create'],
                                  include_objdir=False)
        self.assertIn('Must specify --srcdir', out)
        out = self.run_ocfl_store("No identifier",
                                  ['--create', '--srcdir', 'tmp'],
                                  include_objdir=False)
        self.assertIn('Identifier is not set!', out)


if __name__ == '__main__':
    # Run in demo mode if run directly instead of through py.test
    TestAll.demo = True
    print("# Demo output from " + __file__)
    unittest.main()
