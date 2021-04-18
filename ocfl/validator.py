"""OCFL Validator.

Philosophy of this code is to keep it separate from the implementations
of Store, Object and Version used to build and manipulate OCFL data, but
to leverage lower level functions such as digest creation etc.. Code style
is plain/verbose with detailed and specific validation errors that might
help someone debug an implementation.

This code uses PyFilesystem (import fs) exclusively for access to files. This
should enable application beyond the operating system filesystem.
"""
import json
import re
import fs

from .digest import file_digest, normalized_digest
from .inventory_validator import InventoryValidator
from .namaste import find_namastes
from .pyfs import open_fs, ocfl_walk, ocfl_files_identical
from .validation_logger import ValidationLogger


class ValidatorAbortException(Exception):
    """Exception class to bail out of validation."""


class Validator():
    """Class for OCFL Validator."""

    def __init__(self, log=None, show_warnings=False, show_errors=True, check_digests=True, lax_digests=False, lang='en'):
        """Initialize OCFL validator."""
        self.log = log
        self.check_digests = check_digests
        self.lax_digests = lax_digests
        if self.log is None:
            self.log = ValidationLogger(show_warnings=show_warnings, show_errors=show_errors, lang=lang)
        self.registered_extensions = [
            '0001-digest-algorithms', '0002-flat-direct-storage-layout',
            '0003-hash-and-id-n-tuple-storage-layout', '0004-hashed-n-tuple-storage-layout',
            '0005-mutable-head'
        ]
        # The following actually initialized in initialize() method
        self.digest_algorithm = None
        self.content_directory = None
        self.inventory_digest_files = None
        self.root_inv_validator = None
        self.obj_fs = None
        self.initialize()

    def initialize(self):
        """Initialize object state.

        Must be called between attempts to validate objects.
        """
        self.digest_algorithm = 'sha512'
        self.content_directory = 'content'
        self.inventory_digest_files = {}  # index by version_dir, algorithms may differ
        self.root_inv_validator = None
        self.obj_fs = None

    def __str__(self, prefix=''):
        """Make string representation of validation log."""
        return self.log.__str__(prefix=prefix)

    def validate(self, path):
        """Validate OCFL object at path or pyfs root.

        Returns True if valid (warnings permitted), False otherwise.
        """
        self.initialize()
        try:
            if isinstance(path, str):
                self.obj_fs = open_fs(path)
            else:
                self.obj_fs = path
                path = self.obj_fs.desc('')
        except fs.errors.CreateFailed:
            self.log.error('E003c', path=path)
            return False
        # Object declaration
        namastes = find_namastes(0, pyfs=self.obj_fs)
        if len(namastes) == 0:
            self.log.error('E003a')
        elif len(namastes) > 1:
            self.log.error('E003b', files=len(namastes))
        elif not namastes[0].content_ok(pyfs=self.obj_fs):
            self.log.error('E007')
        # Object root inventory file
        inv_file = 'inventory.json'
        if not self.obj_fs.exists(inv_file):
            self.log.error('E063')
            return False
        try:
            inventory, inv_validator = self.validate_inventory(inv_file)
            self.root_inv_validator = inv_validator
            all_versions = inv_validator.all_versions
            self.content_directory = inv_validator.content_directory
            self.digest_algorithm = inv_validator.digest_algorithm
            self.validate_inventory_digest(inv_file, self.digest_algorithm)
            if self.log.num_errors > 0:
                # Don't look at storage if inventory fails validation
                return False
            # Object root
            self.validate_object_root(all_versions)
            # Version inventory files
            prior_manifest_digests = self.validate_version_inventories(all_versions)
            # Object content
            self.validate_content(inventory, all_versions, prior_manifest_digests)
        except ValidatorAbortException:
            pass
        return self.log.num_errors == 0

    def validate_inventory(self, inv_file, where='root'):
        """Validate a given inventory file, record errors with self.log.error().

        Returns inventory object for use in later validation
        of object content. Does not look at anything else in the
        object itself.
        """
        try:
            with self.obj_fs.openbin(inv_file, 'r') as fh:
                inventory = json.load(fh)
        except json.decoder.JSONDecodeError as e:
            self.log.error('E033', where=where, explanation=str(e))
            raise ValidatorAbortException
        inv_validator = InventoryValidator(log=self.log, where=where,
                                           lax_digests=self.lax_digests)
        inv_validator.validate(inventory)
        return inventory, inv_validator

    def validate_inventory_digest(self, inv_file, digest_algorithm, where="root"):
        """Validate the appropriate inventory digest file in path."""
        inv_digest_file = inv_file + '.' + digest_algorithm
        if not self.obj_fs.exists(inv_digest_file):
            self.log.error('E058a', where=where, path=inv_digest_file)
        else:
            self.validate_inventory_digest_match(inv_file, inv_digest_file)

    def validate_inventory_digest_match(self, inv_file, inv_digest_file):
        """Validate a given inventory digest for a given inventory file.

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
                digest_actual = file_digest(inv_file, digest_algorithm, pyfs=self.obj_fs)
                if digest_actual != digest_recorded:
                    self.log.error("E060", inv_file=inv_file, actual=digest_actual, recorded=digest_recorded, inv_digest_file=inv_digest_file)
            except Exception as e:  # pylint: disable=broad-except
                self.log.error("E061", description=str(e))
        else:
            self.log.error("E058b", inv_digest_file=inv_digest_file)

    def validate_object_root(self, version_dirs):
        """Validate object root.

        All expected_files must be present and no other files.
        All expected_dirs must be present and no other dirs.
        """
        expected_files = ['0=ocfl_object_1.0', 'inventory.json',
                          'inventory.json.' + self.digest_algorithm]
        for entry in self.obj_fs.scandir(''):
            if entry.is_file:
                if entry.name not in expected_files:
                    self.log.error('E001a', file=entry.name)
            elif entry.is_dir:
                if entry.name in version_dirs:
                    pass
                elif entry.name == 'extensions':
                    self.validate_extensions_dir()
                else:
                    self.log.error('E001b', dir=entry.name)
            else:
                self.log.error('E001c', entry=entry.name)

    def validate_extensions_dir(self):
        """Validate content of extensions directory inside object root.

        Validate the extensions directory by checking that there aren't any
        entries in the extensions directory that aren't directories themselves.
        Where there are extension directories they SHOULD be registered and
        this code relies up the registered_extensions property to list known
        extensions.
        """
        for entry in self.obj_fs.scandir('extensions'):
            if entry.is_dir:
                if entry.name not in self.registered_extensions:
                    self.log.warning('W013', entry=entry.name)
            else:
                self.log.error('E067', entry=entry.name)

    def validate_version_inventories(self, version_dirs):
        """Each version SHOULD have an inventory up to that point.

        Also keep a record of any content digests different from those in the root inventory
        so that we can also check them when validating the content.
        """
        prior_manifest_digests = {}  # file -> algorithm -> digest -> [versions]
        if len(version_dirs) == 0:
            return prior_manifest_digests
        last_version = version_dirs[-1]
        for version_dir in version_dirs:
            inv_file = fs.path.join(version_dir, 'inventory.json')
            if not self.obj_fs.exists(inv_file):
                self.log.warning('W010', where=version_dir)
            elif version_dir == last_version:
                # Don't validate in this case. Per the spec the inventory in the last version
                # MUST be identical to the copy in the object root
                root_inv_file = 'inventory.json'
                if not ocfl_files_identical(self.obj_fs, inv_file, root_inv_file):
                    self.log.error('E064', root_inv_file=root_inv_file, inv_file=inv_file)
                else:
                    # We could also just compare digest files but this gives a more helpful error for
                    # which file has the incorrect digest if they don't match
                    self.validate_inventory_digest(inv_file, self.digest_algorithm, where=version_dir)
                self.inventory_digest_files[version_dir] = 'inventory.json.' + self.digest_algorithm
            else:
                # Note that inventories in prior versions may use different digest algorithms
                version_inventory, inv_validator = self.validate_inventory(inv_file, where=version_dir)
                digest_algorithm = inv_validator.digest_algorithm
                self.validate_inventory_digest(inv_file, digest_algorithm, where=version_dir)
                self.inventory_digest_files[version_dir] = 'inventory.json.' + digest_algorithm
                # Record all prior digests
                if 'manifest' in version_inventory:
                    for digest in version_inventory['manifest']:
                        for filepath in version_inventory['manifest'][digest]:
                            if filepath not in prior_manifest_digests:
                                prior_manifest_digests[filepath] = {}
                            if digest_algorithm not in prior_manifest_digests[filepath]:
                                prior_manifest_digests[filepath][digest_algorithm] = {}
                            if digest not in prior_manifest_digests[filepath][digest_algorithm]:
                                prior_manifest_digests[filepath][digest_algorithm][digest] = []
                            prior_manifest_digests[filepath][digest_algorithm][digest].append(version_dir)
                # Is this inventory an appropriate prior version of the object root inventory?
                if self.root_inv_validator is not None:
                    self.root_inv_validator.validate_as_prior_version(inv_validator)
        return prior_manifest_digests

    def validate_content(self, inventory, version_dirs, prior_manifest_digests):
        """Validate file presence and content against inventory.

        The root inventory in `inventory` is assumed to be valid and safe to use
        for construction of file paths etc..
        """
        files_seen = set()
        # Check files in each version directory
        for version_dir in version_dirs:
            try:
                # Check contents of version directory except content_directory
                for entry in self.obj_fs.listdir(version_dir):
                    if ((entry == 'inventory.json')
                            or (version_dir in self.inventory_digest_files and entry == self.inventory_digest_files[version_dir])):
                        pass
                    elif entry == self.content_directory:
                        # Check content_directory
                        content_path = fs.path.join(version_dir, self.content_directory)
                        num_content_files_in_version = 0
                        for dirpath, dirs, files in ocfl_walk(self.obj_fs, content_path):
                            if dirpath != '/' + content_path and (len(dirs) + len(files)) == 0:
                                self.log.error("E024", where=version_dir, path=dirpath)
                            for file in files:
                                files_seen.add(fs.path.join(dirpath, file).lstrip('/'))
                                num_content_files_in_version += 1
                        if num_content_files_in_version == 0:
                            self.log.warning("W003", where=version_dir)
                    elif self.obj_fs.isdir(fs.path.join(version_dir, entry)):
                        self.log.warning("W002", where=version_dir, entry=entry)
                    else:
                        self.log.error("E015", where=version_dir, entry=entry)
            except (fs.errors.ResourceNotFound, fs.errors.DirectoryExpected):
                self.log.error('E046', version_dir=version_dir)
        # Check all files in root manifest
        if 'manifest' in inventory:
            for digest in inventory['manifest']:
                for filepath in inventory['manifest'][digest]:
                    if filepath not in files_seen:
                        self.log.error('E023a', where='root', content_path=filepath)
                    else:
                        if self.check_digests:
                            content_digest = file_digest(filepath, digest_type=self.digest_algorithm, pyfs=self.obj_fs)
                            if content_digest != normalized_digest(digest, digest_type=self.digest_algorithm):
                                self.log.error('E092', where='root', digest=digest, content_path=filepath, content_digest=content_digest)
                            # Are there other digests for this same file from other inventories?
                            # If so then check those also
                            if filepath in prior_manifest_digests:
                                for digest_algorithm in prior_manifest_digests[filepath]:
                                    for other_digest in prior_manifest_digests[filepath][digest_algorithm]:
                                        content_digest = file_digest(filepath, digest_type=digest_algorithm, pyfs=self.obj_fs)
                                        if content_digest != normalized_digest(other_digest, digest_type=digest_algorithm):
                                            where = ','.join(prior_manifest_digests[filepath][digest_algorithm][other_digest])
                                            self.log.error('E092', where=where, digest=other_digest, content_path=filepath, content_digest=content_digest)
                            # FIXME - Also other fixity blocks
                        files_seen.discard(filepath)
        # Check any additional digests in root fixity block
        if 'fixity' in inventory and self.check_digests:
            for digest_algorithm in inventory['fixity']:
                for digest in inventory['fixity'][digest_algorithm]:
                    if digest != self.digest_algorithm:  # don't recheck things we check from manifest
                        for filepath in inventory['fixity'][digest_algorithm][digest]:
                            content_digest = file_digest(filepath, digest_type=digest_algorithm, pyfs=self.obj_fs)
                            if content_digest != normalized_digest(digest, digest_type=digest_algorithm):
                                self.log.error('E093', where='root', digest_algorith=digest_algorithm, digest=digest, content_path=filepath, content_digest=content_digest)
        # Anything left in files_seen is not mentioned in the inventory
        if len(files_seen) > 0:
            self.log.error('E023b', where='root', extra_files=', '.join(sorted(files_seen)))

    def read_inventory_digest(self, inv_digest_file):
        """Read inventory digest from sidecar file.

        Raise exception if there is an error, else return digest.
        """
        with self.obj_fs.open(inv_digest_file, 'r') as fh:
            line = fh.readline()
            # we ignore any following lines, could raise exception
        m = re.match(r'''(\w+)\s+(\S+)\s*$''', line)
        if not m:
            raise Exception("Bad inventory digest file %s, wrong format" % (inv_digest_file))
        if m.group(2) != 'inventory.json':
            raise Exception("Bad inventory name in inventory digest file %s" % (inv_digest_file))
        return m.group(1)
