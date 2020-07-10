"""OCFL Storage Root library."""
import fs
import fs.walk
import hashlib
import json
import os.path
import re
import logging
from shutil import copyfile, copytree
try:
    from urllib.parse import quote_plus  # py3
except ImportError:                      # pragma: no cover -- py2
    from urllib import quote_plus        # pragma: no cover -- py2

from .digest import file_digest
from .disposition import get_dispositor
from .namaste import find_namastes, Namaste
from .object import Object
from .validator import Validator


class StoreWalker(fs.walk.Walker):
    """Walker tailered to an OCFL Storage Root."""

    def check_open_dir(self, pyfs, path, info):
        """Check to see whether directory under the storage root should be descended into.

        The condition to descend is:
        1) Continue from the roor (path==/), or
        2) Continue if there are no files (see https://ocfl.io/1.0/spec/#root-structure)

        Arguments:
            fs (FS): A filesystem instance.
            path (str): Path to directory.
            info (Info): A resource info object for the directory.

        Returns:
            bool: `True` if the directory should be opened.
        """
        if path != '/':
            for file in pyfs.scandir(path):
                if file.is_file:
                    return False
        return True


class StoreException(Exception):
    """Exception class for OCFL Storage Root."""

    pass


class Store(object):
    """Class for handling OCFL Storage Root and include OCFL Objects."""

    def __init__(self, root=None, disposition=None, lax_digests=False):
        """Initialize OCFL Storage Root."""
        self.root = root
        self.disposition = disposition
        self.lax_digests = lax_digests
        self._dispositor = None
        #
        self.declaration_tvalue = 'ocfl_1.0'
        self.spec_file = 'ocfl_1.0.txt'
        self.layout_file = 'ocfl_layout.json'
        #
        self.root_fs = None
        self.num_traversal_errors = 0

    def open_root_fs(self, create=False):
        """Open pyfs filesystem for this OCFL storage root."""
        try:
            self.root_fs = fs.open_fs(self.root, create=create)
        except fs.opener.errors.OpenerError as e:
            raise StoreException("Failed to OCFL storage root filesystem '%s' (%s)" % (self.root, str(e)))

    @property
    def dispositor(self):
        """Instance of dispositor class.

        Lazily initialized.
        """
        if not self._dispositor:
            self._dispositor = get_dispositor(disposition=self.disposition)
        return self._dispositor

    def traversal_error(self, message):
        """Record error traversing OCFL storage root."""
        self.num_traversal_errors += 1
        logging.error(message)

    def object_path(self, identifier):
        """Path to OCFL object with given identifier relative to the OCFL storage root."""
        return self.dispositor.identifier_to_path(identifier)

    def initialize(self):
        """Create and initialize a new OCFL storage root."""
        (parent, root_dir) = fs.path.split(self.root)
        parent_fs = fs.open_fs(parent)
        if parent_fs.exists(root_dir):
            raise StoreException("OCFL storage root %s already exists, aborting!" % (self.root))
        self.root_fs = parent_fs.makedir(root_dir)
        logging.debug("Created OCFL storage root at %s" % (self.root))
        # Create root declaration
        Namaste(d=0, content=self.declaration_tvalue).write(pyfs=self.root_fs)
        # Create a layout declaration
        if self.disposition is not None:
            with self.root_fs.open(self.layout_file, 'w') as fh:
                layout = {'key': self.disposition,
                          'description': "Non-standard layout from ocfl-py disposition -- FIXME"}
                json.dump(layout, fh, sort_keys=True, indent=2)
        logging.info("Created OCFL storage root %s" % (self.root))

    def check_root_structure(self):
        """Check the OCFL storage root structure.

        Assumed that self.root_fs filesystem is available. Raises
        StoreException if there is an error.
        """
        # Storage root declaration
        namastes = find_namastes(0, pyfs=self.root_fs)
        if len(namastes) == 0:
            raise StoreException("Storage root %s lacks required 0= declaration file" % (self.root))
        elif len(namastes) > 1:
            raise StoreException("Storage root %s has more than one 0= style declaration file" % (self.root))
        elif namastes[0].tvalue != self.declaration_tvalue:
            raise StoreException("Storage root %s declaration file not as expected, got %s" % (self.root, namastes[0].filename))
        elif not namastes[0].content_ok(self.root):
            raise StoreException("Storage root %s required declaration file %s has invalid content" % (self.root, namastes[0].filename))
        # Specification file and layout file
        if self.root_fs.exists(self.spec_file) and not self.root_fs.isfile(self.spec_file):
            raise StoreException("Storage root %s includes a specification entry that isn't a file" % (self.root))
        if self.root_fs.exists(self.layout_file):
            self.parse_layout_file()
        # Other files are allowed...
        return True

    def parse_layout_file(self):
        """Read and parse layout file in OCFL storage root.

        Returns key and description on success, otherwise raises a StoreException.
        """
        try:
            with self.root_fs.open(self.layout_file) as fh:
                layout = json.load(fh)
            if type(layout) != dict:
                raise StoreException("Storage root %s has layout file that isn't a JSON object" % (self.root))
            elif 'key' not in layout or 'description' not in layout:
                raise StoreException("Storage root %s has layout file doesn't have required key and description entries" % (self.root))
            return layout['key'], layout['description']
        except Exception as e:  # FIXME - more specific?
            raise StoreException("OCFL storage root %s has layout file that can't be read (%s)" % (self.root, str(e)))

    def object_paths(self):
        """Generator for object paths for every obect in the OCFL storage root.

        Yields (dirpath) that is the path to the directory for each object
        located, relative to the OCFL storage root and without a preceding /.

        Will log any errors seen while traversing the directory tree under the
        storage root.
        """
        walker = StoreWalker()
        for (dirpath, dirs, files) in walker.walk(self.root_fs):
            if dirpath == '/':
                pass  # Ignore files in root
            elif (len(dirs) + len(files)) == 0:
                self.traversal_error("Empty directory %d" % (dirpath))
            elif len(files) == 0:
                pass  # Just an intermediate directory
            else:
                # Is this directory an OCFL object? Look for any 0= file.
                zero_eqs = [file.name for file in files if file.is_file and file.name.startswith('0=')]
                if len(zero_eqs) > 1:
                    self.traversal_error("Multiple 0= declaration files in %s, ignoring" % (dirpath))
                elif len(zero_eqs) == 1:
                    declaration = zero_eqs[0]
                    match = re.match(r'''0=ocfl_object_(\d+\.\d+)''', declaration)
                    if match and match.group(1) == '1.0':
                        yield (dirpath.lstrip('/'))
                    elif match:
                        self.traversal_error("Object with unknown version %s in %s, ignoring" % (match.group(1), dirpath))
                    else:
                        self.traversal_error("Object with unrecognized declaration %s in %s, ignoring" % (declaration, dirpath))
                else:
                    self.traversal_error("Directory %s has file but not object declaration, ignoring" % (dirpath))

    def list(self):
        """List contents of this OCFL storage root."""
        self.open_root_fs()
        self.check_root_structure()
        num_objects = 0
        for dirpath in self.object_paths():
            # Parse inventory to extract id
            id = Object().id_from_inventory(dirpath)
            print("%s -- id=%s" % (os.path.relpath(dirpath, self.root), id))
            num_objects += 1
        # FIXME - do some stuff in here
        logging.info("Found %d OCFL Objects under root %s" % (num_objects, self.root))

    def validate(self, validate_objects=True, show_warnings=False, show_errors=True, check_digests=True):
        """Validate OCFL storage root and optionally all objects."""
        valid = True
        self.open_root_fs()
        try:
            self.check_root_structure()
            logging.info("Storage root structure is VALID")
        except StoreException as e:
            valid = False
            logging.info("Storage root structure is INVALID (%s)" % (str(e)))
        num_objects = 0
        good_objects = 0
        for dirpath in self.object_paths():
            if validate_objects:
                validator = Validator(check_digests=check_digests,
                                      lax_digests=self.lax_digests,
                                      show_warnings=show_warnings)

                if validator.validate(self.root_fs.opendir(dirpath)):
                    good_objects += 1
                else:
                    logging.info("Object at %s in INVALID" % (dirpath))
                messages = validator.__str__(prefix='[[' + dirpath + ']]')  # FIXME - how to show warnings sensibly?
                if messages != '':
                    print(messages)
                num_objects += 1
        if validate_objects:
            if good_objects == num_objects:
                logging.info("Objects checked: %d / %d are VALID" % (good_objects, num_objects))
            else:
                valid = False
                logging.info("Objects checked: %d / %d are INVALID" % (num_objects - good_objects, num_objects))
        else:
            logging.info("Not checking OCFL objects")
        if self.num_traversal_errors > 0:
            valid = False
            logging.info("Encountered %d errors traversing storage root" % (self.num_traversal_errors))
        # FIXME - do some stuff in here
        if valid:
            logging.info("Storage root %s is VALID", self.root)
        else:
            logging.info("Storage root %s is INVALID", self.root)
        return valid

    def add(self, object_path):
        """Add pre-constructed object from object_path."""
        # Sanity check
        o = Object()
        inventory = o.parse_inventory(object_path)
        identifier = inventory['id']
        path = self.object_path(identifier)
        logging.info("Copying from %s to %s" % (object_path, path))
        try:
            copytree(object_path, path)
            logging.info("Copied")
        except Exception as e:
            logging.error("Copy failed: " + str(e))
            raise StoreException("Add object failed!")
