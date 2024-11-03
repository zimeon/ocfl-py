"""0002 Flat Direct Storage Layout handler.

Specified by: https://ocfl.github.io/extensions/0002-flat-direct-storage-layout.html
"""
import os

from .layout import Layout, LayoutException


class Layout_0002_Flat_Direct(Layout):
    """Class to support trivial identity layout."""

    def __init__(self):
        """Initialize."""
        super().__init__()
        self.NAME = "0002-flat-direct-storage-layout"
        self.DESCRIPTION = "Extension 0002: Flat Direct Storage Layout"
        self.PARAMS = None  # No parameters

    def identifier_to_path(self, identifier):
        """Convert identifier to path relative to root."""
        if identifier in ("", ".", "..") or os.sep in identifier:
            raise LayoutException("Identifier '%s' unsafe for %s layout" % (identifier, self.NAME))
        return identifier
