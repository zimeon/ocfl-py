"""Identity dispositor tests."""
import json
import unittest
from ocfl.inventory_validator import InventoryValidator


class TLogger():
    """Simplified logger to replace ValidationLogger."""

    def __init__(self):
        """Initialize."""
        self.clear()

    def error(self, code, **args):  # pylint: disable=unused-argument
        """Add error code, discard args."""
        self.errors.append(code)

    def warning(self, code, **args):  # pylint: disable=unused-argument
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
        self.assertIn('E036a', log.errors)
        self.assertIn('E036b', log.errors)
        self.assertIn('E036c', log.errors)
        self.assertIn('E036d', log.errors)
        self.assertIn('E041a', log.errors)
        self.assertIn('E041b', log.errors)
        log.clear()
        iv.validate({"id": []})
        self.assertIn('E037a', log.errors)
        log.clear()
        # Valid and invalid URIs
        iv.validate({"id": "scheme:rest", "digestAlgorithm": "sha512"})
        self.assertNotIn('W005', log.warns)
        log.clear()
        iv.validate({"id": "URN-3:rest", "digestAlgorithm": "sha512"})
        self.assertNotIn('W005', log.warns)
        log.clear()
        iv.validate({"id": "a1+2-3z.:rest", "digestAlgorithm": "sha512"})
        self.assertNotIn('W005', log.warns)
        self.assertNotIn('W004', log.warns)
        log.clear()
        iv.validate({"id": "not_a_uri", "digestAlgorithm": "sha256"})
        self.assertIn('W005', log.warns)
        self.assertIn('W004', log.warns)
        log.clear()
        iv.validate({"id": "like:uri", "type": "wrong type", "digestAlgorithm": "my_digest"})
        self.assertIn('E038', log.errors)
        self.assertIn('E039', log.errors)
        iv = InventoryValidator(log=log, lax_digests=True)
        log.clear()
        iv.validate({"id": "like:uri", "type": "wrong type", "digestAlgorithm": "my_digest"})
        self.assertNotIn('E039', log.errors)
        self.assertEqual(iv.digest_algorithm, "my_digest")
        iv = InventoryValidator(log=log)
        log.clear()
        iv.validate({"id": "like:uri", "contentDirectory": "not/allowed"})
        self.assertIn('E017', log.errors)
        log.clear()
        iv.validate({"id": "like:uri", "contentDirectory": ["s"]})
        self.assertIn('E017', log.errors)
        log.clear()
        iv.validate({"id": "like:uri", "contentDirectory": ".."})
        self.assertIn('E018', log.errors)

    def test_validate_manifest(self):
        """Test validate_manifest method."""
        log = TLogger()
        iv = InventoryValidator(log=log)
        self.assertEqual(iv.validate_manifest("not a manifest"), ({}, [], set()))
        self.assertIn('E041c', log.errors)
        log.clear()
        self.assertEqual(iv.validate_manifest({"xxx": []}), ({}, [], set()))
        self.assertIn('E025a', log.errors)
        log.clear()
        self.assertEqual(iv.validate_manifest({"067eca3f5b024afa00aeac03a3c42dc0042bf43cba56104037abea8b365c0cf672f0e0c14c91b82bbce6b1464e231ac285d630a82cd4d4a7b194bea04d4b2eb7": "not an array"}), ({}, [], set()))
        self.assertIn('E092', log.errors)
        log.clear()
        iv.lax_digests = True
        self.assertEqual(iv.validate_manifest(
            {
                "067eca3f5b024afa00aeac03a3c42dc0042bf43cba56104037abea8b365c0cf672f0e0c14c91b82bbce6b1464e231ac285d630a82cd4d4a7b194bea04d4b2eb7": [],
                "067ECA3f5b024afa00aeac03a3c42dc0042bf43cba56104037abea8b365c0cf672f0e0c14c91b82bbce6b1464e231ac285d630a82cd4d4a7b194bea04d4b2eb7": []
            }), ({}, [], set([
                "067ECA3f5b024afa00aeac03a3c42dc0042bf43cba56104037abea8b365c0cf672f0e0c14c91b82bbce6b1464e231ac285d630a82cd4d4a7b194bea04d4b2eb7",
                "067eca3f5b024afa00aeac03a3c42dc0042bf43cba56104037abea8b365c0cf672f0e0c14c91b82bbce6b1464e231ac285d630a82cd4d4a7b194bea04d4b2eb7"
            ])))
        self.assertIn('E096', log.errors)
        log.clear()
        # Conflicting content paths
        iv.validate_manifest({"067eca3f5b024afa00aeac03a3c42dc0042bf43cba56104037abea8b365c0cf672f0e0c14c91b82bbce6b1464e231ac285d630a82cd4d4a7b194bea04d4b2eb7": ['v1/content/a', 'v1/content/a/b']})
        self.assertEqual(log.errors, ['E101b'])

    def test_validate_fixity(self):
        """Test validate_fixity method."""
        log = TLogger()
        iv = InventoryValidator(log=log)
        iv.validate_fixity("not a fixity block", [])
        self.assertIn('E056a', log.errors)
        log.clear()
        iv.validate_fixity({'a': 'b'}, [])
        self.assertIn('E056b', log.errors)
        log.clear()
        iv.validate_fixity({'md5': 'f1'}, [])
        self.assertIn('E057a', log.errors)
        log.clear()
        iv.validate_fixity({'md5': {'d1': 'f1'}}, [])
        self.assertIn('E057b', log.errors)
        log.clear()
        iv.validate_fixity({'md5': {'68b329da9893e34099c7d8ad5cb9c940': 'f1'}}, [])
        self.assertIn('E057c', log.errors)
        log.clear()
        iv.validate_fixity({'md5': {'68b329da9893e34099c7d8ad5cb9c940': ['f1']}}, [])
        self.assertIn('E057d', log.errors)
        log.clear()
        iv.validate_fixity({'md5': {'68b329da9893e34099c7d8ad5cb9c940': ['f1'],
                                    '68B329DA9893e34099c7d8ad5cb9c940': ['f2']}}, [])
        self.assertIn('E097', log.errors)
        log.clear()
        # Good case
        iv.validate_fixity({'md5': {'68b329da9893e34099c7d8ad5cb9c940': ['f1a', 'f1b'],
                                    '06c7aa0ab7739f5fde7cb8504af3e851': ['f2']},
                            'sha1': {'adc83b19e793491b1c6ea0fd8b46cd9f32e592fc': ['f1a', 'f1b'],
                                     '00be977f5f719e87c17704954341f50d929bc070': ['f2']}},
                           ['f1a', 'f1b', 'f2'])
        self.assertEqual(len(log.errors), 0)
        # Good case when lax_digests
        iv.lax_digests = True
        iv.validate_fixity({'XXX': {'digest1': ['f1a', 'f1b'],
                                    'digest2': ['f2']}},
                           ['f1a', 'f1b', 'f2'])
        self.assertEqual(len(log.errors), 0)

    def test_validate_version_sequence(self):
        """Test validate_version_sequence method."""
        log = TLogger()
        iv = InventoryValidator(log=log)
        self.assertEqual(iv.validate_version_sequence("not an object"), [])
        self.assertIn('E044', log.errors)
        log.clear()
        self.assertEqual(iv.validate_version_sequence({"v2": {}}), [])
        self.assertIn('E009', log.errors)
        log.clear()
        self.assertEqual(iv.validate_version_sequence({"v02": {}}), [])
        self.assertIn('E009', log.errors)
        log.clear()
        self.assertEqual(iv.validate_version_sequence({"v1": {}, 'v2': {}, 'v3': {}}), ['v1', 'v2', 'v3'])
        log.clear()
        self.assertEqual(iv.validate_version_sequence({"v0001": {}, 'v0002': {}}), ['v0001', 'v0002'])
        self.assertIn('W001', log.warns)
        self.assertEqual(len(log.errors), 0)
        log.clear()
        self.assertEqual(iv.validate_version_sequence({"v1": {}, 'v2': {}, 'v4': {}}), ['v1', 'v2'])
        self.assertIn('E010', log.errors)
        log.clear()
        self.assertEqual(iv.validate_version_sequence({"v01": {}, 'v02': {}, 'v03': {}, "v04": {}, 'v05': {}, 'v06': {}, "v07": {}, 'v08': {}, 'v09': {}}), ['v01', 'v02', 'v03', 'v04', 'v05', 'v06', 'v07', 'v08', 'v09'])
        self.assertEqual(len(log.errors), 0)
        log.clear()
        self.assertEqual(iv.validate_version_sequence({"v01": {}, 'v02': {}, 'v03': {}, "v04": {}, 'v05': {}, 'v06': {}, "v07": {}, 'v08': {}, 'v09': {}, 'v10': {}}), ['v01', 'v02', 'v03', 'v04', 'v05', 'v06', 'v07', 'v08', 'v09'])
        self.assertIn('E011', log.errors)

    def test_validate_versions(self):
        """Test validate_versions method."""
        log = TLogger()
        iv = InventoryValidator(log=log)
        self.assertEqual(iv.validate_versions({}, [], set()), [])
        self.assertEqual(len(log.errors), 0)
        log.clear()
        self.assertEqual(iv.validate_versions({}, [], set()), [])
        self.assertEqual(len(log.errors), 0)
        log.clear()
        # First, no useful data
        self.assertEqual(iv.validate_versions({'v1': {}}, ['v1'], set()), [])
        self.assertIn('E048', log.errors)
        self.assertIn('E048c', log.errors)
        self.assertIn('W007a', log.warns)
        self.assertIn('W007b', log.warns)
        log.clear()
        # Second, good data
        versions = {'v1': {"created": "2010-03-30T21:24:00Z",
                           "message": "A useful message",
                           "state": {},
                           "user": {"name": "A Person", "address": "info:uri1"}}}
        self.assertEqual(iv.validate_versions(versions, ['v1'], set()), [])
        self.assertEqual(log.errors, [])
        log.clear()
        versions['v1']['created'] = {}  # not a string
        self.assertEqual(iv.validate_versions(versions, ['v1'], set()), [])
        self.assertIn('E049d', log.errors)
        log.clear()
        versions['v1']['created'] = "not a datetime"
        self.assertEqual(iv.validate_versions(versions, ['v1'], set()), [])
        self.assertIn('E049c', log.errors)
        log.clear()
        versions['v1']['created'] = "2010-03-30T21:24:00"  # no timezone
        self.assertEqual(iv.validate_versions(versions, ['v1'], set()), [])
        self.assertIn('E049a', log.errors)
        log.clear()
        versions['v1']['created'] = "2010-03-30T21:24Z"  # no seconds
        self.assertEqual(iv.validate_versions(versions, ['v1'], set()), [])
        self.assertIn('E049b', log.errors)
        log.clear()
        versions['v1']['created'] = "2010-03-30T21:24:00Z"
        versions['v1']['message'] = {}  # not a string
        self.assertEqual(iv.validate_versions(versions, ['v1'], set()), [])
        self.assertIn('E094', log.errors)
        log.clear()
        versions['v1']['message'] = "A message"
        versions['v1']['user'] = "A string"  # not a dict
        self.assertEqual(iv.validate_versions(versions, ['v1'], set()), [])
        self.assertIn('E054a', log.errors)
        log.clear()
        versions['v1']['user'] = {"name": {}, "address": {}}  # not strings
        self.assertEqual(iv.validate_versions(versions, ['v1'], set()), [])
        self.assertIn('E054b', log.errors)
        self.assertIn('E054c', log.errors)
        log.clear()
        versions['v1']['user'] = {"name": "A Person"}  # no address
        self.assertEqual(iv.validate_versions(versions, ['v1'], set()), [])
        self.assertIn('W008', log.warns)

    def test_validate_state_block(self):
        """Test validate_state_block."""
        log = TLogger()
        iv = InventoryValidator(log=log)
        iv.digest_algorithm = 'sha512'
        self.assertEqual(iv.validate_state_block({}, "v1", set()), [])
        self.assertEqual(len(log.errors), 0)
        log.clear()
        self.assertEqual(iv.validate_state_block("invalid", "v1", set()), [])
        self.assertIn('E050c', log.errors)
        log.clear()
        self.assertEqual(iv.validate_state_block({"not a digest": []}, "v1", set()), [])
        self.assertIn('E050d', log.errors)
        log.clear()
        d = "4a89417821564b1e1956130569c390dd6122b51296ec620cadd0555ff5aae21c2a17383a194290fc95c73c63261bd8cb77ac275c85e6300cd711fa132fe8706e"
        self.assertEqual(iv.validate_state_block({d: "not a list"}, "v1", set()), [])
        self.assertIn('E050e', log.errors)
        log.clear()
        self.assertEqual(iv.validate_state_block({d: ["good path", 'a/./b']}, "v1", set()), [d])
        self.assertIn('E052', log.errors)
        log.clear()
        self.assertEqual(iv.validate_state_block({d: ["good path", '/']}, "v1", set()), [d])
        self.assertIn('E053', log.errors)
        log.clear()
        # Finally a good case
        d2 = "ae16b7632ee42fafd6b510e94a4951b2346ad90a1eff4baae2d7c0d5481515de61dcbc9a8d01f4824ab5215f033858189331859fb5b75fea5809230c63bad34a"
        self.assertEqual(iv.validate_state_block({d2: ["path2", "good/path3"]}, "v1", set([d, d2])), [d2])
        self.assertEqual(log.errors, [])

    def test_check_digests_present_and_used(self):
        """Test check_digests_present_and_used."""
        log = TLogger()
        iv = InventoryValidator(log=log)
        manifest = {'file_aaa1': 'aaa', 'file_aaa2': 'aaa', 'file_bbb': 'bbb'}
        iv.check_digests_present_and_used(manifest, ['aaa', 'bbb'])
        self.assertEqual(len(log.errors), 0)
        iv.check_digests_present_and_used(manifest, ['aaa'])
        self.assertIn('E107', log.errors)
        log.clear()
        iv.check_digests_present_and_used(manifest, ['aaa', 'bbb', 'ccc'])
        self.assertIn('E050a', log.errors)

    def test_digest_regex(self):
        """Test digest_regex."""
        log = TLogger()
        iv = InventoryValidator(log=log)
        iv.digest_algorithm = 'md5'
        self.assertEqual(iv.digest_regex(), '^[0-9a-fA-F]{32}$')
        iv.digest_algorithm = 'not a digest'
        self.assertEqual(iv.digest_regex(), '^.*$')
        self.assertEqual(log.errors, ['E026a'])
        log.clear()
        iv.lax_digests = True
        self.assertEqual(iv.digest_regex(), '^.*$')
        self.assertEqual(log.errors, [])

    def test_validate_as_prior_version(self):
        """Test validate_as_prior_version method."""
        log = TLogger()
        iv = InventoryValidator(log=log)
        prior = InventoryValidator(log=TLogger())
        # Same versions won't work...
        iv.all_versions = ['v1']
        prior.all_versions = ['v1']
        iv.validate_as_prior_version(prior)
        self.assertEqual(log.errors, ['E066a'])
        log.clear()
        # Good inventory in spite of diferent digests
        iv.all_versions = ['v1', 'v2']
        iv.digest_algorithm = 'a1'
        iv.inventory = {"manifest": {"a1d1": ["v1/content/f1"],
                                     "a1d2": ["v1/content/f2"],
                                     "a1d3": ["v2/content/f3"]},
                        "versions": {"v1": {"state": {"a1d1": ["f1"], "a1d2": ["f2"]}},
                                     "v2": {"state": {"a1d1": ["f1"], "a1d3": ["f3"]}}}}
        prior.digest_algorithm = 'a2'
        prior.inventory = {"manifest": {"a2d1": ["v1/content/f1"],
                                        "a2d2": ["v1/content/f2"]},
                           "versions": {"v1": {"state": {"a2d1": ["f1"], "a2d2": ["f2"]}}}}
        iv.validate_as_prior_version(prior)
        self.assertEqual(log.errors, [])
        log.clear()
        # Now let's add a copy file in the state in prior so as not to match
        prior.inventory["versions"]["v1"]["state"]["a2d2"] = ["f2", "f2-copy"]
        iv.validate_as_prior_version(prior)
        self.assertEqual(log.errors, ["E066b"])
        log.clear()
        # Now move that back but change a a manifest location
        prior.inventory["versions"]["v1"]["state"]["a2d2"] = ["f2"]
        prior.inventory["manifest"]["a2d2"] = ["v1/content/f2--moved"]
        iv.validate_as_prior_version(prior)
        self.assertEqual(log.errors, ["E066c"])

    def test_compare_states_for_version(self):
        """Test compare_states_for_version method."""
        log = TLogger()
        iv = InventoryValidator(log=log)
        prior = InventoryValidator(log=TLogger())
        # Same digests
        iv.inventory = {
            "versions": {"v99": {"state": {"a1d1": ["f1"], "a1d2": ["f2", "f3"]}}}}
        prior.inventory = {
            "versions": {"v99": {"state": {"a1d1": ["f1"], "a1d2": ["f2", "f3"]}}}}
        iv.compare_states_for_version(prior, 'v99')
        self.assertEqual(log.errors, [])
        log.clear()
        # Extra in iv
        iv.inventory = {
            "versions": {"v99": {"state": {"a1d1": ["f1"], "a1d2": ["f2", "f3"], "a1d3": ["f4"]}}}}
        iv.compare_states_for_version(prior, 'v99')
        self.assertEqual(log.errors, ['E066d'])
        log.clear()
        # Extra in prior
        iv.inventory = {
            "versions": {"v99": {"state": {"a1d2": ["f2", "f3"]}}}}
        iv.compare_states_for_version(prior, 'v99')
        self.assertEqual(log.errors, ['E066e'])

    def test_check_content_path(self):
        """Test check_content_path method."""
        log = TLogger()
        iv = InventoryValidator(log=log)
        cp = set()
        cd = set()
        self.assertTrue(iv.check_content_path('v1/content/anything', cp, cd))
        self.assertEqual(log.errors, [])
        self.assertEqual(cp, set(['v1/content/anything']))
        self.assertEqual(cd, set(['v1/content']))
        log.clear()
        iv.content_directory = 'xyz'
        self.assertFalse(iv.check_content_path('v1/content/anything', cp, cd))
        self.assertEqual(log.errors, ['E042a'])
        log.clear()
        self.assertTrue(iv.check_content_path('v1/xyz/anything', cp, cd))
        self.assertEqual(log.errors, [])
        # Error cases
        log.clear()
        self.assertFalse(iv.check_content_path('1/xyz/1', cp, cd))
        self.assertEqual(log.errors, ['E042a'])
        log.clear()
        self.assertFalse(iv.check_content_path('vv1/xyz/1', cp, cd))
        self.assertEqual(log.errors, ['E042a'])
        log.clear()
        self.assertFalse(iv.check_content_path('v1/x/1', cp, cd))
        self.assertEqual(log.errors, ['E042a'])
        log.clear()
        self.assertFalse(iv.check_content_path('v1/xyz/1/', cp, cd))
        self.assertEqual(log.errors, ['E100'])
        log.clear()
        self.assertFalse(iv.check_content_path('/v1/xyz/1', cp, cd))
        self.assertEqual(log.errors, ['E100'])
        log.clear()
        self.assertFalse(iv.check_content_path('v1/xyz/', cp, cd))
        self.assertEqual(log.errors, ['E100'])
        log.clear()
        self.assertFalse(iv.check_content_path('v1/xyz//1', cp, cd))
        self.assertEqual(log.errors, ['E099'])
        log.clear()
        self.assertFalse(iv.check_content_path('v1/xyz/abc//d', cp, cd))
        self.assertEqual(log.errors, ['E099'])
        log.clear()
        self.assertFalse(iv.check_content_path('v1/xyz/abc/./d', cp, cd))
        self.assertEqual(log.errors, ['E099'])
        log.clear()
        self.assertFalse(iv.check_content_path('v1/xyz/abc/../d', cp, cd))
        self.assertEqual(log.errors, ['E099'])
        log.clear()
        self.assertFalse(iv.check_content_path('v1/xyz/.', cp, cd))
        self.assertEqual(log.errors, ['E099'])
        log.clear()
        self.assertFalse(iv.check_content_path('v1/xyz/anything', cp, cd))
        self.assertEqual(log.errors, ['E101a'])
        # Good cases
        log.clear()
        self.assertTrue(iv.check_content_path('v1/xyz/.secret/d', cp, cd))
        self.assertEqual(log.errors, [])
        log.clear()
        self.assertTrue(iv.check_content_path('v1/xyz/.a', cp, cd))
        self.assertEqual(log.errors, [])
        # Check good paths accumulated
        self.assertEqual(cp, set(('v1/xyz/anything', 'v1/xyz/.a', 'v1/content/anything', 'v1/xyz/.secret/d')))
        self.assertEqual(cd, set(('v1/xyz', 'v1/content', 'v1/xyz/.secret')))

    def test_check_logical_path(self):
        """Test check_logical_path method."""
        log = TLogger()
        iv = InventoryValidator(log=log)
        lp = set()
        ld = set()
        iv.check_logical_path("almost anything goes", "root", lp, ld)
        self.assertEqual(log.errors, [])
        iv.check_logical_path("including/this/long/path", "root", lp, ld)
        self.assertEqual(log.errors, [])
        iv.check_logical_path("/but not this", "root", lp, ld)
        self.assertEqual(log.errors, ['E053'])
        log.clear()
        iv.check_logical_path("./or this", "root", lp, ld)
        self.assertEqual(log.errors, ['E052'])
        log.clear()
        iv.check_logical_path("or this/", "root", lp, ld)
        self.assertEqual(log.errors, ['E053'])
        # And check only good paths recorded
        self.assertEqual(lp, set(('almost anything goes', 'including/this/long/path')))
        self.assertEqual(ld, set(('', 'including/this/long')))

    def test_bad_inventory_files(self):
        """Test bad inventory files."""
        for bad, codes in {'inventory_E042a_bad_content_paths': ['E042a'],
                           'inventory_E042b_unknown_version': ['E042b'],
                           'inventory_E042b_zero_padding_mismatch': ['E042b']}.items():
            filepath = 'extra_fixtures/bad-inventories/' + bad + '.json'
            with open(filepath, 'r') as fh:
                inventory = json.load(fh)
            log = TLogger()
            iv = InventoryValidator(log=log)
            iv.validate(inventory)
            self.assertEqual(set(codes), set(log.errors), msg="for object at " + filepath)
