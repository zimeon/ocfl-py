"""Python implementation of OCFL."""
import sys
from .object import *
from .version import *
from .store import *
from .digest import *
from .disposition import get_dispositor
from .bagger import bag_as_source, bag_extracted_version, BaggerError

__version__ = '0.0.1'

if sys.version_info < (2, 7):  # pragma: no cover
    raise Exception("Must use python 2.7 or greater (probably)!")
