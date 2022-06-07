"""Test validator module."""
import os
import os.path
import unittest
from ocfl.validator import Validator


def extra_fixture_maybe_zip(filepath):
    """Filepath or URL for extra_fixture that may be a zip file."""
    if filepath.endswith('.zip'):
        zippath = filepath
    else:
        zippath = filepath + '.zip'
    if os.path.isfile(zippath):
        return 'zip://' + zippath
    return filepath


class TestAll(unittest.TestCase):
    """TestAll class to run tests."""

    def test01_bad_v1_0(self):
        """Check bad v1.0 objects fail."""
        for bad, codes in {'does_not_even_exist': ['E003e'],
                           'E001_extra_dir_in_root': ['E001b'],
                           'E001_extra_file_in_root': ['E001a'],
                           'E001_invalid_version_format': ['E009'],  # E009 OK, see https://github.com/OCFL/fixtures/pull/80
                           'E001_v2_file_in_root': ['E001a'],
                           'E003_E063_empty': ['E003a', 'E063'],
                           'E003_no_decl': ['E003a'],
                           'E008_E036_no_versions_no_head': ['E008', 'E036d'],
                           'E009_version_two_only': ['E009'],
                           'E010_missing_versions': ['E046a'],  # FIXME - Check code https://github.com/OCFL/spec/issues/540
                           'E010_skipped_versions': ['E010'],
                           'E011_E013_invalid_padded_head_version': ['E011', 'E040', 'E064'],  # E011 only OK, see https://github.com/OCFL/spec/issues/541
                           'E015_content_not_in_content_dir': ['E042a'],  # FIXME - What should test case and error be?
                           'E017_invalid_content_dir': ['E017'],
                           'E019_inconsistent_content_dir': ['E042a'],  # FIXME - What should error be?
                           'E023_extra_file': ['E023a'],
                           'E023_missing_file': ['E092b'],
                           'E023_old_manifest_missing_entries': ['E023b'],
                           'E024_empty_dir_in_content': ['E024'],
                           'E025_wrong_digest_algorithm': ['E025a'],
                           'E033_inventory_bad_json': ['E033'],
                           'E036_no_id': ['E036a'],
                           'E036_no_head': ['E036d'],
                           'E037_inconsistent_id': ['E037b'],
                           'E040_head_not_most_recent': ['E040'],
                           'E040_wrong_head_doesnt_exist': ['E040'],
                           'E040_wrong_head_format': ['E040'],
                           'E040_wrong_version_in_version_dir': ['E066a'],  # FIXME
                           'E041_no_manifest': ['E041a'],
                           'E041_manifest_not_object': ['E041c'],
                           'E042_bad_manifest_content_path': ['E042a'],
                           'E046_missing_version_dir': ['E046a'],
                           'E046_root_not_most_recent': ['E046b'],
                           'E049_E050_E054_bad_version_block_values': ['E049d', 'E050c', 'E054a', 'E094', 'E107'],
                           'E049_created_no_timezone': ['E049a'],
                           'E049_created_not_to_seconds': ['E049b'],
                           'E050_manifest_digest_wrong_case': ['E050f'],
                           'E050_state_digest_different_case': ['E050f'],
                           'E050_state_repeated_digest': ['E050f'],
                           'E053_E052_invalid_logical_paths': ['E052', 'E053'],
                           'E056_null_fixity': ['E056a'],
                           'E058_no_sidecar': ['E058a'],
                           'E060_E064_root_inventory_digest_mismatch': ['E060', 'E064'],
                           'E061_invalid_sidecar': ['E061'],
                           'E063_no_inv': ['E063'],
                           'E064_different_root_and_latest_inventories': ['E064'],
                           'E066_E092_old_manifest_digest_incorrect': ['E066d', 'E066e', 'E092a'],
                           'E066_algorithm_change_state_mismatch': ['E066b'],
                           'E066_changed_v1_logical_path': ['E066b'],
                           'E066_inconsistent_version_state': ['E066b'],
                           'E066_changed_content_for_logical_path': ['E066c'],
                           'E067_file_in_extensions_dir': ['E067'],
                           'E092_bad_manifest_digest': ['E092a'],
                           'E092_content_file_digest_mismatch': ['E092a'],
                           'E092_algorithm_change_incorrect_digest': ['E092a'],
                           'E092_E093_content_path_does_not_exist': ['E092b', 'E093b'],
                           'E093_fixity_digest_mismatch': ['E093a'],
                           'E093_fixity_digest_mismatch_in_v1': ['E093a'],
                           'E094_message_not_a_string': ['E094'],
                           'E095_conflicting_logical_paths': ['E095b'],
                           'E095_non_unique_logical_paths': ['E095a'],
                           'E096_manifest_repeated_digest': ['E096'],
                           'E096_manifest_duplicate_digests': ['E096'],
                           'E097_fixity_repeated_digest': ['E097'],
                           'E097_fixity_duplicate_digests': ['E097'],
                           'E099_bad_content_path_elements': ['E099'],
                           'E100_E099_fixity_invalid_content_paths': ['E057d'],  # E057 OK, different test approach
                           'E100_E099_manifest_invalid_content_paths': ['E099', 'E100'],
                           'E101_non_unique_content_paths': ['E101a']}.items():
            v = Validator()
            filepath = 'fixtures/1.0/bad-objects/' + bad
            if not os.path.isdir(filepath):
                filepath = extra_fixture_maybe_zip('extra_fixtures/1.0/bad-objects/' + bad)
            self.assertFalse(v.validate(filepath), msg=" for v1.0 object at " + filepath)
            for code in codes:
                self.assertIn(code, v.log.codes, msg="for v1.0 object at " + filepath)

    def test02_bad_v1_1(self):
        """Check bad v1.1 objects fail."""
        for bad, codes in {'does_not_even_exist': ['E003e'],
                           'E001_extra_dir_in_root': ['E001b'],
                           'E001_extra_file_in_root': ['E001a'],
                           'E001_invalid_version_format': ['E009'],  # E009 OK, see https://github.com/OCFL/fixtures/pull/80
                           'E001_v2_file_in_root': ['E001a'],
                           'E003_E063_empty': ['E003a', 'E063'],
                           'E003_no_decl': ['E003a'],
                           'E003_two_declarations': ['E003b'],
                           'E008_E036_no_versions_no_head': ['E008', 'E036d'],
                           'E010_missing_versions': ['E046a'],  # FIXME - Check code https://github.com/OCFL/spec/issues/540
                           'E010_skipped_versions': ['E010'],
                           'E011_E013_invalid_padded_head_version': ['E011', 'E040', 'E064'],  # E011 only OK, see https://github.com/OCFL/spec/issues/541
                           'E015_content_not_in_content_dir': ['E042a'],  # FIXME - What should test case and error be?
                           'E017_invalid_content_dir': ['E017'],
                           'E019_inconsistent_content_dir': ['E042a'],  # FIXME - What should error be?
                           'E023_extra_file': ['E023a'],
                           'E023_missing_file': ['E092b'],
                           'E023_old_manifest_missing_entries': ['E023b'],
                           'E025_wrong_digest_algorithm': ['E025a'],
                           'E036_no_id': ['E036a'],
                           'E036_no_head': ['E036d'],
                           'E037_inconsistent_id': ['E037b'],
                           'E040_head_not_most_recent': ['E040'],
                           'E040_wrong_head_doesnt_exist': ['E040'],
                           'E040_wrong_head_format': ['E040'],
                           'E040_wrong_version_in_version_dir': ['E066a'],  # FIXME
                           'E041_no_manifest': ['E041a'],
                           'E046_root_not_most_recent': ['E046b'],
                           'E049_E050_E054_bad_version_block_values': ['E049d', 'E050c', 'E054a', 'E094', 'E107'],
                           'E049_created_no_timezone': ['E049a'],
                           'E049_created_not_to_seconds': ['E049b'],
                           'E050_manifest_digest_wrong_case': ['E050f'],
                           'E050_state_digest_not_in_manifest': ['E050f'],
                           'E053_E052_invalid_logical_paths': ['E052', 'E053'],
                           'E058_no_sidecar': ['E058a'],
                           'E060_E064_root_inventory_digest_mismatch': ['E060', 'E064'],
                           'E061_invalid_sidecar': ['E061'],
                           'E063_no_inv': ['E063'],
                           'E064_different_root_and_latest_inventories': ['E064'],
                           'E066_E092_old_manifest_digest_incorrect': ['E066d', 'E066e', 'E092a'],
                           'E066_algorithm_change_state_mismatch': ['E066b'],
                           'E066_inconsistent_version_state': ['E066b'],
                           'E067_file_in_extensions_dir': ['E067'],
                           'E092_content_file_digest_mismatch': ['E092a'],
                           'E092_algorithm_change_incorrect_digest': ['E092a'],
                           'E092_E093_content_path_does_not_exist': ['E092b', 'E093b'],
                           'E093_fixity_digest_mismatch': ['E093a'],
                           'E095_conflicting_logical_paths': ['E095b'],
                           'E095_non_unique_logical_paths': ['E095a'],
                           'E096_manifest_duplicate_digests': ['E096'],
                           'E097_fixity_duplicate_digests': ['E097'],
                           'E100_E099_fixity_invalid_content_paths': ['E057d'],  # E057 OK, different test approach
                           'E100_E099_manifest_invalid_content_paths': ['E099', 'E100'],
                           'E101_non_unique_content_paths': ['E101a'],
                           'E103_older_spec_v2': ['E103'],
                           'E107_file_in_manifest_not_used': ['E107'],
                           'E111_null_fixity': ['E111']
                           }.items():
            v = Validator()
            filepath = 'fixtures/1.1/bad-objects/' + bad
            if not os.path.isdir(filepath):
                filepath = extra_fixture_maybe_zip('extra_fixtures/1.1/bad-objects/' + bad)
            self.assertFalse(v.validate(filepath), msg=" for v1.1 object at " + filepath)
            for code in codes:
                self.assertIn(code, v.log.codes, msg="for v1.1 object at " + filepath)

    def test03_warn_1_0(self):
        """Check warn v1.0 objects pass but give expected warnings."""
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
                            'W011_version_inv_diff_metadata': ['W011'],
                            'W013_unregistered_extension': ['W013']}.items():
            v = Validator()
            filepath = 'fixtures/1.0/warn-objects/' + warn
            if not os.path.isdir(filepath):
                filepath = extra_fixture_maybe_zip('extra_fixtures/1.0/warn-objects/' + warn)
            self.assertTrue(v.validate(filepath), msg="for v1.0 object at " + filepath)
            self.assertEqual(set(codes), set(v.log.codes), msg="for v1.0 object at " + filepath)

    def test04_warn_1_1(self):
        """Check warn v1.1 objects pass but give expected warnings."""
        for warn, codes in {'W001_zero_padded_versions': ['W001'],
                            'W001_W004_W005_zero_padded_versions': ['W001', 'W004', 'W005'],
                            'W002_extra_dir_in_version_dir': ['W002'],
                            'W004_uses_sha256': ['W004'],
                            'W004_versions_diff_digests': ['W004'],
                            'W005_id_not_uri': ['W005'],
                            'W007_no_message_or_user': ['W007a', 'W007b'],
                            'W008_user_no_address': ['W008'],
                            'W009_user_address_not_uri': ['W009'],
                            'W010_no_version_inventory': ['W010'],
                            'W011_version_inv_diff_metadata': ['W011'],
                            'W013_unregistered_extension': ['W013']}.items():
            v = Validator()
            filepath = 'fixtures/1.1/warn-objects/' + warn
            if not os.path.isdir(filepath):
                filepath = extra_fixture_maybe_zip('extra_fixtures/1.1/warn-objects/' + warn)
            self.assertTrue(v.validate(filepath), msg="for v1.1 object at " + filepath)
            self.assertEqual(set(codes), set(v.log.codes), msg="for v1.1 object at " + filepath)

    def test05_good(self):
        """Check good objects (v1.0, v1.1 and extra) pass."""
        for base_dir in ['fixtures/1.0/good-objects',
                         'fixtures/1.1/good-objects',
                         'extra_fixtures/1.0/good-objects',
                         'extra_fixtures/1.1/good-objects']:
            for name in os.listdir(base_dir):
                filepath = extra_fixture_maybe_zip(os.path.join(base_dir, name))
                v = Validator()
                self.assertTrue(v.validate(filepath), msg="for object at " + filepath)
