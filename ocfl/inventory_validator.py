"""OCFL Inventory Validator.

Code to validate the Python representation of an OCFL Inventory
as read with json.load(). Does not examine anything in storage.
"""
import re

from .digest import digest_regex, normalized_digest
from .validation_logger import ValidationLogger
from .w3c_datetime import str_to_datetime


def get_file_map(inventory, version_dir):
    """Get a map of file in state to files on disk for version_dir in inventory."""
    state = inventory['versions'][version_dir]['state']
    manifest = inventory['manifest']
    file_map = {}
    for digest in state:
        if digest in manifest:
            for file in state[digest]:
                file_map[file] = manifest[digest]
    return file_map


def is_valid_logical_path(path):
    """True if the logical path is valid, False otherwise.

    Neither a leading or trailing slash is allowed which is caught by the
    split and then test for empty.

    FIXME - https://github.com/OCFL/spec/issues/436
    """
    for element in path.split('/'):
        if element in ['.', '..', '']:
            return False
    return True


class InventoryValidator(object):
    """Class for OCFL Inventory Validator."""

    def __init__(self, log=None, where='???',
                 lax_digests=False):
        """Initialize OCFL Inventory Validator."""
        self.log = ValidationLogger() if log is None else log
        self.where = where
        # Object state
        self.inventory = None
        self.digest_algorithm = 'sha512'
        self.content_directory = 'content'
        self.head = None
        self.all_versions = []
        self.manifest_files = None
        # Validation control
        self.lax_digests = lax_digests

    def error(self, code, **args):
        """Error with added context."""
        self.log.error(code, where=self.where, **args)

    def warn(self, code, **args):
        """Warning with added context."""
        self.log.warn(code, where=self.where, **args)

    def validate(self, inventory):
        """Validate a given inventory."""
        # Basic structure
        self.inventory = inventory
        if 'id' in inventory:
            iid = inventory['id']
            if type(iid) != str or iid == '':
                self.error("E037")
            elif not re.match(r'''(\w+):.+''', iid):
                self.warn("W005", id=iid)
        else:
            self.error("E036a")
        if 'type' not in inventory:
            self.error("E036b")
        elif inventory['type'] != 'https://ocfl.io/1.0/spec/#inventory':
            self.error("E038")
        if 'digestAlgorithm' not in inventory:
            self.error("E036c")
        elif inventory['digestAlgorithm'] == 'sha512':
            pass
        elif self.lax_digests:
            self.digest_algorithm = inventory['digestAlgorithm']
        elif inventory['digestAlgorithm'] == 'sha256':
            self.warn("W004")
            self.digest_algorithm = inventory['digestAlgorithm']
        else:
            self.error("E039", digest_algorithm=inventory['digestAlgorithm'])
        if 'contentDirectory' in inventory:
            # Careful only to set self.content_directory if value is safe
            cd = inventory['contentDirectory']
            if type(cd) != str or '/' in cd or cd in ['.', '..']:
                self.error("E018")
            else:
                self.content_directory = cd
        if 'manifest' not in inventory:
            self.error("E041a")
        else:
            self.manifest_files = self.validate_manifest(inventory['manifest'])
        if 'versions' not in inventory:
            self.error("E041b")
        else:
            self.all_versions = self.validate_version_sequence(inventory['versions'])
            digests_used = self.validate_versions(inventory['versions'], self.all_versions)
        if 'head' in inventory:
            self.head = self.all_versions[-1]
            if inventory['head'] != self.head:
                self.error("E040", got=inventory['head'], expected=self.head)
        else:
            self.error("E036d")
        if 'manifest' in inventory and 'versions' in inventory:
            self.check_digests_present_and_used(self.manifest_files, digests_used)

    def validate_manifest(self, manifest):
        """Validate manifest block in inventory.

        Returns manifest_files, a mapping from file to digest for each file in
        the manifest.
        """
        manifest_files = {}
        manifest_digests = set()
        if type(manifest) != dict:
            self.error('E041c')
        else:
            for digest in manifest:
                m = re.match(self.digest_regex(), digest)
                if not m:
                    self.error('E025a', digest=digest, algorithm=self.digest_algorithm)  # wrong form of digest
                elif type(manifest[digest]) != list:
                    self.error('E092', digest=digest)  # must have path list value
                else:
                    for file in manifest[digest]:
                        norm_digest = normalized_digest(digest, self.digest_algorithm)
                        if norm_digest in manifest_digests:
                            # We have already seen this in different un-normalized form!
                            self.error("E922", digest=norm_digest)
                        else:
                            manifest_files[file] = norm_digest
                            manifest_digests.add(norm_digest)
                            if not self.is_valid_content_path(file):
                                self.error("E042", path=file)
        return manifest_files

    def validate_version_sequence(self, versions):
        """Validate sequence of version names in versions block in inventory.

        Returns an array of in-sequence version directories that are part
        of a valid sequences. May exclude other version directory names that are
        not part of the valid sequence if an error is thrown.
        """
        all_versions = []
        if type(versions) != dict:
            self.error('E044')
            return all_versions
        # Validate version sequence
        # https://ocfl.io/draft/spec/#version-directories
        zero_padded = None
        max_version_num = 999999  # Excessive limit
        if 'v1' in versions:
            fmt = 'v%d'
            zero_padded = False
            all_versions.append('v1')
        else:  # Find padding size
            for n in range(2, 11):
                fmt = 'v%0' + str(n) + 'd'
                vkey = fmt % 1
                if vkey in versions:
                    all_versions.append(vkey)
                    zero_padded = n
                    max_version_num = (10 ** (n - 1)) - 1
                    break
            if not zero_padded:
                self.error("E008")
                return all_versions
        if zero_padded:
            self.warn("W001")
        # Have v1 and know format, work through to check sequence
        for n in range(2, max_version_num + 1):
            v = (fmt % n)
            if v in versions:
                all_versions.append(v)
            else:
                if len(versions) != (n - 1):
                    self.error("E009")  # Extra version dirs outside sequence
                return all_versions
        # We have now included all possible versions up to the zero padding
        # size, if there are more versions than this number then we must
        # have extra that violate the zero-padding rule or are out of
        # sequence
        if len(versions) > max_version_num:
            self.error("E009")
        return all_versions

    def validate_versions(self, versions, all_versions):
        """Validate versions blocks in inventory.

        Requires as input two things which are assumed to be structurally correct
        from prior basic validation:

          * versions - which is the JSON object (dict) from the inventory
          * all_versions - an ordered list of the versions to look at in versions
                           (all other keys in versions will be ignored)

        Returns a list of digests_used which can then be checked against the
        manifest.
        """
        digests_used = []
        for v in all_versions:
            version = versions[v]
            if 'created' not in version:
                self.error('E048', version=v)  # No created
            elif type(versions[v]['created']) != str:
                self.error('E049d', version=v)  # Bad created
            else:
                created = versions[v]['created']
                try:
                    dt = str_to_datetime(created)
                    if not re.search(r'''(Z|[+-]\d\d:\d\d)$''', created):  # FIXME - kludge
                        self.error('E049a', version=v)
                    if not re.search(r'''T\d\d:\d\d:\d\d''', created):  # FIXME - kludge
                        self.error('E049b', version=v)
                except ValueError as e:
                    self.error('E049c', version=v, description=str(e))
            if 'state' in version:
                digests_used += self.validate_state_block(version['state'], version=v)
            else:
                self.error('E410', version=v)
            if 'message' not in version:
                self.warn('W007a', version=v)
            elif type(version['message']) != str:
                self.error('E048b', version=v)  # FIXME https://github.com/OCFL/spec/issues/460
            if 'user' not in version:
                self.warn('W007b', version=v)
            else:
                user = version['user']
                if type(user) != dict:
                    self.error('E054a', version=v)
                else:
                    if 'name' not in user or type(user['name']) != str:
                        self.error('E054b', version=v)
                    if 'address' not in user:
                        self.warn('W008', version=v)
                    elif type(user['address']) != str:
                        self.error('E054c', version=v)
                    elif not re.match(r'''\w{3,6}:''', user['address']):
                        self.warn('W009', version=v)
        return digests_used

    def validate_state_block(self, state, version):
        """Validate state block in a version in an inventory.

        The version is used only for error reporting.

        Returns a list of content digests referenced in the state block.
        """
        digests = []
        if type(state) != dict:
            self.error('E050c', version=version)
        else:
            digest_regex = self.digest_regex()
            for digest in state:
                if not re.match(self.digest_regex(), digest):
                    self.error('E050d', version=version, digest=digest)
                elif type(state[digest]) != list:
                    self.error('E050e', version=version, digest=digest)
                else:
                    for path in state[digest]:
                        if not is_valid_logical_path(path):
                            self.error('E051', version=version, digest=digest, path=path)
                    norm_digest = normalized_digest(digest, self.digest_algorithm)
                    if norm_digest in digests:
                        # We have already seen this in different un-normalized form!
                        self.error("E923", version=version, digest=norm_digest)
                    else:
                        digests.append(norm_digest)
        return digests

    def check_digests_present_and_used(self, manifest_files, digests_used):
        """Check all digests in manifest that are needed are present and used."""
        in_manifest = set(manifest_files.values())
        in_state = set(digests_used)
        not_in_manifest = in_state.difference(in_manifest)
        if len(not_in_manifest) > 0:
            self.error("E050a", digests=", ".join(sorted(not_in_manifest)))
        not_in_state = in_manifest.difference(in_state)
        if len(not_in_state) > 0:
            self.error("E050b", digests=", ".join(sorted(not_in_state)))

    def digest_regex(self):
        """A regex for validating un-normalized digest format."""
        try:
            return digest_regex(self.digest_algorithm)
        except ValueError:
            if not self.lax_digests:
                self.error('E026a', digest=self.digest_algorithm)
        # Match anything
        return r'''^.*$'''

    def is_valid_content_path(self, path):
        """True if path is a valid content path."""
        m = re.match(r'''^v\d+/''' + self.content_directory + r'''/''', path)
        return m is not None

    def validate_as_prior_version(self, prior):
        """Check that prior is a valid InventoryValidator for a prior version of the current inventory object.

        Both inventories are assumed to have been checked for internal consistency.
        """
        # Must have a subset of versions which also check zero padding format etc.
        if not set(prior.all_versions).issubset(set(self.all_versions)):
            self.error('E066a', prior_head=prior.head)
        elif not set(prior.manifest_files.keys()).issubset(self.manifest_files.keys()):
            self.error('E066b', prior_head=prior.head)
        else:
            # Check references to files but realize that there might be different
            # digest algorithms between versions
            for version_dir in prior.all_versions:
                prior_map = get_file_map(prior.inventory, version_dir)
                self_map = get_file_map(self.inventory, version_dir)
                if prior_map.keys() != self_map.keys():
                    self.error('E066c', version_dir=version_dir, prior_head=prior.head)
                else:
                    # Check them all...
                    for file in prior_map:
                        if prior_map[file] != self_map[file]:
                            self.error('E066d', version_dir=version_dir, prior_head=prior.head, file=file)
            # Check metadata
            prior_version = prior.inventory['versions'][version_dir]
            self_version = self.inventory['versions'][version_dir]
            for key in ('created', 'message', 'user'):
                if prior_version.get(key) != self_version.get(key):
                    self.warn('W011', version_dir=version_dir, prior_head=prior.head, key=key)
