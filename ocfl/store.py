"""OCFL Object Store library."""
import hashlib
import json
import os
import os.path
import re
import logging
from shutil import copyfile
import urllib.parse

from .digest import *


class StoreException(Exception):
    """Exception class for OCFL Store."""

    pass


class Store(object):
    """Class for handling OCFL Object Stores."""

    def __init__(self, root=None, disposition=None, default_disposition=None):
        """Initialize OCFL Object Store."""
        self.root = root
        self.disposition = disposition

    @property
    def declaration_file(self):
        """Path of storage root declaration file."""
        return os.path.join(self.root, '0=ocfl_1.0')

    @property
    def disposition_file(self):
        """Path of storage root disposition file."""
        return os.path.join(self.root, '1=' + urllib.parse.quote_plus(self.disposition))

    def create(self):
        """Create object store."""
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
        # FIXME - do some stuff in here
        logging.info("Found %d OCFL Objects under root %s" % (num_objects, self.root))

