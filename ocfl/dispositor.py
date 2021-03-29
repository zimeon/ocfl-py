"""Base class for Dispositor objects."""
import os
import os.path
from urllib.parse import quote_plus, unquote_plus


class Dispositor:
    """Base class for disposition handlers -- let's call them Dispositors."""

    def strip_root(self, path, root):  # pylint: disable=no-self-use
        """Remove root from path, throw exception on failure."""
        root = root.rstrip(os.sep)  # ditch any trailing path separator
        if os.path.commonprefix((path, root)) == root:
            return os.path.relpath(path, start=root)
        raise Exception("Path %s is not in root %s" % (path, root))

    def is_valid(self, identifier):  # pylint: disable=unused-argument,no-self-use
        """Return True if identifier is valid, always True in this base implementation."""
        return True

    def encode(self, identifier):  # pylint: disable=no-self-use
        """Encode identifier to get rid of unsafe chars."""
        return quote_plus(identifier)

    def decode(self, identifier):  # pylint: disable=no-self-use
        """Decode identifier to put back unsafe chars."""
        return unquote_plus(identifier)

    def identifier_to_path(self, identifier):  # pylint: disable=no-self-use
        """Convert identifier to path relative to some root."""
        raise Exception("No yet implemented")

    def relative_path_to_identifier(self, path):  # pylint: disable=no-self-use
        """Convert relative path to identifier."""
        raise Exception("No yet implemented")

    def path_to_identifier(self, path, root=None):
        """Convert path relative to root to identifier."""
        if root is not None:
            path = self.strip_root(path, root)
        return self.relative_path_to_identifier(path)
