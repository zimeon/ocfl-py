"""Inventory tests."""
import unittest

from ocfl.inventory import InventoryException, Inventory


class TestAll(unittest.TestCase):
    """TestAll class to run tests."""

    def test_init(self):
        """Test initialization."""
        self.assertRaises(InventoryException, Inventory, data=[])

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
        # print("###json1###\n" + json1)
        json2 = Inventory(filepath="fixtures/1.1/good-objects/minimal_one_version_one_file/inventory.json").as_json()
        # print("###json2###\n" + json2)
        self.assertEqual(json1, json2)
