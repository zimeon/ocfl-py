"""Identity mapping of identifier to directory structure."""
import os
import os.path

from .dispositor import Dispositor


class Identity(Dispositor):
    """Class to support trivial identity disposition."""

    def __init__(self):
        """Initialize Dispositor."""
        super(Identity, self).__init__()

    def identifier_to_path(self, identifier):
        """Convert identifier to path relative to root."""
        return self.encode(identifier)

    def path_to_identifier(self, path, root=None):
        """Convert path relative to root to identifier."""
        # FIXME - handle root
        # FIXME - exception if any path components
        return self.decode(path)
