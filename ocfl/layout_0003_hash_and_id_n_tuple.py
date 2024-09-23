"""0003: Hashed Truncated N-tuple Trees with Object ID Encapsulating Directory for OCFL Storage Hierarchies handler.

Specified by: https://ocfl.github.io/extensions/0003-hash-and-id-n-tuple-storage-layout.html
"""
import os
import re

import codecs

from .digest import string_digest
from .layout import Layout


def _percent_encode(c):
    """Return % encoded version of string c."""
    c_bytes = c.encode('utf8')
    s = ''
    for b in c_bytes:
        s += '%' + codecs.encode(bytes([b]), encoding='hex_codec').decode('utf8')
    return s


def _get_encapsulation_directory(object_id, digest):
    """Return directory to encapsulate object."""
    d = ''
    for c in object_id:
        if re.match(r'[A-Za-z0-9-_]{1}', c):
            d += c
        else:
            d += _percent_encode(c)
    if len(d) > 100:
        return f'{d[:100]}-{digest}'
    return d


def _id_to_path(identifier, digest_algorithm, tuple_size, number_of_tuples):
    """Return storage path from identifier."""
    digest = string_digest(identifier, digest_algorithm)
    digest = digest.lower()  # Not necessary for current digests
    path = ''
    for i in range(number_of_tuples):
        tuple = digest[i * tuple_size:i * tuple_size + tuple_size]
        path = os.path.join(path, tuple)
    encapsulation_directory = _get_encapsulation_directory(identifier, digest=digest)
    path = os.path.join(path, encapsulation_directory)
    return path


class Layout_0003_Hash_And_Id_N_Tuple(Layout):
    """Class to support trivial identity layout."""

    def __init__(self, params=None):
        """Initialize."""
        self.digest_algorithm = 'sha256'
        self.tuple_size = 3
        self.number_of_tuples = 3

    @property
    def name(self):
        """Canonical name."""
        return '0003-hash-and-id-n-tuple-storage-layout'

    def identifier_to_path(self, identifier):
        """Convert identifier to path relative to root.

        Algorithm:
        1. The OCFL object identifier is encoded as UTF-8 and hashed using the
           specified digestAlgorithm.
        2. The digest is encoded as a lower-case hex string.
        3. Starting at the beginning of the digest and working forwards, the
           digest is divided into numberOfTuples tuples each containing
           tupleSize characters.
        4. The tuples are joined, in order, using the filesystem path separator.
        5. The OCFL object identifier is percent-encoded to create the
            encapsulation directory name. However, if this is > 100 characters
            then it is tuncated at 100 characters and then '-' and the digest
            appended (so it would be 165 chars with sha256).
        6. The encapsulation directory name is joined to the end of the path.
        """
        return _id_to_path(identifier, self.digest_algorithm,
                           self.number_of_tuples, self.tuple_size)
