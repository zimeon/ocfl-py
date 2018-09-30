"""Digest tests."""
import unittest
from ocfl.ntree import Ntree


class TestAll(unittest.TestCase):
    """TestAll class to run tests."""

    def test01_encode(self):
        """Test encode."""
        nt = Ntree()
        self.assertEqual(nt.encode(''), '')
        self.assertEqual(nt.encode('a'), 'a')
        self.assertEqual(nt.encode('a/b:?'), 'a=b+^3f')

    def test02_decode(self):
        """Test decode."""
        nt = Ntree()
        self.assertEqual(nt.decode(''), '')
        self.assertEqual(nt.decode('a'), 'a')
        self.assertEqual(nt.decode('a=b+^3f'), 'a/b:?')

    def test03_identifier_to_path(self):
        """Test path creation."""
        nt = Ntree(n=2, encapsulate=False)
        self.assertEqual(nt.identifier_to_path(''), '')
        self.assertEqual(nt.identifier_to_path('a'), 'a')
        self.assertEqual(nt.identifier_to_path('ab'), 'ab')
        self.assertEqual(nt.identifier_to_path('abc'), 'ab/c')
        self.assertEqual(nt.identifier_to_path('abcde'), 'ab/cd/e')
        nt = Ntree(n=3, encapsulate=False)
        self.assertEqual(nt.identifier_to_path('abcdefg'), 'abc/def/g')
        self.assertEqual(nt.identifier_to_path('abcdefgh'), 'abc/def/gh')
        self.assertEqual(nt.identifier_to_path('abcdefghi'), 'abc/def/ghi')
        nt = Ntree(n=2)
        self.assertEqual(nt.identifier_to_path(''), '')
        self.assertEqual(nt.identifier_to_path('a'), 'a/a')
        self.assertEqual(nt.identifier_to_path('ab'), 'ab/ab')
        self.assertEqual(nt.identifier_to_path('abc'), 'ab/c/abc')
        self.assertEqual(nt.identifier_to_path('abcde'), 'ab/cd/e/abcde')
        nt = Ntree(n=3)
        self.assertEqual(nt.identifier_to_path('abcdefg'), 'abc/def/g/abcdefg')
        self.assertEqual(nt.identifier_to_path('abcdefgh'), 'abc/def/gh/abcdefgh')
        self.assertEqual(nt.identifier_to_path('abcdefghi'), 'abc/def/ghi/abcdefghi')

    def test03_path_to_identifier(self):
        """Test path interpretation."""
        nt = Ntree(n=2, encapsulate=False)
        self.assertEqual(nt.path_to_identifier(''), '')
        self.assertEqual(nt.path_to_identifier('a'), 'a')
        self.assertEqual(nt.path_to_identifier('ab'), 'ab')
        self.assertEqual(nt.path_to_identifier('ab/c'), 'abc')
        self.assertEqual(nt.path_to_identifier('ab/cd/e'), 'abcde')
        nt = Ntree(n=3, encapsulate=False)
        self.assertEqual(nt.path_to_identifier('abc/def/g'), 'abcdefg')
        self.assertEqual(nt.path_to_identifier('abc/def/gh'), 'abcdefgh')
        self.assertEqual(nt.path_to_identifier('abc/def/ghi'), 'abcdefghi')
        nt = Ntree(n=2)
        self.assertEqual(nt.path_to_identifier(''), '')
        self.assertEqual(nt.path_to_identifier('a/a'), 'a')
        self.assertEqual(nt.path_to_identifier('ab/ab'), 'ab')
        self.assertEqual(nt.path_to_identifier('ab/c/abc'), 'abc')
        self.assertEqual(nt.path_to_identifier('ab/cd/e/abcde'), 'abcde')
        nt = Ntree(n=3)
        self.assertEqual(nt.path_to_identifier('abc/def/g/abcdefg'), 'abcdefg')
        self.assertEqual(nt.path_to_identifier('abc/def/gh/abcdefgh'), 'abcdefgh')
        self.assertEqual(nt.path_to_identifier('abc/def/ghi/abcdefghi'), 'abcdefghi')
        # Bad ones
        self.assertRaises(Exception, nt.path_to_identifier, 'abc/def/g/a-diff-g')

       