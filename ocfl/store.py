"""OCFL Object Store library."""
import hashlib
import json
import os
import os.path
import re
import logging
from shutil import copyfile, copytree
try:
    from urllib.parse import quote_plus  # py3
except:                                  # pragma: no cover -- py2
    from urllib import quote_plus        # pragma: no cover -- py2

from .digest import file_digest
from .disposition import get_dispositor
from .object import Object


class StoreException(Exception):
    """Exception class for OCFL Store."""

    pass


class Store(object):
    """Class for handling OCFL Object Stores."""

    def __init__(self, root=None, disposition=None):
        """Initialize OCFL Object Store."""
        self.root = root
        self.disposition = disposition
        self._dispositor = None

    @property
    def declaration_file(self):
        """Path of storage root declaration file."""
        return os.path.join(self.root, '0=ocfl_1.0')

    @property
    def disposition_file(self):
        """Path of storage root disposition file."""
        return os.path.join(self.root, '1=' + quote_plus(self.disposition))

    @property
    def dispositor(self):
        """Instance of dispositor class.

        Lazily initialized.
        """
        if not self._dispositor:
            self._dispositor = get_dispositor(disposition=self.disposition)
        return self._dispositor

    def object_path(self, identifier):
        """Path to OCFL object with given identifier."""
        return os.path.join(self.root, self.dispositor.identifier_to_path(identifier))

    def initialize(self):
        """Initialize an object store."""
        if os.path.exists(self.root):
            raise StoreException("OCFL Object Store root %s already exists, aborting!" % (self.root))
        os.makedirs(self.root)
        logging.debug("Created root directory %s" % (self.root))
        # Create root declaration
        with open(self.declaration_file, 'w') as fh:
            fh.close()
        # Create disposition declaration
        if self.disposition is not None:
            with open(self.disposition_file, 'w') as fh:
                fh.close()
        logging.info("Created OCFL storage root %s" % (self.root))

    def check_root(self):
        """Check the storage root."""
        if not os.path.exists(self.root):
            raise StoreException("Storage root %s does not exist!" % (self.root))
        if not os.path.isdir(self.root):
            raise StoreException("Storage root %s is not a directory" % (self.root))
        if not os.path.isfile(self.declaration_file):
            raise StoreException("Storage root %s lacks required 0= declaration file" % (self.root))
        if self.disposition and not os.path.isfile(self.disposition_file):
            raise StoreException("Storage root %s lacks expected 1= disposition file" % (self.root))
        # FIXME - check for other 0= and 1=

    def list(self):
        """List contents of storage."""
        self.check_root()
        num_objects = 0
        for (dirpath, dirnames, filenames) in os.walk(self.root, followlinks=True):
            # Ignore files in root
            if dirpath != self.root:
                # Is this directory an OCFL object (or root?). Look for any 0= file.
                zero_eqs = list(filter(lambda x: x.startswith('0='), filenames))
                if len(zero_eqs) > 1:
                    logging.error("Multiple 0= declaration files in %s, not descending" % (dirpath))
                    dirnames = []
                elif len(zero_eqs) == 1:
                    declaration = zero_eqs[0]
                    match = re.match(r'''0=ocfl_object_(\d+\.\d+)''', declaration)
                    if match and match.group(1) == '1.0':
                        # Parse inventory to extract id
                        o = Object()
                        inventory = o.parse_inventory(dirpath)
                        print("%s -- id=%s" % (os.path.relpath(dirpath, self.root), inventory['id']))
                        num_objects += 1
                    elif match:
                        logging.error("Object with unknown version %s in %s, ignoring" % (match.group(1), dirpath))
                    else:
                        logging.error("Object with unrecognized declaration %s in %s, ignoring" % (declaration, dirpath))
                    # don't descend
                    dirnames = []
        # FIXME - do some stuff in here
        logging.info("Found %d OCFL Objects under root %s" % (num_objects, self.root))

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
