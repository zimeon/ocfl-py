"""NewVersion class to assemble what will become a new Object version."""

from .digest import file_digest
from .pyfs import pyfs_openfs


class NewVersionException(Exception):
    """Exception class for NewVersion objects."""


class NewVersion():
    """Class to represent a new version to be added to and Object."""

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
        """
        self.inventory = inventory
        self.objdir = objdir
        self.srcdir = srcdir
        self.src_fs = None
        self.forward_delta = forward_delta
        self.dedupe = dedupe
        self.old_digest_algorithm = old_digest_algorithm
        self.files_to_copy = {}  # dict: srcpath -> objpath
        self._start_new_version(carry_content_forward=carry_content_forward,
                                metadata=metadata)

    def _start_new_version(self, *, metadata, carry_content_forward):
        """Start the new version by adjusting inventory.

        If carry_conten_forward is set then the state block of the previous
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

    def delete_content(self, logical_path):
        pass

    def add_content(self, src_path, content_path, logical_path):
        """Add a file to the new version.

        Arguments:
            src_path (str): path within the source directory specified on
                creation
            logical_fileparh (str): logical filepath that this content should
                have within the version of the object
        """
        inventory = self.inventory
        # Does this logical path already exist?
        if logical_path in inventory.current_version.logical_paths:
            raise NewVersionException("Logical path %s already exists in new version %s" % (logical_path, inventory.head))
        # Does this content (digest) already exist?
        digest = file_digest(src_path, inventory.digest_algorithm, pyfs=self.src_fs)
        if digest in inventory.manifest:
            if not self.forward_delta:
                # Already present but we don't dedupeEither new or we don
                pass
        else:
            # New content
            inventory.add_file(digest, content_path)
            inventory.current_version.state[digest] = [logical_path]

    def replace_content(self, file):
        pass
