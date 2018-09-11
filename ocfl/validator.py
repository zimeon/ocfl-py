"""OCFL Validator."""
import json
import os
import os.path
import re
import logging


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
            with open(os.path.join(os.path.dirname(__file__), 'data/validation-errors.jsonld'), 'r') as fh:
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
        # Object declaration
        namastefile = os.path.join(path, '0=ocfl_object_1.0')
        if not os.path.exists(namastefile):
            self.error('E001')
        # No check for E002 as we only know about 1.0
        elif os.path.getsize(namastefile) > 0:
            self.error('E003')
        # Inventory
        invfile = os.path.join(path, 'inventory.jsonld')
        if not os.path.exists(invfile):
            self.error('E004')
        else:
            self.validate_inventory(invfile)
        invdigest = os.path.join(path, 'inventory.jsonld.sha512')  # FIXME - support other digests
        if not os.path.exists(invdigest):
            self.error('E005')
        else:
            # FIXME - check digest against inventory
            pass
        #
        return self.errors == 0

    def validate_inventory(self, invfile):
        """Validate a given inventory file."""
        pass

    def validate_inventory_digest(self, invfile, invdigest):
        """Validate a given inventory digest for a give inventory file."""
        pass

    def __str__(self):
        """String of validator status."""
        s = ''
        for code in sorted(self.codes.keys()):
            s += self.codes[code] + '\n'
        return s
