"""Handle pairtree (n=2) and similar directory structures.

Note that saying Pairtree for a given n, default 2, is not sufficient
to define the object layout. The Pairtree specification
https://confluence.ucop.edu/display/Curation/PairTree
encourages the use of object encapsulation (section 3) but does
not prescribe a particular method. In this implementation the default
it to encapsulate in a directory with the complete encoded identifier
name.

Makes use of encoding and decoding functions from Ben O'Steen's
implementation in the pairtree module
(https://github.com/benosteen/pairtree).
"""
import os
import os.path
from pairtree import id_encode, id_decode

from .layout import Layout, LayoutException


class Layout_NNNN_Tuple_Tree(Layout):
    """Class to support pairtree and related layouts."""

    def __init__(self, tuple_size=2):
        """Initialize Layout."""
        super().__init__()
        self.tuple_size = tuple_size
        self.NAME = "nnnn-tuple-tree-layout"
        self.DESCRIPTION = "Local extension, unhashed tuple-tree with configurable tuple size"
        self.PARAMS = {"tupleSize": self.check_tuple_size}

    @property
    def config(self):
        """Dictionary with config.json configuration for the layout extenstion."""
        return {"extensionName": self.NAME,
                "tupleSize": self.tuple_size}

    def check_tuple_size(self, value):
        """Check tuple size paremeter.

        For config:
            Name: `tupleSize`
            Description: Indicates the size of the segments (in characters)
              that the digest is split into
            Type: number
            Constraints: An integer between 2 and 6 inclusive
            Default: 2

        Argument:
            value (int): integer value for tuple size in characters

        Raises:
            LayoutException: if the tuple size is not allowed

        Sets the tuple_size property of this object as a side effect.
        """
        if value is None:
            raise LayoutException("tupleSize parameter must be specified")
        if not isinstance(value, int) or value < 2 or value > 6:
            raise LayoutException("tupleSize parameter must be an integer between 2 and 6 inclusive")
        self.tuple_size = value

    def encode(self, identifier):
        """Pairtree encode identifier.

        Argument:
            identifier (str): object identifier to encode

        Returns:
            str: encoded identifier
        """
        return id_encode(identifier)

    def decode(self, identifier):
        """Pairtree decode identifier.

        Argument:
            identifier (str): object identifier to decode

        Returns:
            str: decoded identifier
        """
        return id_decode(identifier)

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
        identifier.
        """
        if identifier == "":
            raise LayoutException("Identifier '%s' unsafe for %s layout" % (identifier, self.NAME))
        identifier = self.encode(identifier)
        id_remains = identifier
        segments = []
        while len(id_remains) > self.tuple_size:
            segments.append(id_remains[0:self.tuple_size])
            id_remains = id_remains[self.tuple_size:]
        segments.append(id_remains)  # the statement means that segments will always have at least one element
        # Use full identifier to encapsulate
        segments.append(identifier)
        return os.path.join(*segments)
