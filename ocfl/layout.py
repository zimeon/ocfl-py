"""Handle different storage layouts.

OCFL Storage roots require a deterministic mapping from the object identifiers
to the path within the storage root. This layout must be consistent across all
objects in the storage root. It often includes two components:

1) A mapping from the identifier to a set of directory names to create a path
where objects are somewhatevenly distributed and will not end up with too many
entries in any one directory (useful for filesystem implementations but not
relevant for all object stores). The flat layout, where all objects live in the
storage root, does not use a path.

2) A final directory name that may be a more complete representation of the
object id, by typically with at least some cleaning for safety. Some layouts
use just the remainder of a hash however. Obviously algorithms but avoid
collision in this part within a given path.

See: https://ocfl.io/1.1/spec/#root-hierarchies
"""
import json
import os
import os.path
from urllib.parse import quote_plus, unquote_plus


class LayoutException(Exception):
    """Exception class for OCFL Layout."""


class Layout:
    """Base class for layout handlers.

    This base class includes some common implementations where that makes
    sense for certain methods, other methods must be replace and will
    throw an exception if called.
    """

    def __init__(self):
        """Initialize.

        This is trivial so we don't expect sub-class implementations to call
        this __init__. Instead they will replace it and define PARAMS for the
        new class.
        """
        self.NAME = 'BASE'  # Override this in sub-class with real layout name
        self.DESCRIPTION = 'BASE LAYOUT CLASS'  # Override with layout description
        self.PARAMS = None  # Overrride this in sub-class with a dictionary

    @property
    def config_file(self):
        """Location of config.json configuration file for the layout extenstion."""
        return os.path.join('extensions', self.NAME, 'config.json')

    @property
    def config(self):
        """Dictionary with config.json configuration for the layout extenstion."""
        raise LayoutException("No yet implemented")

    def strip_root(self, path, root):
        """Remove root from path, throw exception on failure."""
        root = root.rstrip(os.sep)  # ditch any trailing path separator
        if os.path.commonprefix((path, root)) == root:
            return os.path.relpath(path, start=root)
        raise LayoutException("Path %s is not in root %s" % (path, root))

    def is_valid(self, identifier):  # pylint: disable=unused-argument
        """Return True if identifier is valid, always True in this base implementation."""
        return True

    def encode(self, identifier):
        """Encode identifier to get rid of unsafe chars."""
        return quote_plus(identifier)

    def decode(self, identifier):
        """Decode identifier to put back unsafe chars."""
        return unquote_plus(identifier)

    def identifier_to_path(self, identifier):
        """Convert identifier to path relative to some root."""
        raise LayoutException("No yet implemented")

    def read_layout_params(self, root_fs=None, params_required=False):
        """Look for and read and layout configuration parameters.

        Arguments:
          root_fs - the storage root fs object
          params_required - if True then throw exception for params file not present

        Returns:
          params - dict of params read
        """
        config = None
        if root_fs.exists(self.config_file):
            try:
                with root_fs.open(self.config_file) as fh:
                    config = json.load(fh)
            except Exception as e:
                raise LayoutException("Storage root extension config file %s exists but can't be read/parsed (%s)" % (self.config_file, str(e)))
            if not isinstance(config, dict):
                raise LayoutException("Storage root extension config %s contents not a JSON object" % (self.config_file))
        elif params_required:
            raise LayoutException("Storage root extension config %s expected but not present" % (self.config_file))
        if config is not None:
            self.check_and_set_layout_params(config, require_extension_name=True)

    def check_and_set_layout_params(self, config, require_extension_name=False):
        """Check the layout extension params and set for this layout object."""
        # Check the extensionName
        if not require_extension_name and 'extensionName' not in config:
            # Fine if we don't require the extension name
            pass
        elif config.get('extensionName') != self.NAME:
            raise LayoutException("Storage root extension config extensionName is %s, expected %s" % (config.get('extensionName'), self.NAME))
        # Read and check the parameters (ignore any extra params)
        for key, method in self.PARAMS.items():
            method(config.get(key))

    def write_layout_params(self, root_fs=None):
        """Write the config.json file with layout parameters if need for this layout.

        Does nothing if there is no config.json required for this payout.
        """
        if self.PARAMS is None:
            # Nothing to write if there are no params
            return
        if root_fs.exists(self.config_file):
            raise LayoutException("Storage root extension layout config %s already exists" % (self.config_file))
        try:
            root_fs.makedirs(os.path.dirname(self.config_file))
            with root_fs.open(self.config_file, 'w') as fh:
                json.dump(self.config, fh, indent=2)
        except Exception as e:
            raise LayoutException("Storage root extension config file %s exists but can't be read/parsed (%s)" % (self.config_file, str(e)))
