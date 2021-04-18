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


class InventoryValidator():
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
        self.all_versions = []
        self.manifest_files = None
        self.unnormalized_digests = None
        self.head = 'UNKNOWN'
        # Validation control
        self.lax_digests = lax_digests

    def error(self, code, **args):
        """Error with added context."""
        self.log.error(code, where=self.where, **args)

    def warning(self, code, **args):
        """Warning with added context."""
        self.log.warning(code, where=self.where, **args)

    def validate(self, inventory):
        """Validate a given inventory."""
        # Basic structure
        self.inventory = inventory
        if 'id' in inventory:
            iid = inventory['id']
            if not isinstance(iid, str) or iid == '':
                self.error("E037")
            elif not re.match(r'''(\w+):.+''', iid):
                self.warning("W005", id=iid)
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
            self.warning("W004")
            self.digest_algorithm = inventory['digestAlgorithm']
        else:
            self.error("E039", digest_algorithm=inventory['digestAlgorithm'])
        if 'contentDirectory' in inventory:
            # Careful only to set self.content_directory if value is safe
            cd = inventory['contentDirectory']
            if not isinstance(cd, str) or '/' in cd or cd in ['.', '..']:
                self.error("E018")
            else:
                self.content_directory = cd
        if 'manifest' not in inventory:
            self.error("E041a")
        else:
            (self.manifest_files, self.unnormalized_digests) = self.validate_manifest(inventory['manifest'])
        if 'versions' not in inventory:
            self.error("E041b")
        else:
            self.all_versions = self.validate_version_sequence(inventory['versions'])
            digests_used = self.validate_versions(inventory['versions'], self.all_versions, self.unnormalized_digests)
        if 'head' not in inventory:
            self.error("E036d")
        elif len(self.all_versions) > 0:
            self.head = self.all_versions[-1]
            if inventory['head'] != self.head:
                self.error("E040", got=inventory['head'], expected=self.head)
        if len(self.all_versions) == 0:
            # Abort tests is we don't have a valid version sequence, otherwise
            # there will likely be spurious subsequent error reports
            return
        if 'manifest' in inventory and 'versions' in inventory:
            self.check_digests_present_and_used(self.manifest_files, digests_used)
        if 'fixity' in inventory:
            self.validate_fixity(inventory['fixity'], self.manifest_files)

    def validate_manifest(self, manifest):
        """Validate manifest block in inventory.

        Returns:
          * manifest_files, a mapping from file to digest for each file in
              the manifest
          * unnormalized_digests - a set of the original digests in unnormalized
              form that MUST match exactly the values used in state blocks
        """
        manifest_files = {}
        unnormalized_digests = set()
        manifest_digests = set()
        if not isinstance(manifest, dict):
            self.error('E041c')
        else:
            content_paths = set()
            content_directories = set()
            for digest in manifest:
                m = re.match(self.digest_regex(), digest)
                if not m:
                    self.error('E025a', digest=digest, algorithm=self.digest_algorithm)  # wrong form of digest
                elif not isinstance(manifest[digest], list):
                    self.error('E092', digest=digest)  # must have path list value
                else:
                    unnormalized_digests.add(digest)
                    norm_digest = normalized_digest(digest, self.digest_algorithm)
                    if norm_digest in manifest_digests:
                        # We have already seen this in different un-normalized form!
                        self.error("E096", digest=norm_digest)
                    else:
                        manifest_digests.add(norm_digest)
                    for file in manifest[digest]:
                        manifest_files[file] = norm_digest
                        self.check_content_path(file, content_paths, content_directories)
            # Check for conflicting content paths
            for path in content_directories:
                if path in content_paths:
                    self.error("E101", path=path)

        return (manifest_files, unnormalized_digests)

    def validate_fixity(self, fixity, manifest_files):
        """Validate fixity block in inventory.

        Check the structure of the fixity block and makes sure that only files
        listed in the manifest are referenced.
        """
        if not isinstance(fixity, dict):
            self.error('E056a')
        else:
            for digest_algorithm in fixity:
                known_digest = True
                try:
                    regex = digest_regex(digest_algorithm)
                except ValueError:
                    if not self.lax_digests:
                        self.error('E056b', algorithm=self.digest_algorithm)
                        continue
                    # Match anything
                    regex = r'''^.*$'''
                    known_digest = False
                fixity_algoritm_block = fixity[digest_algorithm]
                if not isinstance(fixity_algoritm_block, dict):
                    self.error('E057a', algorithm=self.digest_algorithm)
                else:
                    digests_seen = set()
                    for digest in fixity_algoritm_block:
                        m = re.match(regex, digest)
                        if not m:
                            self.error('E057b', digest=digest, algorithm=digest_algorithm)  # wrong form of digest
                        elif not isinstance(fixity_algoritm_block[digest], list):
                            self.error('E057c', digest=digest, algorithm=digest_algorithm)  # must have path list value
                        else:
                            if known_digest:
                                norm_digest = normalized_digest(digest, digest_algorithm)
                            else:
                                norm_digest = digest
                            if norm_digest in digests_seen:
                                # We have already seen this in different un-normalized form!
                                self.error("E097", digest=norm_digest, algorithm=digest_algorithm)
                            else:
                                digests_seen.add(norm_digest)
                            for file in fixity_algoritm_block[digest]:
                                if file not in manifest_files:
                                    self.error("E057d", digest=norm_digest, algorithm=digest_algorithm, path=file)

    def validate_version_sequence(self, versions):
        """Validate sequence of version names in versions block in inventory.

        Returns an array of in-sequence version directories that are part
        of a valid sequences. May exclude other version directory names that are
        not part of the valid sequence if an error is thrown.
        """
        all_versions = []
        if not isinstance(versions, dict):
            self.error("E044")
            return all_versions
        if len(versions) == 0:
            self.error("E008")
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
                self.error("E009")
                return all_versions
        if zero_padded:
            self.warning("W001")
        # Have v1 and know format, work through to check sequence
        for n in range(2, max_version_num + 1):
            v = (fmt % n)
            if v in versions:
                all_versions.append(v)
            else:
                if len(versions) != (n - 1):
                    self.error("E010")  # Extra version dirs outside sequence
                return all_versions
        # We have now included all possible versions up to the zero padding
        # size, if there are more versions than this number then we must
        # have extra that violate the zero-padding rule or are out of
        # sequence
        if len(versions) > max_version_num:
            self.error("E011")
        return all_versions

    def validate_versions(self, versions, all_versions, unnormalized_digests):
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
            elif not isinstance(versions[v]['created'], str):
                self.error('E049d', version=v)  # Bad created
            else:
                created = versions[v]['created']
                try:
                    str_to_datetime(created)  # catch ValueError if fails
                    if not re.search(r'''(Z|[+-]\d\d:\d\d)$''', created):  # FIXME - kludge
                        self.error('E049a', version=v)
                    if not re.search(r'''T\d\d:\d\d:\d\d''', created):  # FIXME - kludge
                        self.error('E049b', version=v)
                except ValueError as e:
                    self.error('E049c', version=v, description=str(e))
            if 'state' in version:
                digests_used += self.validate_state_block(version['state'], version=v, unnormalized_digests=unnormalized_digests)
            else:
                self.error('E048c', version=v)
            if 'message' not in version:
                self.warning('W007a', version=v)
            elif not isinstance(version['message'], str):
                self.error('E094', version=v)
            if 'user' not in version:
                self.warning('W007b', version=v)
            else:
                user = version['user']
                if not isinstance(user, dict):
                    self.error('E054a', version=v)
                else:
                    if 'name' not in user or not isinstance(user['name'], str):
                        self.error('E054b', version=v)
                    if 'address' not in user:
                        self.warning('W008', version=v)
                    elif not isinstance(user['address'], str):
                        self.error('E054c', version=v)
                    elif not re.match(r'''\w{3,6}:''', user['address']):
                        self.warning('W009', version=v)
        return digests_used

    def validate_state_block(self, state, version, unnormalized_digests):
        """Validate state block in a version in an inventory.

        The version is used only for error reporting.

        Returns a list of content digests referenced in the state block.
        """
        digests = []
        logical_paths = set()
        logical_directories = set()
        if not isinstance(state, dict):
            self.error('E050c', version=version)
        else:
            digest_re = re.compile(self.digest_regex())
            for digest in state:
                if not digest_re.match(digest):
                    self.error('E050d', version=version, digest=digest)
                elif not isinstance(state[digest], list):
                    self.error('E050e', version=version, digest=digest)
                else:
                    for path in state[digest]:
                        self.check_logical_path(path, version, logical_paths, logical_directories)
                    if digest not in unnormalized_digests:
                        # Exact string value must match, not just normalized
                        self.error("E050f", version=version, digest=digest)
                    norm_digest = normalized_digest(digest, self.digest_algorithm)
                    digests.append(norm_digest)
            # Check for conflicting logical paths
            for path in logical_directories:
                if path in logical_paths:
                    self.error("E095", version=version, path=path)
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
        """Return regex for validating un-normalized digest format."""
        try:
            return digest_regex(self.digest_algorithm)
        except ValueError:
            if not self.lax_digests:
                self.error('E026a', digest=self.digest_algorithm)
        # Match anything
        return r'''^.*$'''

    def check_logical_path(self, path, version, logical_paths, logical_directories):
        """Check logical path and accumulate paths/directories for E095 check.

        logical_paths and logical_directories are expected to be sets.

        Only adds good paths to the accumulated paths/directories.
        """
        if path.startswith('/') or path.endswith('/'):
            self.error("E053", version=version, path=path)
        else:
            elements = path.split('/')
            for element in elements:
                if element in ['.', '..', '']:
                    self.error("E052", version=version, path=path)
                    return
            # Accumulate paths and directories
            logical_paths.add(path)
            logical_directories.add('/'.join(elements[0:-1]))

    def check_content_path(self, path, content_paths, content_directories):
        """Check logical path and accumulate paths/directories for E101 check.

        Only adds good paths to the accumulated paths/directories.
        """
        if path.startswith('/') or path.endswith('/'):
            self.error("E100", path=path)
        else:
            m = re.match(r'''^(v\d+/''' + self.content_directory + r''')/(.*)''', path)
            if m:
                elements = m.group(2).split('/')
                for element in elements:
                    if element in ('', '.', '..'):
                        self.error("E099", path=path)
                        return
                # Accumulate paths and directories
                content_paths.add(path)
                content_directories.add('/'.join([m.group(1)] + elements[0:-1]))
            else:
                self.error("E042", path=path)

    def validate_as_prior_version(self, prior):
        """Check that prior is a valid InventoryValidator for a prior version of the current inventory object.

        Both inventories are assumed to have been checked for internal consistency.
        """
        # Must have a subset of versions which also check zero padding format etc.
        if not set(prior.all_versions) < set(self.all_versions):
            self.error('E066a', prior_head=prior.head)
        else:
            # Check references to files but realize that there might be different
            # digest algorithms between versions
            version_dir = 'no-version'
            for version_dir in prior.all_versions:
                prior_map = get_file_map(prior.inventory, version_dir)
                self_map = get_file_map(self.inventory, version_dir)
                if prior_map.keys() != self_map.keys():
                    self.error('E066b', version_dir=version_dir, prior_head=prior.head)
                else:
                    # Check them all...
                    for file in prior_map:
                        if prior_map[file] != self_map[file]:
                            self.error('E066c', version_dir=version_dir, prior_head=prior.head, file=file)
            # Check metadata
            prior_version = prior.inventory['versions'][version_dir]
            self_version = self.inventory['versions'][version_dir]
            for key in ('created', 'message', 'user'):
                if prior_version.get(key) != self_version.get(key):
                    self.warning('W011', version_dir=version_dir, prior_head=prior.head, key=key)
