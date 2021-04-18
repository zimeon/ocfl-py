"""Handle UUID URNs encoding with an unencapsualted quadtree path.

Follows similar pattern to Archivematica.
"""
import os
import os.path
import re

from .dispositor import Dispositor


class UUIDQuadtree(Dispositor):
    """Class to support UUID URIs with quadtree directory names."""

    def __init__(self, prefix='urn:uuid:'):
        """Initialize Dispositor."""
        super().__init__()
        self.prefix = prefix

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
        match = re.match(r'''([\da-f]{4})([\da-f]{4})\-([\da-f]{4})\-([\da-f]{4})\-([\da-f]{4})\-([\da-f]{4})([\da-f]{4})([\da-f]{4})$''', identifier)
        if not match:
            raise Exception("UUIDQuadtree identifier %s not valid" % (identifier))
        return os.path.join(match.group(1), match.group(2), match.group(3), match.group(4),
                            match.group(5), match.group(6), match.group(7), match.group(8))

    def relative_path_to_identifier(self, path):
        """Convert relative path to identifier."""
        # Combine all directories
        segments = path.split(os.sep)
        if len(segments) != 8:
            raise Exception("Exepected path 8 segments in UUIDQuadtree, got %d from %s" % (len(segments), path))
        for segment in segments:
            if not re.match(r'''[\da-f]{4}$''', segment):
                raise Exception("Bad path segment %s in UUIDQuadtree path %s" % (segment, path))
        return(self.prefix + segments[0] + segments[1] + '-'
               + segments[2] + '-' + segments[3] + '-' + segments[4] + '-'
               + segments[5] + segments[6] + segments[7])
