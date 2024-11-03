"""Handle UUID URNs encoding with an unencapsualted quadtree path.

Follows similar pattern to Archivematica.
"""
import os
import os.path
import re

from .layout import Layout, LayoutException


class Layout_NNNN_UUID_Quadtree(Layout):
    """Class to support UUID URIs with quadtree directory names."""

    def __init__(self, prefix="urn:uuid:"):
        """Initialize Layout."""
        super().__init__()
        self.prefix = prefix
        self.NAME = "nnnn-uuid-quadtree"
        self.DESCRIPTION = "Local extension to support UUID URIs with quadtree directory names"
        self.PARAMS = {"prefix": self.check_prefix}

    @property
    def config(self):
        """Dictionary with config.json configuration for the layout extenstion."""
        return {"extensionName": self.NAME,
                "prefix": self.prefix}

    def check_prefix(self, value):
        """Check prefix paremeter.

        Any string is allowed.
        """
        if value is None:
            raise LayoutException("prefix parameter must be specified")
        if not isinstance(value, str):
            raise LayoutException("prefix parameter must be a string")
        self.prefix = value

    def encode(self, identifier):
        """NOOP encode identifier."""
        return identifier

    def decode(self, identifier):
        """NOOP decode identifier."""
        return identifier

    def identifier_to_path(self, identifier):
        """Convert identifier to path relative to root.

        Must match prefix:6ba7b810-9dad-11d1-80b4-00c04fd430c8
        """
        if identifier.startswith(self.prefix):
            identifier = identifier[len(self.prefix):]
        else:
            raise Exception("UUIDQuadtree identifier %s does not start with prefix %s" % (identifier, self.prefix))
        match = re.match(r"""([\da-f]{4})([\da-f]{4})\-([\da-f]{4})\-([\da-f]{4})\-([\da-f]{4})\-([\da-f]{4})([\da-f]{4})([\da-f]{4})$""", identifier)
        if not match:
            raise Exception("UUIDQuadtree identifier %s not valid" % (identifier))
        return os.path.join(match.group(1), match.group(2), match.group(3), match.group(4),
                            match.group(5), match.group(6), match.group(7), match.group(8))
