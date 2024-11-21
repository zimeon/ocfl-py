"""NewVersion tests."""
import unittest

from ocfl.inventory import Inventory
from ocfl.new_version import NewVersion, NewVersionException
from ocfl.pyfs import pyfs_openfs


class TestNewVersion(unittest.TestCase):
    """TestNewVersion class to run test for the Invenory class."""

    def test_init(self):
        """Test initialization."""
        nv = NewVersion(objdir="", srcdir="")
        self.assertEqual(nv.inventory.head, "v1")

    def test__map_filepath(self):
        """Test _map_filepath method."""
        nv = NewVersion()
        # default is uri
        nv.head = "v1"
        self.assertEqual(nv._map_filepath("a"), "v1/content/a")
        self.assertEqual(nv._map_filepath(".a?"), "v1/content/%2Ea%3F")
        nv.inventory.manifest = {"digest1": ["v1/content/a"]}
        self.assertEqual(nv._map_filepath("a"), "v1/content/a__2")
        # md5
        nv = NewVersion()
        nv.head = "v1"
        nv.content_path_normalization = "md5"
        self.assertEqual(nv._map_filepath("a"), "v1/content/0cc175b9c0f1b6a8")
        nv.inventory.manifest = {"digest1": ["v1/content/0cc175b9c0f1b6a8"]}
        self.assertEqual(nv._map_filepath("a"), "v1/content/0cc175b9c0f1b6a8__2")
        # error case
        nv = NewVersion()
        nv.head = "v1"
        nv.content_path_normalization = "???"
        self.assertRaises(NewVersionException, nv._map_filepath, "a")

    def test_add(self):
        """Test add method."""
        inv = Inventory(filepath="fixtures/1.1/good-objects/updates_three_versions_one_file/inventory.json")
        nv = NewVersion(inventory=inv)
        # Bad content paths
        self.assertRaises(NewVersionException, nv.add, "src1", "log1", "vBAD/content/something")
        self.assertRaises(NewVersionException, nv.add, "src1", "log1", "v4/BAD/something")
        # Content path already exists
        nv.add("fixtures/1.1/content/README.md", "log1", "v4/content/a_file.txt")
        self.assertRaises(NewVersionException, nv.add, "src1", "log1", "v4/content/a_file.txt")
        # Generate content path


    def test_delete(self):
        """Test delete method."""
        pass

    def test_rename(self):
        """Test rename method."""
        pass
