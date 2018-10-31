"""Test validation."""
import os
import unittest
from ocfl.validator import OCFLValidator


class TestAll(unittest.TestCase):
    """TestAll class to run tests."""

    def test01_bad(self):
        """Check bad objects fail."""
        v = OCFLValidator()
        self.assertFalse(v.validate('fixtures/bad-objects/does_not_even_exist'))
        self.assertIn('E000', v.codes)
        v = OCFLValidator()
        self.assertFalse(v.validate('fixtures/bad-objects/bad00_empty'))
        self.assertIn('E001', v.codes)
        v = OCFLValidator()
        self.assertFalse(v.validate('fixtures/bad-objects/bad01_no_decl'))
        self.assertIn('E001', v.codes)
        v = OCFLValidator()
        self.assertFalse(v.validate('fixtures/bad-objects/bad02_no_id'))
        self.assertIn('E100', v.codes)
        v = OCFLValidator()
        self.assertFalse(v.validate('fixtures/bad-objects/bad03_no_inv'))
        self.assertIn('E005', v.codes)
        v = OCFLValidator()
        self.assertFalse(v.validate('fixtures/bad-objects/bad04_no_sidecar'))
        self.assertIn('E005', v.codes)

    def test02_good(self):
        """Check good objects pass."""
        dirs = next(os.walk('fixtures/objects'))[1]
        for dirname in dirs:
            dirpath = os.path.join('fixtures/objects', dirname)
            v = OCFLValidator()
            self.assertEqual((True, dirpath),  # add dirpath for better reporting
                             (v.validate(dirpath), dirpath))
