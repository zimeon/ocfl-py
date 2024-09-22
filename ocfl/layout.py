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
import os
import os.path
from urllib.parse import quote_plus, unquote_plus


class LayoutException(Exception):
    """Exception class for OCFL Layout."""


class Layout:
    """Base class for layout handlers.

    This base class includes some commont implementations where that makes
    sense for certain methods, other methods must be replace and will
    throw an exception if called.
    """

    @property
    def name(self):
        """Canonical name of this layout to go in ocfl_layout.json."""
        raise Exception("No yet implemented")

    def strip_root(self, path, root):
        """Remove root from path, throw exception on failure."""
        root = root.rstrip(os.sep)  # ditch any trailing path separator
        if os.path.commonprefix((path, root)) == root:
            return os.path.relpath(path, start=root)
        raise Exception("Path %s is not in root %s" % (path, root))

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
        raise Exception("No yet implemented")
