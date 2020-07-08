"""Namaste tests."""
import fs
import fs.tempfs
import os.path
import tempfile
import unittest
from ocfl.namaste import content_to_tvalue, find_namastes, get_namaste, Namaste, NamasteException


class TestAll(unittest.TestCase):
    """TestAll class to run tests."""

    def test01_content_to_tvalue(self):
        """Test content_to_tvalue function."""
        self.assertEqual(content_to_tvalue(''), '')
        self.assertEqual(content_to_tvalue('something'), 'something')
        self.assertEqual(content_to_tvalue('a_b-c.d.EEE123'), 'a_b-c.d.EEE123')
        self.assertEqual(content_to_tvalue('  \t hello   \n'), 'hello')
        self.assertEqual(content_to_tvalue('x' * 100), 'x' * 40)
        self.assertEqual(content_to_tvalue('0!@#$%^&*()\\/1'), '0____________1')
        self.assertEqual(content_to_tvalue('ocfl_object_1.0'), 'ocfl_object_1.0')

    def test02_find_namastes(self):
        """Test find_namastes."""
        namastes = find_namastes(0, 'tests/testdata/namaste')
        self.assertEqual(set([x.tvalue for x in namastes]), set(['frog', 'bison', 'snake']))
        self.assertRaises(NamasteException, find_namastes, 0, 'tests/testdata/namaste', max=2)

    def test03_get_namaste(self):
        """Test get_namaste."""
        n = get_namaste(1, 'tests/testdata/namaste')
        self.assertEqual(n.tvalue, 'red')
        # More than one
        self.assertRaises(NamasteException, get_namaste, 0, 'tests/testdata/namaste')
        # None
        self.assertRaises(NamasteException, get_namaste, 4, 'tests/testdata/namaste')

    def test11_init(self):
        """Test initialization."""
        n = Namaste()
        self.assertEqual(n.d, 0)
        self.assertEqual(n._tr_func, content_to_tvalue)
        n = Namaste(0, 'myspec')
        self.assertEqual(n.d, 0)
        self.assertEqual(n.content, 'myspec')
        n = Namaste(d=0, content='whatevs', tvalue='myspec_1', tr_func=lambda x: x[:3])
        self.assertEqual(n.content, 'whatevs')

    def test12_filename(self):
        """Test filename property."""
        n = Namaste()
        self.assertEqual(n.filename, '0=')
        n = Namaste(2, 'wibble')
        self.assertEqual(n.filename, '2=wibble')

    def test13_tvalue(self):
        """Test tvalue property."""
        # Explicitly set
        n = Namaste(tvalue='xyz')
        self.assertEqual(n.tvalue, 'xyz')
        # Derived from content
        n = Namaste(content='x y z\n')
        self.assertEqual(n.tvalue, 'x_y_z')

    def test14_write(self):
        """Test write method."""
        tempdir = tempfile.mkdtemp(prefix='test_namaste')
        # Plain OS method
        n = Namaste(0, 'balloon')
        n.write(tempdir)
        filepath = os.path.join(tempdir, '0=balloon')
        self.assertTrue(os.path.isfile(filepath))
        with open(filepath, 'r') as fh:
            self.assertEqual(fh.read(), 'balloon\n')
        # With fs filesystem
        tmpfs = fs.tempfs.TempFS()
        n = Namaste(1, 'jelly')
        n.write(obj_fs=tmpfs)
        self.assertTrue(tmpfs.isfile('1=jelly'))
        self.assertEqual(tmpfs.readtext('1=jelly'), 'jelly\n')

    def test15_check_content(self):
        """Test check_content method."""
        Namaste(0, 'frog').check_content('tests/testdata/namaste')
        self.assertRaises(NamasteException, Namaste().check_content, 'tests/testdata/namaste')
        self.assertRaises(NamasteException, Namaste(0, 'a').check_content, 'tests/testdata/namaste/does_not_exist')
        self.assertRaises(NamasteException, Namaste(0, 'bison').check_content, 'tests/testdata/namaste')

    def test16_content_ok(self):
        """Test content_ok method."""
        self.assertTrue(Namaste(0, 'frog').content_ok('tests/testdata/namaste'))
        self.assertFalse(Namaste().content_ok('tests/testdata/namaste'))
        self.assertFalse(Namaste(0, 'bison').content_ok('tests/testdata/namaste'))
