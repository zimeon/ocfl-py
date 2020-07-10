"""Test validation."""
import os
import os.path
import shutil
from zipfile import ZipFile
import unittest
from ocfl.validator import Validator

# Setup to unpack a test case with an empty content directory
# that we can't store in git
for unpacked_directory in ['extra_fixtures/warn-objects/W003_empty_content_dir',
                           'extra_fixtures/bad-objects/E024_empty_dir_in_content']:
    zip_file = unpacked_directory + '.zip'
    if not os.path.isfile(zip_file):
        sys.exit(1)
    if os.path.isdir(unpacked_directory):
        shutil.rmtree(unpacked_directory)
    if os.path.isfile(zip_file):
        zf = ZipFile(zip_file, 'r')
        zf.extractall(os.path.dirname(unpacked_directory))
        zf.close()
    if not os.path.isdir(unpacked_directory):
        raise Exception("Oops, something went wrong with unzipping extra_fixtures/warn-objects/W003_empty_content_dir.zip")


class TestAll(unittest.TestCase):
    """TestAll class to run tests."""

    def test01_bad(self):
        """Check bad objects fail."""
        for bad, codes in {'does_not_even_exist': ['E003c'],
                           'E001_extra_dir_in_root': ['E001b'],
                           'E001_extra_file_in_root': ['E001a'],
                           'E003_E034_empty': ['E003a', 'E034'],
                           'E003_no_decl': ['E003a'],
                           'E008_E036_no_versions_no_head': ['E008', 'E036d'],
                           'E009_version_two_only': ['E009'],
                           'E015_content_not_in_content_dir': ['E042'],  # FIXME - What should test case and error be?
                           'E023_extra_file': ['E023b'],
                           'E023_missing_file': ['E023a'],
                           'E024_empty_dir_in_content': ['E024'],
                           'E033_inventory_bad_json': ['E033'],
                           'E034_no_inv': ['E034'],
                           'E036_no_id': ['E036a'],
                           'E040_wrong_head_doesnt_exist': ['E040'],
                           'E040_wrong_head_format': ['E040'],
                           'E041_no_manifest': ['E041a'],
                           'E042_bad_manifest_content_path': ['E042'],
                           'E046_missing_version_dir': ['E046'],
                           'E049_E050_E054_bad_version_block_values': ['E049d', 'E050b', 'E050c', 'E054a', 'E094'],
                           'E049_created_no_timezone': ['E049a'],
                           'E049_created_not_to_seconds': ['E049b'],
                           'E050_file_in_manifest_not_used': ['E050b'],
                           'E050_state_repeated_digest': ['E050f'],
                           'E058_no_sidecar': ['E058a'],
                           'E064_different_root_and_latest_inventories': ['E064'],
                           'E067_file_in_extensions_dir': ['E067'],
                           'E092_bad_manifest_digest': ['E092'],
                           'E094_message_not_a_string': ['E094'],
                           'E095_conflicting_logical_paths': ['E095'],
                           'E096_manifest_repeated_digest': ['E096'],
                           'E097_fixity_repeated_digest': ['E097'],
                           'E099_bad_content_path_elements': ['E099']}.items():
            v = Validator()
            filepath = 'fixtures/1.0/bad-objects/' + bad
            if not os.path.isdir(filepath):
                filepath = 'extra_fixtures/bad-objects/' + bad
            self.assertFalse(v.validate(filepath), msg=" for object at " + filepath)
            for code in codes:
                self.assertIn(code, v.log.codes, msg="for object at " + filepath)

    def test02_warn(self):
        """Check warm objects pass but give expected warnings."""
        for warn, codes in {'W001_zero_padded_versions': ['W001'],
                            'W001_W004_W005_zero_padded_versions': ['W001', 'W004', 'W005'],
                            'W002_extra_dir_in_version_dir': ['W002'],
                            'W003_empty_content_dir': ['W003'],
                            'W004_uses_sha256': ['W004'],
                            'W004_versions_diff_digests': ['W004'],
                            'W005_id_not_uri': ['W005'],
                            'W007_no_message_or_user': ['W007a', 'W007b'],
                            'W008_user_no_address': ['W008'],
                            'W009_user_address_not_uri': ['W009'],
                            'W010_no_version_inventory': ['W010'],
                            'W011_version_inv_diff_metadata': ['W011']}.items():
            v = Validator()
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
            v = Validator()
            self.assertEqual((True, dirpath),  # add dirpath for better reporting
                             (v.validate(dirpath), dirpath))
