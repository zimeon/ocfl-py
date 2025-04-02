"""NewVersion class to assemble what will become a new Object version.

It is expected that instances of this class will only be created
and used through ocfl.Object, see the start_new_version() and
write_new_version() methods.
"""
import copy
import hashlib
import logging
import os.path
from urllib.parse import quote as urlquote

import fs.path

from .constants import DEFAULT_DIGEST_ALGORITHM, DEFAULT_CONTENT_DIRECTORY, DEFAULT_SPEC_VERSION
from .digest import file_digest
from .inventory import Inventory, InventoryException
from .object_utils import make_unused_filepath
from .pyfs import pyfs_openfs


class NewVersionException(Exception):
    """Exception class for NewVersion objects."""


class NewVersion():
    """Class to represent a new version to be added to an Object."""

    def __init__(self, *, srcdir="."):
        """Create NewVersion object.

        Arguments:
            srcdir (str): source directory name for files that will be added
                to this new version. May be a pyfs filesystem specification.
                Default is "."

        The default constructor is not expected to be used directly, see
        NewVersion.first_version(...) and NewVersion.next_version(..) for the
        two cases in which a new version can be created.
        """
        # Configuration
        self.inventory = None
        self.srcdir = srcdir
        self.src_fs = None
        self.content_path_normalization = None
        self.forward_delta = None
        self.dedupe = None
        # Additional state needed for final commit
        self.old_digest_algorithm = None
        self.files_to_copy = {}  # dict: src_path -> content_path
        self.src_fs = pyfs_openfs(self.srcdir)

    @classmethod
    def first_version(cls, *,
                      srcdir=".",
                      identifier,
                      spec_version=DEFAULT_SPEC_VERSION,
                      digest_algorithm=None,
                      content_directory=None,
                      metadata=None,
                      dedupe=False,
                      fixity=None,
                      content_path_normalization="uri"):
        """Start the first version for this object.

        Arguments:
            srcdir (str): source directory name for files that will be added
                to this new version. May be a pyfs filesystem specification
            identifier (str): identifier of the object to be created
            spec_version (str): the specification version that the new version
                should be created in accord with. Defaults to
                ocfl.constants.DEFAULT_SPEC_VERSION
            digest_algorithm (str or None): the digest algorithm to use for
                content addressing. If None (default) then will use the value
                ocfl.constants.DEFAULT_DIGEST_ALGORITHM
            content_directory (str or None): the content directory name. If
                None (default) then will use the value "content" (as set in
                ocfl.constants.DEFAULT_CONTENT_DIRECTORY)
            dedupe (bool): True to deduplicate files within this
                version, meaning that only one copy of a given file will be
                included in the content directory even if there are multiple
                copies in the new version state. If False then will store
                multiple copies. Defaults to False.
            metadata (ocfl.VersionMetadata or None): if an ocfl.VersionMetadata
                object is provided then this is used to set the metadata of the
                new version. The setters .created, .message, .user_address and
                .user_name may alternatively be used
            fixity (None or list of str): If a list then will be interpretted as
                the set of fixity digest types to be added for all content files
                in this version
            content_path_normalization (str): the path normalization strategy
                to use with content paths when files are added to this object
                (default "uri")

        Example use:

        >>> import ocfl
        >>> nv = ocfl.NewVersion.first_version(identifier="http://example.org/minimal")
        >>> nv.add("fixtures/1.1/good-objects/spec-ex-minimal/v1/content/file.txt", "file.txt")
        >>> nv.created = "2018-10-02T12:00:00Z"
        >>> nv.message = "One file"
        >>> nv.user_address = "mailto:alice@example.org"
        >>> nv.user_name = "Alice"
        >>> print(nv.inventory.as_json())
        {
          "digestAlgorithm": "sha512",
          "head": "v1",
          "id": "http://example.org/minimal",
          "manifest": {
            "7545b8720a601235067473f2c87f43461f5c147fb622d51bfcdcda05e0773c96e9f922f4d88d371bb7f87793b655b9e1c3b8bbca35f2950c5c87eda955179f67": [
              "v1/content/fixtures/1.1/good-objects/spec-ex-minimal/v1/content/file.txt"
            ]
          },
          "type": "https://ocfl.io/1.1/spec/#inventory",
          "versions": {
            "v1": {
              "created": "2018-10-02T12:00:00Z",
              "message": "One file",
              "state": {
                "7545b8720a601235067473f2c87f43461f5c147fb622d51bfcdcda05e0773c96e9f922f4d88d371bb7f87793b655b9e1c3b8bbca35f2950c5c87eda955179f67": [
                  "file.txt"
                ]
              },
              "user": {
                "address": "mailto:alice@example.org",
                "name": "Alice"
              }
            }
          }
        }
        """
        self = cls(srcdir=srcdir)
        inventory = Inventory()
        self.inventory = inventory
        self.dedupe = dedupe
        inventory.id = identifier
        inventory.spec_version = spec_version
        inventory.digest_algorithm = digest_algorithm
        inventory.init_manifest_and_versions()
        # Add contentDirectory if not "content"
        if self.content_directory != DEFAULT_CONTENT_DIRECTORY:
            inventory.content_directory = self.content_directory
        # Add fixity section if requested
        if fixity is not None and len(fixity) > 0:
            for fixity_type in fixity:
                inventory.add_fixity_type(fixity_type)
        #
        inventory.add_version(metadata=metadata)  # also sets head "v1"
        if digest_algorithm is None:
            digest_algorithm = DEFAULT_DIGEST_ALGORITHM
        inventory.digest_algorithm = digest_algorithm
        if (content_directory is not None
                and content_directory != DEFAULT_CONTENT_DIRECTORY):
            inventory.content_directory = content_directory
        self.content_path_normalization = content_path_normalization
        return self

    @classmethod
    def next_version(cls, *,
                     inventory,
                     srcdir=".",
                     spec_version=DEFAULT_SPEC_VERSION,
                     metadata=None,
                     content_path_normalization="uri",
                     forward_delta=True,
                     dedupe=True,
                     carry_content_forward=False,
                     old_digest_algorithm=None):
        """Start the new version by adjusting inventory.

        If carry_content_forward is set then the state block of the previous
        version is copied forward into the new version. Items may later be
        added or deleted.

        Arguments:
            inventory (ocfl.Inventory): inventory that we will modify to build
                the new version.
            srcdir (str): source directory name for files that will be added
                to this new version. May be a pyfs filesystem specification
            metadata (ocfl.VersionMetadata or None): Either a VersionMetadata
                object to set the metadata for the new version, None to not set
                metadata
            content_path_normalization (str): the path normalization strategy
                to use with content paths when files are added to this object
                (default "uri")
            forward_delta (bool): True (default) to use forward delta strategy
                for files in the new version, meaning that only files not
                present in a previous version will be added in the content
                directory of this new version. If False the all files that are
                part of this version's state will be added in the content
                directory
            dedupe (bool): True (defult) to deduplicate files within this
                version, meaning that only one copy of a given file will be
                included in the content directory even if there are multiple
                copies in the new version state. If False then will store
                multiple copies
            carry_content_forward (bool): True to carry forward the state from
                the last current version as a starting point. False to start
                with empty version state.
            old_digest_algorithm (str): Can be used to record the digest
                algorithm of the previous version so that the root inventory
                sidecar is cleaned up when writing the new inventory in the
                object root. The value is not used within NewVerion code.
                Default is None

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
        self = cls(srcdir=srcdir)
        self.inventory = inventory
        self.content_path_normalization = content_path_normalization
        self.forward_delta = forward_delta
        self.dedupe = dedupe
        self.old_digest_algorithm = old_digest_algorithm
        state = {}
        if spec_version != inventory.spec_version:
            # Check we are upgrading
            if spec_version < inventory.spec_version:
                raise NewVersionException("Must not create new version with lower spec version (%s) than last version (%s)"
                                          % (spec_version, inventory.spec_version))
            inventory.spec_version = spec_version
        if carry_content_forward:
            state = copy.deepcopy(self.inventory.current_version.state)
        self.inventory.add_version(state=state, metadata=metadata)
        return self

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

    def add(self, src_path, logical_path, content_path=None, src_path_has_prefix=False):  # pylint: disable=unused-argument
        """Add a file to the new version.

        Arguments:
            src_path (str): path within the source directory specified on
                creation
            logical_path (str): logical filepath that this content should
                have within the version of the object
            content_path (str or None): if None (default) then will generate a
                content path based on the src_path and the
                content_path_normalization strategy selected. Otherwise will
                use the speficied content path provided is in the current
                versions content directory (must start with
                "vdir/content_directory/") and doesn't already exist in the
                object

        Raises:
            NewVersionException: if the specifies content path is not allowed
        """
        inventory = self.inventory
        prefix = inventory.head + "/" + self.content_directory + "/"
        if content_path is None:
            # src_path = src_path if src_path_has_prefix else prefix + src_path
            content_path = self._map_filepath(src_path)
        elif not content_path.startswith(prefix):
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
        if digest in inventory.current_version.state_add_if_not_present():
            inventory.current_version.state[digest].append(logical_path)
        else:
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
            inventory.add_file_to_manifest(digest=digest, content_path=content_path)

    def delete(self, logical_path):
        """Delete a logical path from this new version.

        This is likely to be used when constructing a new version starting from
        the previous state (initialization with carry_content_forward=True).

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

    def add_from_srcdir(self):
        """Add all content from srcdir."""
        for src_path in sorted(self.src_fs.walk.files()):
            src_path = os.path.relpath(src_path, "/")
            self.add(src_path, src_path, src_path_has_prefix=False)

    @property
    def created(self):
        """Created string for this version."""
        return self.inventory.current_version.created

    @created.setter
    def created(self, value):
        """Set created string for this version."""
        self.inventory.current_version.created = value

    @property
    def message(self):
        """Message string for this version."""
        return self.inventory.current_version.message

    @message.setter
    def message(self, value):
        """Set message string for this version."""
        self.inventory.current_version.message = value

    @property
    def user_address(self):
        """User_address string for this version."""
        return self.inventory.current_version.user_address

    @user_address.setter
    def user_address(self, value):
        """Set user_address string for this version."""
        self.inventory.current_version.user_address = value

    @property
    def user_name(self):
        """user_name string for this version."""
        return self.inventory.current_version.user_name

    @user_name.setter
    def user_name(self, value):
        """Set user_name string for this version."""
        self.inventory.current_version.user_name = value
