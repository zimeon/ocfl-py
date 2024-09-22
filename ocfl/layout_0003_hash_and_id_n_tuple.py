"""0002 0003: Hashed Truncated N-tuple Trees with Object ID Encapsulating Directory for OCFL Storage Hierarchies handler.

Specified by: https://ocfl.github.io/extensions/0003-hash-and-id-n-tuple-storage-layout.html
"""
import os

from .layout import Layout, LayoutException


class Layout_0003_Hash_And_Id_N_Tuple(Layout):
    """Class to support trivial identity layout."""

    @property
    def name(self):
        """Canonical name"""
        return '0003-hash-and-id-n-tuple-storage-layout'

    def identifier_to_path(self, identifier):
        """Convert identifier to path relative to root."""
        if identifier in ('', '.', '..') or os.sep in identifier:
            raise LayoutException("Identifier '%s' unsafe for %s layout" % (identifier, self.name))
        return identifier

    def relative_path_to_identifier(self, path):
        """Convert relative path to identifier.

        It is an error to include more than one path segment so raise
        and exception if os.sep exists in the path.
        """
        if os.sep in path:
            raise Exception("Relative path in Identity layout must not have multiple path segments!")
        return self.decode(path)
