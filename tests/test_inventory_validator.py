"""Identity dispositor tests."""
import os.path
import unittest
from ocfl.inventory_validator import InventoryValidator, is_valid_logical_path


class TLogger(object):
    """Simplified logger to replace ValidationLogger."""

    def __init__(self):
        """Initialize."""
        self.clear()

    def error(self, code, **args):
        """Add error code, discard args."""
        self.errors.append(code)

    def warn(self, code, **args):
        """Add warn code, discard args."""
        self.warns.append(code)

    def clear(self):
        """Clear records."""
        self.errors = []
        self.warns = []


class TestAll(unittest.TestCase):
    """TestAll class to run tests."""

    def test_init(self):
        """Test object creation."""
        iv = InventoryValidator()
        self.assertEqual(iv.where, '???')
        iv = InventoryValidator(log='LOGGER', where="HERE", lax_digests=True)
        self.assertEqual(iv.log, 'LOGGER')
        self.assertEqual(iv.where, 'HERE')
        self.assertTrue(iv.lax_digests)

    def test_validate(self):
        """Test validate method."""
        log = TLogger()
        iv = InventoryValidator(log=log)
        iv.validate({})
        self.assertIn('E100', log.errors)
        self.assertIn('E102', log.errors)
        self.assertIn('E104', log.errors)
        self.assertIn('E106', log.errors)
        self.assertIn('E107', log.errors)
        self.assertIn('E108', log.errors)
        log.clear()
        iv.validate({"id": []})
        self.assertIn('E101', log.errors)
        log.clear()
        iv.validate({"id": "not_a_uri", "digestAlgorithm": "sha256"})
        self.assertIn('W207', log.warns)
        self.assertIn('W206', log.warns)
        log.clear()
        iv.validate({"id": "like:uri", "type": "wrong type", "digestAlgorithm": "my_digest"})
        self.assertIn('E103', log.errors)
        self.assertIn('E105', log.errors)
        iv = InventoryValidator(log=log, lax_digests=True)
        log.clear()
        iv.validate({"id": "like:uri", "type": "wrong type", "digestAlgorithm": "my_digest"})
        self.assertNotIn('E105', log.errors)
        self.assertEqual(iv.digest_algorithm, "my_digest")
        iv = InventoryValidator(log=log)
        log.clear()
        iv.validate({"id": "like:uri", "contentDirectory": "not/allowed"})
        self.assertIn('E051', log.errors)
        log.clear()
        iv.validate({"id": "like:uri", "contentDirectory": ".."})
        self.assertIn('E051', log.errors)

    def test_validate_manifest(self):
        """Test validate_manifest method."""
        log = TLogger()
        iv = InventoryValidator(log=log)
        self.assertEqual(iv.validate_manifest("not a manifest"), {})
        self.assertIn('E307', log.errors)
        log.clear()
        self.assertEqual(iv.validate_manifest({"xxx": []}), {})
        self.assertIn('E304', log.errors)
        self.assertEqual(iv.validate_manifest({"067eca3f5b024afa00aeac03a3c42dc0042bf43cba56104037abea8b365c0cf672f0e0c14c91b82bbce6b1464e231ac285d630a82cd4d4a7b194bea04d4b2eb7": "not an array"}), {})
        self.assertIn('E308', log.errors)

    def test_validate_version_sequence(self):
        """Test validate_version_sequence method."""
        log = TLogger()
        iv = InventoryValidator(log=log)
        self.assertEqual(iv.validate_version_sequence("not an object"), [])
        self.assertIn('E310', log.errors)
        log.clear()
        self.assertEqual(iv.validate_version_sequence({"v2": {}}), [])
        self.assertIn('E311', log.errors)
        log.clear()
        self.assertEqual(iv.validate_version_sequence({"v02": {}}), [])
        self.assertIn('E311', log.errors)
        log.clear()
        self.assertEqual(iv.validate_version_sequence({"v1": {}, 'v2': {}, 'v3': {}}), ['v1', 'v2', 'v3'])
        log.clear()
        self.assertEqual(iv.validate_version_sequence({"v0001": {}, 'v0002': {}}), ['v0001', 'v0002'])
        self.assertIn('W203', log.warns)
        self.assertEqual(len(log.errors), 0)
        log.clear()
        self.assertEqual(iv.validate_version_sequence({"v1": {}, 'v2': {}, 'v4': {}}), ['v1', 'v2'])
        self.assertIn('E312', log.errors)
        log.clear()
        self.assertEqual(iv.validate_version_sequence({"v01": {}, 'v02': {}, 'v03': {}, "v04": {}, 'v05': {}, 'v06': {}, "v07": {}, 'v08': {}, 'v09': {}}), ['v01', 'v02', 'v03', 'v04', 'v05', 'v06', 'v07', 'v08', 'v09'])
        self.assertEqual(len(log.errors), 0)
        log.clear()
        self.assertEqual(iv.validate_version_sequence({"v01": {}, 'v02': {}, 'v03': {}, "v04": {}, 'v05': {}, 'v06': {}, "v07": {}, 'v08': {}, 'v09': {}, 'v10': {}}), ['v01', 'v02', 'v03', 'v04', 'v05', 'v06', 'v07', 'v08', 'v09'])
        self.assertIn('E312', log.errors)

    def test_validate_versions(self):
        """Test validate_versions method."""
        log = TLogger()
        iv = InventoryValidator(log=log)
        self.assertEqual(iv.validate_versions({}, []), [])
        self.assertEqual(len(log.errors), 0)
        log.clear()
        self.assertEqual(iv.validate_versions({}, []), [])
        self.assertEqual(len(log.errors), 0)
        log.clear()
        # First, no useful data
        self.assertEqual(iv.validate_versions({'v1': {}}, ['v1']), [])
        self.assertIn('E401', log.errors)
        self.assertIn('E410', log.errors)
        self.assertIn('W201', log.warns)
        self.assertIn('W202', log.warns)
        log.clear()
        # Second, good data
        versions = {'v1': {"created": "2020-03-30T21:24:00Z",
                           "message": "A useful message",
                           "state": {},
                           "user": {"name": "A Person", "address": "info:uri1"}}}
        self.assertEqual(iv.validate_versions(versions, ['v1']), [])
        self.assertEqual(log.errors, [])
        log.clear()
        versions['v1']['created'] = {}  # not a string
        self.assertEqual(iv.validate_versions(versions, ['v1']), [])
        self.assertIn('E401', log.errors)
        log.clear()
        versions['v1']['created'] = "not a datetime"
        self.assertEqual(iv.validate_versions(versions, ['v1']), [])
        self.assertIn('E402', log.errors)
        log.clear()
        versions['v1']['created'] = "2020-03-30T21:24:00"  # no timezone
        self.assertEqual(iv.validate_versions(versions, ['v1']), [])
        self.assertIn('W208', log.warns)
        log.clear()
        versions['v1']['created'] = "2020-03-30T21:24Z"  # no seconds
        self.assertEqual(iv.validate_versions(versions, ['v1']), [])
        self.assertIn('W209', log.warns)
        log.clear()
        versions['v1']['created'] = "2020-03-30T21:24:00Z"
        versions['v1']['message'] = {}  # not a string
        self.assertEqual(iv.validate_versions(versions, ['v1']), [])
        self.assertIn('E403', log.errors)
        log.clear()
        versions['v1']['message'] = "A message"
        versions['v1']['user'] = "A string"  # not a dict
        self.assertEqual(iv.validate_versions(versions, ['v1']), [])
        self.assertIn('E404', log.errors)
        log.clear()
        versions['v1']['user'] = {"name": {}, "address": {}}  # not strings
        self.assertEqual(iv.validate_versions(versions, ['v1']), [])
        self.assertIn('E405', log.errors)
        self.assertIn('E406', log.errors)
        log.clear()
        versions['v1']['user'] = {"name": "A Person"}  # no address
        self.assertEqual(iv.validate_versions(versions, ['v1']), [])
        self.assertIn('W210', log.warns)

    def test_validate_state_block(self):
        """Test validate_state_block."""
        log = TLogger()
        iv = InventoryValidator(log=log)
        iv.digest_algorithm = 'sha512'
        self.assertEqual(iv.validate_state_block({}, "v1"), [])
        self.assertEqual(len(log.errors), 0)
        log.clear()
        self.assertEqual(iv.validate_state_block("invalid", "v1"), [])
        self.assertIn('E912', log.errors)
        log.clear()
        self.assertEqual(iv.validate_state_block({"not a digest": []}, "v1"), [])
        self.assertIn('E305', log.errors)
        log.clear()
        d = "4a89417821564b1e1956130569c390dd6122b51296ec620cadd0555ff5aae21c2a17383a194290fc95c73c63261bd8cb77ac275c85e6300cd711fa132fe8706e"
        self.assertEqual(iv.validate_state_block({d: "not a list"}, "v1"), [])
        self.assertIn('E919', log.errors)
        log.clear()
        self.assertEqual(iv.validate_state_block({d: ["good path", '/']}, "v1"), [d])
        self.assertIn('E920', log.errors)

    def test_check_digests_present_and_used(self):
        """Test check_digests_present_and_used."""
        log = TLogger()
        iv = InventoryValidator(log=log)
        manifest = {'file_aaa1': 'aaa', 'file_aaa2': 'aaa', 'file_bbb': 'bbb'}
        iv.check_digests_present_and_used(manifest, ['aaa', 'bbb'])
        self.assertEqual(len(log.errors), 0)
        iv.check_digests_present_and_used(manifest, ['aaa'])
        self.assertIn('E302', log.errors)
        log.clear()
        iv.check_digests_present_and_used(manifest, ['aaa', 'bbb', 'ccc'])
        self.assertIn('E913', log.errors)

    def test_is_valid_logical_path(self):
        """Test is_valid_logical_path function."""
        self.assertTrue(is_valid_logical_path("almost anything goes"))
        self.assertFalse(is_valid_logical_path("/but not this"))
        self.assertFalse(is_valid_logical_path("./or this"))
        self.assertFalse(is_valid_logical_path("or/../this"))
        self.assertFalse(is_valid_logical_path("or this/"))
