"""OCFL Storage Root library.

This code uses PyFilesystem (import fs) exclusively for access to files. This
should enable application beyond the operating system filesystem.
"""
import json
import logging
import re

import fs
from fs.copy import copy_dir

from .constants import DEFAULT_SPEC_VERSION, SPEC_VERSIONS_SUPPORTED
from .namaste import find_namastes, Namaste
from .object import Object
from .pyfs import pyfs_openfs, pyfs_walk, pyfs_opendir
from .validator import Validator
from .validation_logger import ValidationLogger

# Specific layouts
from .layout_0002_flat_direct import Layout_0002_Flat_Direct
from .layout_0003_hash_and_id_n_tuple import Layout_0003_Hash_And_Id_N_Tuple
from .layout_nnnn_flat_quoted import Layout_NNNN_Flat_Quoted
from .layout_nnnn_tuple_tree import Layout_NNNN_Tuple_Tree
from .layout_nnnn_uuid_quadtree import Layout_NNNN_UUID_Quadtree


def _get_layout(layout_name=None):
    """Find Layout object for the given layout name.

    Returns a layout object for the appropriate layour if the layour_name
    is recognized, otherwise throws a StorageRootException.
    """
    if layout_name in ("0002-flat-direct-storage-layout", "0002", "flat-direct"):
        return Layout_0002_Flat_Direct()
    if layout_name in ("0003-hash-and-id-n-tuple-storage-layout", "0003"):
        return Layout_0003_Hash_And_Id_N_Tuple()
    if layout_name in ("nnnn-flat-quoted-storage-layout", "flat-quoted"):
        return Layout_NNNN_Flat_Quoted()
    if layout_name == "nnnn-tuple-tree":
        return Layout_NNNN_Tuple_Tree()
    if layout_name == "nnnn-uuid-quadtree":
        return Layout_NNNN_UUID_Quadtree()
    raise StorageRootException("Unsupported layout_name %s, aborting!" % (layout_name))


class StorageRootException(Exception):
    """Exception class for OCFL Storage Root."""


class StorageRoot():
    """Class for handling OCFL Storage Root and include OCFL Objects."""

    def __init__(self, root=None, layout_name=None, lax_digests=False,
                 spec_version=None):
        """Initialize OCFL Storage Root."""
        self.root = root
        self.layout_name = layout_name
        self.layout_description = None
        self.lax_digests = lax_digests
        self._layout = None  # Lazily initialized in layout property
        self.spec_version = None
        if spec_version is not None:
            self.check_spec_version(spec_version)
        self.layout_file = "ocfl_layout.json"
        self.registered_extensions = [
            "0002-flat-direct-storage-layout",
            "0003-hash-and-id-n-tuple-storage-layout"
        ]
        self.supported_layouts = [
            "0002-flat-direct-storage-layout",
            "0003-hash-and-id-n-tuple-storage-layout",
            "nnnn-flat-quoted-storage-layout",
            "nnnn-tuple-tree",
            "nnnn-uuid-quadtree"
        ]
        #
        self.root_fs = None
        # Validation records
        self.num_traversal_errors = 0
        self.log = None
        self.num_objects = 0
        self.good_objects = 0
        self.errors = None
        self.structure_error = None
        self.traversal_errors = None

    def check_spec_version(self, spec_version, default=DEFAULT_SPEC_VERSION):
        """Check the OCFL specification version is supported."""
        if spec_version is None and self.spec_version is None:
            spec_version = default
        if spec_version not in SPEC_VERSIONS_SUPPORTED:
            raise StorageRootException("Unsupported OCFL specification version %s requested" % (spec_version))
        self.spec_version = spec_version

    def open_root_fs(self, create=False):
        """Open pyfs filesystem for this OCFL storage root."""
        try:
            self.root_fs = pyfs_openfs(self.root, create=create)
        except (fs.opener.errors.OpenerError, fs.errors.CreateFailed) as e:
            raise StorageRootException("Failed to open OCFL storage root filesystem '%s' (%s)" % (self.root, str(e)))

    def root_declaration_object(self):
        """NAMASTE object declaration Namaste object."""
        return Namaste(0, "ocfl_" + self.spec_version)

    def write_root_declaration(self, root_fs):
        """Write NAMASTE object declaration.

        Assumes self.obj_fs is open for this object.
        """
        self.root_declaration_object().write(pyfs=root_fs)

    @property
    def layout(self):
        """Instance of layout class.

        Lazily initialized. Will return either a valid layout name or None
        if the layout is not set.
        """
        if not self._layout and self.layout_name is not None:
            self._layout = _get_layout(layout_name=self.layout_name)
        return self._layout

    def traversal_error(self, code, **kwargs):
        """Record error traversing OCFL storage root."""
        self.num_traversal_errors += 1
        if self.log is None:  # FIXME - What to do in non-validator context?
            args = ", ".join("{0}={1!r}".format(k, v) for k, v in kwargs.items())
            logging.error("Traversal error %s - %s", code, args)
        else:
            self.log.error(code, **kwargs)

    def object_path(self, identifier):
        """Path to OCFL object with given identifier relative to the OCFL storage root."""
        if self.layout is None:
            self.open_root_fs()
            self.check_root_structure()
        return self.layout.identifier_to_path(identifier)

    def initialize(self, spec_version=None, layout_params=None):
        """Create and initialize a new OCFL storage root."""
        # Do the checks we can before we do anything on storage
        if self.layout is not None and layout_params is not None:
            # Parse as JSON
            try:
                config = json.loads(layout_params)
            except Exception as e:
                raise StorageRootException("Bad layout params supplied: %s" % (str(e)))
            self.layout.check_and_set_layout_params(config=config, require_extension_name=False)
        self.check_spec_version(spec_version=spec_version)
        # Now create the storage root
        (parent, root_dir) = fs.path.split(self.root)
        parent_fs = pyfs_openfs(parent)
        if parent_fs.exists(root_dir):
            raise StorageRootException("OCFL storage root %s already exists, aborting!" % (self.root))
        self.root_fs = parent_fs.makedir(root_dir)
        logging.debug("Created OCFL storage root directory at %s", self.root)
        # Create root declaration
        self.write_root_declaration(self.root_fs)
        # Create a layout declaration if the layout ise set, it is valid to have
        # a storage root with no layout information
        if self.layout is not None:
            with self.root_fs.open(self.layout_file, "w") as fh:
                layout = {"extension": self.layout.NAME,
                          "description": self.layout.DESCRIPTION}
                json.dump(layout, fh, sort_keys=True, indent=2)
            # Do we need to qrite a extension description?
            self.layout.write_layout_params(root_fs=self.root_fs)
        else:
            logging.debug("No layout set so no %s file written", self.layout_file)

    def check_root_structure(self):
        """Check the OCFL storage root structure.

        Assumed that self.root_fs filesystem is available. Raises
        StorageRootException if there is an error.
        """
        # Storage root declaration
        namastes = find_namastes(0, pyfs=self.root_fs)
        if len(namastes) == 0:
            raise StorageRootException("E069a Storage root %s lacks required 0= declaration file" % (self.root))
        if len(namastes) > 1:
            raise StorageRootException("E069b Storage root %s has more than one 0= style declaration file" % (self.root))
        spec_version = None
        for version in SPEC_VERSIONS_SUPPORTED:
            if namastes[0].filename == "0=ocfl_" + version:
                spec_version = version
                break
        else:
            raise StorageRootException("E069c Storage root %s has unrecognized 0= declaration file %s" % (self.root, namastes[0].filename))
        if self.spec_version is not None and self.spec_version != spec_version:
            raise StorageRootException("E069d Storage root %s 0= declaration is for spec version %s, not %s as expected" % (self.root, spec_version, self.spec_version))
        if not namastes[0].content_ok(pyfs=self.root_fs):
            raise StorageRootException("E069e Storage root %s required declaration file %s has invalid content" % (self.root, namastes[0].filename))
        # Layout file (if present)
        if self.root_fs.exists(self.layout_file):
            self.layout_name, self.layout_description = self.parse_layout_file()
            try:
                if self.layout.NAME == self.layout_name:
                    logging.info("Storage root layout is %s", self.layout_name)
                else:
                    logging.warning("Non-canonical layout name %s, should be %s", self.layout_name, self.layout.NAME)
            except StorageRootException as e:
                raise StorageRootException("Storage root %s includes ocfl_layout.json with unknown layout %s (%s)" % (self.root, self.layout_name, str(e)))
            # Is there a corresponding extensions dir with params in config.json?
            self.layout.read_layout_params(root_fs=self.root_fs)
        # Other files are allowed...
        return True

    def parse_layout_file(self):
        """Read and parse layout file in OCFL storage root.

        Returns:
          - (extension, description) strings on success,
          - otherwise raises a StorageRootException.
        """
        try:
            with self.root_fs.open(self.layout_file) as fh:
                layout = json.load(fh)
        except Exception as e:
            raise StorageRootException("OCFL storage root %s has layout file that cant be read/parsed (%s)" % (self.root, str(e)))
        if not isinstance(layout, dict):
            raise StorageRootException("Storage root %s has layout file that isn't a JSON object" % (self.root))
        if ("extension" not in layout or not isinstance(layout["extension"], str)
                or "description" not in layout or not isinstance(layout["description"], str)):
            raise StorageRootException("Storage root %s has layout file doesn't have required extension and description string entries" % (self.root))
        return layout["extension"], layout["description"]

    def object_paths(self):
        """Generate object paths for every obect in the OCFL storage root.

        Yields (dirpath) that is the path to the directory for each object
        located, relative to the OCFL storage root and without a preceding /.

        Will log any errors seen while traversing the directory tree under the
        storage root.
        """
        for (dirpath, dirs, files) in pyfs_walk(self.root_fs, is_storage_root=True):
            if dirpath == "/":
                if "extensions" in dirs:
                    self.validate_extensions_dir()
                    dirs.remove("extensions")
                # Ignore any other files in storage root
            elif (len(dirs) + len(files)) == 0:
                self.traversal_error("E073", path=dirpath)
            elif len(files) == 0:
                pass  # Just an intermediate directory
            else:
                # Is this directory an OCFL object? Look for any 0= file.
                zero_eqs = [file for file in files if file.startswith("0=")]
                if len(zero_eqs) > 1:
                    self.traversal_error("E003d", path=dirpath)
                elif len(zero_eqs) == 1:
                    declaration = zero_eqs[0]
                    match = re.match(r"""0=ocfl_object_(\d+\.\d+)""", declaration)
                    if match and match.group(1) in SPEC_VERSIONS_SUPPORTED:
                        yield dirpath.lstrip("/")
                    elif match:
                        self.traversal_error("E004a", path=dirpath, version=match.group(1))
                    else:
                        self.traversal_error("E004b", path=dirpath, declaration=declaration)
                else:
                    self.traversal_error("E072", path=dirpath)

    def validate_extensions_dir(self):
        """Validate content of extensions directory inside storage root.

        Validate the extensions directory by checking that there aren't any
        entries in the extensions directory that aren't directories themselves.
        Where there are extension directories they SHOULD be registered and
        this code relies up the registered_extensions property to list known
        storage root extensions.
        """
        for entry in self.root_fs.scandir("extensions"):
            if entry.is_dir:
                if entry.name not in self.registered_extensions:
                    self.log.warning("W901", entry=entry.name)  # FIXME - No good warning code in spec
            else:
                self.traversal_error("E086", entry=entry.name)

    def list_objects(self):
        """List contents of this OCFL storage root.

        Generator that yields tuple for each object, which contain
        (dirpath, identifier)

        Side effects: The count of num_objects is updated through the taversal
        of the storage root and is available afterwards.
        """
        self.open_root_fs()
        self.check_root_structure()
        self.num_objects = 0
        for dirpath in self.object_paths():
            with pyfs_opendir(pyfs=self.root_fs, dir=dirpath) as obj_fs:
                # Parse inventory to extract id
                identifier = Object(obj_fs=obj_fs).id_from_inventory()
                self.num_objects += 1
                yield (dirpath, identifier)
                # FIXME - maybe do some more stuff in here

    def validate_hierarchy(self, validate_objects=True, check_digests=True,
                           log_warnings=False, max_errors=100):
        """Validate storage root hierarchy and, optionally, all objects.

        Returns:
            num_objects - number of objects checked
            good_objects - number of objects checked that were found to be valid
            errors - list of [dirpath, message] pairs for up to max_errors errors
        """
        num_objects = 0
        good_objects = 0
        errors = []
        for dirpath in self.object_paths():
            if validate_objects:
                validator = Validator(check_digests=check_digests,
                                      lax_digests=self.lax_digests,
                                      log_warnings=log_warnings)
                # FIXME - Should check that all objest are not higher spec
                # version that storage root https://ocfl.io/1.1/spec/#E081
                if validator.validate_object(pyfs_opendir(pyfs=self.root_fs, dir=dirpath)):
                    good_objects += 1
                else:
                    logging.debug("Object at %s in INVALID", dirpath)
                if len(errors) < max_errors:
                    # Record detail of errors (and warnings if log_warnings)
                    messages = validator.status_str(prefix="[[" + dirpath + "]]")
                    if messages != "":
                        errors.append([dirpath, messages])
                num_objects += 1
        return num_objects, good_objects, errors

    def validate(self, *, validate_objects=True, check_digests=True,
                 log_warnings=False, log_errors=True, max_errors=100,
                 lang="en"):
        """Validate OCFL storage root, structure, and optionally all objects.

        Arguments:
           validate_objects (bool): True (default) to validate each object on
               the storage root, otherwise will not validate the objects
           check_digests (bool): True (default) to check the digests of each
               file while validating objects
           log_warnings (bool): True if warnings should be logged, default False
           log_errors (bool): True (default) if errors should be logged
           max_errors (int): Number of errors and warnings to log, default
               is 100
           lang (str): Language of error and warning descriptions to look for,
               default is "en"

        Returns True if everything checked is valid, False otherwise.

        Side effects:
            self.num_objects - number of objects examined
            self.good_objects - number of valid objects
            self.errors - list of [dirpath, message] pairs for up to max_errors errors
            self.structure_error - Error in storage root structure
            self.log - ValidationLogger object with any traversal errors
        """
        valid = True
        self.structure_error = None
        self.log = ValidationLogger(log_warnings=log_warnings, log_errors=log_errors, lang=lang)
        self.open_root_fs()
        try:
            self.check_root_structure()
        except StorageRootException as e:
            valid = False
            self.structure_error = str(e)
            logging.debug("Storage root structure is INVALID (%s)", str(e))
        self.log.spec_version = self.spec_version
        self.num_objects, self.good_objects, self.errors = self.validate_hierarchy(validate_objects=validate_objects, check_digests=check_digests, log_warnings=log_warnings, max_errors=max_errors)
        if self.num_traversal_errors > 0:
            valid = False
        return valid

    def add(self, object_path):
        """Add pre-constructed object from object_path.

        The identifier is extracted from the object and the path is determined
        by the storage layouts

        Return the (identifier, path) on success, raises a StorageException on
        failure.
        """
        self.open_root_fs()
        self.check_root_structure()
        # Sanity check
        o = Object(path=object_path)
        inventory = o.parse_inventory()
        identifier = inventory.id
        # Now copy
        path = self.object_path(identifier)
        if self.root_fs.exists(path):
            raise StorageRootException("Add object failed because path %s exists" % (path))
        logging.debug("Copying from %s to %s", object_path, fs.path.join(self.root, path))
        try:
            copy_dir(o.obj_fs, "/", self.root_fs, path)
        except Exception as e:
            raise StorageRootException("Add object at path %s failed! (%s)" % (path, str(e)))
        return (identifier, path)
