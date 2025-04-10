"""Layout_NNNN_Flat_Quoted mapping of identifier to directory structure."""
from .layout import Layout, LayoutException


class Layout_NNNN_Flat_Quoted(Layout):
    """Class to support trivial identity layout."""

    def __init__(self):
        """Initialize."""
        super().__init__()
        self.NAME = "nnnn-flat-quoted-storage-layout"
        self.DESCRIPTION = "Local extension, flat layout with simple quoting of object ids"
        self.PARAMS = None  # No parameters

    def identifier_to_path(self, identifier):
        """Convert identifier to path relative to root.

        Argument:
            identifier (str): object identifier

        Returns:
            str: object path for this layout

        Raises:
            LayoutException: if the identifier cannot be converted to a valid
            object path. Currently just a check for blank

        Uses Layout.encode() to generate a safe directory name from any
        identifier. Length is not checked but could cause operating system
        errors.
        """
        if identifier == "":
            raise LayoutException("Identifier '%s' unsafe for %s layout" % (identifier, self.NAME))
        return self.encode(identifier)
