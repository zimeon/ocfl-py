"""Digest tests."""
import unittest
from ocfl.layout import Dispositor


class TestAll(unittest.TestCase):
    """TestAll class to run tests."""

    def test01_almost_everything(self):
        """Test almost everything, just a little."""
        d = Dispositor()
        self.assertEqual(type(d), Dispositor)
        self.assertEqual(d.strip_root('a/b', 'a'), 'b')
        self.assertEqual(d.strip_root('a/b', ''), 'a/b')
        self.assertEqual(d.strip_root('a/b/c', 'a/b/c'), '.')
        self.assertEqual(d.strip_root('a/b/c', 'a/b/'), 'c')
        self.assertEqual(d.strip_root('a/b/c/', 'a/b'), 'c')
        self.assertRaises(Exception, d.strip_root, 'a', 'b')
        self.assertRaises(Exception, d.strip_root, 'a', 'a/b')
        self.assertRaises(Exception, d.strip_root, '', 'a/b')
        self.assertTrue(d.is_valid(''))
        self.assertTrue(d.is_valid('anything'))
        self.assertEqual(d.encode(''), '')
        self.assertEqual(d.encode('something'), 'something')
        self.assertEqual(d.encode('http://a.b.c'), 'http%3A%2F%2Fa.b.c')
        self.assertEqual(d.decode(''), '')
        self.assertEqual(d.decode('something-else'), 'something-else')
        self.assertEqual(d.decode('http%3a%2f%2Fa.b.c'), 'http://a.b.c')
        self.assertRaises(Exception, d.identifier_to_path, 'id')
        self.assertRaises(Exception, d.path_to_identifier, 'a/b/c')

    def test02_path_to_identifier(self):
        """Test path_to_identifier."""
        d = Dispositor()
        d.relative_path_to_identifier = lambda x: x  # so we get result from path_to_identifier
        self.assertEqual(d.path_to_identifier('a/b/c/', 'a/b'), 'c')
