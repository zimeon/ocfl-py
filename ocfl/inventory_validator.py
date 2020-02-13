"""OCFL Inventory Validator.

Code to validate the Python representation of an OCFL Inventory
as read with json.load(). Does not examine anything in storage.
"""
import re

from .w3c_datetime import str_to_datetime


class InventoryValidator(object):
    """Class for OCFL Inventory Validator."""

    def __init__(self, log=None):
        """Initialize OCFL Inventory Validator."""
        self.log = log
        # Object state
        self.digest_algorithm = 'sha512'
        self.content_directory = 'content'
        self.all_versions = []

    def validate(self, inventory):
        """Validate a given inventory."""
        # Basic structure
        if 'id' in inventory:
            iid = inventory['id']
            if type(iid) != str or iid == '':
                self.log.error("E101")
            elif not re.match(r'''(\w+):.+''', iid):
                self.log.warn("W007", id=iid)
        else:
            self.log.error("E100")
        if 'type' not in inventory:
            self.log.error("E102")
        elif inventory['type'] != 'https://ocfl.io/1.0/spec/#inventory':
            self.log.error("E103")
        if 'digestAlgorithm' not in inventory:
            self.log.error("E104")
        elif inventory['digestAlgorithm'] == 'sha512':
            pass
        elif inventory['digestAlgorithm'] == 'sha256':
            self.log.warn("W006")
            self.digest_algorithm = inventory['digestAlgorithm']
        else:
            self.log.error("E105", digest_algorithm=inventory['digestAlgorithm'])
        if 'contentDirectory' in inventory:
            self.content_directory = inventory['contentDirectory']
            if re.match(r'''/''', self.content_directory) or self.content_directory in ['.', '..']:
                # See https://github.com/OCFL/spec/issues/415
                self.log.error("E998")
        if 'manifest' not in inventory:
            self.log.error("E107")
        else:
            manifest_files = self.validate_manifest(inventory['manifest'])
        if 'versions' not in inventory:
            self.log.error("E108")
        else:
            self.all_versions = self.validate_version_sequence(inventory['versions'])
            digests_used = self.validate_versions(inventory['versions'], self.all_versions, manifest_files)
        if 'head' in inventory:
            head = self.all_versions[-1]
            if inventory['head'] != head:
                self.log.error("E914", got=inventory['head'], expected=head)
        else:
            self.log.error("E106")
        if 'manifest' in inventory and 'versions' in inventory:
            self.check_digests_present_and_used(inventory['manifest'], digests_used)

    def validate_manifest(self, manifest):
        """Validate manifest block in inventory."""
        # Get regex for checking form of digest
        manifest_files = {}
        for digest in manifest:
            m = re.match(self.digest_regex(), digest)
            if not m:
                self.log.error('E304', digest=digest)
            else:
                for file in manifest[digest]:
                    manifest_files[file] = digest
                    if not self.is_valid_content_path(file):
                        self.log.error("E913", path=file)
        return manifest_files

    def validate_version_sequence(self, versions):
        """Validate sequence of version names in versions block in inventory.

        Returns an array of in-sequence version directories.
        """
        # Validate version sequence
        # https://ocfl.io/draft/spec/#version-directories
        zero_padded = None
        max_version_num = 999999  # Excessive limit
        all_versions = []
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
                    max_version_num = (10 ** n) - 1
                    break
            if not zero_padded:
                self.log.error("E305")
                return
        if zero_padded:
            self.log.warn("W003")
        # Have v1 and know format, work through to check sequence
        for n in range(2, max_version_num + 1):
            v = (fmt % n)
            if v in versions:
                all_versions.append(v)
            else:
                if len(versions) != (n - 1):
                    self.log.error("E306")  # Extra version dirs outside sequence
                return(all_versions)
        # n now exceeds the zero padding size, we might either have an object that
        # is correct with its maximum number of versions, or else an error
        if len(versions) != max_version_num:
            self.log.error("E306")
        return(all_versions)

    def validate_versions(self, versions, all_versions, manifest_files):
        """Validate versions block in inventory."""
        digests_used = []
        for v in all_versions:
            version = versions[v]
            if 'created' not in version or type(versions[v]['created']) != str:
                self.log.error('E401')  # No created
            else:
                created = versions[v]['created']
                try:
                    dt = str_to_datetime(created)
                    if not re.search(r'''(Z|[+-]\d\d:\d\d)$''', created):  # FIXME - kludge
                        self.log.warn('W008')
                    if not re.search(r'''T\d\d:\d\d:\d\d''', created):  # FIXME - kludge
                        self.log.warn('W009')
                except ValueError as e:
                    self.log.error('E402', description=str(e))
            if 'state' in version:
                digests_used += self.validate_state_block(version['state'])
            else:
                self.log.error('E402')
            if 'message' not in version:
                self.log.warn('W001')
            elif type(version['message']) != str:
                self.log.error('E403')
            if 'user' not in version:
                self.log.warn('W002')
            else:
                user = version['user']
                if type(user) != dict:
                    self.log.error('E404')
                else:
                    if 'name' not in user or type(user['name']) != str:
                        self.log.error('E405')
                    if 'address' not in user:
                        self.log.warn('W010')
                    elif type(user['address']) != str:
                        self.log.error('E406')
        return digests_used

    def validate_state_block(self, state):
        """Validate state block in a version in an inventory.

        Returns a list of content digests referenced in the state block.
        """
        digests = []
        if type(state) != dict:
            self.log.error('E912')
        else:
            digest_regex = self.digest_regex()
            for digest in state:
                if not re.match(self.digest_regex(), digest):
                    self.log.error('E305', digest=digest)
                else:
                    for file in state[digest]:
                        # FIXME - Validate logical file names
                        pass
                    digests.append(digest)
        return digests

    def check_digests_present_and_used(self, manifest, digests_used):
        """Check all digests in manifest that are needed are present and used."""
        if set(manifest.keys()) != set(digests_used):
            not_in_state = []
            for digest in manifest:
                if digest not in digests_used:
                    not_in_state.append(digest)
            not_in_manifest = []
            for digest in digests_used:
                if digest not in manifest:
                    not_in_manifest.append(digest)
            description = ''
            if len(not_in_manifest) > 0:
                self.log.error("E913", description="in state but not in manifest: " + ", ".join(not_in_manifest))
            if len(not_in_state) > 0:
                self.log.error("E302", description="in manifest but not in state: " + ", ".join(not_in_state))

    def digest_regex(self):
        """A regex for validating digest algorithm format."""
        if self.digest_algorithm == 'sha512':
            return r'''^[0-9a-z]{128}$'''
        elif self.digest_algorithm == 'sha256':
            return r'''^[0-9a-z]{64}$'''
        raise Exception("Bad digest algorithm %s" % (self.digest_algorithm))

    def is_valid_content_path(self, path):
        """True if path is a valid content path."""
        m = re.match(r'''^v\d+/''' + self.content_directory + r'''/''', path)
        return m is not None
