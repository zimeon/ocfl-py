"""Fsw tests."""
import unittest

from ocfl.fsw import fsw_openfs, fsw_opendir_as_fs, fsw_walk, fsw_walk_files, fsw_listdir_names, fsw_files_identical


class TestAll(unittest.TestCase):
    """TestAll class to run tests."""

    def test01_fsw_openfs(self):
        """Test fsw_openfs."""
        # local path
        fs = fsw_openfs("tests/testdata/files")
        self.assertEqual(len(fs.ls("")), 2)
        self.assertEqual(len(fs.ls("empty")), 1)
        self.assertRaises(FileNotFoundError, fs.ls, "does_not_exist")
        # path does not exists
        self.assertRaises(FileNotFoundError, fsw_openfs, "path_does_not_exist")
        # memory filesystem
        fs = fsw_openfs("memory://")
        self.assertEqual(len(fs.ls("")), 0)
        # dir doesn't exists
        self.assertRaises(FileNotFoundError, fsw_openfs, "temp://new_dir")
        # test of create
        fs = fsw_openfs("temp://new_dir", create=True)

    def test02_fsw_opendir_as_fs(self):
        """Test fsw_opendir_as_fs."""
        # local path
        fs = fsw_openfs("tests")
        dfs = fsw_opendir_as_fs(fs, "testdata/files")
        self.assertTrue(dfs.exists("empty"))

    def test03_fsw_walk(self):
        """Test fsw_walk."""
        fs = fsw_openfs("fixtures/1.0/content/spec-ex-full")
        edirs = {}
        efiles = {}
        for dirpath, dirs, files in fsw_walk(fs, "/"):
            edirs[dirpath] = sorted(dirs)
            efiles[dirpath] = sorted(files)
        self.assertEqual(edirs["/"], ["v1", "v2", "v3"])
        self.assertEqual(efiles["/"], ["v1_inventory.json", "v2_inventory.json", "v3_inventory.json"])
        self.assertEqual(edirs["/v2"], ["foo"])
        self.assertEqual(efiles["/v2"], ["empty.txt", "empty2.txt"])
        # Test with zip because that is special case with
        # known issue -- FIXME
        # fs = fsw_openfs("zip://extra_fixtures/1.0/bad-storage-roots/simple-bad-root.zip")
        # edirs = {}
        # efiles = {}
        # for dir, dirs, files in fsw_walk(fs, "/"):
        #    edirs[dir] = sorted(dirs)
        #    efiles[dir] = sorted(files)
        # self.assertEqual(edirs["/"], ['ark%3A%2F12345%2Fbcd987', 'ark%3A123%2Fabc', 'dir_with_file_but_no_declaration', 'empty_dir', 'object_multiple_declarations', 'object_unknown_version', 'object_unrecognized_declaration'])
        # self.assertEqual(efiles["/"], ["0=ocfl_1.0"])
        # self.assertEqual(edirs["/object_multiple_declarations"], ["v1"])
        # self.assertEqual(efiles["/object_multiple_declarations"], [])

    def test04_fsw_walk_file(self):
        """Test fsw_walk_file."""
        fs = fsw_openfs("fixtures/1.0/content/spec-ex-full")
        self.assertEqual(sorted(fsw_walk_files(fs, "/v3")),
                         ['empty2.txt', 'foo/bar.xml', 'image.tiff'])
        files = fsw_walk_files(fs, "/")
        self.assertIn("v3_inventory.json", files)
        self.assertIn("v1/foo/bar.xml", files)
        # Check zip - FIXME
        # fs = fsw_openfs("zip://extra_fixtures/1.0/warn-objects/W003_empty_content_dir.zip")
        # files = fsw_walk_files(fs, "/")
        # self.assertIn("0=ocfl_object_1.0", files)
        # self.assertIn("inventory.json", files)
        # self.assertIn("v1/content/my_content/poe.txt", files)

    def test05_fsw_listdir_names(self):
        """Test fsw_listdir_names."""
        fs = fsw_openfs("fixtures/1.0/content/spec-ex-full")
        files = sorted(fsw_listdir_names(fs, path="v3"))
        self.assertEqual(files, ['empty2.txt', 'foo', 'image.tiff'])
        # zip - FIXME
        # fs = fsw_openfs("zip://extra_fixtures/1.0/warn-objects/W003_empty_content_dir.zip")
        # files = sorted(fsw_listdir_names(fs, "v1"))
        # self.assertEqual(files, ['content', 'inventory.json', 'inventory.json.sha512'])

    def test06_fsw_files_identical(self):
        """Test fsw_files_identical."""
        def _write_file(fs, name, kbs, extra=""):
            with fs.open(name, "wb") as fh:
                for _ in range(0, kbs):  # write 1kb at a time
                    fh.write(b"0123456789abcdef" * 64)
                fh.write(extra)
                fh.close()
        fs = fsw_openfs("memory://")
        _write_file(fs, "file0", 0, b"small")
        _write_file(fs, "file1", 16384, b"hello")
        _write_file(fs, "file2", 16384, b"hello")
        _write_file(fs, "file3", 16384, b"hell")
        _write_file(fs, "file4", 16384, b"hellb")
        self.assertTrue(fsw_files_identical(fs, "file0", "file0"))
        self.assertFalse(fsw_files_identical(fs, "file0", "file1"))
        self.assertTrue(fsw_files_identical(fs, "file1", "file2"))
        self.assertFalse(fsw_files_identical(fs, "file1", "file3"))
        self.assertFalse(fsw_files_identical(fs, "file1", "file4"))
        # File doesn't exist
        self.assertRaises(FileNotFoundError, fsw_files_identical, fs, "nope", "file0")
