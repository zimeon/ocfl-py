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

from .dispositor import Dispositor


class Ntree(Dispositor):
    """Class to support pairtree and related dispositions."""

    def __init__(self, n=2, encapsulate=True):
        """Initialize Dispositor."""
        super().__init__()
        self.n = n
        self.encapsulate = encapsulate

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
        while len(id_remains) > self.n:
            segments.append(id_remains[0:self.n])
            id_remains = id_remains[self.n:]
        segments.append(id_remains)  # the statement means that segmets will always have at least one element
        if self.encapsulate:
            segments.append(identifier)
        return os.path.join(*segments)  # pylint: disable=no-value-for-parameter

    def relative_path_to_identifier(self, path):
        """Convert relative path to identifier."""
        if self.encapsulate:
            (path, encap_id) = os.path.split(path)
        # Combine all directories
        identifier = ''.join(path.split(os.sep))
        if self.encapsulate and identifier != encap_id:
            raise Exception("Bad ntree path: id from path (%s) does not match encapsulation id (%s)" % (identifier, encap_id))
        return identifier
