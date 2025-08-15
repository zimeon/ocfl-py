"""NewVersion tests."""
import unittest

from ocfl.constants import DEFAULT_DIGEST_ALGORITHM, DEFAULT_SPEC_VERSION
from ocfl.inventory import Inventory
from ocfl.new_version import NewVersion, NewVersionException
from ocfl.version_metadata import VersionMetadata


def make_inventory_with_state(state, head="v2", prev_state=None):
    """Make inventory with given state and head for tests."""
    inv = Inventory()
    inv.spec_version = "1.1"
    inv.id = "test"
    inv.digest_algorithm = "sha512"
    inv.init_manifest_and_versions()
    # Add previous version if provided
    if prev_state is not None:
        inv.add_version("v1", state=prev_state)
        inv.head = "v1"
    inv.add_version(head, state=state)
    inv.head = head
    return inv


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

    def test_diff_with_previous_add_delete(self):
        """Test diff_with_previous method with add and delete."""
        # Previous version: one file
        prev_state = {
            "digestA": ["fileA.txt"]
        }
        # Current version: fileA.txt deleted, fileB.txt added, fileC.txt added with same digest as fileA.txt
        curr_state = {
            "digestB": ["fileB.txt"],
            "digestA": ["fileC.txt"]
        }
        inv = make_inventory_with_state(curr_state, head="v2", prev_state=prev_state)
        # Instead of creating a new version, just set head to v2 and use NewVersion with carry_content_forward=True
        nv = NewVersion.next_version(inventory=inv)
        nv.inventory.head = "v2"
        diff = nv.diff_with_previous()
        assert ("A", "digestB", "fileB.txt") in diff
        assert ("A", "digestA", "fileC.txt") in diff
        assert ("D", "digestA", "fileA.txt") in diff
        assert len(diff) == 3

    def test_diff_with_previous_no_previous_version_all_adds(self):
        """Test diff_with_previous method with no previous version."""
        curr_state = {
            "digestA": ["fileA.txt"],
            "digestB": ["fileB.txt"]
        }
        inv = make_inventory_with_state(curr_state, head="v1")
        nv = NewVersion.next_version(inventory=inv)
        nv.inventory.head = "v1"
        diff = nv.diff_with_previous()
        self.assertIn(("A", "digestA", "fileA.txt"), diff)
        self.assertIn(("A", "digestB", "fileB.txt"), diff)
        self.assertEqual(len(diff), 2)

    def test_diff_with_previous_multiple_logical_paths_same_digest(self):
        """Test diff_with_previous with same digest, changing logical paths."""
        # Previous version: two logical paths for same digest
        prev_state = {
            "digestX": ["file1.txt", "file2.txt"]
        }
        # Current version: file2.txt deleted, file3.txt added for same digest
        curr_state = {
            "digestX": ["file1.txt", "file3.txt"]
        }
        inv = make_inventory_with_state(curr_state, head="v2", prev_state=prev_state)
        nv = NewVersion.next_version(inventory=inv)
        nv.inventory.head = "v2"
        diff = nv.diff_with_previous()
        self.assertIn(("D", "digestX", "file2.txt"), diff)
        self.assertIn(("A", "digestX", "file3.txt"), diff)
        for op in diff:
            self.assertIn(op[0], ("A", "D"))

    def test_diff_with_previous_multiple_adds_and_deletes(self):
        """Test diff_with_previous with a mix of changes."""
        # Previous version: two logical paths for same digest
        prev_state = {
            "digestY": ["a.txt", "b.txt"]
        }
        # Current version: both logical paths deleted, two new added
        curr_state = {
            "digestY": ["c.txt", "d.txt"]
        }
        inv = make_inventory_with_state(curr_state, head="v2", prev_state=prev_state)
        nv = NewVersion.next_version(inventory=inv)
        nv.inventory.head = "v2"
        diff = nv.diff_with_previous()
        self.assertIn(("D", "digestY", "a.txt"), diff)
        self.assertIn(("D", "digestY", "b.txt"), diff)
        self.assertIn(("A", "digestY", "c.txt"), diff)
        self.assertIn(("A", "digestY", "d.txt"), diff)
        self.assertEqual(len(diff), 4)
