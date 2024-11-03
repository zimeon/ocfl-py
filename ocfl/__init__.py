"""Python implementation of OCFL."""
import sys
from ._version import __version__
from .object import *
from .inventory import *
from .version_metadata import *
from .storage_root import *
from .digest import *
from .bagger import bag_as_source, bag_extracted_version, BaggerError
from .object_utils import find_path_type, ObjectException

if sys.version_info < (3, 6):  # pragma: no cover
    raise Exception("Must use python 3.6 or greater!")  # pragma: no cover
