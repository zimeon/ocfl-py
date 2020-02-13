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

from .digest import file_digest
from .inventory_validator import InventoryValidator
from .namaste import find_namastes, NamasteException
from .validation_logger import ValidationLogger
from .w3c_datetime import str_to_datetime


class OCFLValidator(object):
    """Class for OCFL Validator."""

    def __init__(self, log=None, lang='en'):
        """Initialize OCFL validator."""
        self.log = log
        if self.log is None:
            self.log = ValidationLogger(lang)
        # Object state
        self.digest_algorithm = 'sha512'
        self.content_directory = 'content'

    def __str__(self):
        """String representation."""
        return str(self.log)

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
        self.log.error_or_warning(code, severity='error', **args)
        self.log.errors += 1

    def warn(self, code, **args):
        """Add warning code to self.codes."""
        self.log.error_or_warning(code, severity='warning', **args)
        self.log.warnings += 1

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
            self.log.error('E987', path=path)
            return False
        # Object declaration
        namastes = find_namastes(0, path)
        if len(namastes) == 0:
            self.log.error('E001')
        elif len(namastes) > 1:
            self.log.error('E901', files=len(namastes))
        elif not namastes[0].content_ok(path):
            self.log.error('E003')
        # Object root inventory file
        inv_file = os.path.join(path, 'inventory.json')
        if not os.path.exists(inv_file):
            self.log.error('E004')
            return False
        inventory, all_versions = self.validate_inventory(inv_file)
        inv_digest_file = os.path.join(path, 'inventory.json.' + self.digest_algorithm)
        if not os.path.exists(inv_digest_file):
            self.log.error('E005')
        else:
            try:
                self.validate_inventory_digest(inv_file, inv_digest_file)
            except Exception as e:
                self.log.error('E999', description=str(e))
        # Object root
        self.validate_object_root(path, all_versions)
        # Object content
        self.validate_content(path, inventory)
        return self.log.errors == 0

    def validate_inventory(self, inv_file):
        """Validate a given inventory file, record errors with self.log.error().

        Returns inventory object for use in later validation
        of object content. Does not look at anything else in the
        object itself.
        """
        with open(inv_file) as fh:
            inventory = json.load(fh)
        inv_validator = InventoryValidator(log=self.log)
        inv_validator.validate(inventory)
        self.content_directory = inv_validator.content_directory
        self.digest_algorithm = inv_validator.digest_algorithm
        return inventory, inv_validator.all_versions

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
                    self.log.error('E915', file=entry)
            elif os.path.isdir(filepath):
                if entry in version_dirs:
                    pass
                elif entry == 'extensions':
                    self.validate_extensions_dir(path)
                else:
                    self.log.error('E916', dir=entry)
            else:
                self.log.error('E917', entry=entry)

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
                self.log.error('E918', entry=entry)

    def validate_content(self, path, inventory):
        """Validate file presence and content at path against inventory.

        The inventory is assumed to be valid and safe to use for construction
        of file paths etc..
        """
        files_seen = dict()
        for version in inventory['versions']:
            version_path = os.path.join(path, version)
            if not os.path.isdir(version_path):
                self.log.error('E301', version_path=version_path)
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
                            self.log.warn("W005")
                    elif os.path.isdir(os.path.join(version_path, entry)):
                        self.log.warn("W004", entry=entry)
                    else:
                        self.log.error("E306", entry=entry)
        # Check all files in manifest
        for digest in inventory['manifest']:
            for filepath in inventory['manifest'][digest]:
                if filepath not in files_seen:
                    print(str(files_seen))
                    self.log.error('E302', content_path=filepath)
                else:
                    # FIXME - check digest
                    files_seen.pop(filepath)
        # Anything left in files_seen is not mentioned in the inventory
        if len(files_seen) > 0:
            self.log.error('E303', extra_files=', '.join(files_seen.keys()))

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
