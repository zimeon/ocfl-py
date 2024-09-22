"""Identity mapping of identifier to directory structure."""
import os

from .layout import Layout, LayoutException


class Layout_NNNN_Flat_Quoted(Layout):
    """Class to support trivial identity layout."""

    @property
    def name(self):
        """Canonical name of this layout extension."""
        return "nnnn-flat-quoted-storage-layout"

    def identifier_to_path(self, identifier):
        """Convert identifier to path relative to root."""
        return self.encode(identifier)

    def relative_path_to_identifier(self, path):
        """Convert relative path to identifier.

        It is an error to include more than one path segment so raise
        and exception if os.sep exists in the path.
        """
        if os.sep in path:
            raise LayoutException("Relative path in NNNN-flat-quoted layout must not have multiple path segments!")
        return self.decode(path)
