"""Digest tests."""
import unittest
from ocfl.object import Object, remove_first_directory


class TestAll(unittest.TestCase):
    """TestAll class to run tests."""

    def test01_init(self):
        """Test Object init."""
        oo = Object()
        self.assertEqual(oo.identifier, None)
        self.assertEqual(oo.digest_algorithm, 'sha512')
        self.assertEqual(oo.skips, set())
        self.assertEqual(oo.ocfl_version, 'draft')
        self.assertEqual(oo.fixity, None)
        oo = Object(identifier='a:b', digest_algorithm='sha1', skips=['1', '2'],
                    ocfl_version='0.9.9', fixity=['md5', 'crc16'])
        self.assertEqual(oo.identifier, 'a:b')
        self.assertEqual(oo.digest_algorithm, 'sha1')
        self.assertEqual(oo.skips, set(('1', '2')))
        self.assertEqual(oo.ocfl_version, '0.9.9')
        self.assertEqual(oo.fixity, ['md5', 'crc16'])

    def test02_parse_version_directory(self):
        """Test parse_version_directory."""
        oo = Object()
        self.assertEqual(oo.parse_version_directory('v1'), 1)
        self.assertEqual(oo.parse_version_directory('v00001'), 1)
        self.assertEqual(oo.parse_version_directory('v99999'), 99999)
        # Bad
        self.assertRaises(Exception, oo.parse_version_directory, None)
        self.assertRaises(Exception, oo.parse_version_directory, '')
        self.assertRaises(Exception, oo.parse_version_directory, '1')
        self.assertRaises(Exception, oo.parse_version_directory, 'v0')
        self.assertRaises(Exception, oo.parse_version_directory, 'v-1')
        self.assertRaises(Exception, oo.parse_version_directory, 'v0000')
        self.assertRaises(Exception, oo.parse_version_directory, 'vv')
        self.assertRaises(Exception, oo.parse_version_directory, 'v000001')

    def test90_remove_first_directory(self):
        """Test encode."""
        self.assertEqual(remove_first_directory(''), '')
        self.assertEqual(remove_first_directory('a'), '')
        self.assertEqual(remove_first_directory('a/b'), 'b')
        self.assertEqual(remove_first_directory('a/b/'), 'b')
        self.assertEqual(remove_first_directory('a/b/c'), 'b/c')
