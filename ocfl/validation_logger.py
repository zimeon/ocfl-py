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

from .constants import DEFAULT_SPEC_VERSION


class ValidationLogger():
    """Class for OCFL ValidationLogger.

    All validation issues to be recorded are either errors (corresponding with
    MUST etc. in the specification) or warnings (corresponding with SHOULD etc.
    in the specification).
    """

    validation_codes = None

    def __init__(self, *, log_warnings=False, log_errors=True,
                 spec_version=DEFAULT_SPEC_VERSION,
                 lang="en", validation_codes=None):
        """Initialize OCFL validation logger.

        Arguments:
            log_warnings (bool): True to log warnings via the
                warning() method. Default False
            log_errors (bool): True to logs errors via the error()
                method. Default True
            spec_version (str): Specification version being validated
                against, default taken from ocfl.constants.DEFAULT_SPEC_VERSION
            lang (str): Language code to look up description strings
                with, default "en"
            validation_codes (dict): Default None. Usual behavior is to
                not use this argument in which case the validation codes
                and description data are loaded from the normal location
                on first use of this class. Subsequent instantiations use
                the same class data. Allows an override to supply the
                data explicitly
        """
        self.log_warnings = log_warnings
        self.log_errors = log_errors
        self.spec_version = spec_version
        self.lang = lang
        if validation_codes is not None:
            self.validation_codes = validation_codes
        elif self.validation_codes is None:
            with open(os.path.join(os.path.dirname(__file__), "data/validation-errors.json"), "r", encoding="utf-8") as fh:
                self.validation_codes = json.load(fh)
        # Instance variables to accumulate log data
        self.codes = {}
        self.messages = []
        self.num_errors = 0
        self.num_warnings = 0

    @property
    def spec_url(self):
        """Link to the relevant specification version."""
        return "https://ocfl.io/" + self.spec_version + "/spec/"

    def log(self, code, is_error, **args):
        """Log either an error or a warning.

        Arguments:
            code: string for the error code (starts with `E` or `W`).
            is_error: boolean, True for an error, False for a wanring.
            **args: additional arguments that correspond with named arguments
                in the error messages.

        Adds or updates the `codes` attribute with the last message for the given
        code.

        Adds to the log of all messages in the `messages` atttibute depending
        whether we are dealing with an error or a warning, and the values of
        the `log_warnings` and `log_errors` attributes.
        """
        severity = "error" if is_error else "warning"
        if code in self.validation_codes and "description" in self.validation_codes[code]:
            desc = self.validation_codes[code]["description"]
            lang_desc = None
            if self.lang in desc:
                lang_desc = desc[self.lang]
            elif "en" in desc:
                lang_desc = desc["en"]
            elif len(desc) > 0:
                # first key alphabetically
                lang_desc = desc[sorted(list(desc.keys()))[0]]
            else:
                lang_desc = "Unknown " + severity + " without a description"
            # Add in any parameters
            if "params" in self.validation_codes[code]:
                params = []
                for param in self.validation_codes[code]["params"]:
                    params.append(str(args[param]) if param in args else "???")
                try:
                    lang_desc = lang_desc % tuple(params)
                except TypeError:
                    lang_desc += " " + str(args)
            message = "[" + code + "] " + lang_desc
        else:
            message = "Unknown " + severity + ": %s - params (%s)" % (code, str(args))
        # Add link to spec
        m = re.match(r"""([EW](\d\d\d))""", code)
        if m and int(m.group(2)) < 200:
            message += " (see " + self.spec_url + "#" + m.group(1) + ")"
        # Store set of codes with last message for that code, and _full_ list of messages
        self.codes[code] = message
        if (is_error and self.log_errors) or (not is_error and self.log_warnings):
            self.messages.append(message)

    def error(self, code, **args):
        """Log an error."""
        self.log(code, is_error=True, **args)
        self.num_errors += 1

    def warning(self, code, **args):
        """Log a warning."""
        self.log(code, is_error=False, **args)
        self.num_warnings += 1

    def status_str(self, prefix=""):
        """Return string of validator status, with optional prefix."""
        s = ""
        for message in sorted(self.messages):
            s += prefix + message + "\n"
        return s[:-1]

    def __str__(self):
        """Return status string."""
        return self.status_str()
