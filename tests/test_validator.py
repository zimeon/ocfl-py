"""Test validation."""
import os
import os.path
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
                           'bad13_file_in_extensions_dir': ['E918'],
                           'bad14_different_root_and_latest_inventories': ['E099'],
                           'bad15_wrong_version_block_values': ['E302', 'E401', 'E403', 'E404', 'E912'],
                           'bad16_digest_repeated': ['E922', 'E923']}.items():
            v = OCFLValidator()
            filepath = 'fixtures/1.0/bad-objects/' + bad
            if not os.path.isdir(filepath):
                filepath = 'extra_fixtures/bad-objects/' + bad
            self.assertFalse(v.validate(filepath))
            for code in codes:
                self.assertIn(code, v.log.codes, msg="for object at " + filepath)

    def test02_warn(self):
        """Check warm objects pass but give expected warnings."""
        for warn, codes in {'warn01_no_message_or_user': ['W201', 'W202'],
                            'warn02_zero_padded_versions': ['W203'],
                            'warn03_zero_padded_versions': ['W203', 'W206', 'W207', 'W208', 'W209'],
                            'warn04_extra_dir_in_version_dir': ['W204'],
                            'warn05_uses_sha256': ['W206'],
                            'warn06_id_not_uri': ['W207'],
                            'warn07_created_no_timezone': ['W208'],
                            'warn08_created_not_to_seconds': ['W209'],
                            'warn09_user_no_address': ['W210'],
                            'warn10_versions_diff_digests': ['W206'],
                            'warn11_version_inv_diff_metadata': ['W212']}.items():
            v = OCFLValidator()
            filepath = 'fixtures/1.0/warn-objects/' + warn
            if not os.path.isdir(filepath):
                filepath = 'extra_fixtures/warn-objects/' + warn
            self.assertTrue(v.validate(filepath), msg="for object at " + filepath)
            self.assertEqual(set(codes), set(v.log.codes), msg="for object at " + filepath)

    def test03_good(self):
        """Check good objects pass."""
        dirs = next(os.walk('fixtures/1.0/good-objects'))[1]
        for dirname in dirs:
            dirpath = os.path.join('fixtures/1.0/good-objects', dirname)
            v = OCFLValidator()
            self.assertEqual((True, dirpath),  # add dirpath for better reporting
                             (v.validate(dirpath), dirpath))
