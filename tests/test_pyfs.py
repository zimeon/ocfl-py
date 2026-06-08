"""Pyfs tests."""
import os.path
import unittest

from ocfl.pyfs import pyfs_openfs, pyfs_opendir_as_fs, pyfs_files_identical


class TestAll(unittest.TestCase):
    """TestAll class to run tests."""

    def test01_pyfs_openfs(self):
        """Test pyfs_openfs."""
        # local path
        fs = pyfs_openfs("tests/testdata/files")
        self.assertEqual(len(fs.ls("")), 2)
        self.assertEqual(len(fs.ls("empty")), 1)
        self.assertRaises(FileNotFoundError, fs.ls, "does_not_exist")
        # path does not exists
        self.assertRaises(FileNotFoundError, pyfs_openfs, "path_does_not_exist")
        # memory filesystem
        fs = pyfs_openfs("memory://")
        self.assertEqual(len(fs.ls("")), 0)

    def test02_pyfs_opendir_as_fs(self):
        """Test pyfs_opendir_as_fs."""
        # local path
        fs = pyfs_openfs("tests")
        dfs = pyfs_opendir_as_fs(fs, "testdata/files")
        self.assertTrue(dfs.exists("empty"))

    def testXX_pyfs_files_identical(self):
        """Test pyfs_files_identical."""
        def _write_file(fs, name, kbs, extra=""):
            with fs.open(name, "wb") as fh:
                for a in range(0, kbs):  # write 1kb at a time
                    fh.write(b"0123456789abcdef"*64)
                fh.write(extra)
                fh.close()
        fs = pyfs_openfs("memory://")
        _write_file(fs, "file0", 0, b"small")
        _write_file(fs, "file1", 16384, b"hello")
        _write_file(fs, "file2", 16384, b"hello")
        _write_file(fs, "file3", 16384, b"hell")
        _write_file(fs, "file4", 16384, b"hellb")
        self.assertTrue(pyfs_files_identical(fs, "file0", "file0"))
        self.assertFalse(pyfs_files_identical(fs, "file0", "file1"))
        self.assertTrue(pyfs_files_identical(fs, "file1", "file2"))
        self.assertFalse(pyfs_files_identical(fs, "file1", "file3"))
        self.assertFalse(pyfs_files_identical(fs, "file1", "file4"))
        # File doesn't exist
        self.assertRaises(FileNotFoundError, pyfs_files_identical, fs, "nope", "file0")
