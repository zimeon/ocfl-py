"""Python implementation of OCFL."""
import sys
from ._version import __version__
from .bagger import bag_as_source, bag_extracted_version, BaggerError
from .constants import *
from .digest import file_digest, string_digest, digest_regex, normalized_digest
from .inventory import Inventory, InventoryException
from .inventory_validator import InventoryVadlidator
from .object import Object
from .object_utils import find_path_type, ObjectException
from .storage_root import StorageRoot, StorageRootException
from .version_metadata import VersionMetadata

if sys.version_info < (3, 6):  # pragma: no cover
    raise Exception("Must use python 3.6 or greater!")  # pragma: no cover
