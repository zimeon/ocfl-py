# -*- coding: utf-8 -*-
"""Core of OCFL Object library."""
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

from .digest import file_digest, normalized_digest
from .inventory_validator import InventoryValidator
from .object_utils import make_unused_filepath, next_version, ObjectException
from .pyfs import open_fs
from .namaste import Namaste
from .validator import Validator, ValidatorAbortException
from .version_metadata import VersionMetadata

INVENTORY_FILENAME = 'inventory.json'


def parse_version_directory(dirname):
    """Get version number from version directory name."""
    m = re.match(r'''v(\d{1,5})$''', dirname)
    if not m:
        raise Exception("Bad version directory name: %s" % (dirname))
    v = int(m.group(1))
    if v == 0:
        raise Exception("Bad version directory name: %s, v0 no allowed" % (dirname))
    return v


class Object():
    """Class for handling OCFL Object data and operations."""

    def __init__(self, identifier=None, content_directory='content',
                 digest_algorithm='sha512', filepath_normalization='uri',
                 forward_delta=True, dedupe=True,
                 lax_digests=False, fixity=None, verbose=True,
                 obj_fs=None, path=None, create=False):
        """Initialize OCFL object.

        Parameters relevant to building an object:
          identifier - id for this object
          content_directory - allow override of the default 'content'
          digest_algorithm - allow override of the default 'sha512'
          filepath_normalization = allow override of default 'uri'
          forward_delta - set False to turn off foward delta. With forward delta
            turned off, the same content will be repeated in a new version
            rather than simply being included by reference through the
            digest linking to the copy in the previous version
          dedupe - set False to turn off dedupe within versions. With dedupe
            turned off, the same content will be repeated within a given version
            rather than one copy being included and then a reference being used
            from the multiple logical files
          lax_digests - set True to allow digests beyond those included in the
            specification for fixity and to allow non-preferred digest algorithms
            for content references in the object
          fixity - list of fixity types to add as fixity section
          verbose - set logging level to INFO rather than WARN

          obj_fs - a pyfs filesystem reference for the root of this object
          path - if set then open a pyfs filesystem at path (alternative to obj_fs)
          create - set True to allow opening filesystem at path to create a directory
        """
        self.id = identifier
        self.content_directory = content_directory
        self.digest_algorithm = digest_algorithm
        self.filepath_normalization = filepath_normalization
        self.forward_delta = forward_delta
        self.dedupe = dedupe
        self.fixity = fixity
        self.lax_digests = lax_digests
        self.src_files = {}
        self.log = logging.getLogger(name="ocfl.object")
        self.log.setLevel(level=logging.INFO if verbose else logging.WARN)
        self.obj_fs = obj_fs  # fs filesystem (or sub-filesystem) for object
        if path is not None:
            self.open_fs(path, create=create)

    def open_fs(self, objdir, create=False):
        """Open an fs filesystem for this object."""
        try:
            self.obj_fs = open_fs(fs_url=objdir, create=create)
        except (fs.opener.errors.OpenerError, fs.errors.CreateFailed) as e:
            raise ObjectException("Failed to open object filesystem '%s' (%s)" % (objdir, e))

    def copy_into_object(self, src_fs, srcfile, filepath, create_dirs=False):
        """Copy from srcfile to filepath in object."""
        dstpath = fs.path.dirname(filepath)
        if create_dirs and not self.obj_fs.exists(dstpath):
            self.obj_fs.makedirs(dstpath)
        fs.copy.copy_file(src_fs, srcfile, self.obj_fs, filepath)

    def digest(self, pyfs, filename):
        """Digest for file filename in the object filesystem."""
        return file_digest(filename, self.digest_algorithm, pyfs=pyfs)

    def map_filepath(self, filepath, vdir, used):
        """Map source filepath to a content path within the object.

        The purpose of the mapping might be normalization, sanitization,
        content distribution, or something else.

        Parameters:
          filepath - the source filepath
          vdir - the current version directory
          used - disctionary used to check whether a given vfilepath has
            been used already

        Returns:
          vfilepath - the version filepath for this content that starts
            with vdir/content_directory/
        """
        if self.filepath_normalization == 'uri':
            filepath = urlquote(filepath)
            # also encode any leading period to unhide files
            if filepath[0] == '.':
                filepath = '%2E' + filepath[1:]
        elif self.filepath_normalization == 'md5':
            # Truncated MD5 hash of the _filepath_ as an illustration of diff paths for spec,
            # not sure there could be any real application of this
            filepath = hashlib.md5(filepath.encode('utf-8')).hexdigest()[0:16]
        elif self.filepath_normalization is not None:
            raise Exception("Unknown filepath normalization '%s' requested" % (self.filepath_normalization))
        vfilepath = fs.path.join(vdir, self.content_directory, filepath)  # path relative to root, inc v#/content
        # Check we don't already have this vfilepath from many to one normalization,
        # add suffix to distinguish if necessary
        if vfilepath in used:
            vfilepath = make_unused_filepath(vfilepath, used)
        return vfilepath

    def start_inventory(self):
        """Create inventory start with metadata from self."""
        inventory = {
            'id': self.id,
            'type': 'https://ocfl.io/1.0/spec/#inventory',
            'digestAlgorithm': self.digest_algorithm,
            'versions': {},
            'manifest': {}
        }
        # Add contentDirectory if not 'content'
        if self.content_directory != 'content':
            inventory['contentDirectory'] = self.content_directory
        # Add fixity section if requested
        if self.fixity is not None and len(self.fixity) > 0:
            inventory['fixity'] = {}
            for fixity_type in self.fixity:
                inventory['fixity'][fixity_type] = {}
        else:
            self.fixity = None
        return inventory

    def add_version(self, inventory, src_fs, src_dir, vdir, metadata=None):
        """Add to inventory data for new version based on files in srcdir.

        Parameters:
          inventory - the inventory up to (vdir-1) which must include blocks
            for ['manifest'] and ['versions']. It must also include
            a ['fixity'][algorithm] block for every algorithm in self.fixity
          src_fs - pyfs filesystem where this new version exist
          src_dir - the version directory in src_fs that files are being added
            from
          vdir - the version name of the version being created
          metadata - a VersionMetadata object with any metadata for this
            version

        Returns:
          manifest_to_srcfile - dict mapping from paths in manifest to the path
            of the source file in src_fs that should be include in the content
            for this new version
        """
        state = {}  # state for this new version
        manifest = inventory['manifest']
        digests_in_version = {}
        manifest_to_srcfile = {}
        # Go through all files to find new files in manifest and state for this version
        for filepath in sorted(src_fs.walk.files(src_dir)):
            sfilepath = os.path.relpath(filepath, src_dir)
            vfilepath = self.map_filepath(sfilepath, vdir, used=manifest_to_srcfile)
            digest = self.digest(src_fs, filepath)
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
                fixities = inventory['fixity'][fixity_type]
                for digest, vfilepaths in digests_in_version.items():
                    for vfilepath in vfilepaths:
                        fixity_digest = file_digest(manifest_to_srcfile[vfilepath], fixity_type, pyfs=src_fs)
                        if fixity_digest not in fixities:
                            fixities[fixity_digest] = [vfilepath]
                        else:
                            fixities[fixity_digest].append(vfilepath)
        # Set head to this latest version, and add this version to inventory
        inventory['head'] = vdir
        inventory['versions'][vdir] = metadata.as_dict(state=state)
        return manifest_to_srcfile

    def build_inventory(self, src_fs, metadata=None):
        """Generate an OCFL inventory from a set of source files.

        Parameters:
            src_fc - pyfs filesystem of source files
            metadata - metadata to apply to each version

        Yields (vdir, inventory, manifest_to_srcfile) for each version in sequence,
        where vdir is the version directory name, inventory is the inventory for that
        version, and manifest_to_srcfile is a dictionary that maps filepaths in the
        manifest to actual source filepaths.
        """
        inventory = self.start_inventory()
        # Find the versions
        versions = {}
        for vdir in src_fs.listdir('/'):
            if not src_fs.isdir(vdir):
                continue
            vn = parse_version_directory(vdir)
            versions[vn] = vdir
        # Go through versions in order building versions array, deduping if selected
        for vn in sorted(versions.keys()):
            vdir = versions[vn]
            manifest_to_srcfile = self.add_version(inventory, src_fs, vdir, vdir,
                                                   metadata=metadata)
            yield (vdir, inventory, manifest_to_srcfile)

    def write_object_declaration(self):
        """Write NAMASTE object declaration.

        Assumes self.obj_fs is open for this object.
        """
        Namaste(0, 'ocfl_object_1.0').write(pyfs=self.obj_fs)

    def write_inventory_and_sidecar(self, inventory, vdir='', write_inventory=True):
        """Write inventory and sidecar to vdir in the current object.

        Assumes self.obj_fs is open for this object. Will create vdir if that
        does not exist. If vdir is not specified then will write to root of
        the object.

        Returns the inventory sidecar filename.
        """
        if not self.obj_fs.exists(vdir):
            self.obj_fs.makedir(vdir)
        invfile = fs.path.join(vdir, INVENTORY_FILENAME)
        if write_inventory:
            with self.obj_fs.open(invfile, 'w') as fh:
                json.dump(inventory, fh, sort_keys=True, indent=2)
        digest = file_digest(invfile, self.digest_algorithm, pyfs=self.obj_fs)
        sidecar = fs.path.join(vdir, INVENTORY_FILENAME + '.' + self.digest_algorithm)
        with self.obj_fs.open(sidecar, 'w') as fh:
            fh.write(digest + ' ' + INVENTORY_FILENAME + '\n')
        return sidecar

    def write_inventory_sidecar(self):
        """Write just sidecare for this object's already existing root inventory file.

        Returns the inventory sidecar filename.
        """
        return self.write_inventory_and_sidecar(None, write_inventory=False)

    def build(self, srcdir, metadata=None, objdir=None):
        """Build an OCFL object and write to objdir if set, else print inventories.

        Parameters:
          srcdir - source directory with version sub-directories
          metadata - VersionMetadata object applied to all versions
          objdir - output directory for object (must not already exist), if not
              set then will just write out inventories that would have been
              created
        """
        if self.id is None:
            raise ObjectException("Identifier is not set!")
        if objdir is not None:
            self.open_fs(objdir, create=True)
        num_versions = 0
        src_fs = open_fs(srcdir)
        inventory = None
        for (vdir, inventory, manifest_to_srcfile) in self.build_inventory(src_fs, metadata):
            num_versions += 1
            if objdir is None:
                self.log.warning("### Inventory for %s\n",
                                 vdir + json.dumps(inventory, sort_keys=True, indent=2))
            else:
                self.write_inventory_and_sidecar(inventory, vdir)
                # Copy files into this version
                for (path, srcfile) in manifest_to_srcfile.items():
                    self.copy_into_object(src_fs, srcfile, path, create_dirs=True)
        if objdir is None:
            return
        # Write object declaration, inventory and sidecar
        self.write_object_declaration()
        self.write_inventory_and_sidecar(inventory)
        self.log.info("Built object %s with %s versions", self.id, num_versions)

    def create(self, srcdir, metadata=None, objdir=None):
        """Create a new OCFL object with v1 content from srcdir.

        Parameters:
          srcdir - source directory with content for v1
          metadata - VersionMetadata object for v1
          objdir - output directory for object (must not already exist), if not
              set then will just write out inventories that would have been
              created
        """
        if self.id is None:
            raise ObjectException("Identifier is not set!")
        src_fs = open_fs(srcdir)
        if objdir is not None:
            self.open_fs(objdir, create=True)
        inventory = self.start_inventory()
        vdir = 'v1'
        manifest_to_srcfile = self.add_version(inventory, src_fs, '', vdir, metadata=metadata)
        if objdir is None:
            self.log.warning("### Inventory for %s\n",
                             vdir + json.dumps(inventory, sort_keys=True, indent=2))
            return
        # Else write out object
        self.write_inventory_and_sidecar(inventory, vdir)
        # Write object declaration, inventory and sidecar
        self.write_object_declaration()
        self.write_inventory_and_sidecar(inventory)
        # Write version files
        for paths in inventory['manifest'].values():
            for path in paths:
                srcfile = manifest_to_srcfile[path]
                self.copy_into_object(src_fs, srcfile, path, create_dirs=True)
        self.log.info("Created OCFL object %s in %s", self.id, objdir)

    def update(self, objdir, srcdir=None, metadata=None):
        """Update object creating a new version with content matching srcdir.

        Parameters:
          objdir - directory for object to be update, must contain a valid object!
          srcdir - source directory with version sub-directories
          metadata - VersionMetadata object applied to all versions

        If srcdir is None then the update will be just of metadata and any settings
        (such as using a new digest). There will be no content change between
        versions.
        """
        self.open_fs(objdir)
        validator = Validator(check_digests=False, lax_digests=self.lax_digests)
        if not validator.validate(objdir):
            raise ObjectException("Object at '%s' is not valid, aborting" % objdir)
        inventory = self.parse_inventory()
        self.id = inventory['id']
        old_head = inventory['head']
        head = next_version(old_head)
        self.log.info("Will update %s %s -> %s", self.id, old_head, head)
        self.obj_fs.makedir(head)
        # Is this a request to change the digest algorithm?
        old_digest_algorithm = inventory['digestAlgorithm']
        digest_algorithm = self.digest_algorithm
        if digest_algorithm is None:
            digest_algorithm = old_digest_algorithm
        elif digest_algorithm != old_digest_algorithm:
            self.log.info("New version with use %s instead of %s digestAlgorithm",
                          digest_algorithm, old_digest_algorithm)
            inventory['digestAlgorithm'] = digest_algorithm
        # Is this a request to change the set of fixity information?
        fixity = self.fixity
        old_fixity = set(inventory['fixity'].keys()) if 'fixity' in inventory else set()
        if fixity is None:
            # Not explicit, carry forward from previous version. Only change will
            # be adding old digest information if we are changing digestAlgorithm
            fixity = old_fixity.copy()
            if digest_algorithm != old_digest_algorithm and old_digest_algorithm not in old_fixity:
                # Add old manifest digests to fixity block
                if 'fixity' not in inventory:
                    inventory['fixity'] = {}
                inventory['fixity'][old_digest_algorithm] = inventory['manifest'].copy()
                fixity.add(old_digest_algorithm)
        else:
            # Fixity to be stored is explicit, may be a change
            fixity = set(fixity)
            if fixity != old_fixity:
                for digest in old_fixity.difference(fixity):
                    inventory['fixity'].pop(digest)
                for digest in fixity.difference(old_fixity):
                    self.log.info("FIXME - need to add fixity with digest %s", digest)
        if fixity != old_fixity:
            self.log.info("New version will have %s instead of %s fixity",
                          ','.join(sorted(fixity)), ','.join(sorted(old_fixity)))
        # Now look at contents, manifest and state
        manifest = copy.deepcopy(inventory['manifest'])
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
            for vdir in inventory['versions']:
                old_state = inventory['versions'][vdir]['state']
                state = {}
                for old_digest, files in old_state.items():
                    state[old_to_new_digest[old_digest]] = old_state[old_digest]
                inventory['versions'][vdir]['state'] = state
        inventory['manifest'] = manifest
        # Add and remove any contents by comparing srcdir with existing state and manifest
        if srcdir is None:
            # No content Update
            inventory['head'] = head
            state = copy.deepcopy(inventory['versions'][old_head]['state'])
            inventory['versions'][head] = metadata.as_dict(state=state)
        else:
            src_fs = open_fs(srcdir)
            manifest_to_srcfile = self.add_version(inventory=inventory, src_fs=src_fs, src_dir='', vdir=head, metadata=metadata)
            # Copy files into this version
            for (path, srcfile) in manifest_to_srcfile.items():
                self.copy_into_object(src_fs, srcfile, path, create_dirs=True)
        # Write inventory in both root and head version
        self.write_inventory_and_sidecar(inventory, head)
        self.write_inventory_and_sidecar(inventory)
        # Delete old root inventory sidecar if we changed digest algorithm
        if digest_algorithm != old_digest_algorithm:
            self.obj_fs.remove(INVENTORY_FILENAME + '.' + old_digest_algorithm)
        self.log.info("Updated OCFL object %s in %s by adding %s", self.id, objdir, head)

    def show(self, objdir):
        """Show OCFL object at objdir."""
        def _show_indent(level, last=False, last_v=False):
            """Indent string for tree view at level for intermediate or last."""
            tree_next = '├── '
            tree_last = '└── '
            tree_pass = '│   '
            tree_indent = '    '
            if level == 0:
                return tree_last if last else tree_next
            return (tree_indent if last else tree_pass) + (tree_last if last_v else tree_next)

        validator = Validator(show_warnings=False,
                              show_errors=True,
                              check_digests=False,
                              lax_digests=self.lax_digests)
        passed = validator.validate(objdir)
        if passed:
            self.log.warning("OCFL object at %s has VALID STRUCTURE (DIGESTS NOT CHECKED) ", objdir)
        else:
            self.log.warning("OCFL object at %s is INVALID", objdir)
        tree = '[' + objdir + ']\n'
        self.open_fs(objdir)
        entries = sorted(self.obj_fs.listdir(''))
        n = 0
        seen_sidecar = False
        for entry in entries:
            n += 1
            note = entry + ' '
            v_notes = []
            if re.match(r'''v\d+$''', entry):
                seen_v_sidecar = False
                for v_entry in sorted(self.obj_fs.listdir(entry)):
                    v_note = v_entry + ' '
                    if v_entry == INVENTORY_FILENAME:
                        pass
                    elif v_entry.startswith(INVENTORY_FILENAME + '.'):
                        if seen_v_sidecar:
                            v_note += '<--- multiple inventory digests?'
                            seen_v_sidecar = True
                    elif v_entry == 'content':
                        num_files = 0
                        for (v_dirpath, v_dirs, v_files) in self.obj_fs.walk(fs.path.join(entry, v_entry)):  # pylint: disable=unused-variable
                            num_files += len(v_files)
                        v_note += '(%d files)' % num_files
                    else:
                        v_note += '<--- ???'
                    v_notes.append(v_note)
            elif entry in ('0=ocfl_object_1.0', INVENTORY_FILENAME):
                pass
            elif entry.startswith(INVENTORY_FILENAME + '.'):
                if seen_sidecar:
                    note += '<--- multiple inventory digests?'
                seen_sidecar = True
            else:
                note += '<--- ???'
            last = (n == len(entries))
            tree += _show_indent(0, last) + note + "\n"
            nn = 0
            for v_note in v_notes:
                nn += 1
                tree += _show_indent(1, last, (nn == len(v_notes))) + v_note + "\n"
        self.log.warning("Object tree\n%s", tree)

    def validate(self, objdir, show_warnings=True, show_errors=True, check_digests=True):
        """Validate OCFL object at objdir."""
        validator = Validator(show_warnings=show_warnings,
                              show_errors=show_errors,
                              check_digests=check_digests,
                              lax_digests=self.lax_digests)
        passed = validator.validate(objdir)
        messages = str(validator)
        if messages != '':
            print(messages)
        if passed:
            self.log.info("OCFL object at %s is VALID", objdir)
        else:
            self.log.info("OCFL object at %s is INVALID", objdir)
        return passed

    def validate_inventory(self, path, show_warnings=True, show_errors=True):
        """Validate just an OCFL Object inventory at path."""
        validator = Validator(show_warnings=show_warnings,
                              show_errors=show_errors)
        try:
            (inv_dir, inv_file) = fs.path.split(path)
            validator.obj_fs = open_fs(inv_dir, create=False)
            validator.validate_inventory(inv_file, where='standalone')
        except fs.errors.ResourceNotFound:
            validator.log.error('E033', where='standalone', explanation='failed to open directory')
        except ValidatorAbortException:
            pass
        passed = (validator.log.num_errors == 0)
        messages = str(validator)
        if messages != '':
            print(messages)
        if passed:
            self.log.info("Standalone OCFL inventory at %s is VALID", path)
        else:
            self.log.info("Standalone OCFL inventory at %s is INVALID", path)
        return passed

    def extract(self, objdir, version, dstdir):
        """Extract version from object at objdir into dstdir.

        The dstdir itself must not exist but the parent directory must.

        Returns the version block from the inventory.
        """
        self.open_fs(objdir)
        # Read inventory, set up version
        inv = self.parse_inventory()
        if version == 'head':
            version = inv['head']
            self.log.info("Object at %s has head %s", objdir, version)
        elif version not in inv['versions']:
            raise ObjectException("Object at %s does not include a version '%s'" % (objdir, version))
        # Sanity check on destination
        if os.path.isdir(dstdir):
            raise ObjectException("Target directory %s already exists, aborting!" % (dstdir))

        (parentdir, dir) = os.path.split(os.path.normpath(dstdir))
        try:
            parent_fs = open_fs(parentdir)
        except (fs.opener.errors.OpenerError, fs.errors.CreateFailed) as e:
            raise ObjectException("Destination parent %s does not exist or could not be opened (%s)" % (parentdir, e))
        parent_fs.makedir(dir)
        dst_fs = parent_fs.opendir(dir)  # Open a sub-filesystem as our destination
        # Now extract...
        manifest = inv['manifest']
        state = inv['versions'][version]['state']
        for (digest, logical_files) in state.items():
            existing_file = manifest[digest][0]  # FIXME - pick "best" (closest version?) not first?
            for logical_file in logical_files:
                self.log.debug("Copying %s -> %s", digest, logical_file)
                dst_fs.makedirs(fs.path.dirname(logical_file), recreate=True)
                fs.copy.copy_file(self.obj_fs, existing_file, dst_fs, logical_file)
        self.log.info("Extracted %s into %s", version, dstdir)
        return VersionMetadata(inventory=inv, version=version)

    def parse_inventory(self):
        """Read JSON root inventory file for this object.

        Will validate the inventory and normalize the digests so that the rest
        of the Object methods can assume correctness and matching string digests
        between state and manifest blocks.
        """
        with self.obj_fs.open(INVENTORY_FILENAME) as fh:
            inventory = json.load(fh)
        # Validate
        iv = InventoryValidator()
        iv.validate(inventory)
        if iv.log.num_errors > 0:
            raise ObjectException("Root inventory is not valid (%d errors)" % iv.log.num_errors)
        digest_algorithm = iv.digest_algorithm
        # Normalize digests in place
        manifest = inventory['manifest']
        from_to = {}
        for digest in manifest:
            norm_digest = normalized_digest(digest, digest_algorithm)
            if digest != norm_digest:
                from_to[digest] = norm_digest
        for (digest, norm_digest) in from_to.items():
            manifest[norm_digest] = manifest.pop(digest)
        for v in inventory['versions']:
            state = inventory['versions'][v]['state']
            from_to = {}
            for digest in state:
                norm_digest = normalized_digest(digest, digest_algorithm)
                if digest != norm_digest:
                    from_to[digest] = norm_digest
            for (digest, norm_digest) in from_to.items():
                state[norm_digest] = state.pop(digest)
        return inventory

    def id_from_inventory(self, failure_value='UNKNOWN-ID'):
        """Read JSON root inventory file for this object and extract id.

        Returns the id from the inventory or failure_value is none can
        be extracted.
        """
        try:
            inventory = self.parse_inventory()
            return inventory['id']
        except ObjectException:
            return failure_value
