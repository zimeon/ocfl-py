"""OCFL Validation Logger.

Handle logging of validation errors and warnings.
"""
import json
import os
import os.path
import re
import logging


class ValidationLogger(object):
    """Class for OCFL ValidationLogger."""

    validation_codes = None

    def __init__(self, lang='en'):
        """Initialize OCFL validation logger."""
        self.lang = lang
        self.codes = {}
        self.errors = 0
        self.warnings = 0
        self.info = 0
        if self.validation_codes is None:
            with open(os.path.join(os.path.dirname(__file__), 'data/validation-errors.json'), 'r') as fh:
                self.validation_codes = json.load(fh)['codes']

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
        self.error_or_warning(code, severity='error', **args)
        self.errors += 1

    def warn(self, code, **args):
        """Add warning code to self.codes."""
        self.error_or_warning(code, severity='warning', **args)
        self.warnings += 1

    def __str__(self):
        """String of validator status."""
        s = ''
        for code in sorted(self.codes.keys()):
            s += self.codes[code] + '\n'
        return s
