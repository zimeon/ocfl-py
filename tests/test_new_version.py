"""NewVersion tests."""
import unittest

from ocfl.constants import DEFAULT_DIGEST_ALGORITHM, DEFAULT_SPEC_VERSION
from ocfl.inventory import Inventory
from ocfl.new_version import NewVersion, NewVersionException
from ocfl.version_metadata import VersionMetadata


class TestNewVersion(unittest.TestCase):
    """TestNewVersion class to run test for the Invenory class."""

    def test_init(self):
        """Test initialization."""
        nv = NewVersion(srcdir="fixtures")
        self.assertEqual(nv.srcdir, "fixtures")

    def test__map_filepath(self):
        """Test _map_filepath method."""
        nv = NewVersion()
        # default is uri
        nv.inventory = Inventory()
        nv.inventory.head = "v1"
        nv.content_path_normalization = "uri"
        self.assertEqual(nv._map_filepath("a"), "v1/content/a")
        self.assertEqual(nv._map_filepath(".a?"), "v1/content/%2Ea%3F")
        nv.inventory.manifest = {"digest1": ["v1/content/a"]}
        self.assertEqual(nv._map_filepath("a"), "v1/content/a__2")
        # md5
        nv = NewVersion()
        nv.inventory = Inventory()
        nv.inventory.head = "v1"
        nv.content_path_normalization = "md5"
        self.assertEqual(nv._map_filepath("a"), "v1/content/0cc175b9c0f1b6a8")
        nv.inventory.manifest = {"digest1": ["v1/content/0cc175b9c0f1b6a8"]}
        self.assertEqual(nv._map_filepath("a"), "v1/content/0cc175b9c0f1b6a8__2")
        # error case
        nv = NewVersion()
        nv.inventory = Inventory()
        nv.inventory.head = "v1"
        nv.content_path_normalization = "???"
        self.assertRaises(NewVersionException, nv._map_filepath, "a")

    def test_first_version(self):
        """Test first_version method."""
        # Minimal settings
        nv = NewVersion.first_version(srcdir="fixtures/1.1/content/spec-ex-full/v1",
                                      identifier="tfv1")
        self.assertEqual(nv.srcdir, "fixtures/1.1/content/spec-ex-full/v1")
        self.assertEqual(nv.inventory.id, "tfv1")
        self.assertEqual(nv.inventory.spec_version, DEFAULT_SPEC_VERSION)
        self.assertEqual(nv.inventory.digest_algorithm, DEFAULT_DIGEST_ALGORITHM)
        self.assertEqual(nv.inventory.content_directory, None)
        self.assertEqual(nv.inventory.fixity, {})
        self.assertTrue(nv.dedupe)
        self.assertEqual(nv.content_path_normalization, "uri")
        # Set everything
        vm = VersionMetadata(message="hello", name="me")
        nv = NewVersion.first_version(srcdir="fixtures/1.1/content/spec-ex-full/v2",
                                      identifier="tfv2",
                                      spec_version="1.0",
                                      digest_algorithm="sha256",
                                      content_directory="c",
                                      dedupe=False,
                                      metadata=vm,
                                      fixity=["md5", "sha1"],
                                      content_path_normalization="md5")
        self.assertEqual(nv.srcdir, "fixtures/1.1/content/spec-ex-full/v2")
        self.assertEqual(nv.inventory.id, "tfv2")
        self.assertEqual(nv.inventory.spec_version, "1.0")
        self.assertEqual(nv.inventory.digest_algorithm, "sha256")
        self.assertEqual(nv.inventory.content_directory, "c")
        self.assertEqual(nv.inventory.fixity, {"md5": {}, "sha1": {}})
        self.assertEqual(nv.message, "hello")
        self.assertEqual(nv.user_name, "me")
        self.assertFalse(nv.dedupe)
        self.assertEqual(nv.content_path_normalization, "md5")

    def test_next_version(self):
        """Test next_version_method."""
        inv = Inventory(filepath="fixtures/1.1/good-objects/spec-ex-full/v1/inventory.json")
        # Minimal, just inventory
        nv = NewVersion.next_version(srcdir="fixtures/1.1/content/spec-ex-full/v2",
                                     inventory=inv)
        self.assertEqual(nv.srcdir, "fixtures/1.1/content/spec-ex-full/v2")
        self.assertEqual(nv.inventory.id, "ark:/12345/bcd987")
        self.assertEqual(nv.inventory.spec_version, DEFAULT_SPEC_VERSION)
        self.assertEqual(nv.inventory.digest_algorithm, DEFAULT_DIGEST_ALGORITHM)
        self.assertEqual(nv.inventory.content_directory, None)
        self.assertEqual(set(nv.inventory.fixity.keys()), set(["md5", "sha1"]))
        self.assertTrue(nv.forward_delta)
        self.assertTrue(nv.dedupe)
        self.assertEqual(nv.content_path_normalization, "uri")
        # Maximal, set everything
        vm = VersionMetadata(message="unhelpful message")
        nv = NewVersion.next_version(srcdir="fixtures/1.1/content/spec-ex-full/v3",
                                     inventory=inv,
                                     forward_delta=False,
                                     dedupe=False,
                                     metadata=vm,
                                     content_path_normalization="md5",
                                     carry_content_forward=True,
                                     old_digest_algorithm="bogus")
        self.assertEqual(nv.srcdir, "fixtures/1.1/content/spec-ex-full/v3")
        self.assertEqual(nv.inventory.id, "ark:/12345/bcd987")
        self.assertEqual(nv.message, "unhelpful message")
        self.assertEqual(nv.user_name, None)
        self.assertFalse(nv.forward_delta)
        self.assertFalse(nv.dedupe)
        self.assertEqual(nv.content_path_normalization, "md5")
        self.assertEqual(nv.old_digest_algorithm, "bogus")
        self.assertEqual(nv.inventory.content_paths, ['v1/content/foo/bar.xml', 'v1/content/empty.txt', 'v1/content/image.tiff'])
        # Error
        self.assertRaises(NewVersionException,
                          NewVersion.next_version,
                          srcdir="fixtures/1.1/content/spec-ex-full/v2",
                          inventory=inv,
                          spec_version="1.0")

    def test_add(self):
        """Test add method."""
        inv = Inventory(filepath="fixtures/1.1/good-objects/updates_three_versions_one_file/inventory.json")
        nv = NewVersion.next_version(inventory=inv)
        # Bad content paths
        self.assertRaises(NewVersionException, nv.add, "src1", "logical1", "vBAD/content/something")
        self.assertRaises(NewVersionException, nv.add, "src1", "logical1", "v4/BAD/something")
        # Content path already exists
        nv.add("fixtures/1.1/content/README.md", "logical1", "v4/content/a_file.txt")
        self.assertRaises(NewVersionException, nv.add, "src1", "logical1", "v4/content/a_file.txt")
        # Deduping checks (use the content already added)
        nv.dedupe = False
        nv.add("fixtures/1.1/content/README.md", "logical2", "v4/content/a_file_dupe.txt")
        self.assertIn("v4/content/a_file_dupe.txt", nv.inventory.content_paths)
        nv.dedupe = True
        nv.add("fixtures/1.1/content/README.md", "logical3", "v4/content/a_file_dupe2.txt")
        self.assertNotIn("v4/content/a_file_dupe2.txt", nv.inventory.content_paths)

    def test_delete(self):
        """Test delete method."""

    def test_rename(self):
        """Test rename method."""
