"""OCFL Validator.

Philosophy of this code is to keep it separate from the implementations
of Store, Object and Version used to build and manipulate OCFL data, but
to leverage lower level functions such as digest creation etc.. Code style
is plain/verbose with detailed and specific validation errors that might
help someone debug an implementation.
"""
import json
import os
import os.path
import re
import logging

from .digest import file_digest
from .namaste import find_namastes, NamasteException
from .w3c_datetime import str_to_datetime


class OCFLValidator(object):
    """Class for OCFL Validator."""

    validation_codes = None

    def __init__(self, lang='en'):
        """Initialize OCFL validator."""
        self.lang = lang
        self.codes = {}
        self.errors = 0
        self.warnings = 0
        self.info = 0
        if self.validation_codes is None:
            with open(os.path.join(os.path.dirname(__file__), 'data/validation-errors.json'), 'r') as fh:
                self.validation_codes = json.load(fh)['codes']
        # Object state
        self.digest_algorithm = 'sha512'
        self.content_directory = 'content'

    def error_or_warning(self, code, severity='error', **args):
        """Add error or warning to self.codes."""
        if code in self.validation_codes and 'description' in self.validation_codes[code]:
            desc = self.validation_codes[code]['description']
            lang_desc = None
            if self.lang in desc:
                lang_desc = desc[self.lang]
            elif 'en' in desc:
                lang_desc = desc['en']
            elif len(desc) > 0:
                # first key alphabetically
                lang_desc = desc[sorted(list(desc.keys()))[0]]
            else:
                lang_desc = "Unknown " + severity + ": %s - no description, params (%s)"
            # Add in any parameters
            if 'params' in self.validation_codes[code]:
                params = []
                for param in self.validation_codes[code]['params']:
                    params.append(str(args[param]) if param in args else '???')
                try:
                    lang_desc = lang_desc % tuple(params)
                except TypeError:
                    lang_desc += str(args)
            self.codes[code] = '[' + code + '] ' + lang_desc
        else:
            self.codes[code] = "Unknown " + severity + ": %s - params (%s)" % (code, str(args))

    def error(self, code, **args):
        """Add error code to self.codes."""
        self.error_or_warning(code, severity='error', **args)
        self.errors += 1

    def warn(self, code, **args):
        """Add warning code to self.codes."""
        self.error_or_warning(code, severity='warning', **args)
        self.warnings += 1

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

    def validate(self, path):
        """Validate OCFL object at path."""
        if not os.path.isdir(path):
            self.error('E987', path=path)
            return False
        # Object declaration
        namastes = find_namastes(0, path)
        if len(namastes) == 0:
            self.error('E001')
        elif len(namastes) > 1:
            self.error('E901', files=len(namastes))
        elif not namastes[0].content_ok(path):
            self.error('E003')
        # Inventory
        inv_file = os.path.join(path, 'inventory.json')
        if not os.path.exists(inv_file):
            self.error('E004')
            return False
        inventory, all_versions = self.validate_inventory(inv_file)
        inv_digest_file = os.path.join(path, 'inventory.json.' + self.digest_algorithm)
        if not os.path.exists(inv_digest_file):
            self.error('E005')
        else:
            try:
                self.validate_inventory_digest(inv_file, inv_digest_file)
            except Exception as e:
                self.error('E999', description=str(e))
        # Object root
        self.validate_object_root(path, all_versions)
        # Object content
        self.validate_content(path, inventory)
        return self.errors == 0

    def validate_inventory(self, inv_file):
        """Validate a given inventory file, record errors with self.error().

        Returns inventory object for use in later validation
        of object content. Does not look at anything else in the
        object itself.
        """
        with open(inv_file) as fh:
            inventory = json.load(fh)
        # Basic structure
        if 'id' in inventory:
            iid = inventory['id']
            if type(iid) != str or iid == '':
                self.error("E101")
            elif not re.match(r'''(\w+):.+''', iid):
                self.warn("W007", id=iid)
        else:
            self.error("E100")
        if 'type' not in inventory:
            self.error("E102")
        elif inventory['type'] != 'https://ocfl.io/1.0/spec/#inventory':
            self.error("E103")
        if 'digestAlgorithm' not in inventory:
            self.error("E104")
        elif inventory['digestAlgorithm'] == 'sha512':
            pass
        elif inventory['digestAlgorithm'] == 'sha256':
            self.warn("W006")
            self.digest_algorithm = inventory['digestAlgorithm']
        else:
            self.error("E105", digest_algorithm=inventory['digestAlgorithm'])
        if 'contentDirectory' in inventory:
            self.content_directory = inventory['contentDirectory']
            if re.match(r'''/''', self.content_directory) or self.content_directory in ['.', '..']:
                # See https://github.com/OCFL/spec/issues/415
                self.error("E998")
        if 'manifest' not in inventory:
            self.error("E107")
        else:
            manifest_files = self.validate_manifest(inventory['manifest'])
        if 'versions' not in inventory:
            self.error("E108")
        else:
            all_versions = self.validate_version_sequence(inventory['versions'])
            digests_used = self.validate_versions(inventory['versions'], all_versions, manifest_files)
        if 'head' in inventory:
            if inventory['head'] != all_versions[-1]:
                self.error("E914", got=inventory['head'], expected=all_versions[-1])
        else:
            self.error("E106")
        if 'manifest' in inventory and 'versions' in inventory:
            self.check_digests_present_and_used(inventory['manifest'], digests_used)
        return inventory, all_versions

    def validate_inventory_digest(self, inv_file, inv_digest_file):
        """Validate a given inventory digest for a give inventory file.

        On error throws exception with debugging string intended to
        be presented to a user.
        """
        m = re.match(r'''.*\.(\w+)$''', inv_digest_file)
        if not m:
            raise Exception("Cannot extract digest type from inventory digest file name %s" % (inv_digest_file))
        digest_algorithm = m.group(1)
        digest_recorded = self.read_inventory_digest(inv_digest_file)
        digest_actual = file_digest(inv_file, digest_algorithm)
        if digest_actual != digest_recorded:
            raise Exception("Mismatch between actual and recorded inventory digests for %s (calcuated %s but read %s from %s)" % (inv_file, digest_actual, digest_recorded, inv_digest_file))

    def validate_manifest(self, manifest):
        """Validate manifest block in inventory."""
        # Get regex for checking form of digest
        manifest_files = {}
        for digest in manifest:
            m = re.match(self.digest_regex(), digest)
            if not m:
                self.error('E304', digest=digest)
            else:
                for file in manifest[digest]:
                    manifest_files[file] = digest
                    if not self.is_valid_content_path(file):
                        self.error("E913", path=file)
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
                self.error("E305")
                return
        if zero_padded:
            self.warn("W003")
        # Have v1 and know format, work through to check sequence
        for n in range(2, max_version_num + 1):
            v = (fmt % n)
            if v in versions:
                all_versions.append(v)
            else:
                if len(versions) != (n - 1):
                    self.error("E306")  # Extra version dirs outside sequence
                return(all_versions)
        # n now exceeds the zero padding size, we might either have an object that
        # is correct with its maximum number of versions, or else an error
        if len(versions) != max_version_num:
            self.error("E306")
        return(all_versions)

    def validate_versions(self, versions, all_versions, manifest_files):
        """Validate versions block in inventory."""
        digests_used = []
        for v in all_versions:
            version = versions[v]
            if 'created' not in version or type(versions[v]['created']) != str:
                self.error('E401')  # No created
            else:
                created = versions[v]['created']
                try:
                    dt = str_to_datetime(created)
                    if not re.search(r'''(Z|[+-]\d\d:\d\d)$''', created):  # FIXME - kludge
                        self.warn('W008')
                    if not re.search(r'''T\d\d:\d\d:\d\d''', created):  # FIXME - kludge
                        self.warn('W009')
                except ValueError as e:
                    self.error('E402', description=str(e))
            if 'state' in version:
                digests_used += self.validate_state_block(version['state'])
            else:
                self.error('E402')
            if 'message' not in version:
                self.warn('W001')
            elif type(version['message']) != str:
                self.error('E403')
            if 'user' not in version:
                self.warn('W002')
            else:
                user = version['user']
                if type(user) != dict:
                    self.error('E404')
                else:
                    if 'name' not in user or type(user['name']) != str:
                        self.error('E405')
                    if 'address' not in user:
                        self.warn('W010')
                    elif type(user['address']) != str:
                        self.error('E406')
        return digests_used

    def validate_state_block(self, state):
        """Validate state block in a version in an inventory.

        Returns a list of content digests referenced in the state block.
        """
        digests = []
        if type(state) != dict:
            self.error('E912')
        else:
            digest_regex = self.digest_regex()
            for digest in state:
                if not re.match(self.digest_regex(), digest):
                    self.error('E305', digest=digest)
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
                self.error("E913", description="in state but not in manifest: " + ", ".join(not_in_manifest))
            if len(not_in_state) > 0:
                self.error("E302", description="in manifest but not in state: " + ", ".join(not_in_state))

    def validate_object_root(self, path, version_dirs):
        """Validate object root at path.

        All expected_files must be present and no other files.
        All expected_dirs must be present and no other dirs.
        """
        expected_files = ['0=ocfl_object_1.0', 'inventory.json',
                          'inventory.json.' + self.digest_algorithm]
        for entry in os.listdir(path):
            filepath = os.path.join(path, entry)
            if os.path.isfile(filepath):
                if entry not in expected_files:
                    self.error('E915', file=entry)
            elif os.path.isdir(filepath):
                if entry in version_dirs:
                    pass
                elif entry == 'extensions':
                    self.validate_extensions_dir(path)
                else:
                    self.error('E916', dir=entry)
            else:
                self.error('E917', entry=entry)

    def validate_extensions_dir(self, path):
        """Validate content of extensions directory inside object root at path.

        So far this is just to check that there aren't any entries in the
        extensions directory that aren't directories themselves. Should refine/check
        when https://github.com/OCFL/spec/issues/403 is resolved.
        """
        extpath = os.path.join(path, 'extensions')
        for entry in os.listdir(extpath):
            filepath = os.path.join(extpath, entry)
            if not os.path.isdir(filepath):
                self.error('E918', entry=entry)

    def validate_content(self, path, inventory):
        """Validate file presence and content at path against inventory.

        The inventory is assumed to be valid and safe to use for construction
        of file paths etc..
        """
        files_seen = dict()
        for version in inventory['versions']:
            version_path = os.path.join(path, version)
            if not os.path.isdir(version_path):
                self.error('E301', version_path=version_path)
            else:
                # Check contents of version directory execpt content_directory
                for entry in os.listdir(version_path):
                    if entry == 'inventory.json':
                        pass
                    elif entry == 'inventory.json.' + self.digest_algorithm:
                        pass
                    elif entry == self.content_directory:
                        # Check content_directory
                        content_path = os.path.join(version_path, self.content_directory)
                        for dirpath, dirs, files in os.walk(content_path, topdown=True):
                            for file in files:
                                obj_path = os.path.relpath(os.path.join(dirpath, file), start=path)
                                files_seen[obj_path] = True
                        if len(files_seen) == 0:
                            self.warn("W005")
                    elif os.path.isdir(os.path.join(version_path, entry)):
                        self.warn("W004", entry=entry)
                    else:
                        self.error("E306", entry=entry)
        # Check all files in manifest
        for digest in inventory['manifest']:
            for filepath in inventory['manifest'][digest]:
                if filepath not in files_seen:
                    self.error('E302', content_path=filepath)
                else:
                    # FIXME - check digest
                    files_seen.pop(filepath)
        # Anything left in files_seen is not mentioned in the inventory
        if len(files_seen) > 0:
            self.error('E303', extra_files=', '.join(files_seen.keys()))

    def read_inventory_digest(self, inv_digest_file):
        """Read inventory digest from sidecar file.

        Raise exception if there is an error, else return digest.
        """
        with open(inv_digest_file, 'r') as fh:
            line = fh.readline()
            # we ignore any following lines, could raise exception
        m = re.match(r'''(\w+)\s+(\S+)\s*$''', line)
        if not m:
            raise Exception("Bad inventory digest file %s, wrong format" % (inv_digest_file))
        elif m.group(2) != 'inventory.json':
            raise Exception("Bad inventory name in inventory digest file %s" % (inv_digest_file))
        return m.group(1)

    def __str__(self):
        """String of validator status."""
        s = ''
        for code in sorted(self.codes.keys()):
            s += self.codes[code] + '\n'
        return s
