"""OCFL Validation Logger.

Handle logging of validation errors and warnings. All the error and
warning messages are stored in a separate JSON file that is keyed
by the anchors ("E001", "W001") that are used in the specification.

The format of the `validation-codes.json` files is as follows:
```
{
  "E001a": {
    "params": ["file"],
    "description": {
       "en": "OCFL Object root contains unexpected file: %s"
    }
  },
  "E001b": {
    "params": ["dir"],
    "description": {
       "en": "OCFL Object root contains unexpected directory: %s"
    }
  },
  ...
}
```
"""
import json
import os
import os.path
import re


class ValidationLogger():
    """Class for OCFL ValidationLogger."""

    validation_codes = None

    def __init__(self, show_warnings=False, show_errors=True,
                 lang='en', validation_codes=None):
        """Initialize OCFL validation logger."""
        self.show_warnings = show_warnings
        self.show_errors = show_errors
        self.lang = lang
        self.codes = {}
        self.messages = []
        self.num_errors = 0
        self.num_warnings = 0
        self.spec = 'https://ocfl.io/1.0/spec/'
        if validation_codes is not None:
            self.validation_codes = validation_codes
        elif self.validation_codes is None:
            with open(os.path.join(os.path.dirname(__file__), 'data/validation-errors.json'), 'r', encoding="utf-8") as fh:
                self.validation_codes = json.load(fh)

    def error_or_warning(self, code, severity='error', **args):
        """Add error or warning to self.codes.

        Arguments:
            code: string for the error code (starts with `E` or `W`).
            severity: string for severity, `error` (default) or `warning`.
            **args: additional arguments that correspond with named arguments
                in the error messages.

        Adds or updates the `codes` attribute with the last message for the given
        code.

        Adds to the log of all messages in the `messages` atttibute depending on
        severity and the values of the `show_warnings` and `show_errors` attributes.
        """
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
                lang_desc = "Unknown " + severity + " without a description"
            # Add in any parameters
            if 'params' in self.validation_codes[code]:
                params = []
                for param in self.validation_codes[code]['params']:
                    params.append(str(args[param]) if param in args else '???')
                try:
                    lang_desc = lang_desc % tuple(params)
                except TypeError:
                    lang_desc += ' ' + str(args)
            message = '[' + code + '] ' + lang_desc
        else:
            message = "Unknown " + severity + ": %s - params (%s)" % (code, str(args))
        # Add link to spec
        m = re.match(r'''([EW](\d\d\d))''', code)
        if m and int(m.group(2)) < 200:
            message += ' (see ' + self.spec + '#' + m.group(1) + ')'
        # Store set of codes with last message for that code, and _full_ list of messages
        self.codes[code] = message
        if (severity == 'error' and self.show_errors) or (severity != 'error' and self.show_warnings):
            self.messages.append(message)

    def error(self, code, **args):
        """Log an error."""
        self.error_or_warning(code, severity='error', **args)
        self.num_errors += 1

    def warning(self, code, **args):
        """Log a warning."""
        self.error_or_warning(code, severity='warning', **args)
        self.num_warnings += 1

    def status_str(self, prefix=''):
        """Return string of validator status, with optional prefix."""
        s = ''
        for message in sorted(self.messages):
            s += prefix + message + '\n'
        return s[:-1]

    def __str__(self):
        """Return status string."""
        return self.status_str()
