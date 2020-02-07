"""Test validation."""
import os
import unittest
from ocfl.validator import OCFLValidator


class TestAll(unittest.TestCase):
    """TestAll class to run tests."""

    def test01_bad(self):
        """Check bad objects fail."""
        v = OCFLValidator()
        self.assertFalse(v.validate('fixtures/1.0/bad-objects/does_not_even_exist'))
        self.assertIn('E987', v.codes)
        v = OCFLValidator()
        self.assertFalse(v.validate('fixtures/1.0/bad-objects/bad00_empty'))
        self.assertIn('E001', v.codes)
        v = OCFLValidator()
        self.assertFalse(v.validate('fixtures/1.0/bad-objects/bad01_no_decl'))
        self.assertIn('E001', v.codes)
        v = OCFLValidator()
        self.assertFalse(v.validate('fixtures/1.0/bad-objects/bad02_no_id'))
        self.assertIn('E100', v.codes)
        v = OCFLValidator()
        self.assertFalse(v.validate('fixtures/1.0/bad-objects/bad03_no_inv'))
        self.assertIn('E004', v.codes)
        v = OCFLValidator()
        self.assertFalse(v.validate('fixtures/1.0/bad-objects/bad04_no_sidecar'))
        self.assertIn('E005', v.codes)
        v = OCFLValidator()
        self.assertFalse(v.validate('fixtures/1.0/bad-objects/bad05_missing_file'))
        self.assertIn('E302', v.codes)
        v = OCFLValidator()
        self.assertFalse(v.validate('fixtures/1.0/bad-objects/bad06_extra_file'))
        self.assertIn('E303', v.codes)
        v = OCFLValidator()
        self.assertFalse(v.validate('fixtures/1.0/bad-objects/bad07_file_in_manifest_not_used'))
        self.assertIn('E302', v.codes)
        v = OCFLValidator()
        self.assertFalse(v.validate('fixtures/1.0/bad-objects/bad08_content_not_in_content_dir'))
        self.assertIn('E913', v.codes)

    def test02_good(self):
        """Check good objects pass."""
        dirs = next(os.walk('fixtures/1.0/objects'))[1]
        for dirname in dirs:
            dirpath = os.path.join('fixtures/1.0/objects', dirname)
            v = OCFLValidator()
            self.assertEqual((True, dirpath),  # add dirpath for better reporting
                             (v.validate(dirpath), dirpath))
