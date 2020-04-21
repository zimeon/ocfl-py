"""Bagger tests."""
import unittest
import bagit
from ocfl.bagger import BaggerError, bag_as_source, bag_extracted_version
from ocfl.version import VersionMetadata

class TestAll(unittest.TestCase):
    """TestAll class to run tests."""

    def test_bag_as_source(self):
        """Test bag_as_source method."""
        metadata = VersionMetadata()
        self.assertRaises(bagit.BagError, bag_as_source, 'tests/testdata/files/hello_out_there.txt', metadata)
        self.assertRaises(BaggerError, bag_as_source, 'tests/testdata/bags/invalid_bag', metadata)
        # Check metadata update
        metadata = VersionMetadata()
        bag_as_source('tests/testdata/bags/uaa_v1', metadata)
        self.assertEqual(metadata.created, '2020-01-01T00:00:00Z')
        self.assertEqual(metadata.address, 'mailto:all_seeing_spheres@miskatonic.edu')
        self.assertEqual(metadata.name, 'Yog-Sothoth')
        self.assertEqual(metadata.message, 'First version')
        self.assertEqual(metadata.id, 'info:bb123cd4567')
        # Check metedata still None when not in bag
        metadata = VersionMetadata()
        bag_as_source('tests/testdata/bags/bag_no_metadata', metadata)
        self.assertEqual(metadata.created, None)
        self.assertEqual(metadata.address, None)
        self.assertEqual(metadata.name, None)
        self.assertEqual(metadata.message, None)
        self.assertEqual(metadata.id, None)

    def test_bag_extracted_version(self):
        """Test bag_extracted_version method."""
