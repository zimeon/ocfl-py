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
        self.PARAMS = {'tupleSize': self.check_tuple_size}

    @property
    def config(self):
        """Dictionary with config.json configuration for the layout extenstion."""
        return {'extensionName': self.NAME,
                'tupleSize': self.tuple_size}

    def check_tuple_size(self, value):
        """Check tuple size paremeter.

        For config:
            Name: `tupleSize`
            Description: Indicates the size of the segments (in characters)
              that the digest is split into
            Type: number
            Constraints: An integer between 0 and 32 inclusive
            Default: 3
        """
        if value is None:
            raise LayoutException('tupleSize parameter must be specified')
        if not isinstance(value, int) or value < 2 or value > 6:
            raise LayoutException('tupleSize parameter must be an integer between 2 and 6 inclusive')
        self.tuple_size = value

    def encode(self, identifier):
        """Pairtree encode identifier."""
        return id_encode(identifier)

    def decode(self, identifier):
        """Pairtree decode identifier."""
        return id_decode(identifier)

    def identifier_to_path(self, identifier):
        """Convert identifier to path relative to root."""
        identifier = self.encode(identifier)
        id_remains = identifier
        segments = []
        while len(id_remains) > self.tuple_size:
            segments.append(id_remains[0:self.tuple_size])
            id_remains = id_remains[self.tuple_size:]
        segments.append(id_remains)  # the statement means that segmets will always have at least one element
        # Use full identifier to encapsulate
        segments.append(identifier)
        return os.path.join(*segments)  # pylint: disable=no-value-for-parameter
