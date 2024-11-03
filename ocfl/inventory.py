"""OCFL Inventory and Version.

The storage mechanism for the inventory data is the python dict()
structure resulting from reading the inventory JSON file and suitable
for writing an inventory JSON file. Here we provide convenient
property based access to read and set this data safely without
needing such intimate knowledge of the JSON format.
"""
import copy
import json
import os.path
import re

from .digest import normalized_digest
from .object_utils import first_version_directory, next_version_directory, \
    parse_version_directory, make_unused_filepath
from .pyfs import pyfs_openfile


class InventoryException(Exception):
    """Exception class for Inventory class."""


class Inventory():  # pylint: disable=too-many-public-methods
    """Class wrapping OCFL inventory data.

    In general, the property accessors and methods return None if the
    attribute is a string that is not set in the underlying data, else
    the value if it is. In the cases that the normal return value would
    be an array or a dict, then and empty array or empty dict are returned
    if not present in the underlying data.

    Instance attributes:
        data: dict that is the top level JSON object of the parsed JSON
            representation of the inventory file. This is the only place
            that an Inventory instance stores information.
    """

    def __init__(self, data=None, filepath=None, pyfs=None):
        """Initialize Inventory object.

        Argument:
            data: If not None (default) the must be either an Inventory
                object or inventory data to initialise from. In either
                case the underlying data is deep copied to create a separate
                new object.
            filepath: If not None then the string file path from which to
                read a JSON inventory file to initialize from.
            pyfs: pyfs object for the filesystem to use, else None to use the
                local filesystem (default). filepath is interpretted within
                pyfs
        """
        if data is None:
            if filepath is None:
                self.data = {}
            else:
                with pyfs_openfile(filepath, "r", pyfs=pyfs, encoding="utf-8") as fh:
                    self.data = json.load(fh)
        elif isinstance(data, Inventory):
            self.data = copy.deepcopy(data.data)
        elif isinstance(data, dict):
            self.data = data
        else:
            raise InventoryException("Bad data type supplied to Inventory() creator, " + str(type(data)))

    @property
    def spec_version(self):
        """Get specification version from the conformance declaration."""
        decl = self.data.get("type", "")
        m = re.match(r"""https://ocfl.io/(\d+.\d)/spec/#inventory""", decl)
        if m:
            return m.group(1)
        return None

    @spec_version.setter
    def spec_version(self, value):
        """Set specification version in the conformance declaration."""
        self.data["type"] = "https://ocfl.io/" + value + "/spec/#inventory"

    @property
    def digest_algorithm(self):
        """Get digest algorithm."""
        return self.data.get("digestAlgorithm")

    @digest_algorithm.setter
    def digest_algorithm(self, value):
        """Set digest algorithm."""
        self.data["digestAlgorithm"] = value

    @property
    def id(self):
        """Get object id."""
        return self.data.get("id")

    @id.setter
    def id(self, value):
        """Set object id."""
        self.data["id"] = value

    @property
    def head(self):
        """Get head version directory."""
        return self.data.get("head")

    @head.setter
    def head(self, value):
        """Set head version directory."""
        self.data["head"] = value

    @property
    def content_directory(self):
        """Get contentDirectory."""
        return self.data.get("contentDirectory")

    @property
    def content_directory_to_use(self):
        """Get contentDirectory to use, default 'content' is not specified."""
        return self.data.get("contentDirectory", "content")

    @content_directory.setter
    def content_directory(self, value):
        """Set the contentDirectory."""
        self.data["contentDirectory"] = value

    @property
    def manifest(self):
        """Get the manifest of digests and corresponding content paths.

        Returns dict of digest -> [file paths], an empty dict is there
        is no manifest.
        """
        return self.data.get("manifest", {})

    @manifest.setter
    def manifest(self, value):
        """Set the manifest to the supplied dict()."""
        self.data["manifest"] = value

    @property
    def manifest_add_if_not_present(self):
        """Get the manifest of digests and corresponding content paths.

        Returns dict of digest -> [file paths]. As a side effect will create
        an empty dict in the data structure if none was present, so that new
        data can be added.
        """
        if "manifest" not in self.data:
            self.data["manifest"] = {}
        return self.data["manifest"]

    @property
    def fixity(self):
        """Get fixity block as dict().

        Returns fixity block else an empty dict() if there is no fixity block.
        """
        return self.data.get("fixity", {})

    @fixity.setter
    def fixity(self, value):
        """Set the fixity to the supplied dict()."""
        self.data["fixity"] = value

    @property
    def content(self):
        """Get all the content paths and their digests stored within the object.

        Returns a dictionary of content paths with values that are the
        digests for each file. Essentially an inversion of the manifest.
        """
        files = {}
        for digest, files_for_digest in self.manifest.items():
            for file in files_for_digest:
                files[file] = digest
        return files

    @property
    def content_paths(self):
        """Get all the content paths.

        Returns a list of content paths for all files in the object. Will
        be and empty list if there is no content.
        """
        paths = []
        for files in self.manifest.values():
            paths += files
        return paths

    @property
    def versions_block(self):
        """Dict of the versions block.

        Returns a dict whether or not there is a versions block in the
        underlying data.
        """
        return self.data.get("versions", {})

    @versions_block.setter
    def versions_block(self, value):
        """Set dict of the versions block."""
        self.data["versions"] = value

    @property
    def version_directories(self):
        """List of all version directories.

        Returns a list of all version in the versions block. The values
        in the list are the version directory names so they will have
        the "v" prefix and may or may not be zero padded.

        See also: inv.version_numbers for just the numbers: [1, 2, 3].
        """
        return list(self.versions_block.keys())

    @property
    def version_numbers(self):
        """List of all version numbers as integers."""
        vnums = []
        for vdir in self.version_directories:
            vnums.append(parse_version_directory(vdir))
        return vnums

    def versiondata(self, vdir):
        """Return data for the version in vdir.

        Returns a dict whether or not any data exists.
        """
        return self.versions_block.get(vdir, {})

    def version(self, vdir):
        """Version object for the specified version directory."""
        return Version(self, vdir)

    def versions(self):
        """Generate Version objects for each version.

        Yields a Version() object for each version in this Inventiry in
        numeric order.
        """
        for vdir in sorted(self.version_directories, key=parse_version_directory):
            yield Version(self, vdir)

    def digest_for_content_path(self, path):
        """Return digest corresponding to specified content path.

        Argument:
            path: string of content path

        Returns None if the content path is not specified in the
        manifest, else the path string.
        """
        for digest, paths in self.manifest.items():
            if path in paths:
                return digest
        return None

    def content_paths_for_digest(self, digest):
        """Content paths for the given digest.

        Returns a list of content paths or and empty list if there
        isn't one for the given digest. The list is used because there
        may be more than one content path for the given digest.
        """
        return self.manifest.get(digest, [])

    def content_path_for_digest(self, digest):
        """Content path for the given digest.

        Arguments:
            digest: string value of digest

        Returns a content path or None if there isn't one for the
        given digest. There may actually be more than one content
        path for the given digest, we return the first in the
        underlying data.
        """
        paths = self.content_paths_for_digest(digest)
        if len(paths) > 0:
            return paths[0]
        return None

    def _next_version_directory(self, zero_padded_width=None):
        """Work out next version directory.

        Arguments:
            zero_padded_width: an integer to set the number if digits
                used for zero padded identifiers, else None (default)

        Returns the next version directory name as a string, based on the
        set of existing versions in this inventory. Will only use the
        zero_padded_width setting if there are no current versions and thus
        we are creating the first version directory name.

        Raises InventoryException if the value of zero_padded_width doesn't
        make sense,
        """
        # Find higest version and add one to get next version number
        highest_version = 0
        vdir = None
        for vdir in self.version_directories:
            highest_version = max(highest_version,
                                  parse_version_directory(vdir))
        if highest_version == 0:
            return first_version_directory(zero_padded_width)
        return next_version_directory(vdir)

    def add_version(self, vdir=None, metadata=None, state=None,
                    zero_padded_width=None):
        """Add new version object to the versions block.

        Arguments:
            vdir: string with the version directory name (e.g. "v1" or "v0006").
                If None then will create the next version in sequence
            metadata: dict to initialize version metadata with, else None to
                create empty (default)
            state: either a dict with the state block for the version, an
                object with an as_dict() method to producde such a
                dictionary (e.g. from VersionMetadat), else None (default)
            zero_padded_width: an integer to set the number if digits
                used for zero padded identifiers, else None (default). Applies
                only when creating first version

        Returns a Version object that may be used to access version properties.
        """
        # Work out the new version directory if not specified
        if vdir is None:
            vdir = self._next_version_directory(zero_padded_width=zero_padded_width)
        # Add the new version information
        if "versions" not in self.data:
            self.data["versions"] = {}
        if metadata is None:
            self.data["versions"][vdir] = {}
        elif isinstance(metadata, dict):
            self.data["versions"][vdir] = metadata
        else:
            self.data["versions"][vdir] = metadata.as_dict()
        if state is not None:
            self.data["versions"][vdir]["state"] = state
        # Update head to point to the newly added version
        self.head = vdir
        return self.version(vdir)

    def add_file(self, *, digest, content_path):
        """Add file to the manifest.

        Arguments:
            digest: the digest string computed with the specified digest
                algorithm.
            content_path: the full content path including version directory,
                content directory, and the path with the content directory.

        Adds and entry to the manifest with the specified digest and the
        specified content_path. Takes account of mutliple content paths with
        the same digest.

        Raises and InventoryException if there is an attempt to add a
        content_path that is already included.

        WARNING: Does not check that the content path is valid in that it
        is within an extant version director, or that it is within the
        specified content_directory for a version.

        See also: Version.add_file() to add a file with logical_path in the
        context of a specific version.
        """
        if content_path in self.content_paths:
            raise InventoryException("Attempt to add a content path that already exists: %s" % content_path)
        # Does this digest already exist?
        if digest in self.manifest_add_if_not_present:
            # Yes, add to file list
            self.manifest[digest].append(content_path)
        else:
            # No, new manifest etry
            self.manifest[digest] = [content_path]

    def as_json(self):
        """Serlialize JSON representation."""
        return json.dumps(self.data, sort_keys=True, indent=2)

    def write_json(self, fh):
        """Serialise JSON representation to file.

        Arguments:
            fh - filehandle to write to
        """
        json.dump(self.data, fh, sort_keys=True, indent=2)

    def init_manifest_and_versions(self):
        """Initialize manifest and versions blocks for building new inventory."""
        self.manifest = {}
        self.versions_block = {}

    def add_fixity_type(self, digest_algorithm, map=None):
        """Add fixity type with no file data.

        Arguments:
            digest_algorithm: string of the digest algorithm specifying this
                fixity type
            map: None (default) to create an empty entry for the specified
                digest algorithm, else a dict() with mapping from digest
                to array of files according to the specified digest algorithm

        If there is no fixity data then will start a fixity block.
        """
        if "fixity" not in self.data:
            self.data["fixity"] = {}
        self.data["fixity"][digest_algorithm] = {} if map is None else map

    def add_fixity_data(self, digest_algorithm, digest, filepath):
        """Add fixity information for a file.

        Arguments:
            digest_algorithm: string of the digest algorithm specifying this
                fixity type

        Assumes that there is already fixity block and within that a block for
        the specific digest_algorithm.
        """
        fixities = self.fixity[digest_algorithm]
        if digest not in fixities:
            fixities[digest] = [filepath]
        else:
            fixities[digest].append(filepath)

    def normalize_digests(self, digest_algorithm=None):
        """Normalize the digests used in manifest and state.

        Arguments:
            digest_algorithm: string with the name of the digest algorithm
                used

        No arguments and no return value. Operates on the current object
        in-place, normalizing the digest values use in the manifest and
        state blocks. Does not change any separate fixity information.
        """
        from_to = {}
        manifest = self.manifest
        for digest in manifest:
            norm_digest = normalized_digest(digest, digest_algorithm)
            if digest != norm_digest:
                from_to[digest] = norm_digest
        for (digest, norm_digest) in from_to.items():
            manifest[norm_digest] = manifest.pop(digest)
        for v in self.versions():
            state = v.state
            from_to = {}
            for digest in state:
                norm_digest = normalized_digest(digest, digest_algorithm)
                if digest != norm_digest:
                    from_to[digest] = norm_digest
            for (digest, norm_digest) in from_to.items():
                state[norm_digest] = state.pop(digest)


class Version():
    """Version class to represent version information in an Inventory.

    The class stores only pointers to the appropriate inventory and
    version directory with the versions block. These are used to access
    data in the inventory.
    """

    def __init__(self, inv, vdir):
        """Initialize Version object.

        Arguments:
            inv: Inventory object for which this is one version.
            vdir: Version directory string for the version of interest.
        """
        self.inv = inv
        self.vdir = vdir

    @property
    def created(self):
        """Created string for this version."""
        return self.inv.versiondata(self.vdir).get("created")

    @created.setter
    def created(self, value):
        """Set created string for this version."""
        self.inv.versiondata(self.vdir)["created"] = value

    @property
    def message(self):
        """Message string for this verion."""
        return self.inv.versiondata(self.vdir).get("message")

    @message.setter
    def message(self, value):
        """Set message string for this version."""
        self.inv.versiondata(self.vdir)["message"] = value

    @property
    def state(self):
        """State block for this version.

        Returns a dict for the state block or and empty dict if
        there is no state block.
        """
        return self.inv.versiondata(self.vdir).get("state", {})

    @state.setter
    def state(self, value):
        """Set state block for this version."""
        self.inv.versiondata(self.vdir)["state"] = value

    @property
    def state_add_if_not_present(self):
        """State block for this version.

        Returns a dict for the state block.As a side effect will create
        an empty dict in the data structure if none was present, so that new
        data can be added.
        """
        if "state" not in self.inv.versiondata(self.vdir):
            self.inv.versiondata(self.vdir)["state"] = {}
        return self.inv.versiondata(self.vdir)["state"]

    @property
    def user(self):
        """User block for this version."""
        return self.inv.versiondata(self.vdir).get("user", {})

    @property
    def user_add_if_not_present(self):
        """User block for this version, add if not present."""
        if "user" not in self.inv.versiondata(self.vdir):
            self.inv.versiondata(self.vdir)["user"] = {}
        return self.inv.versiondata(self.vdir)["user"]

    @property
    def user_address(self):
        """Address element in the user description for this version.

        Returns a string or None is there is no name.
        """
        return self.user.get("address")

    @user_address.setter
    def user_address(self, value):
        """Set address element in the user description for this version."""
        self.user_add_if_not_present["address"] = value

    @property
    def user_name(self):
        """Name element in the user description for this version.

        Returns a string or None is there is no name.
        """
        return self.user.get("name")

    @user_name.setter
    def user_name(self, value):
        """Set name element in the user description for this version."""
        self.user_add_if_not_present["name"] = value

    @property
    def logical_paths(self):
        """List of the logical paths in this version.

        Returns a list, will be empty if there are no logical paths.
        """
        paths = []
        for files in self.state.values():
            paths += files
        return paths

    @property
    def number(self):
        """Version number for this version.

        See also vdir attribute for version directory name.
        """
        return parse_version_directory(self.vdir)

    def digest_for_logical_path(self, path):
        """Digest for the given logical path in this version.

        Return digest string or None is path not found.
        """
        for digest, paths in self.state.items():
            if path in paths:
                return digest
        return None

    def content_path_for_logical_path(self, path):
        """Content path for the file in this version for the logical path.

        Note that there could be more than one content path with the
        digest. Here we just return the first one. Returns None if there
        no matching content path.
        """
        digest = self.digest_for_logical_path(path)
        if digest is None:
            return None
        return self.inv.content_path_for_digest(digest)

    def add_file(self, *, digest, logical_path, content_path=None, dedupe=True):
        """Add information for a file with given digest in this version.

        Arguments:
            digest: the file digest that must be created using the
                appropriate digestAlgorithm.
            logical_path: path within the state for this version.
            content_path: local content path to be used if a file is created
                within this version. If not specified then the logical_path name
                will be used as the basis.
            dedupe: bool, True (default) to not add files for which there is
                already a file with the same digest, False to add anyway

        Returns the full content path (including vdir and content directory) of
        the file added, else None if no file was added. Makes changes to both
        the state for this version and the inventory manifest.

        Raises an InventoryException if there is an attempt to add a logical
        path that already exists in this version.
        """
        # Check logical_file not already present
        if logical_path in self.logical_paths:
            raise InventoryException("Logical path already exists in this version: %s" % logical_path)
        # Do we have any files with this digest already?
        files = self.inv.content_paths_for_digest(digest)
        if len(files) == 0 or not dedupe:
            # Add the file because no match exists or we don't want to dedupe
            suggested = os.path.join(self.vdir,
                                     self.inv.content_directory_to_use,
                                     logical_path if content_path is None else content_path)
            content_path = make_unused_filepath(filepath=suggested,
                                                used=self.inv.content_paths)
            # Have location now, add to manifest
            self.inv.add_file(digest=digest, content_path=content_path)
        else:
            # File or files with same digest exist
            content_path = None
        # Now add to the version state
        if digest in self.state_add_if_not_present:
            self.state[digest].append(logical_path)
        else:
            self.state[digest] = [logical_path]
        return content_path
