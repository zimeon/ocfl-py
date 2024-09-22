"""0002 Flat Direct Storage Layout handler.

Specified by: https://ocfl.github.io/extensions/0002-flat-direct-storage-layout.html
"""
import os

from .layout import Layout, LayoutException


class Layout_0002_Flat_Direct(Layout):
    """Class to support trivial identity layout."""

    @property
    def name(self):
        """Canonical name."""
        return "0002-flat-direct-storage-layout"

    def identifier_to_path(self, identifier):
        """Convert identifier to path relative to root."""
        if identifier in ('', '.', '..') or os.sep in identifier:
            raise LayoutException("Identifier '%s' unsafe for %s layout" % (identifier, self.name))
        return identifier
