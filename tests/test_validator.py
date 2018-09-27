"""Test validation."""
import os
import unittest
from ocfl.validator import OCFLValidator


class TestAll(unittest.TestCase):
    """TestAll class to run tests."""

    def test01_bad(self):
        """Check bad objects fail."""
        v = OCFLValidator()
        self.assertFalse(v.validate('fixtures/bad-objects/bad1'))
        self.assertIn('E001', v.codes)
        v = OCFLValidator()
        self.assertFalse(v.validate('fixtures/bad-objects/bad2'))
        self.assertIn('E003', v.codes)
        v = OCFLValidator()
        self.assertFalse(v.validate('fixtures/bad-objects/bad3'))
        self.assertIn('E004', v.codes)
        v = OCFLValidator()
        self.assertFalse(v.validate('fixtures/bad-objects/bad4'))
        self.assertIn('E005', v.codes)

    def test02_good(self):
        """Check good objects pass."""
        dirs = next(os.walk('fixtures/objects'))[1]
        for dirname in dirs:
            dirpath = os.path.join('fixtures/objects', dirname)
            v = OCFLValidator()
            self.assertEqual((True, dirpath),  # add dirpath for better reporting
                             (v.validate(dirpath), dirpath))
