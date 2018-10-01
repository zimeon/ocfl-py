"""Base class for Dispositor objects."""
try:
    from urllib.parse import quote_plus, unquote_plus  # py3
except:
    from urllib import quote_plus, unquote_plus  # py2


class Dispositor(object):
    """Base class for disposition handlers -- let's call them Dispositors."""

    def __init__(self):
        """Initialize Dispositor."""
        pass

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
        """Convert identifier to path relative to root."""
        raise Exeption("No yet implemented")

    def path_to_identifier(self, path, root=None):
        """Convert path relative to root to identifier."""
        raise Exeption("No yet implemented")
