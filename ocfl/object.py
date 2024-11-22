# -*- coding: utf-8 -*-
"""OCFL Object Implementation.

This code uses PyFilesystem2 (import fs) exclusively for access to files,
with some convenience functions in ocfl.pyfs. This enables application
beyond the operating system filesystem to include ``mem://``, ``zip://`` and
``s3://`` filesystems.
"""
import copy
import hashlib
import json
import os.path
import re
import logging
from urllib.parse import quote as urlquote

import fs
import fs.path
import fs.copy

from .constants import INVENTORY_FILENAME, DEFAULT_CONTENT_DIRECTORY
from .digest import file_digest
from .inventory import Inventory
from .inventory_validator import InventoryValidator
from .new_version import NewVersion
from .object_utils import make_unused_filepath, parse_version_directory, \
    ObjectException
from .pyfs import pyfs_openfs
from .namaste import Namaste
from .validator import Validator, ValidatorAbortException
from .version_metadata import VersionMetadata


class Object():  # pylint: disable=too-many-public-methods
    """Class for handling OCFL Object data and operations.

    Operation supported include building, updating and inspecting OCFL Objects.
    Also provides support for generating and updating OCFL inventories
    implemented via the ocfl.Inventory class.

    Example use:

    >>> import ocfl
    >>> object = ocfl.Object(path="fixtures/1.1/good-objects/spec-ex-full")
    >>> passed, validator = object.validate()
    >>> passed
    True
    >>> validator.spec_version
    "1.1"
    >>> inv = object.parse_inventory()
    >>> inv.digest_algorithm
    'sha512'
    >>> inv.version_directories
    ['v1', 'v2', 'v3']
    >>> inv.version("v1").created
    '2018-01-01T01:01:01Z'
    >>> inv.version("v1").message
    'Initial import'
    >>> inv.version("v1").user_name
    'Alice'

    Attributes:
        identifier (str): id for this object
        content_directory (str): the content directory used within this object
            (default "content")
        digest_algorithm (str): the digest algorithm used for content addressing
            within this object (default "sha512")
        content_path_normalization (str): the filepath normalization strategy to
            use when files are added to this object (default "uri")
        spec_version (str): OCFL specification version of this object
        forward_delta (bool): if True then indicates that forward delta file
            versioning should be used when files are added, not if False
        dedupe (bool): if True then indicates that files are deduped within a
            version when files are added, not if False
        lax_digests (bool): if True then digests beyond those included in the
            specification for fixity and to allow non-preferred digest algorithms
            for content references in the object will be allowed. Defaults to
            False
        fixity (list): list of fixity types to add as fixity section
        obj_fs (io.IOBase): a pyfs filesystem reference for the root of this object

    """

    def __init__(self, *, identifier=None,
                 content_directory=DEFAULT_CONTENT_DIRECTORY,
                 digest_algorithm="sha512", content_path_normalization="uri",
                 spec_version="1.1", forward_delta=True, dedupe=True,
                 lax_digests=False, fixity=None,
                 obj_fs=None, path=None, create=False):
        """Initialize OCFL object.

        Arguments:
            identifier: id for this object
            content_directory: allow override of the default "content"
            digest_algorithm: allow override of the default "sha512"
            content_path_normalization: allow override of default "uri"
            spec_version: OCFL specification version
            forward_delta: set False to turn off foward delta. With forward delta
                turned off, the same content will be repeated in a new version
                rather than simply being included by reference through the
                digest linking to the copy in the previous version
            dedupe: set False to turn off dedupe within versions. With dedupe
                turned off, the same content will be repeated within a given version
                rather than one copy being included and then a reference being used
                from the multiple logical files
            lax_digests: set True to allow digests beyond those included in the
                specification for fixity and to allow non-preferred digest algorithms
                for content references in the object
            fixity: list of fixity types to add as fixity section
            obj_fs: a pyfs filesystem for the root of this object
            path: if set then open a pyfs filesystem at path (alternative to obj_fs)
            create: set True to allow opening filesystem at path to create a directory
        """
        self.id = identifier
        self.content_directory = content_directory
        self.digest_algorithm = digest_algorithm
        self.content_path_normalization = content_path_normalization
        self.spec_version = spec_version
        self.forward_delta = forward_delta
        self.dedupe = dedupe
        self.fixity = fixity
        self.lax_digests = lax_digests
        self.src_files = {}
        self.obj_fs = obj_fs  # fs filesystem (or sub-filesystem) for object
        if path is not None:
            self.open_obj_fs(path, create=create)

    def open_obj_fs(self, objdir, create=False):
        """Open an fs filesystem for this object.

        Arguments:
            objdir: path string to either regular filesystem directory or else
                to a fs filesystem string (e.g. may be "zip://.../zipfile.zip"
                or "mem://")
            create: True to create path/filesystem as needed, defaults to False.

        Sets obj_fs attribute with the filesystem instance.

        Raises ObjectException on failure to open filesystem.
        """
        try:
            self.obj_fs = pyfs_openfs(fs_url=objdir, create=create)
        except (fs.opener.errors.OpenerError, fs.errors.CreateFailed) as e:
            raise ObjectException("Failed to open object filesystem '%s' (%s)" % (objdir, e))

    def copy_into_object(self, src_fs, srcfile, filepath, create_dirs=False):
        """Copy from srcfile to filepath in object."""
        dstpath = fs.path.dirname(filepath)
        if create_dirs and not self.obj_fs.exists(dstpath):
            self.obj_fs.makedirs(dstpath)
        fs.copy.copy_file(src_fs, srcfile, self.obj_fs, filepath)

    def map_filepath(self, filepath, vdir, used):
        """Map source filepath to a content path within the object.

        FIXME - Remove this method in favor or NewVersion._map_filepath

        The purpose of the mapping might be normalization, sanitization,
        content distribution, or something else. The mapping is set by the
        content_path_normalization attribute where None indicates no mapping, the
        source file name and path are preserved.

        Arguments:
            filepath: the source filepath (possibly including directories) that
                will be mapped into the object content path.
            vdir: the current version directory name.
            used: distionary used to check whether a given vfilepath has
                been used already.

        Returns vfilepath, the version filepath for this content that starts
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
            raise Exception("Unknown filepath normalization '%s' requested" % (self.content_path_normalization))
        vfilepath = fs.path.join(vdir, self.content_directory, filepath)  # path relative to root, inc v#/content
        # Check we don"t already have this vfilepath from many to one
        # normalization, add suffix to distinguish if necessary
        if vfilepath in used:
            vfilepath = make_unused_filepath(vfilepath, used)
        return vfilepath

    def start_inventory(self):
        """Create inventory start with metadata from self.

        Returns the start of an Inventory object based on the instance data
        in this object.
        """
        inventory = Inventory()
        inventory.id = self.id
        inventory.spec_version = self.spec_version
        inventory.digest_algorithm = self.digest_algorithm
        inventory.init_manifest_and_versions()
        # Add contentDirectory if not "content"
        if self.content_directory != DEFAULT_CONTENT_DIRECTORY:
            inventory.content_directory = self.content_directory
        # Add fixity section if requested
        if self.fixity is not None and len(self.fixity) > 0:
            for fixity_type in self.fixity:
                inventory.add_fixity_type(fixity_type)
        else:
            # Make sure None rather than just zero length
            self.fixity = None
        return inventory

    def _add_version_to_inventory(self, *,
                                  inventory, src_fs, src_dir, vdir,
                                  metadata=None):
        """Add to inventory data for new version based on files in srcdir.

        Changes the inventory data for this object but does change anything on
        storage (inventory, inventory digest files, or content files).

        Arguments:
            inventory: an Invenory object with data up to version (vdir-1)
                which must include blocks for the manifest and versions. It
                must also include a fixity block for every algorithm in
                self.fixity
            src_fs: pyfs filesystem where the new version files exist
            src_dir: the version directory in src_fs that files are being
                added from
            vdir: the version directory name of the version being added
            metadata: a VersionMetadata object with any metadata for this
                version

        Returns:
            dict: manifest_to_srcfile, a dict mapping from paths in manifest to
                the path of the source file in src_fs that should be include in
                the content for this new version.
        """
        state = {}  # state for this new version
        manifest = inventory.manifest
        digests_in_version = {}
        manifest_to_srcfile = {}
        # Go through all files to find new files in manifest and state for this version
        for filepath in sorted(src_fs.walk.files(src_dir)):
            sfilepath = os.path.relpath(filepath, src_dir)
            vfilepath = self.map_filepath(sfilepath, vdir, used=manifest_to_srcfile)
            digest = file_digest(filepath, self.digest_algorithm, pyfs=src_fs)
            # Always add file to state
            if digest not in state:
                state[digest] = []
            state[digest].append(sfilepath)
            if self.forward_delta and digest in manifest:
                # We already have this content in a previous version and we are using
                # forward deltas so do not need to copy in this one
                pass
            else:
                # This is a new digest so an addition in this version and
                # we save the information for later includes
                if digest not in digests_in_version:
                    digests_in_version[digest] = [vfilepath]
                elif not self.dedupe:
                    digests_in_version[digest].append(vfilepath)
                manifest_to_srcfile[vfilepath] = filepath

        # Add any new digests in this version to the manifest
        for digest, paths in digests_in_version.items():
            if digest not in manifest:
                manifest[digest] = paths
            else:
                for p in paths:
                    manifest[digest].append(p)
        # Add extra fixity entries if required
        if self.fixity is not None:
            for fixity_type in self.fixity:
                for digest, vfilepaths in digests_in_version.items():
                    for vfilepath in vfilepaths:
                        fixity_digest = file_digest(manifest_to_srcfile[vfilepath], fixity_type, pyfs=src_fs)
                        inventory.add_fixity_data(digest_algorithm=fixity_type,
                                                  digest=fixity_digest,
                                                  filepath=vfilepath)
        # Add this new version to inventory (also updates head)
        inventory.add_version(vdir=vdir, metadata=metadata, state=state)
        return manifest_to_srcfile

    def build_inventory(self, src_fs, versions_metadata=None):
        """Generate an OCFL inventory from a set of source files.

        Arguments:
            src_fc: pyfs filesystem of source files.
            versions_metadata: dict of VersionMetadata objects for each
                version, key is the integer version number. Default is None
                in which case no metadata is added.

        Yields (vdir, inventory, manifest_to_srcfile) for each version in
        sequence, where vdir is the version directory name, inventory is the
        Inventory object for that version, and manifest_to_srcfile is a
        dictionary that maps filepaths in the manifest to actual source
        filepaths.
        """
        if versions_metadata is None:
            versions_metadata = {}
        inventory = self.start_inventory()
        # Find the versions
        versions = {}
        for vdir in src_fs.listdir("/"):
            if not src_fs.isdir(vdir):
                continue
            try:
                vn = parse_version_directory(vdir)
                versions[vn] = vdir
            except ObjectException:
                # Ignore directories that are not valid version dirs
                pass
        # Go through versions in order building versions array, deduping
        # files to include if selected
        for vn in sorted(versions.keys()):
            vdir = versions[vn]
            # Do we have metadata for this version? Else empty.
            metadata = versions_metadata.get(vn, VersionMetadata())
            manifest_to_srcfile = self._add_version_to_inventory(inventory=inventory,
                                                                 src_fs=src_fs,
                                                                 src_dir=vdir,
                                                                 vdir=vdir,
                                                                 metadata=metadata)
            yield (vdir, inventory, manifest_to_srcfile)

    def object_declaration_object(self):
        """NAMASTE object declaration Namaste object."""
        return Namaste(0, "ocfl_object_" + self.spec_version)

    def write_object_declaration(self):
        """Write NAMASTE object declaration.

        Assumes self.obj_fs is open for this object and writes into the
        root directory of that filesystem.
        """
        self.object_declaration_object().write(pyfs=self.obj_fs)

    def write_inventory_and_sidecar(self, inventory=None, vdir=""):
        """Write inventory and sidecar to vdir in the current object.

        Arguments:
            inventory: an Inventory object to write the inventory, else None
                if only the sidecar should be written (default)
            vdir: string of the directory name within self.obj_fs that the
                inventory and sidecar should be written to. Default is ""

        Assumes self.obj_fs is open for this object. Will create vdir if that
        does not exist. If vdir is not specified then will write to root of
        the object filesystem.

        Returns the inventory sidecar filename.
        """
        if not self.obj_fs.exists(vdir):
            self.obj_fs.makedir(vdir)
        invfile = fs.path.join(vdir, INVENTORY_FILENAME)
        if inventory is not None:
            with self.obj_fs.open(invfile, "w") as fh:
                inventory.write_json(fh)
        digest = file_digest(invfile, self.digest_algorithm, pyfs=self.obj_fs)
        sidecar = fs.path.join(vdir, INVENTORY_FILENAME + "." + self.digest_algorithm)
        with self.obj_fs.open(sidecar, "w") as fh:
            fh.write(digest + " " + INVENTORY_FILENAME + "\n")
        return sidecar

    def write_inventory_sidecar(self):
        """Write just sidecare for this object's already existing root inventory file.

        Returns the inventory sidecar filename.
        """
        return self.write_inventory_and_sidecar(inventory=None)

    def build(self, srcdir, versions_metadata=None, objdir=None):
        """Build an OCFL object with multiple versions.

        Will write the object to objdir if set, else just build inventory.

        Arguments:
          srcdir: source directory with version sub-directories.
          versions_metadata: dict of VersionMetadata objects for each
              version, key is the integer version number. Default is None
              in which case no metadata is added.
          objdir: output directory for object (must not already exist), if not
              set then will just return head inventory that would have been
              created as a dry-run.

        Returns the Inventory object for the last version.

        See also create(...) for creating a new object with one version.
        """
        if self.id is None:
            raise ObjectException("Can't build object, identifier is not set!")
        if objdir is not None:
            self.open_obj_fs(objdir, create=True)
        num_versions = 0
        src_fs = pyfs_openfs(srcdir)
        inventory = None
        # Create each version of the object
        for (vdir, inventory, manifest_to_srcfile) in self.build_inventory(src_fs, versions_metadata):
            num_versions += 1
            if objdir is not None:
                self.write_inventory_and_sidecar(inventory, vdir)
                # Copy files into this version
                for (path, srcfile) in manifest_to_srcfile.items():
                    self.copy_into_object(src_fs, srcfile, path, create_dirs=True)
        # Finally populate the object root
        if objdir is not None:
            # Write object declaration, inventory and sidecar
            self.write_object_declaration()
            self.write_inventory_and_sidecar(inventory)
            logging.info("Built object %s at %s with %s versions", self.id, objdir, num_versions)
        # Whether object written or not, return the last inventory
        return inventory

    def create(self, srcdir, metadata=None, objdir=None):
        """Create a new OCFL object with v1 content from srcdir.

        Arguments:
            srcdir - source directory with content for v1.
            metadata - VersionMetadata object for v1.
            objdir - output directory for object (must not already exist), if not
                set then will just return inventory for object that would have been
                created.

        Returns the Inventory object for the last version.

        See also build(...) for building a new object with multiple versions.
        """
        if self.id is None:
            raise ObjectException("Identifier is not set!")
        src_fs = pyfs_openfs(srcdir)
        if objdir is not None:
            self.open_obj_fs(objdir, create=True)
        inventory = self.start_inventory()
        vdir = "v1"
        manifest_to_srcfile = self._add_version_to_inventory(inventory=inventory,
                                                             src_fs=src_fs,
                                                             src_dir="", vdir=vdir,
                                                             metadata=metadata)
        if objdir is None:
            return inventory
        # Write out v1 object
        self.write_inventory_and_sidecar(inventory, vdir)
        # Write object root with object declaration, inventory and sidecar
        self.write_object_declaration()
        self.write_inventory_and_sidecar(inventory)
        # Write version files
        for path in inventory.content_paths:
            srcfile = manifest_to_srcfile[path]
            self.copy_into_object(src_fs, srcfile, path, create_dirs=True)
        logging.info("Created OCFL object %s in %s", self.id, objdir)
        return inventory

    def add_version_with_content(self, objdir="", srcdir=None, metadata=None):
        """Update object by adding a new version with content matching srcdir.

        Arguments:
            objdir (str): sub-directory of the object filesystem that contains the
                object to be update. The default is "" in which case the object
                is assume to be at the filesystem root.
            srcdir: source directory with version sub-directories
            metadata: VersionMetadata object applied to all versions

        Returns:
            ocfl.Inventory: inventory of updated object

        As a first step the object is validated.

        If srcdir is None then the update will be just of metadata and any
        settings (such as using a new digest). There will be no content change
        between versions.
        """
        print("### " + str(metadata))
        new_version = self.start_new_version(objdir=objdir,
                                             srcdir=srcdir,
                                             digest_algorithm=self.digest_algorithm,
                                             fixity=self.fixity,
                                             metadata=metadata,
                                             carry_content_forward=False)
        # Add and remove any contents by comparing srcdir with existing state and manifest
        if srcdir is not None:
            src_fs = pyfs_openfs(srcdir)
            for src_path in sorted(src_fs.walk.files()):
                src_path = os.path.relpath(src_path, "/")
                obj_path = self.map_filepath(src_path, new_version.inventory.head, used={})
                new_version.add(src_path, src_path, obj_path)
        # Write the new version
        return self.write_new_version(new_version)

    def start_new_version(self, *,
                          objdir=None,
                          srcdir="",
                          digest_algorithm=None,
                          fixity=None,
                          metadata=None,
                          carry_content_forward=True):
        """Start a new version to be added to this object.

        Arguments:
            objdir (str or None): sub-directory of the object filesystem that
                contains the object to be update. The default is None in which
                case the object is assumed to be at the filesystem root of the
                currently open object filesystem.
            srcdir (str): the source directory
            digest_algorithm (str or None): the digest algorithm used for content addressing
                within the new version of this object. Default None which means use
                same digest algorithm as the last version
            fixity (list or None): list of fixity types use for the fixity section of the
                new version. Default None which means to use the same fixity digests as
                the last version
            carry_content_forward (bool): True to carry forward the state from
                the last current version as a starting point. False to start
                with empty version state.

        Returns:
            ocfl.NewVersion: object where the new version will be built before
                finally be added with write_new_version()
        """
        # Check the current object
        self.open_obj_fs(objdir)
        validator = Validator(check_digests=False, lax_digests=self.lax_digests)
        if not validator.validate_object(objdir):
            raise ObjectException("Object at '%s' is not valid, aborting" % objdir)
        inventory = self.parse_inventory()
        # Object is valid, have inventory
        #
        # Is this a request to change the digest algorithm? We implement this
        # as part of the Object class because it requires access to all
        # current object content files for potential recaclculation of digests
        old_digest_algorithm = inventory.digest_algorithm
        if digest_algorithm is None:
            digest_algorithm = old_digest_algorithm
        elif digest_algorithm != old_digest_algorithm:
            logging.info("New version with use %s instead of %s digestAlgorithm",
                         digest_algorithm, old_digest_algorithm)
            inventory.digest_algorithm = digest_algorithm
        # Is this a request to change the set of fixity information?
        old_fixity = set(inventory.fixity.keys())
        if fixity is None:
            # Not explicit, carry forward from previous version. Only change will
            # be adding old digest information if we are changing digestAlgorithm
            fixity = old_fixity.copy()
            if digest_algorithm != old_digest_algorithm and old_digest_algorithm not in old_fixity:
                # Add old manifest digests to fixity block
                inventory.add_fixity_type(digest_algorithm=old_digest_algorithm,
                                          map=inventory.manifest.copy())
                fixity.add(old_digest_algorithm)
        else:
            # Fixity to be stored is explicit, may be a change
            fixity = set(fixity)
            if fixity != old_fixity:
                for digest in old_fixity.difference(fixity):
                    inventory.fixity.pop(digest)
                for digest in fixity.difference(old_fixity):
                    logging.info("FIXME - need to add fixity with digest %s", digest)
        if fixity != old_fixity:
            logging.info("New version will have %s instead of %s fixity",
                         ",".join(sorted(fixity)), ",".join(sorted(old_fixity)))
        # Now look at contents, manifest and state
        manifest = copy.deepcopy(inventory.manifest)
        if digest_algorithm != old_digest_algorithm:
            old_to_new_digest = {}
            new_manifest = {}
            for old_digest, files in manifest.items():
                digest = file_digest(files[0], digest_algorithm, pyfs=self.obj_fs)
                old_to_new_digest[old_digest] = digest
                for file in files[1:]:
                    # Sanity check that any dupe files also match
                    d = file_digest(file, digest_algorithm, pyfs=self.obj_fs)
                    if d != digest:
                        raise ObjectException("Failed sanity check - files %s and %s should have same %s digest but calculated %s and %s respectively" %
                                              files[0], file, digest_algorithm, digest, d)
                new_manifest[digest] = manifest[old_digest]
            manifest = new_manifest
            # Now update all state blocks
            for vdir in inventory.version_directories:
                old_state = inventory.version(vdir).state
                state = {}
                for old_digest, files in old_state.items():
                    state[old_to_new_digest[old_digest]] = old_state[old_digest]
                inventory.version(vdir).state = state
        inventory.manifest = manifest
        return NewVersion.next_version(inventory=inventory,
                                       objdir=objdir,
                                       srcdir=srcdir,
                                       metadata=metadata,
                                       content_path_normalization=self.content_path_normalization,
                                       forward_delta=self.forward_delta,
                                       dedupe=self.dedupe,
                                       carry_content_forward=carry_content_forward,
                                       old_digest_algorithm=old_digest_algorithm)

    def write_new_version(self, new_version):
        """Update this object with the specified new version.

        Arguments:
            object (ocfl.NewVersion): object with new version information to be
                added

        Returns:
            ocfl.Inventory:
        """
        inventory = new_version.inventory
        # Delete old root inventory sidecar if we changed digest algorithm
        if (new_version.old_digest_algorithm is not None
                and inventory.digest_algorithm != new_version.old_digest_algorithm):
            self.obj_fs.remove(INVENTORY_FILENAME + "." + new_version.old_digest_algorithm)
        # Make new version directory
        self.obj_fs.makedir(inventory.head)
        # Copy files into this version
        for (srcpath, objpath) in new_version.files_to_copy.items():
            self.copy_into_object(new_version.src_fs, srcpath, objpath, create_dirs=True)
        # Write inventory in both root and head version
        self.write_inventory_and_sidecar(inventory, inventory.head)
        self.write_inventory_and_sidecar(inventory)
        logging.info("Updated OCFL object %s in %s by adding %s", inventory.id, new_version.objdir, inventory.head)
        return inventory

    def tree(self, objdir):
        """Build human readable tree showing OCFL object at objdir.

        Arguments:
            objdir - object directory to examine.

        Returns human readable string with tree of object structure.
        """
        def _show_indent(level, last=False, last_v=False):
            """Indent string for tree view at level for intermediate or last."""
            tree_next = "├── "
            tree_last = "└── "
            tree_pass = "│   "
            tree_indent = "    "
            if level == 0:
                return tree_last if last else tree_next
            return (tree_indent if last else tree_pass) + (tree_last if last_v else tree_next)

        validator = Validator(log_warnings=False,
                              log_errors=True,
                              check_digests=False,
                              lax_digests=self.lax_digests)
        passed = validator.validate_object(objdir)
        self.spec_version = validator.spec_version
        self.content_directory = validator.content_directory
        if passed:
            logging.info("OCFL v%s Object at %s has VALID STRUCTURE (DIGESTS NOT CHECKED)",
                         validator.spec_version, objdir)
        else:
            logging.warning("OCFL v%s Object at %s is INVALID",
                            validator.spec_version, objdir)
        tree = "[" + objdir + "]\n"
        self.open_obj_fs(objdir)
        entries = sorted(self.obj_fs.listdir(""))
        n = 0
        seen_sidecar = False
        object_declaration_filename = self.object_declaration_object().filename
        for entry in entries:
            n += 1
            note = entry + " "
            v_notes = []
            if re.match(r"""v\d+$""", entry):
                seen_v_sidecar = False
                for v_entry in sorted(self.obj_fs.listdir(entry)):
                    v_note = v_entry + " "
                    if v_entry == INVENTORY_FILENAME:
                        pass
                    elif v_entry.startswith(INVENTORY_FILENAME + "."):
                        if seen_v_sidecar:
                            v_note += "<--- multiple inventory digests?"
                            seen_v_sidecar = True
                    elif v_entry == self.content_directory:
                        num_files = 0
                        for (v_dirpath, v_dirs, v_files) in self.obj_fs.walk(fs.path.join(entry, v_entry)):  # pylint: disable=unused-variable
                            num_files += len(v_files)
                        v_note += "(%d files)" % num_files
                    else:
                        v_note += "<--- ???"
                    v_notes.append(v_note)
            elif entry in (object_declaration_filename, INVENTORY_FILENAME):
                pass
            elif entry.startswith(INVENTORY_FILENAME + "."):
                if seen_sidecar:
                    note += "<--- multiple inventory digests?"
                seen_sidecar = True
            else:
                note += "<--- ???"
            last = (n == len(entries))
            tree += _show_indent(0, last) + note + "\n"
            nn = 0
            for v_note in v_notes:
                nn += 1
                tree += _show_indent(1, last, (nn == len(v_notes))) + v_note + "\n"
        return tree

    def validate(self, objdir=None, log_warnings=True,
                 log_errors=True, check_digests=True):
        """Validate OCFL object at objdir.

        Returns tuple (passed, validator) where:
            passed: True is validation passed, False otherwise.
            validator: Validator object used for validation. State records
                validation history including validator.messages
        """
        validator = Validator(log_warnings=log_warnings,
                              log_errors=log_errors,
                              check_digests=check_digests,
                              lax_digests=self.lax_digests)
        if objdir is None:
            objdir = self.obj_fs
        passed = validator.validate_object(objdir)
        return passed, validator

    def validate_inventory(self, path, log_warnings=True,
                           log_errors=True, force_spec_version=None):
        """Validate just an OCFL Object inventory at path.

        Arguments:
            path: path of inventory file
            log_warnings (bool): True to log warnings
            log_errors (bool): True to log errors
            force_spec_version: None to read specification version from
                inventory; or specific number to force validation against
                that specification version

        Returns tuple (passed, validator) where:
            passed: True is validation passed, False otherwise.
            validator: Validator object with state that records validation
                log and results
        """
        validator = Validator(log_warnings=log_warnings,
                              log_errors=log_errors,
                              lax_digests=self.lax_digests)
        try:
            (inv_dir, inv_file) = fs.path.split(path)
            validator.obj_fs = pyfs_openfs(inv_dir, create=False)
            validator.validate_inventory(inv_file, where="standalone", force_spec_version=force_spec_version)
        except fs.errors.ResourceNotFound:
            validator.log.error("E033", where="standalone", explanation="failed to open directory")
        except ValidatorAbortException:
            pass
        return (validator.log.num_errors == 0), validator

    def _extract_setup(self, objdir, version):
        """Check object and version for extract() and extract_file().

        Arguments:
            objdir: directory for the object
            version: version to be extracted ("v1", etc.) or "head" for latest

        Returns tuple of (inv, version) where inv is the parsed inventory and
        version if the checked object version.

        Raises an ObjectException is the inventory Can't be parsed or if the
        version doesn"t exist.
        """
        self.open_obj_fs(objdir)
        # Read inventory, set up version
        inv = self.parse_inventory()
        if version == "head":
            version = inv.head
            logging.debug("Object at %s has head %s", objdir, version)
        elif version not in inv.version_directories:
            raise ObjectException("Object at %s does not include a version '%s'" % (objdir, version))
        return inv, version

    def extract(self, objdir, version, dstdir):
        """Extract version from object at objdir into dstdir.

        Arguments:
            objdir: directory for the object
            version: version to be extracted ("v1", etc.) or "head" for latest
            dstdir: directory to create with extracted version

        The dstdir itself may exist bit if it is then it must be empty. The
        parent directory of dstdir must exist.

        Returns a VersionMetadata object for the version extracted.
        """
        inv, version = self._extract_setup(objdir, version)
        # Check the destination
        (parentdir, dir) = os.path.split(os.path.normpath(dstdir))
        try:
            parent_fs = pyfs_openfs(parentdir)
        except (fs.opener.errors.OpenerError, fs.errors.CreateFailed) as e:
            raise ObjectException("Destination parent %s does not exist or could not be opened (%s)" % (parentdir, e))
        if parent_fs.isdir(dir):
            if not parent_fs.isempty(dir):
                raise ObjectException("Target directory %s already exists and is not empty, aborting!" % (dstdir))
        else:  # Make dstdir
            parent_fs.makedir(dir)
        dst_fs = parent_fs.opendir(dir)  # Open a sub-filesystem as our destination
        # Now extract...
        manifest = inv.manifest
        state = inv.version(version).state
        # Extract all files for this version
        for (digest, logical_files) in state.items():
            existing_file = manifest[digest][0]  # First entry with the digest, there could be > 1
            for logical_file in logical_files:
                logging.debug("Copying %s -> %s", digest, logical_file)
                dst_fs.makedirs(fs.path.dirname(logical_file), recreate=True)
                fs.copy.copy_file(self.obj_fs, existing_file, dst_fs, logical_file)
        logging.info("Extracted %s into %s", version, dstdir)
        return VersionMetadata(inventory=inv.data, version=version)

    def extract_file(self, objdir, version, dstdir, logical_path):
        """Extract one file from version from object at objdir into dstdir.

        Arguments:
            objdir - directory for the object
            version - version to be extracted ("v1", etc.) or "head" for latest
            dstdir - directory to create with extracted version
            logical_path - extract just one logical path into dstdir, without
                any path segments below dstdir

        If dstdir doesn"t exists then create it. The parent directory of dstdir
        must exist. If dstdir exists, then a file of the same name must not
        exist.

        Returns a VersionMetadata object for the version extracted.
        """
        inv, version = self._extract_setup(objdir, version)
        # Check the destination
        try:
            dst_fs = pyfs_openfs(dstdir)
        except (fs.opener.errors.OpenerError, fs.errors.CreateFailed):
            # Doesn"t exist, can we create it?
            (parentdir, dir) = os.path.split(os.path.normpath(dstdir))
            if parentdir == "":
                parentdir = "."
            try:
                parent_fs = pyfs_openfs(parentdir)
            except (fs.opener.errors.OpenerError, fs.errors.CreateFailed) as e:
                raise ObjectException("Destination parent %s does not exist or could not be opened (%s)" % (parentdir, e))
            dst_fs = parent_fs.makedir(dir)
        # Does the destination file already exist?
        basename = os.path.basename(logical_path)
        if dst_fs.exists(basename):
            raise ObjectException("Destination file %s in %s already exists" % (basename, dstdir))
        # Now extract...
        manifest = inv.manifest
        state = inv.version(version).state
        # Extract the specified file
        copied = False
        for (digest, logical_files) in state.items():
            existing_file = manifest[digest][0]  # First entry with the digest, there could be > 1
            for logical_file in logical_files:
                if logical_file == logical_path:
                    logging.debug("Copying %s -> %s", digest, basename)
                    fs.copy.copy_file(self.obj_fs, existing_file, dst_fs, basename)
                    copied = True
                    break
            if copied:
                break
        else:
            raise ObjectException("Logical path %s not found in %s" % (logical_path, version))
        return VersionMetadata(inventory=inv, version=version)

    def parse_inventory(self):
        """Read JSON root inventory file for this object.

        Will validate the inventory and normalize the digests so that the rest
        of the Object methods can assume correctness and matching string digests
        between state and manifest blocks.

        Returns:
            ocfl.Inventory: new Inventory object for the parsed inventory.
        """
        with self.obj_fs.open(INVENTORY_FILENAME) as fh:
            inventory = Inventory(json.load(fh))
        # Validate
        iv = InventoryValidator()
        if not iv.validate(inventory=inventory.data):
            raise ObjectException("Root inventory is not valid (%d errors)" % iv.log.num_errors)
        self.spec_version = iv.spec_version
        # Normalize digests in place
        inventory.normalize_digests(iv.digest_algorithm)
        return inventory

    def id_from_inventory(self, failure_value="UNKNOWN-ID"):
        """Read JSON root inventory file for this object and extract id.

        Returns the id from the inventory or failure_value is none can
        be extracted.
        """
        try:
            inventory = self.parse_inventory()
            return inventory.id
        except ObjectException:
            return failure_value
