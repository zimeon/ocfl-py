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
        self.id = None
        self.spec_version = None
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
        self.id = None
        self.spec_version = '1.0'  # default to latest published version
        self.digest_algorithm = 'sha512'
        self.content_directory = 'content'
        self.inventory_digest_files = {}  # index by version_dir, algorithms may differ
        self.root_inv_validator = None
        self.obj_fs = None

    def status_str(self, prefix=''):
        """Return string representation of validation log, with optional prefix"""
        return self.log.status_str(prefix=prefix)

    def __str__(self):
        """Return string representation of validation log."""
        return self.status_str()

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
            self.log.error('E003e', path=path)
            return False
        # Object declaration, set spec version number. If there are multiple declarations,
        # look for the lastest object version then report any others as errors
        namastes = find_namastes(0, pyfs=self.obj_fs)
        if len(namastes) == 0:
            self.log.error('E003a', assumed_version=self.spec_version)
        else:
            spec_version = None
            for namaste in namastes:
                # Extract and check spec version number
                this_file_version = None
                for version in ('1.1', '1.0'):
                    if namaste.filename == '0=ocfl_object_' + version:
                        this_file_version = version
                        break
                if this_file_version is None:
                    self.log.error('E006', filename=namaste.filename)
                elif spec_version is None or this_file_version > spec_version:
                    spec_version = this_file_version
                    if not namaste.content_ok(pyfs=self.obj_fs):
                        self.log.error('E007', filename=namaste.filename)
            if spec_version is None:
                self.log.error('E003c', assumed_version=self.spec_version)
            else:
                self.spec_version = spec_version
                if len(namastes) > 1:
                    self.log.error('E003b', files=len(namastes), using_version=self.spec_version)
        # Object root inventory file
        inv_file = 'inventory.json'
        if not self.obj_fs.exists(inv_file):
            self.log.error('E063')
            return False
        try:
            inventory, inv_validator = self.validate_inventory(inv_file)
            inventory_is_valid = self.log.num_errors == 0
            self.root_inv_validator = inv_validator
            all_versions = inv_validator.all_versions
            self.id = inv_validator.id
            self.content_directory = inv_validator.content_directory
            self.digest_algorithm = inv_validator.digest_algorithm
            self.validate_inventory_digest(inv_file, self.digest_algorithm)
            # Object root
            self.validate_object_root(all_versions, already_checked=[namaste.filename for namaste in namastes])
            # Version inventory files
            (prior_manifest_digests, prior_fixity_digests) = self.validate_version_inventories(all_versions)
            if inventory_is_valid:
                # Object content
                self.validate_content(inventory, all_versions, prior_manifest_digests, prior_fixity_digests)
        except ValidatorAbortException:
            pass
        return self.log.num_errors == 0

    def validate_inventory(self, inv_file, where='root', extract_spec_version=False):
        """Validate a given inventory file, record errors with self.log.error().

        Returns inventory object for use in later validation
        of object content. Does not look at anything else in the
        object itself.

        where - used for reporting messages of where inventory is in object

        extract_spec_version - if set True will attempt to take spec_version from the
            inventory itself instead of using the spec_version provided
        """
        try:
            with self.obj_fs.openbin(inv_file, 'r') as fh:
                inventory = json.load(fh)
        except json.decoder.JSONDecodeError as e:
            self.log.error('E033', where=where, explanation=str(e))
            raise ValidatorAbortException
        inv_validator = InventoryValidator(log=self.log, where=where,
                                           lax_digests=self.lax_digests,
                                           spec_version=self.spec_version)
        inv_validator.validate(inventory, extract_spec_version=extract_spec_version)
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

    def validate_object_root(self, version_dirs, already_checked):
        """Validate object root.

        All expected_files must be present and no other files.
        All expected_dirs must be present and no other dirs.
        """
        expected_files = ['0=ocfl_object_' + self.spec_version, 'inventory.json',
                          'inventory.json.' + self.digest_algorithm]
        for entry in self.obj_fs.scandir(''):
            if entry.is_file:
                if entry.name not in expected_files and entry.name not in already_checked:
                    self.log.error('E001a', file=entry.name)
            elif entry.is_dir:
                if entry.name in version_dirs:
                    pass
                elif entry.name == 'extensions':
                    self.validate_extensions_dir()
                elif re.match(r'''v\d+$''', entry.name):
                    # Looks like a version directory so give more specific error
                    self.log.error('E046b', dir=entry.name)
                else:
                    # Simply an unexpected directory
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

        version_dirs is an array of version directory names and is assumed to be in
        version sequence (1, 2, 3...).
        """
        prior_manifest_digests = {}  # file -> algorithm -> digest -> [versions]
        prior_fixity_digests = {}  # file -> algorithm -> digest -> [versions]
        if len(version_dirs) == 0:
            return prior_manifest_digests, prior_fixity_digests
        last_version = version_dirs[-1]
        prev_version_dir = "NONE"  # will be set for first directory with inventory
        prev_spec_version = '1.0'  # lowest version
        for version_dir in version_dirs:
            inv_file = fs.path.join(version_dir, 'inventory.json')
            if not self.obj_fs.exists(inv_file):
                self.log.warning('W010', where=version_dir)
                continue
            # There is an inventory file for this version directory, check it
            if version_dir == last_version:
                # Don't validate in this case. Per the spec the inventory in the last version
                # MUST be identical to the copy in the object root, just check that
                root_inv_file = 'inventory.json'
                if not ocfl_files_identical(self.obj_fs, inv_file, root_inv_file):
                    self.log.error('E064', root_inv_file=root_inv_file, inv_file=inv_file)
                else:
                    # We could also just compare digest files but this gives a more helpful error for
                    # which file has the incorrect digest if they don't match
                    self.validate_inventory_digest(inv_file, self.digest_algorithm, where=version_dir)
                self.inventory_digest_files[version_dir] = 'inventory.json.' + self.digest_algorithm
                this_spec_version = self.spec_version
            else:
                # Note that inventories in prior versions may use different digest algorithms
                # from the current invenotory. Also,
                # an may accord with the same or earlier versions of the specification
                version_inventory, inv_validator = self.validate_inventory(inv_file, where=version_dir, extract_spec_version=True)
                this_spec_version = inv_validator.spec_version
                digest_algorithm = inv_validator.digest_algorithm
                self.validate_inventory_digest(inv_file, digest_algorithm, where=version_dir)
                self.inventory_digest_files[version_dir] = 'inventory.json.' + digest_algorithm
                if self.id and 'id' in version_inventory:
                    if version_inventory['id'] != self.id:
                        self.log.error('E037b', where=version_dir, root_id=self.id, version_id=version_inventory['id'])
                if 'manifest' in version_inventory:
                    # Check that all files listed in prior inventories are in manifest
                    not_seen = set(prior_manifest_digests.keys())
                    for digest in version_inventory['manifest']:
                        for filepath in version_inventory['manifest'][digest]:
                            # We rely on the validation to check that anything present is OK
                            if filepath in not_seen:
                                not_seen.remove(filepath)
                    if len(not_seen) > 0:
                        self.log.error('E023b', where=version_dir, missing_filepaths=', '.join(sorted(not_seen)))
                    # Record all prior digests
                    for unnormalized_digest in version_inventory['manifest']:
                        digest = normalized_digest(unnormalized_digest, digest_type=digest_algorithm)
                        for filepath in version_inventory['manifest'][unnormalized_digest]:
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
                # Fixity blocks are independent in each version. Record all values and the versions
                # they occur in for later checks against content
                if 'fixity' in version_inventory:
                    for digest_algorithm in version_inventory['fixity']:
                        for unnormalized_digest in version_inventory['fixity'][digest_algorithm]:
                            digest = normalized_digest(unnormalized_digest, digest_type=digest_algorithm)
                            for filepath in version_inventory['fixity'][digest_algorithm][unnormalized_digest]:
                                if filepath not in prior_fixity_digests:
                                    prior_fixity_digests[filepath] = {}
                                if digest_algorithm not in prior_fixity_digests[filepath]:
                                    prior_fixity_digests[filepath][digest_algorithm] = {}
                                if digest not in prior_fixity_digests[filepath][digest_algorithm]:
                                    prior_fixity_digests[filepath][digest_algorithm][digest] = []
                                prior_fixity_digests[filepath][digest_algorithm][digest].append(version_dir)
            # We are validating the inventories in sequence and each new version must
            # follow the same or later spec version to previous inventories
            if prev_spec_version > this_spec_version:
                self.log.error('E103', where=version_dir, this_spec_version=this_spec_version,
                               prev_version_dir=prev_version_dir, prev_spec_version=prev_spec_version)
            prev_version_dir = version_dir
            prev_spec_version = this_spec_version
        return prior_manifest_digests, prior_fixity_digests

    def validate_content(self, inventory, version_dirs, prior_manifest_digests, prior_fixity_digests):
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
                self.log.error('E046a', version_dir=version_dir)
        # Extract any digests in fixity and organize by filepath
        fixity_digests = {}
        if 'fixity' in inventory:
            for digest_algorithm in inventory['fixity']:
                for digest in inventory['fixity'][digest_algorithm]:
                    for filepath in inventory['fixity'][digest_algorithm][digest]:
                        if filepath in files_seen:
                            if filepath not in fixity_digests:
                                fixity_digests[filepath] = {}
                            if digest_algorithm not in fixity_digests[filepath]:
                                fixity_digests[filepath][digest_algorithm] = {}
                            if digest not in fixity_digests[filepath][digest_algorithm]:
                                fixity_digests[filepath][digest_algorithm][digest] = ['root']
                        else:
                            self.log.error('E093b', where='root', digest_algorithm=digest_algorithm, digest=digest, content_path=filepath)
        # Check all files in root manifest
        if 'manifest' in inventory:
            for digest in inventory['manifest']:
                for filepath in inventory['manifest'][digest]:
                    if filepath not in files_seen:
                        self.log.error('E092b', where='root', content_path=filepath)
                    else:
                        if self.check_digests:
                            content_digest = file_digest(filepath, digest_type=self.digest_algorithm, pyfs=self.obj_fs)
                            if content_digest != normalized_digest(digest, digest_type=self.digest_algorithm):
                                self.log.error('E092a', where='root', digest_algorithm=self.digest_algorithm, digest=digest, content_path=filepath, content_digest=content_digest)
                            known_digests = {self.digest_algorithm: content_digest}
                            # Are there digest values in the fixity block?
                            self.check_additional_digests(filepath, known_digests, fixity_digests, 'E093a')
                            # Are there other digests for this same file from other inventories?
                            self.check_additional_digests(filepath, known_digests, prior_manifest_digests, 'E092a')
                            self.check_additional_digests(filepath, known_digests, prior_fixity_digests, 'E093a')
                        files_seen.discard(filepath)
        # Anything left in files_seen is not mentioned in the inventory
        if len(files_seen) > 0:
            self.log.error('E023a', where='root', extra_files=', '.join(sorted(files_seen)))

    def check_additional_digests(self, filepath, known_digests, additional_digests, error_code):
        """Check all the additional digests for filepath.

        This method is intended to be used both for manifest digests in prior versions and
        for fixity digests. The digests_seen dict is used to store any values calculated
        so that we don't recalculate digests that might appear multiple times. It is added to
        with any additional values calculated.

        Parameters:
            filepath - path of file in object (`v1/content/something` etc.)
            known_digests - dict of algorithm->digest that we have calculated
            additional_digests - dict: filepath -> algorithm -> digest -> [versions appears in]
            error_code - error code to log on mismatch (E092a for manifest, E093a for fixity)
        """
        if filepath in additional_digests:
            for digest_algorithm in additional_digests[filepath]:
                if digest_algorithm in known_digests:
                    # Don't recompute anything, just use it if we've seen it before
                    content_digest = known_digests[digest_algorithm]
                else:
                    content_digest = file_digest(filepath, digest_type=digest_algorithm, pyfs=self.obj_fs)
                    known_digests[digest_algorithm] = content_digest
                for digest in additional_digests[filepath][digest_algorithm]:
                    if content_digest != normalized_digest(digest, digest_type=digest_algorithm):
                        where = ','.join(additional_digests[filepath][digest_algorithm][digest])
                        self.log.error(error_code, where=where, digest_algorithm=digest_algorithm, digest=digest, content_path=filepath, content_digest=content_digest)

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
