"""Test validation."""
import os
import unittest
from ocfl.validator import OCFLValidator


class TestAll(unittest.TestCase):
    """TestAll class to run tests."""

    def test01_bad(self):
        """Check bad objects fail."""
        for bad, codes in {'does_not_even_exist': ['E987'],
                           'bad01_no_decl': ['E001'],
                           'bad02_no_id': ['E100'],
                           'bad03_no_inv': ['E004'],
                           'bad04_no_sidecar': ['E005'],
                           'bad05_missing_file': ['E302'],
                           'bad06_extra_file': ['E303'],
                           'bad07_file_in_manifest_not_used': ['E302'],
                           'bad08_content_not_in_content_dir': ['E913'],
                           'bad09_wrong_head_doesnt_exist': ['E914'],
                           'bad10_wrong_head_format': ['E914'],
                           'bad11_extra_file_in_root': ['E915'],
                           'bad12_extra_dir_in_root': ['E916'],
                           'bad13_file_in_extensions_dir': ['E918']}.items():
            v = OCFLValidator()
            filepath = 'fixtures/1.0/bad-objects/' + bad
            self.assertFalse(v.validate(filepath))
            for code in codes:
                self.assertIn(code, v.codes, msg="for object at " + filepath)

    def test02_good(self):
        """Check good objects pass."""
        dirs = next(os.walk('fixtures/1.0/objects'))[1]
        for dirname in dirs:
            dirpath = os.path.join('fixtures/1.0/objects', dirname)
            v = OCFLValidator()
            self.assertEqual((True, dirpath),  # add dirpath for better reporting
                             (v.validate(dirpath), dirpath))
