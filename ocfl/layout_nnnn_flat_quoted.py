"""Layout_NNNN_Flat_Quoted mapping of identifier to directory structure."""
from .layout import Layout


class Layout_NNNN_Flat_Quoted(Layout):
    """Class to support trivial identity layout."""

    @property
    def name(self):
        """Canonical name of this layout extension."""
        return "nnnn-flat-quoted-storage-layout"

    @property
    def description(self):
        """Description of this layout to go in ocfl_layout.json."""
        return "Local extension, flat layout with simple quoting of object ids"

    def identifier_to_path(self, identifier):
        """Convert identifier to path relative to root."""
        return self.encode(identifier)
