# -*- coding: utf-8 -*-
"""Core of OCFL Object library."""
import hashlib
import json
import os
import os.path
import re
import logging
from shutil import copyfile
import sys

from .digest import file_digest
from .validator import OCFLValidator
from .version import VersionMetadata


def add_object_args(parser):
    """Add Object settings to argparse instance parser."""
    # Disk scanning
    parser.add_argument('--skip', action='append', default=['README.md', '.DS_Store'],
                        help='directories and files to ignore')
    # Versioning strategy settings
    parser.add_argument('--no-forward-delta', action='store_true',
                        help='do not use forward deltas')
    parser.add_argument('--no-dedupe', '--no-dedup', action='store_true',
                        help='do not use deduplicate files within a version')
    # Object files
    parser.add_argument('--objdir', '--obj',
                        help='read from or write to OCFL object directory objdir')
    parser.add_argument('--ocfl-version', default='draft',
                        help='OCFL specification version')


class ObjectException(Exception):
    """Exception class for OCFL Object."""

    pass


class Object(object):
    """Class for handling OCFL Object data and operations."""

    def __init__(self, identifier=None,
                 digest_algorithm='sha512', skips=None,
                 forward_delta=True, dedupe=True,
                 ocfl_version='draft', fixity=None, fhout=sys.stdout):
        """Initialize OCFL builder.

        Parameters:
           forward_delta - set False to turn off foward delta
           dedupe - set False to turn off dedupe within versions
           fixity - list of fixity types to add as fixity section
           fhout - optional overwrite of STDOUT for print outputs
        """
        self.identifier = identifier
        self.digest_algorithm = digest_algorithm
        self.skips = set() if skips is None else set(skips)
        self.forward_delta = forward_delta
        self.dedupe = dedupe
        self.ocfl_version = ocfl_version
        self.fixity = fixity
        self.src_files = {}
        self.validation_codes = None
        self.fhout = fhout

    def parse_version_directory(self, dirname):
        """Get version number from version directory name."""
        m = re.match(r'''v(\d{1,5})$''', dirname)
        if not m:
            raise Exception("Bad version directory name: %s" % (dirname))
        v = int(m.group(1))
        if v == 0:
            raise Exception("Bad version directory name: %s, v0 no allowed" % (dirname))
        return v

    def digest(self, filename):
        """Digest for file filename."""
        return file_digest(filename, self.digest_algorithm)

    def normalize_filename(self, filename):
        """Translate source filename to a normalized (safe and sanitized) name within object."""
        # FIXME - noop for now
        return filename

    def start_inventory(self):
        """Create inventory start with metadata from self."""
        inventory = {
            'id': self.identifier,
            'type': 'Object',
            'digestAlgorithm': self.digest_algorithm,
            'versions': {},
            'manifest': {}
        }
        # Add fixity section if requested
        if self.fixity is not None and len(self.fixity) > 0:
            inventory['fixity'] = {}
            for fixity_type in self.fixity:
                inventory['fixity'][fixity_type] = {}
        else:
            fixity = None
        return inventory

    def add_version(self, inventory, srcdir, vdir, metadata=None):
        """Add to inventory data for new version based on files in srcdir.

        srcdir - the directory path where the files for this version exist,
                 including any version directory that might be present
        vdir - the version directory that these files are being added in

        Returns:

        manifest_to_srcfile - dict mapping from paths in manifest to the full
            path of the source file
        """
        state = {}
        manifest = inventory['manifest']
        digests_in_version = {}
        manifest_to_srcfile = {}
        # Go through all files to find new files in manifest and state for each version
        for (dirpath, dirnames, filenames) in os.walk(srcdir, followlinks=True):
            # Go through filenames, in sort order so the it is deterministic
            # which file is included and which is/are referenced in the case
            # of multiple additions with the same digest
            for filename in sorted(filenames):
                if filename == "inventory.json":
                    # Read metadata for this version
                    metadata.from_inventory_file(os.path.join(dirpath, filename), vdir)
                    continue
                filepath = os.path.join(dirpath, filename)
                sfilepath = os.path.relpath(filepath, srcdir)  # path relative to this version
                norm_path = self.normalize_filename(sfilepath)
                vfilepath = os.path.join(vdir, 'content', norm_path)  # path relative to root, inc v#/content
                digest = self.digest(filepath)
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
                        fixity_digest = file_digest(manifest_to_srcfile[vfilepath], fixity_type)
                        if fixity_digest not in fixities:
                            fixities[fixity_digest] = [vfilepath]
                        else:
                            fixities[fixity_digest].append(vfilepath)
        # Set head to this latest version, and add this version to inventory
        inventory['head'] = vdir
        inventory['versions'][vdir] = metadata.as_dict(state=state)
        return manifest_to_srcfile

    def build_inventory(self, path, metadata=None):
        """Generator for building an OCFL inventory.

        Yields (vdir, inventory, manifest_to_srcfile) for each version in sequence,
        where vdir is the version directory name, inventory is the inventory for that
        version, and manifest_to_srcfile is a dictionary that maps filepaths in the
        manifest to actual source filepaths.
        """
        inventory = self.start_inventory()
        # Find the versions
        versions = {}
        for vdir in os.listdir(path):
            if vdir in self.skips:
                continue
            vn = self.parse_version_directory(vdir)
            versions[vn] = vdir
        # Go through versions in order building versions array, deduping if selected
        for vn in sorted(versions.keys()):
            vdir = versions[vn]
            manifest_to_srcfile = self.add_version(inventory, os.path.join(path, vdir), vdir,
                                                   metadata=metadata)
            yield (vdir, inventory, manifest_to_srcfile)

    def write_object_declaration(self, objdir):
        """Write NAMASTE object declaration to objdir."""
        namastefile = os.path.join(objdir, '0=ocfl_object_1.0')
        with open(namastefile, 'w') as fh:
            pass  # empty file

    def write_inventory_and_sidecar(self, objdir, inventory):
        """Write inventory and sidecar to objdir."""
        invfilename = 'inventory.json'
        if not os.path.exists(objdir):
            os.makedirs(objdir)
        invfile = os.path.join(objdir, invfilename)
        with open(invfile, 'w') as fh:
            json.dump(inventory, fh, sort_keys=True, indent=2)
        sidecar = os.path.join(objdir, invfilename + '.' + self.digest_algorithm)
        digest = file_digest(invfile, self.digest_algorithm)
        with open(sidecar, 'w') as fh:
            fh.write(digest + ' ' + invfilename + '\n')

    def write(self, srcdir, metadata=None, objdir=None):
        """Write out OCFL object to dst if set, else print inventory.

        Parameters:
          srcdir - source directory with version sub-directories
          metadata - VersionMetadata object applied to all versions
          objdir - output directory for object (must not already exist), if not
              set then will just write out inventories that would have been
              created
        """
        if self.identifier is None:
            raise ObjectException("Identifier is not set!")
        if objdir is not None:
            os.makedirs(objdir)
        for (vdir, inventory, manifest_to_srcfile) in self.build_inventory(srcdir, metadata=metadata):
            if objdir is None:
                self.prnt("\n\n### Inventory for %s\n" % (vdir))
                self.prnt(json.dumps(inventory, sort_keys=True, indent=2))
            else:
                self.write_inventory_and_sidecar(os.path.join(objdir, vdir), inventory)
                # Copy files into this version
                for (path, srcfile) in manifest_to_srcfile.items():
                    dstfile = os.path.join(objdir, path)
                    dstpath = os.path.dirname(dstfile)
                    if not os.path.exists(dstpath):
                        os.makedirs(dstpath)
                    copyfile(srcfile, dstfile)
        if objdir is None:
            return
        # Write NAMASTE, inventory and sidecar
        self.write_object_declaration(objdir)
        self.write_inventory_and_sidecar(objdir, inventory)

    def create(self, srcdir, metadata=None, objdir=None):
        """Create an OCFL object with v1 content from srcdir.

        Write to dst if set, else just print inventory.
        """
        if self.identifier is None:
            raise ObjectException("Identifier is not set!")
        if objdir is not None:
            os.makedirs(objdir)
        inventory = self.start_inventory()
        vdir = 'v1'
        manifest_to_srcfile = self.add_version(inventory, srcdir, vdir,
                                               metadata=metadata)
        if objdir is None:
            self.prnt("\n\n### Inventory for %s\n" % (vdir))
            self.prnt(json.dumps(inventory, sort_keys=True, indent=2))
            return
        # Else write out object
        self.write_inventory_and_sidecar(os.path.join(objdir, vdir), inventory)
        # Write NAMASTE, inventory and sidecar
        self.write_object_declaration(objdir)
        self.write_inventory_and_sidecar(objdir, inventory)
        # Write version files
        for digest, paths in inventory['manifest'].items():
            for path in paths:
                srcfile = manifest_to_srcfile[path]
                dstfile = os.path.join(objdir, path)
                dstpath = os.path.dirname(dstfile)
                if not os.path.exists(dstpath):
                    os.makedirs(dstpath)
                copyfile(srcfile, dstfile)

    def _show_indent(self, level, last=False):
        tree_next = '├── '
        tree_last = '└── '
        tree_indent = '    '
        return tree_indent * level + (tree_last if last else tree_next)

    def show(self, path):
        """Show OCFL object at path."""
        level = 0
        dirs = sorted(os.listdir(path))
        self.prnt('[' + path + ']')
        n = 0
        for d in dirs:
            n += 1
            note = ''
            if re.match(r'''v\d+$''', d):
                num_files = 0
                for (dirpath, dirnames, filenames) in os.walk(os.path.join(path, d), followlinks=True):
                    num_files += len(filenames)
                note += '(%d files)' % num_files
            elif d not in ('0=ocfl_object_1.0', 'inventory.json', 'inventory.json.sha512'):
                note += '<--- ???'
            # for (dirpath, dirnames, filenames) in os.walk(, followlinks=True):
            self.prnt(self._show_indent(level, (n == len(dirs))) + d + '   ' + note)

    def validate(self, path):
        """Validate OCFL object at path."""
        validator = OCFLValidator()
        passed = validator.validate(path)
        if passed:
            self.prnt("OCFL object at %s is VALID" % (path))
        else:
            self.prnt("OCFL object at %s is INVALID" % (path))
        self.prnt(str(validator))
        return passed

    def parse_inventory(self, path):
        """Read JSON top-level inventory file for object at path."""
        inv_file = os.path.join(path, 'inventory.json')
        with open(inv_file) as fh:
            inventory = json.load(fh)
        # Sanity checks
        if 'id' not in inventory:
            raise ObjectException("Inventory %s has no id property" % (inv_file))
        return inventory

    def prnt(self, *objects):
        """Print method that uses object fhout property.

        Avoid using Python 3 print function so we can run on 2.7 still.

        Can't call this 'print' in 2.7, hence 'prnt'.
        """
        s = ' '.join(str(o) for o in objects) + '\n'
        if sys.version_info > (3, 0):
            self.fhout.write(s)
        else:
            self.fhout.write(s.decode('utf-8'))


def remove_first_directory(path):
    """Remove first directory from input path.

    The return value will not have a trailing parh separator, even if
    the input path does. Will return an empty string if the input path
    has just one path segment.
    """
    # FIXME - how to do this efficiently? Current code does complete
    # split and rejoins, excluding the first directory
    rpath = ''
    while True:
        (head, tail) = os.path.split(path)
        if head == path or tail == path:
            break
        else:
            path = head
            rpath = tail if rpath == '' else os.path.join(tail, rpath)
    return rpath
