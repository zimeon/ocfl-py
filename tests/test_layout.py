"""Digest tests."""
import unittest
from ocfl.layout import Layout


class TestAll(unittest.TestCase):
    """TestAll class to run tests."""

    def test_almost_everything(self):
        """Test almost everything, just a little."""
        d = Layout()
        self.assertEqual(type(d), Layout)
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
