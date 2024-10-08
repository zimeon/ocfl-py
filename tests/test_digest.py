"""Digest tests."""
import unittest
import sys

import fs

from ocfl.digest import file_digest, string_digest, digest_regex, normalized_digest


class TestAll(unittest.TestCase):
    """TestAll class to run tests."""

    def test_file_digest__empty(self):
        """Test file_digest method with empty file."""
        self.assertEqual(file_digest(filename='tests/testdata/files/empty', digest_type='md5'),
                         'd41d8cd98f00b204e9800998ecf8427e')
        self.assertEqual(file_digest('tests/testdata/files/empty', 'sha1'),
                         'da39a3ee5e6b4b0d3255bfef95601890afd80709')
        self.assertEqual(file_digest('tests/testdata/files/empty', 'sha256'),
                         'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855')
        self.assertEqual(file_digest('tests/testdata/files/empty', 'sha512'),
                         'cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3e')
        self.assertEqual(file_digest('tests/testdata/files/empty'),
                         'cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3e')
        if sys.version_info > (3, 4):  # Old hashlib doesn't have blake2b
            self.assertEqual(file_digest('tests/testdata/files/empty', 'blake2b-512'),
                             '786a02f742015903c6c6fd852552d272912f4740e15847618a86e217f71f5419d25e1031afee585313896444934eb04b903a685b1448b755d56f701afe9be2ce')
            self.assertEqual(file_digest('tests/testdata/files/empty', 'blake2b-384'),
                             'b32811423377f52d7862286ee1a72ee540524380fda1724a6f25d7978c6fd3244a6caf0498812673c5e05ef583825100')
            self.assertEqual(file_digest('tests/testdata/files/empty', 'blake2b-256'),
                             '0e5751c026e543b2e8ab2eb06099daa1d1e5df47778f7787faab45cdf12fe3a8')
            self.assertEqual(file_digest('tests/testdata/files/empty', 'blake2b-160'),
                             '3345524abf6bbe1809449224b5972c41790b6cf2')
        self.assertEqual(file_digest('tests/testdata/files/empty', 'sha512-spec-ex'),
                         'cf83e1357eefb8b...a3e')
        self.assertEqual(file_digest('tests/testdata/files/empty', 'sha256-spec-ex'),
                         'e3b0c4...855')
        self.assertRaises(Exception, file_digest, 'tests/testdata/files/empty', 'bad-digest-type')

    def test_file_digest__long(self):
        """Test file_digest method with content."""
        self.assertEqual(file_digest('tests/testdata/files/hello_out_there.txt', 'md5'),
                         '9c7ec1389a61f1e15185bd976672bc63')

    def test_file_digest__pyfs(self):
        """Test file_digest method with content."""
        td_fs = fs.open_fs('tests/testdata')
        self.assertEqual(file_digest('files/hello_out_there.txt', 'md5', pyfs=td_fs),
                         '9c7ec1389a61f1e15185bd976672bc63')

    def test_string_digest(self):
        """Test string_digest method."""
        self.assertEqual(string_digest(txt='Sunny San Rafael\n', digest_type='md5'),
                         '0fa187d02e87902418af02e9a91c7603')
        self.assertEqual(string_digest('Sunny San Rafael\n', 'sha1'),
                         '14ca9011850fe349fb29e056a1fcfe018e035b44')
        self.assertEqual(string_digest('Sunny San Rafael\n', 'sha256'),
                         '50e8300695614f1298ceeac4a6a456ef875c4fac12dfd873736d8247dd4354b4')
        self.assertEqual(string_digest('Sunny San Rafael\n', 'sha512'),
                         '660473b7045af0ede6955236567893aef0dc5907252cc1c2d93b2a419545ea2ca599847995af50162f5f66f1b5231552b64b0a976b3b7d9433153539605093db')
        self.assertEqual(string_digest('Sunny San Rafael\n'),
                         '660473b7045af0ede6955236567893aef0dc5907252cc1c2d93b2a419545ea2ca599847995af50162f5f66f1b5231552b64b0a976b3b7d9433153539605093db')
        self.assertRaises(ValueError, string_digest, 'Any string', 'unknown_digest')

    def test_digest_regex(self):
        """Test digest regex."""
        self.assertEqual(digest_regex('md5'), r'''^[0-9a-fA-F]{32}$''')
        self.assertRaises(ValueError, digest_regex, 'unknown_digest')

    def test_normalized_digest(self):
        """Test normalized_digest."""
        self.assertEqual(normalized_digest('DA39a3ee5e6b4b0d3255BFEf95601890afd80709'), 'da39a3ee5e6b4b0d3255bfef95601890afd80709')
        self.assertEqual(normalized_digest('DA39a3ee5e6b4b0d3255BFEf95601890afd80709', 'sha1'), 'da39a3ee5e6b4b0d3255bfef95601890afd80709')
        # The following not changed
        self.assertEqual(normalized_digest('E3b0c4...855', 'sha256-spec-ex'), 'E3b0c4...855')
