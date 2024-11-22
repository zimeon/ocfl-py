"""Inventory and Version tests."""
import unittest

from ocfl.inventory import InventoryException, Inventory, Version
from ocfl.pyfs import pyfs_openfs


class TestInventory(unittest.TestCase):
    """TestInventory class to run test for the Invenory class."""

    def test_init(self):
        """Test initialization."""
        inv = Inventory()
        self.assertEqual(inv.data, {})
        inv = Inventory(data={"id": "uri:a"})
        self.assertEqual(inv.data, {"id": "uri:a"})
        inv = Inventory(filepath="fixtures/1.0/good-objects/spec-ex-full/inventory.json")
        self.assertEqual(inv.id, "ark:/12345/bcd987")
        self.assertEqual(inv.spec_version, "1.0")
        inv = Inventory(filepath="fixtures/1.0/good-objects/spec-ex-full/inventory.json")
        self.assertEqual(inv.id, "ark:/12345/bcd987")
        self.assertEqual(inv.spec_version, "1.0")
        inv = Inventory(filepath="fixtures/1.0/good-objects/spec-ex-full/inventory.json")
        self.assertEqual(inv.id, "ark:/12345/bcd987")
        self.assertEqual(inv.spec_version, "1.0")
        pyfs = pyfs_openfs("zip://extra_fixtures/1.0/good-objects/ten_level_deep_directories.zip")
        inv = Inventory(pyfs=pyfs, filepath="v1/inventory.json")
        self.assertEqual(inv.id, "http://example.org/ten_level_deep_directories")
        # Check deep copy of inventory
        inv1 = Inventory(filepath="fixtures/1.0/good-objects/spec-ex-full/inventory.json")
        inv2 = Inventory(inv1)
        inv1.id = "zap"
        self.assertEqual(inv1.id, "zap")
        self.assertEqual(inv2.id, "ark:/12345/bcd987")
        inv1.version("v3").message = "no message"
        self.assertEqual(inv1.version("v3").message, "no message")
        self.assertEqual(inv2.version("v3").message, "Reinstate image.tiff, delete empty.txt")
        # Init from data
        inv = Inventory({"b": "bad"})
        self.assertEqual(inv.data, {"b": "bad"})
        inv = Inventory(data={"a": "still bad"})
        self.assertEqual(inv.data, {"a": "still bad"})
        # Exception
        self.assertRaises(InventoryException, Inventory, data=[])

    def test_spec_version_getter(self):
        """Test spec_version getter."""
        inv = Inventory()
        self.assertEqual(inv.spec_version, None)
        inv = Inventory({"type": "https://ocfl.io/1.1/spec/#inventory"})
        self.assertEqual(inv.spec_version, "1.1")
        inv = Inventory({"type": "https://ocfl.io/BAD/spec/#inventory"})
        self.assertEqual(inv.spec_version, None)

    def test_fixity(self):
        """Test fixity get and set."""
        inv = Inventory()
        self.assertEqual(inv.fixity, {})
        inv.fixity = {'md5': {"184f84e28cbe75e050e9c25ea7f2e939":
                              ["v1/content/foo/bar.xml"]}}
        self.assertEqual(list(inv.fixity.keys()), ["md5"])

    def test_content(self):
        """Test content property."""
        inv = Inventory(filepath="fixtures/1.1/good-objects/spec-ex-full/inventory.json")
        self.assertEqual(set(inv.content.keys()),
                         set(["v2/content/foo/bar.xml",
                              "v1/content/image.tiff",
                              "v1/content/empty.txt",
                              "v1/content/foo/bar.xml"]))
        self.assertEqual(inv.content["v1/content/empty.txt"][0:16], "cf83e1357eefb8bd")

    def test_content_path_for_digest(self):
        """Test content_path_for_digest."""
        inv = Inventory()
        inv.manifest = {"qwerty": ["f1"],
                        "asdfgh": ["f2", "f3"]}
        self.assertEqual(inv.content_path_for_digest("qwerty"), "f1")
        self.assertEqual(inv.content_path_for_digest("asdfgh"), "f2")
        self.assertEqual(inv.content_path_for_digest("not-there"), None)

    def test_next_version_directory(self):
        """Test _next_version_directory method."""
        inv = Inventory()
        self.assertEqual(inv._next_version_directory(), "v1")  # pylint: disable=protected-access
        self.assertEqual(inv._next_version_directory(5), "v00001")  # pylint: disable=protected-access
        inv.data["versions"] = {"v1": {}}
        self.assertEqual(inv._next_version_directory(), "v2")  # pylint: disable=protected-access
        inv.data["versions"] = {"v0009": {}}
        self.assertEqual(inv._next_version_directory(), "v0010")  # pylint: disable=protected-access

    def test_add_version(self):
        """Test add_version method."""
        # Simple sequence
        inv = Inventory()
        v = inv.add_version(metadata={"message": "hello"})
        self.assertEqual(v.vdir, "v1")
        self.assertEqual(v.message, "hello")
        self.assertEqual(inv.head, "v1")
        v = inv.add_version(state={"digest": ["path"]})
        self.assertEqual(v.vdir, "v2")
        self.assertEqual(v.state["digest"], ["path"])
        self.assertEqual(inv.head, "v2")
        v = inv.add_version(zero_padded_width=5)  # has no effect
        self.assertEqual(v.vdir, "v3")
        self.assertEqual(v.message, None)
        self.assertEqual(inv.head, "v3")
        # Simple sequence with zero
        inv = Inventory()
        v = inv.add_version(metadata={"message": "hello again"},
                            zero_padded_width=4)
        self.assertEqual(v.vdir, "v0001")
        self.assertEqual(v.message, "hello again")
        self.assertEqual(inv.head, "v0001")
        v = inv.add_version(metadata={"message": "and again"})
        self.assertEqual(v.vdir, "v0002")
        self.assertEqual(v.message, "and again")
        self.assertEqual(inv.head, "v0002")

    def test_add_file(self):
        """Test add_file method."""
        inv = Inventory()
        inv.add_file(digest="abc123", content_path="file1")
        self.assertEqual(inv.manifest["abc123"], ["file1"])
        inv.add_file(digest="abc123", content_path="file2")
        self.assertEqual(inv.manifest["abc123"], ["file1", "file2"])
        inv.add_file(digest="def456", content_path="file3")
        self.assertEqual(inv.manifest["abc123"], ["file1", "file2"])
        self.assertEqual(inv.manifest["def456"], ["file3"])
        # Errors
        self.assertRaises(InventoryException, inv.add_file,
                          digest="anything", content_path="file1")

    def test_getter_properties_minimal_example(self):
        """Test read of fixture and extract properties."""
        inv = Inventory(filepath="fixtures/1.1/good-objects/minimal_one_version_one_file/inventory.json")
        self.assertEqual(inv.spec_version, "1.1")
        self.assertEqual(inv.digest_algorithm, "sha512")
        self.assertEqual(inv.id, "ark:123/abc")
        self.assertEqual(inv.head, "v1")
        self.assertEqual(inv.content_paths, ["v1/content/a_file.txt"])
        self.assertEqual(inv.digest_for_content_path("v1/content/a_file.txt"),
                         "43a43fe8a8a082d3b5343dfaf2fd0c8b8e370675b1f376e92e9994612c33ea255b11298269d72f797399ebb94edeefe53df243643676548f584fb8603ca53a0f")
        self.assertEqual(inv.version_directories, ["v1"])
        self.assertEqual(inv.version_numbers, [1])
        self.assertEqual(inv.version("v1").created,
                         "2019-01-01T02:03:04Z")
        self.assertEqual(inv.version("v1").message,
                         "An version with one file")
        self.assertEqual(inv.version("v1").user_name,
                         "A Person")
        self.assertEqual(inv.version("v1").user_address,
                         "mailto:a_person@example.org")
        self.assertEqual(inv.version("v1").logical_paths, ["a_file.txt"])
        self.assertEqual(inv.version("v1").digest_for_logical_path("a_file.txt"),
                         "43a43fe8a8a082d3b5343dfaf2fd0c8b8e370675b1f376e92e9994612c33ea255b11298269d72f797399ebb94edeefe53df243643676548f584fb8603ca53a0f")
        self.assertEqual(inv.version("v1").content_path_for_logical_path("a_file.txt"),
                         "v1/content/a_file.txt")
        self.assertEqual(inv.fixity, {})

    def test_creation_of_minimal_example(self):
        """Test creation of minimal example."""
        inv = Inventory()
        inv.spec_version = "1.1"
        inv.digest_algorithm = "sha512"
        inv.id = "ark:123/abc"
        v = inv.add_version()
        v.created = "2019-01-01T02:03:04Z"
        v.message = "An version with one file"
        v.user_name = "A Person"
        v.user_address = "mailto:a_person@example.org"
        v.add_file(digest="43a43fe8a8a082d3b5343dfaf2fd0c8b8e370675b1f376e92e9994612c33ea255b11298269d72f797399ebb94edeefe53df243643676548f584fb8603ca53a0f",
                   logical_path="a_file.txt")
        json1 = inv.as_json()
        json2 = Inventory(filepath="fixtures/1.1/good-objects/minimal_one_version_one_file/inventory.json").as_json()
        self.assertEqual(json1, json2)


class TestVersion(unittest.TestCase):
    """TestVersion class to run tests for the Version class."""

    def test_init(self):
        """Test initialization."""
        inv = Inventory()
        v = Version(inv=inv, vdir="v99")
        self.assertEqual(v.inv, inv)
        self.assertEqual(v.vdir, "v99")

    def test_number(self):
        """Test version number property."""
        v = Version(inv=Inventory(), vdir="v98")
        self.assertEqual(v.number, 98)
        v = Version(inv=Inventory(), vdir="v00023")
        self.assertEqual(v.number, 23)

    def test_digest_for_content_path(self):
        """Test digest_for_content_path mathod."""
        inv = Inventory()
        inv.manifest = {"abc123": ["v1/content/file1", "v2/content/file2"],
                        "def456": ["v2/content/file3"]}
        self.assertEqual(inv.digest_for_content_path("does_not_exist"), None)
        self.assertEqual(inv.digest_for_content_path("v2/content/file2"), "abc123")
        self.assertEqual(inv.digest_for_content_path("v2/content/file3"), "def456")

    def test_digest_for_logical_path(self):
        """Test digest_for_logical_path method."""
        v = Inventory().add_version(state={"digest1": ["file1", "file2"],
                                           "digest2": ["file3"]})
        self.assertEqual(v.digest_for_logical_path("file1"), "digest1")
        self.assertEqual(v.digest_for_logical_path("file2"), "digest1")
        self.assertEqual(v.digest_for_logical_path(path="file3"), "digest2")
        self.assertEqual(v.digest_for_logical_path("file4"), None)

    def test_content_path_for_logical_path(self):
        """Test content_path_for_logical_path method."""
        inv = Inventory()
        inv.manifest = {"abc123": ["v1/content/file1", "v2/content/file2"],
                        "def456": ["v2/content/file3"]}
        v1 = inv.add_version(state={"abc123": ["file1_added_v1"]})
        self.assertEqual(v1.content_path_for_logical_path("file1_added_v1"),
                         "v1/content/file1")
        self.assertEqual(v1.content_path_for_logical_path("not-there!"), None)
        v2 = inv.add_version(state={"abc123": ["file1_added_v1_moved", "file2_added_v2"],
                                    "def456": ["file3_added_v2"]})
        self.assertEqual(v2.content_path_for_logical_path("file1_added_v1"), None)
        self.assertEqual(v2.content_path_for_logical_path("file1_added_v1_moved"),
                         "v1/content/file1")
        self.assertEqual(v2.content_path_for_logical_path("file3_added_v2"),
                         "v2/content/file3")

    def test_add_file(self):
        """Test add_file method."""
        inv = Inventory()
        v1 = inv.add_version()
        self.assertEqual(v1.add_file(digest="digest1", logical_path="file1"),
                         "v1/content/file1")
        self.assertEqual(v1.add_file(digest="digest1", logical_path="file2_same_as_1"),
                         None)
        self.assertEqual(v1.add_file(digest="digest2", logical_path="file3", content_path="file4"),
                         "v1/content/file4")
        self.assertEqual(v1.add_file(digest="digest3", logical_path="file4"),
                         "v1/content/file4__2")
        self.assertEqual(v1.add_file(digest="digest4", logical_path="file4__2"),
                         "v1/content/file4__2__2")
        v2 = inv.add_version()
        self.assertEqual(v2.add_file(digest="digest1", logical_path="file1_deduped"),
                         None)
        self.assertEqual(v2.add_file(digest="digest1", logical_path="file1_duped", dedupe=False),
                         "v2/content/file1_duped")
        self.assertEqual(inv.manifest["digest1"], ["v1/content/file1", "v2/content/file1_duped"])
        # Error
        self.assertRaises(InventoryException, v2.add_file, digest="digest5", logical_path="file1_deduped")

    def test_find_logical_path(self):
        """Test find_local_path method."""
        inv = Inventory()
        inv.manifest = {"abc123": ["v1/content/file1", "v2/content/file2"],
                        "def456": ["v2/content/file3"]}
        inv.add_version(state={"abc123": ["file1_added_v1"]})  # v1
        inv.add_version(state={"abc123": ["file1_added_v1_moved", "file2_added_v2"],
                               "def456": ["file3_added_v2"]})  # v2
        self.assertEqual(inv.find_logical_path("not there"), (None, None))
        self.assertEqual(inv.find_logical_path("file1_added_v1_moved"), ("v2", "v1/content/file1"))
        self.assertEqual(inv.find_logical_path("file3_added_v2"), ("v2", "v2/content/file3"))

    def test_delete_logical_path(self):
        """Test delete_logical_path method."""
        inv = Inventory()
        inv.manifest = {"d1": ["v1/content/file1", "v2/content/file3"],
                        "d2": ["v1/content/file2"]}
        inv.add_version(state={"d1": ["file1"],
                               "d2": ["file2"]})  # v1
        inv.add_version(state={"d1": ["file1_moved", "file3"],
                               "d2": ["file2"]})  # v2
        self.assertRaises(InventoryException, inv.current_version.delete_logical_path, "file1")
        self.assertEqual(inv.current_version.delete_logical_path("file1_moved"), "d1")
        self.assertEqual(inv.manifest["d1"], ["v1/content/file1", "v2/content/file3"])
        self.assertEqual(inv.current_version.delete_logical_path("file3"), "d1")
        self.assertEqual(inv.manifest["d1"], ["v1/content/file1"])
        self.assertEqual(inv.current_version.delete_logical_path("file2"), "d2")
        self.assertEqual(inv.manifest["d2"], ["v1/content/file2"])
