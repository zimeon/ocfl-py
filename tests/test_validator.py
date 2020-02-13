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
                self.assertIn(code, v.log.codes, msg="for object at " + filepath)
        #
        # Extra local fixtures that perhaps should be moved into the main set
        for bad, codes in {'bad15_wrong_version_block_values': ['E302', 'E401', 'E403', 'E404', 'E912']}.items():
            v = OCFLValidator()
            filepath = 'extra_fixtures/bad-objects/' + bad
            self.assertFalse(v.validate(filepath))
            for code in codes:
                self.assertIn(code, v.log.codes, msg="for object at " + filepath)

    def test02_warn(self):
        """Check warm objects pass but give expected warnings."""
        for warn, codes in {'warn01_no_message_or_user': ['W001', 'W002'],
                            'warn02_zero_padded_versions': ['W003'],
                            'warn03_zero_padded_versions': ['W003', 'W006', 'W007', 'W008', 'W009'],
                            'warn04_extra_dir_in_version_dir': ['W004'],
                            'warn05_uses_sha256': ['W006'],
                            'warn06_id_not_uri': ['W007'],
                            'warn07_created_no_timezone': ['W008'],
                            'warn08_created_not_to_seconds': ['W009'],
                            'warn09_user_no_address': ['W010']}.items():
            v = OCFLValidator()
            filepath = 'fixtures/1.0/warn-objects/' + warn
            self.assertTrue(v.validate(filepath), msg="for object at " + filepath)
            self.assertEqual(set(codes), set(v.log.codes), msg="for object at " + filepath)

    def test03_good(self):
        """Check good objects pass."""
        dirs = next(os.walk('fixtures/1.0/objects'))[1]
        for dirname in dirs:
            dirpath = os.path.join('fixtures/1.0/objects', dirname)
            v = OCFLValidator()
            self.assertEqual((True, dirpath),  # add dirpath for better reporting
                             (v.validate(dirpath), dirpath))
