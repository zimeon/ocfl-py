"""NewVersion class to assemble what will become a new Object version."""
import copy
import logging

from .digest import file_digest
from .inventory import InventoryException
from .pyfs import pyfs_openfs


class NewVersionException(Exception):
    """Exception class for NewVersion objects."""


class NewVersion():
    """Class to represent a new version to be added to an Object."""

    def __init__(self, *,
                 inventory,
                 objdir=None,
                 srcdir=None,
                 metadata=None,
                 carry_content_forward=True,
                 forward_delta=True,
                 dedupe=False,
                 old_digest_algorithm=None):
        """Create NewVersion object.

        Arguments:
            object (ocfl.Object): instance for which this is a new version.
            inventory (ocfl.Inventory): inventory that we will modify to build
                the new version.
            carry_content_forward (bool): True to carry forward the state from
                the last current version as a starting point. False to start
                with empty version state.

        Example:
            # mkdir tmp
            # cp -rp fixtures/1.1/good-objects/spec-ex-full tmp/spec-ex-full
            # python
            >>> import ocfl
            >>> object = ocfl.Object()
            >>> nv = object.start_new_version(objdir="tmp/spec-ex-full", carry_content_forward=True)
            >>> nv.inventory.current_version.logical_paths
            ['foo/bar.xml', 'empty2.txt', 'image.tiff']
            >>> nv.delete("foo/bar.xml")
            >>> nv.rename("empty2.txt", "empty3.txt")
            >>> nv.add_content("fixtures/1.1/content/README.md", "readme", "v4/readme")
            >>> object.commit_new_version(nv)
            INFO:root:Updated OCFL object ark:/12345/bcd987 in tmp/spec-ex-full by adding v4
            <ocfl.inventory.Inventory object at 0x1014e6cd0>
        """
        # Configuration
        self.inventory = inventory
        self.objdir = objdir
        self.srcdir = srcdir
        self.src_fs = None
        self.forward_delta = forward_delta
        self.dedupe = dedupe
        # Additional state needed for final commit
        self.old_digest_algorithm = old_digest_algorithm
        self.files_to_copy = {}  # dict: src_path -> content_path
        self._start_new_version(carry_content_forward=carry_content_forward,
                                metadata=metadata)

    def _start_new_version(self, *, metadata, carry_content_forward=False):
        """Start the new version by adjusting inventory.

        If carry_content_forward is set then the state block of the previous
        version is copied forward into the new version. Items may later be
        added or deleted.

        Arguments:
            metadata (ocfl.VersionMetadata or None): Either a VersionMetadata
                object to set the metadata for the new version, None to not set
                metadata
            carry_content_forward (bool): True to copy state forward, False to
                creat new version with empty state
        """
        state = {}
        if carry_content_forward:
            state = copy.deepcopy(self.inventory.current_version.state)
        self.inventory.add_version(state=state, metadata=metadata)
        self.src_fs = pyfs_openfs(self.srcdir)

    def add_content(self, src_path, logical_path, content_path=None):
        """Add a file to the new version.

        Arguments:
            src_path (str): path within the source directory specified on
                creation
            logical_path (str): logical filepath that this content should
                have within the version of the object
        """
        logging.debug("add_content(%s %s %s)", src_path, content_path, logical_path)
        inventory = self.inventory
        # Does this logical path already exist?
        if logical_path in inventory.current_version.logical_paths:
            raise NewVersionException("Logical path %s already exists in new version %s" % (logical_path, inventory.head))
        # Work out digest, add to state
        digest = file_digest(src_path, inventory.digest_algorithm, pyfs=self.src_fs)
        inventory.current_version.state[digest] = [logical_path]
        # Work out whether we already have this content in the current
        # and or previous versions, as a basis to work out whether we want
        # to add a content file
        in_previous_version = False
        in_current_version = False
        existing_paths = inventory.content_paths_for_digest(digest)
        for path in existing_paths:
            if path.startswith(inventory.head + "/"):
                in_current_version = True
            else:
                in_previous_version = True
        # If there is no copy of this content then we add, but we might also
        # add extra copies depending on forward_delta and dedupe settings
        if ((not in_previous_version and not in_current_version)  # pylint: disable=too-many-boolean-expressions
                or (not in_current_version and not self.forward_delta)
                or (in_current_version and not self.dedupe)):
            # Yes, we copy this file in...
            self.files_to_copy[src_path] = content_path
            inventory.add_file(digest=digest, content_path=content_path)

    def delete(self, logical_path):
        """Delete a logical path from this new version.

        This is likely to be used when constructing a new version starting from
        the previous state (initialization with carry_content_forward=True).

        Assumes that the content is used in a previous version to will not
        check to delete content from the manifest. Thus add_content() followed
        but delete_content() could leave the new version in a bad state.

        Arguments:
            logical_path (str): logical path that should not appear in the new
                version state

        Raises:
            NewVersionException: if the logical path doesn't exist in the new
                version state
        """
        inventory = self.inventory
        try:
            inventory.current_version.delete_logical_path(logical_path)
        except InventoryException:
            raise NewVersionException("Cannot delete logical path %s that does not exist in new version %s" % (logical_path, inventory.head))

    def rename(self, old_logical_path, new_logical_path):
        """Rename content in the version state to a new logical_path.

        Arguments:
            old_logical_path (str): logical path that should be renamed
            new_logical_path (str): new logical path to replace old_logical_path

        Raises:
            NewVersionException: if the old logical path doesn't exist in the
                new version state, or if the new logical path already exists
        """
        inventory = self.inventory
        if new_logical_path in inventory.current_version.logical_paths:
            raise NewVersionException("Cannot rename to logical path %s that already exists in new version %s" % (new_logical_path, inventory.head))
        try:
            digest = inventory.current_version.delete_logical_path(old_logical_path)
            if digest in inventory.current_version.state:
                inventory.current_version.state[digest].append(new_logical_path)
            else:
                inventory.current_version.state[digest] = [new_logical_path]
        except InventoryException:
            raise NewVersionException("Cannot rename logical path %s that does not exist in new version %s" % (old_logical_path, inventory.head))
