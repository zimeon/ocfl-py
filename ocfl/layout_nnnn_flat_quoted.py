"""Layout_NNNN_Flat_Quoted mapping of identifier to directory structure."""
from .layout import Layout


class Layout_NNNN_Flat_Quoted(Layout):
    """Class to support trivial identity layout."""

    def __init__(self):
        """Initialize."""
        super().__init__()
        self.NAME = "nnnn-flat-quoted-storage-layout"
        self.DESCRIPTION = "Local extension, flat layout with simple quoting of object ids"
        self.PARAMS = None  # No parameters

    def identifier_to_path(self, identifier):
        """Convert identifier to path relative to root."""
        return self.encode(identifier)
