"""Handle different storage layouts.

OCFL Storage Roots require a deterministic mapping from the object identifiers
to the path within the storage root. (It is not required that one can deduce the
object id from the path, as is the case with a hashed layout for example). The
layout must be consistent across all objects in the storage root. It often
includes two components:

1) A mapping from the identifier to a set of directory names to create a path
where objects are somewhatevenly distributed and will not end up with too many
entries in any one directory (useful for filesystem implementations but not
relevant for all object stores). The flat layout, where all objects live in the
storage root, does not use a path.

2) A final directory name that may be a more complete representation of the
object id, by typically with at least some cleaning for safety. Some layouts
use just the remainder of a hash however. Obviously algorithms must avoid
collision in this part within a given path.

See: https://ocfl.io/1.1/spec/#root-hierarchies
"""
import json
import logging
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

    Attributes:
        NAME: string for name of the extension
        DESCRIPTION: sting with longer description of extension
        PARAMS: None if the extension has no parameters, otherwise a dict
            with keys that are the parameter names, and values that are
            the methods used to parse/check the paremeter.
    """

    def __init__(self):
        """Initialize.

        This is trivial so we don't expect sub-class implementations to call
        this __init__. Instead they will replace it and define PARAMS for the
        new class.
        """
        self.NAME = "BASE"  # Override this in sub-class with real layout name
        self.DESCRIPTION = "BASE LAYOUT CLASS"  # Override with layout description
        self.PARAMS = None  # Overrride this in sub-class with a dictionary

    @property
    def config_file(self):
        """Location of config.json configuration file for the layout extenstion."""
        return os.path.join("extensions", self.NAME, "config.json")

    @property
    def config(self):
        """Dictionary with config.json configuration for the layout extenstion.

        Dict values are based on the current attributes (as would be serialized
        with json.dump()), else None indicates that there is no config.json
        this layout.
        """
        return None

    def check_full_config(self):
        """Check full configuration in instance variables.

        Trivial implementation that does nothing. It is intended that
        sub-classes will override to do real checks if necessary. No
        return value, raise a LayoutException on error.
        """
        return

    def strip_root(self, path, root):
        """Remove root from path, throw exception on failure.

        Arguments:
            path (str): file path from which root will be stripped
            root (str): root path that will be stripped from path, also
                any leading path separator is removed.

        Raises:
            LayoutException: if the path is not within the given root and thus
                root cannot be stripped from it
        """
        root = root.rstrip(os.sep)  # ditch any trailing path separator
        if os.path.commonprefix((path, root)) == root:
            return os.path.relpath(path, start=root)
        raise LayoutException("Path %s is not in root %s" % (path, root))

    def is_valid(self, identifier):  # pylint: disable=unused-argument
        """Check validity of identifier for this layout.

        Arguments:
            identifier (str): identifier to check

        Returns:
            bool: True if valid, False otherwise. Always True in this base
            implementation.
        """
        return True

    def encode(self, identifier):
        """Encode identifier to get rid of unsafe chars.

        Arguments:
            identifier (str): identifier to encode

        Returns:
            str: encoded identifier
        """
        return quote_plus(identifier)

    def decode(self, identifier):
        """Decode identifier to put back unsafe chars.

        Arguments:
            identifier (str): identifier to decode

        Returns:
            str: decoded identifier
        """
        return unquote_plus(identifier)

    def identifier_to_path(self, identifier):
        """Convert identifier to path relative to some root.

        Arguments:
            identifier (str): identifier to encode

        Returns:
            str: object path for this identifier

        Raises:
            LayoutException: if the identifer cannot be used to create an object
                path. In this base implementation, an exception is always raised.
                The method should be overridded with the same signature
        """
        raise LayoutException("No yet implemented")

    def read_layout_params(self, root_fs=None, params_required=False):
        """Look for and read and layout configuration parameters.

        Arguments:
            root_fs (str): the storage root fs object
            params_required (bool): if True then throw exception for params file
                not present

        Raises:
            LayoutException: if the config can't be read or if required by
                params_required but not present

        Sets instance data in accord with the configuration using the methods
        in self.PARAMS to parse for each key.
        """
        config = None
        logging.debug("Reading extension config file %s", self.config_file)
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
            self.check_and_set_layout_params(config)

    def check_and_set_layout_params(self, config, require_extension_name=True):
        """Check the layout extension params and set for this layout object.

        Arguments:
            config: dict representing the parse JSON config.json file
            require_extension_name: boolean, True by default. If set False then
                the extensionName paramater is not required

        Raises:
            LayoutException: if the extensionName is missig from the config, if
                support for the named extension isn't implemented, or if there
                is an error in the parameters or full configuration.

        For each parameter that is recognized, the appropriate check and set
        method in self.PARAMS is called. The methods set instance attributes.
        Finally, the check_full_config method is called to check anything that
        might required all of the configuration to be known.
        """
        # Check the extensionName if required and/or specified
        if "extensionName" not in config:
            if require_extension_name:
                raise LayoutException("Storage root extension config missing extensionName")
        elif config.get("extensionName") != self.NAME:
            raise LayoutException("Storage root extension config extensionName is %s, expected %s" % (config.get("extensionName"), self.NAME))
        # Read and check the parameters (ignore any extra params)
        for key, method in self.PARAMS.items():
            method(config.get(key))
        # Finally, check full config
        self.check_full_config()

    def write_layout_params(self, root_fs=None):
        """Write the config.json file with layout parameters if need for this layout.

        Arguments:
            root_fs (str): the storage root fs object

        Raises:
            LayoutException: if there is an error trying to write the config.json
            file, including if one already exists.

        Does nothing if there is no config.json content defined for this layout.
        """
        config = self.config
        if config is None:
            # Nothing to write if there is no config defined
            return
        logging.debug("Writing extension config file %s", self.config_file)
        if root_fs.exists(self.config_file):
            raise LayoutException("Storage root extension layout config %s already exists" % (self.config_file))
        try:
            root_fs.makedirs(os.path.dirname(self.config_file))
            with root_fs.open(self.config_file, "w") as fh:
                json.dump(config, fh, indent=2)
        except Exception as e:
            raise LayoutException("Storage root extension config file %s couldn't be written (%s)" % (self.config_file, str(e)))
