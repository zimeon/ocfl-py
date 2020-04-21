"""Bagger tests."""
import unittest
import bagit
import os.path
import tempfile
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
        # Write bag with no metadata
        tempdir = tempfile.mkdtemp(prefix='test_bag1')
        with open(os.path.join(tempdir, 'my_file'), 'w') as fh:
            fh.write("Something\n")
        metadata = VersionMetadata()
        bag_extracted_version(tempdir, metadata)
        with open(os.path.join(tempdir, 'bag-info.txt'), 'r') as fh:
            info = fh.read()
        self.assertNotIn('Contact-Email', info)
        self.assertNotIn('Contact-Name', info)
        self.assertNotIn('External-Description', info)
        self.assertNotIn('External-Identifier', info)
        self.assertIn('Payload-Oxum', info)
        # Write bag with all metadata
        tempdir = tempfile.mkdtemp(prefix='test_bag2')
        with open(os.path.join(tempdir, 'my_file2'), 'w') as fh:
            fh.write("Something else\n")
        metadata = VersionMetadata()
        metadata.message = "hello"
        metadata.name = "A Person"
        metadata.address = "mailto:a.person@example.org"
        metadata.id = 'info:a-bag-2'
        bag_extracted_version(tempdir, metadata)
        with open(os.path.join(tempdir, 'bag-info.txt'), 'r') as fh:
            info = fh.read()
        self.assertIn('Contact-Email: a.person@example.org', info)
        self.assertIn('Contact-Name: A Person', info)
        self.assertIn('External-Description: hello', info)
        self.assertIn('External-Identifier: info:a-bag-2', info)
        self.assertIn('Payload-Oxum', info)
