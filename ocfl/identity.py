"""Identity mapping of identifier to directory structure."""
import os

from .dispositor import Dispositor


class Identity(Dispositor):
    """Class to support trivial identity disposition."""

    def identifier_to_path(self, identifier):
        """Convert identifier to path relative to root."""
        return self.encode(identifier)

    def relative_path_to_identifier(self, path):
        """Convert relative path to identifier.

        It is an error to include more than one path segment so raise
        and exception if os.sep exists in the path.
        """
        if os.sep in path:
            raise Exception("Relative path in Identity dispositor must not have multiple path segments!")
        return self.decode(path)
