"""NewVersion tests."""
import unittest

from ocfl.new_version import NewVersion, NewVersionException
from ocfl.pyfs import pyfs_openfs


class TestNewVersion(unittest.TestCase):
    """TestNewVersion class to run test for the Invenory class."""

    def test_init(self):
        """Test initialization."""
        nv = NewVersion(objdir="", srcdir="")
        self.assertEqual(nv.inventory.head, "v1")
