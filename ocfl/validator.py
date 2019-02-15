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


class OCFLValidator(object):
    """Class for OCFL Validator."""

    validation_codes = None

    def __init__(self, lang='en'):
        """Initialize OCFL validator."""
        self.codes = {}
        self.lang = lang
        self.errors = 0
        self.warnings = 0
        self.info = 0
        if self.validation_codes is None:
            with open(os.path.join(os.path.dirname(__file__), 'data/validation-errors.json'), 'r') as fh:
                self.validation_codes = json.load(fh)['codes']

    def error(self, code, **args):
        """Add error code to self.codes."""
        # print("args = %s" % (str(**args)))
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
                lang_desc = "Error %s - no description, params (%s)"
            self.codes[code] = '[' + code + '] ' + lang_desc  # FIXME - use **args
        else:
            self.codes[code] = "Unknown error %s - params (%s)" % (code, str(**args))
        self.errors += 1

    def validate(self, path):
        """Validate OCFL object at path."""
        if not os.path.isdir(path):
            self.error('E000')
            return False
        # Object declaration
        namastes = find_namastes(0, path)
        if len(namastes) == 0:
            self.error('E001')
        elif len(namastes) > 1:
            self.error('E901')
        elif not namastes[0].content_ok(path):
            self.error('E902')
        # Inventory
        inv_file = os.path.join(path, 'inventory.json')
        if not os.path.exists(inv_file):
            self.error('E004')
        else:
            self.validate_inventory(inv_file)
        inv_digest_file = os.path.join(path, 'inventory.json.sha512')  # FIXME - support other digests
        if not os.path.exists(inv_digest_file):
            self.error('E005')
        else:
            try:
                self.validate_inventory_digest(inv_file, inv_digest_file)
            except Exception as e:
                self.error(str(e))
        return self.errors == 0

    def validate_inventory(self, inv_file):
        """Validate a given inventory file, record errors with self.error()."""
        with open(inv_file) as fh:
            inventory = json.load(fh)
        # Basic structure
        if 'id' not in inventory:
            self.error("E100")
        elif inventory['id'] == '':
            self.error("E101")
        if 'type' not in inventory:
            self.error("E102")
        elif inventory['type'] != 'https://ocfl.io/1.0/spec/#inventory':
            self.error("E103")
        if 'digestAlgorithm' not in inventory:
            self.error("E104")
        elif inventory['digestAlgorithm'] not in ('sha256', 'sha512'):
            self.error("E105")  # FIXME - WARN if not sha512?
        if 'head' not in inventory:
            self.error("E106")
        if 'manifest' not in inventory:
            self.error("E107")
        else:
            self.validate_manifest(inventory['manifest'])
        if 'versions' not in inventory:
            self.error("E108")
        else:
            self.validate_versions(inventory['versions'])

    def validate_inventory_digest(self, inv_file, inv_digest_file):
        """Validate a given inventory digest for a give inventory file."""
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
        pass

    def validate_versions(self, versions):
        """Validate versions block in inventory."""
        pass

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
