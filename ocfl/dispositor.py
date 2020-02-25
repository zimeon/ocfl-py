"""Base class for Dispositor objects."""
import os
import os.path
try:
    from urllib.parse import quote_plus, unquote_plus  # py3
except ImportError:                                    # pragma: no cover -- py2
    from urllib import quote_plus, unquote_plus        # pragma: no cover -- py2


class Dispositor(object):
    """Base class for disposition handlers -- let's call them Dispositors."""

    def __init__(self):
        """Initialize Dispositor."""
        pass

    def strip_root(self, path, root):
        """Remove root from path, throw exception on failure."""
        root = root.rstrip(os.sep)  # ditch any trailing path separator
        if os.path.commonprefix((path, root)) == root:
            return os.path.relpath(path, start=root)
        else:
            raise Exception("Path %s is not in root %s" % (path, root))

    def is_valid(self, identifier):
        """True if identifier is valid, always True in this base implementation."""
        return True

    def encode(self, identifier):
        """Encode identifier to get rid of unsafe chars."""
        return quote_plus(identifier)

    def decode(self, identifier):
        """Decode identifier to put back unsafe chars."""
        return unquote_plus(identifier)

    def identifier_to_path(self, identifier):
        """Convert identifier to path relative to some root."""
        raise Exeption("No yet implemented")

    def relative_path_to_identifier(self, path):
        """Convert relative path to identifier."""
        raise Exeption("No yet implemented")

    def path_to_identifier(self, path, root=None):
        """Convert path relative to root to identifier."""
        if root is not None:
            path = self.strip_root(path, root)
        return self.relative_path_to_identifier(path)
