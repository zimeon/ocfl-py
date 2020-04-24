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

    def __init__(self, log=None, warnings=False, check_digests=True, lax_digests=False, lang='en'):
        """Initialize OCFL validator."""
        self.log = log
        self.warnings = warnings
        self.check_digests = check_digests
        self.lax_digests = lax_digests
        if self.log is None:
            self.log = ValidationLogger(warnings=warnings, lang=lang)
        self.registered_extensions = ['FIXME']  # FIXME - add names when something registered
        # Object state
        self.digest_algorithm = 'sha512'
        self.content_directory = 'content'
        self.inventory_digest_files = {}  # index by version_dir, algorithms may differ
        self.root_inv_validator = None

    def __str__(self):
        """String representation."""
        return str(self.log)

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
        inventory, inv_validator = self.validate_inventory(inv_file)
        self.root_inv_validator = inv_validator
        all_versions = inv_validator.all_versions
        self.content_directory = inv_validator.content_directory
        self.digest_algorithm = inv_validator.digest_algorithm
        self.validate_inventory_digest(inv_file, self.digest_algorithm)
        # Object root
        self.validate_object_root(path, all_versions)
        # Version inventory files
        self.validate_version_inventories(path, inventory, all_versions)
        # Object content
        self.validate_content(path, inventory, all_versions)
        return self.log.num_errors == 0

    def validate_inventory(self, inv_file, where='root'):
        """Validate a given inventory file, record errors with self.log.error().

        Returns inventory object for use in later validation
        of object content. Does not look at anything else in the
        object itself.
        """
        with open(inv_file) as fh:
            inventory = json.load(fh)
        inv_validator = InventoryValidator(log=self.log, where=where,
                                           lax_digests=self.lax_digests)
        inv_validator.validate(inventory)
        return inventory, inv_validator

    def validate_inventory_digest(self, inv_file, digest_algorithm, where="root"):
        """Validate the appropriate inventory digest file in path."""
        inv_digest_file = inv_file + '.' + digest_algorithm
        if not os.path.exists(inv_digest_file):
            self.log.error('E005', where=where, path=inv_digest_file)
        else:
            self.validate_inventory_digest_match(inv_file, inv_digest_file)

    def validate_inventory_digest_match(self, inv_file, inv_digest_file):
        """Validate a given inventory digest for a give inventory file.

        On error throws exception with debugging string intended to
        be presented to a user.
        """
        if not self.check_digests:
            return
        m = re.match(r'''.*\.(\w+)$''', inv_digest_file)
        if m:
            digest_algorithm = m.group(1)
            try:
                digest_recorded = self.read_inventory_digest(inv_digest_file)
                digest_actual = file_digest(inv_file, digest_algorithm)
                if digest_actual != digest_recorded:
                    self.log.error("E006", inv_file=inv_file, actual=digest_actual, recorded=digest_recorded, inv_digest_file=inv_digest_file)
            except Exception as e:
                self.log.error("E008", description=str(e))
        else:
            self.log.error("E007", inv_digest_file=inv_digest_file)

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
            if os.path.isdir(filepath):
                if entry not in self.registered_extensions:
                    self.log.warn('W013', entry=entry)
            else:
                self.log.error('E067', entry=entry)

    def validate_version_inventories(self, path, inventory, version_dirs):
        """Each version SHOULD have an inventory up to that point."""
        inv_digest_files = {}  # index by version_dir
        last_version = version_dirs[-1]
        for version_dir in version_dirs:
            version_path = os.path.join(path, version_dir)
            inv_file = os.path.join(version_path, 'inventory.json')
            if not os.path.exists(inv_file):
                self.log.warn('W010', where=version_dir)
            elif version_dir == last_version:
                # Don't validate in this case. Per the spec the inventory in the last version
                # MUST be identical to the copy in the object root
                root_inv_file = os.path.join(path, 'inventory.json')
                # FIXME -- how to diff efficiently?
                with open(inv_file, 'r') as ifh:
                    inv = ifh.read()
                with open(root_inv_file, 'r') as rifh:
                    root_inv = rifh.read()
                if inv != root_inv:
                    self.log.error('E099', root_inv_file=root_inv_file, inv_file=inv_file)
                else:
                    # FIXME - could just compare digest files...
                    self.validate_inventory_digest(inv_file, self.digest_algorithm, where=version_dir)
                self.inventory_digest_files[version_dir] = 'inventory.json.' + self.digest_algorithm
            else:
                # Note that inventories in prior versions may use different digest algorithms
                version_inventory, inv_validator = self.validate_inventory(inv_file, where=version_dir)
                self.validate_inventory_digest(inv_file, inv_validator.digest_algorithm, where=version_dir)
                self.inventory_digest_files[version_dir] = 'inventory.json.' + inv_validator.digest_algorithm
                # Is this inventory an appropriate prior version of the object root inventory?
                if self.root_inv_validator is not None:
                    self.root_inv_validator.validate_as_prior_version(inv_validator)

    def validate_content(self, path, inventory, version_dirs):
        """Validate file presence and content at path against inventory.

        The inventory is assumed to be valid and safe to use for construction
        of file paths etc..
        """
        files_seen = set()
        # Check on disk in each version directory
        for version_dir in version_dirs:
            version_path = os.path.join(path, version_dir)
            if not os.path.isdir(version_path):
                self.log.error('E301', version_path=version_path)
            else:
                # Check contents of version directory execpt content_directory
                for entry in os.listdir(version_path):
                    if ((entry == 'inventory.json')
                            or (version_dir in self.inventory_digest_files and entry == self.inventory_digest_files[version_dir])):
                        pass
                    elif entry == self.content_directory:
                        # Check content_directory
                        content_path = os.path.join(version_path, self.content_directory)
                        num_content_files_in_version = 0
                        for dirpath, dirs, files in os.walk(content_path, topdown=True):
                            for file in files:
                                obj_path = os.path.relpath(os.path.join(dirpath, file), start=path)
                                files_seen.add(obj_path)
                                num_content_files_in_version += 1
                        if num_content_files_in_version == 0:
                            self.log.warn("W003", where=version_dir)
                    elif os.path.isdir(os.path.join(version_path, entry)):
                        self.log.warn("W002", where=version_dir, entry=entry)
                    else:
                        self.log.error("E306", where=version_dir, entry=entry)
        # Check all files in root manifest
        for digest in inventory['manifest']:
            for filepath in inventory['manifest'][digest]:
                if filepath not in files_seen:
                    self.log.error('E302', where='root', content_path=filepath)
                else:
                    # FIXME - check digest
                    files_seen.discard(filepath)
        # Anything left in files_seen is not mentioned in the inventory
        if len(files_seen) > 0:
            self.log.error('E303', where='root', extra_files=', '.join(sorted(files_seen)))

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
