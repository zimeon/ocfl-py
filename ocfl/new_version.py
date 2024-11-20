"""NewVersion class to assemble what will become a new Object version.

It is expected that instances of this class will only be created
and used through ocfl.Object, see the start_new_version() and
write_new_version() methods.
"""
import copy
import hashlib
import logging
from urllib.parse import quote as urlquote

import fs.path

from .constants import DEFAULT_DIGEST_ALGORITHM, DEFAULT_CONTENT_DIRECTORY
from .digest import file_digest
from .inventory import Inventory, InventoryException
from .object_utils import make_unused_filepath
from .pyfs import pyfs_openfs


class NewVersionException(Exception):
    """Exception class for NewVersion objects."""


class NewVersion():
    """Class to represent a new version to be added to an Object."""

    def __init__(self, *,
                 inventory=None,
                 objdir=None,
                 srcdir=None,
                 metadata=None,
                 digest_algorithm=None,
                 content_directory=None,
                 content_path_normalization="uri",
                 carry_content_forward=True,
                 forward_delta=True,
                 dedupe=False,
                 old_digest_algorithm=None):
        """Create NewVersion object.

        Arguments:
            inventory (ocfl.Inventory): inventory that we will modify to build
                the new version.
            content_path_normalization (str): the path normalization strategy
                to use with content paths when files are added to this object
                (default "uri")
            carry_content_forward (bool): True to carry forward the state from
                the last current version as a starting point. False to start
                with empty version state.

        Example use:

        >>> # Prep:
        >>> # mkdir tmp
        >>> # cp -rp fixtures/1.1/good-objects/spec-ex-full tmp/spec-ex-full
        >>>
        >>> import ocfl
        >>> object = ocfl.Object()
        >>> nv = object.start_new_version(objdir="tmp/spec-ex-full", carry_content_forward=True)
        >>> nv.inventory.current_version.logical_paths
        ['foo/bar.xml', 'empty2.txt', 'image.tiff']
        >>> nv.delete("foo/bar.xml")
        >>> nv.rename("empty2.txt", "empty3.txt")
        >>> nv.add("fixtures/1.1/content/README.md", "readme", "v4/readme")
        >>> object.write_new_version(nv)
        INFO:root:Updated OCFL object ark:/12345/bcd987 in tmp/spec-ex-full by adding v4
        <ocfl.inventory.Inventory object at 0x1014e6cd0>
        """
        # Configuration
        self.inventory = inventory
        self.objdir = objdir
        self.srcdir = srcdir
        self.src_fs = None
        self.content_path_normalization = content_path_normalization
        self.forward_delta = forward_delta
        self.dedupe = dedupe
        # Additional state needed for final commit
        self.old_digest_algorithm = old_digest_algorithm
        self.files_to_copy = {}  # dict: src_path -> content_path
        if inventory is None:
            self._start_first_version(digest_algorithm=digest_algorithm,
                                      content_directory=content_directory,
                                      metadata=metadata)
        else:
            self._start_next_version(carry_content_forward=carry_content_forward,
                                     metadata=metadata)
        self.src_fs = pyfs_openfs(self.srcdir)

    def _start_first_version(self, *,
                             digest_algorithm=None,
                             content_directory=None,
                             metadata):
        """Start the first version for this object.

        Arguments:
            digest_algorithm (str or None):
            content_directort (str or None):
        """
        inventory = Inventory()
        inventory.add_version(metadata=metadata)  # also sets head "v1"
        if digest_algorithm is None:
            digest_algorithm = DEFAULT_DIGEST_ALGORITHM
        inventory.digest_algorithm = digest_algorithm
        if (content_directory is not None
                and content_directory != DEFAULT_CONTENT_DIRECTORY):
            inventory.content_directory = content_directory
        self.inventory = inventory

    def _start_next_version(self, *, metadata, carry_content_forward=False):
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

    @property
    def content_directory(self):
        """Get content directory catering for default."""
        return self.inventory.content_directory_to_use

    def _map_filepath(self, filepath):
        """Map source filepath to a content path within the object.

        The purpose of the mapping might be normalization, sanitization,
        content distribution, or something else. The mapping is set by the
        content_path_normalization attribute where None indicates no mapping, the
        source file name and path are preserved.

        Arguments:
            filepath: the source filepath (possibly including directories) that
                will be mapped into the object content path.

        Returns:
            str: the full content path for this content that starts
                with `vdir/content_directory/`.
        """
        if self.content_path_normalization == "uri":
            filepath = urlquote(filepath)
            # also encode any leading period to unhide files
            if filepath[0] == ".":
                filepath = "%2E" + filepath[1:]
        elif self.content_path_normalization == "md5":
            # Truncated MD5 hash of the _filepath_ as an illustration of diff
            # paths for the specification. Not sure whether there should be any
            # real application of this
            filepath = hashlib.md5(filepath.encode("utf-8")).hexdigest()[0:16]
        elif self.content_path_normalization is not None:
            raise NewVersionException("Unknown filepath normalization '%s' requested"
                                      % (self.content_path_normalization))
        vfilepath = fs.path.join(self.inventory.head, self.content_directory, filepath)  # path relative to root, inc v#/content
        # Check we don't already have this vfilepath from many to one
        # normalization, add suffix to distinguish if necessary
        used = self.inventory.content_paths
        if vfilepath in used:
            vfilepath = make_unused_filepath(vfilepath, used)
        return vfilepath

    def add(self, src_path, logical_path, content_path=None):
        """Add a file to the new version.

        Arguments:
            src_path (str): path within the source directory specified on
                creation
            logical_path (str): logical filepath that this content should
                have within the version of the object
        """
        inventory = self.inventory
        if content_path is None:
            content_path = self._map_filepath(src_path)
        elif not content_path.startswith(inventory.head + "/" + self.content_directory + "/"):
            raise NewVersionException("Bad content path %s, must start with version directory and content directory path elements"
                                      % (content_path))
        elif content_path in inventory.content_paths:
            raise NewVersionException("Bad content path %s, already exists!"
                                      % (content_path))
        logging.debug("add(%s %s %s)", src_path, content_path, logical_path)
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
        check to delete content from the manifest. Thus add() followed
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
