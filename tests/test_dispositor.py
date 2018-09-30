"""Digest tests."""
import unittest
from ocfl.dispositor import Dispositor


class TestAll(unittest.TestCase):
    """TestAll class to run tests."""

    def test_everything(self): 
        d = Dispositor()
        self.assertEqual(type(d), Dispositor)
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
