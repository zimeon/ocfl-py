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
try:
    from urllib.parse import quote as urlquote  # python3
except:
    from urllib import quote as urlquote  # python2

from .digest import file_digest
from .namaste import Namaste
from .validator import OCFLValidator
from .version import VersionMetadata


NORMALIZATIONS = ['uri', 'md5']  # Must match possibilities in map_filepaths()


def add_object_args(parser):
    """Add Object settings to argparse instance parser."""
    # Disk scanning
    parser.add_argument('--skip', action='append', default=['README.md', '.DS_Store'],
                        help='directories and files to ignore')
    parser.add_argument('--normalization', '--norm', default=None,
                        help='filepath normalization strategy (None, %s)' %
                        (', '.join(NORMALIZATIONS)))
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
                 digest_algorithm='sha512', filepath_normalization='uri',
                 skips=None, forward_delta=True, dedupe=True,
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
        self.filepath_normalization = filepath_normalization
        self.skips = set() if skips is None else set(skips)
        self.forward_delta = forward_delta
        self.dedupe = dedupe
        self.ocfl_version = ocfl_version
        self.fixity = fixity
        self.src_files = {}
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

    def map_filepath(self, filepath, vdir, used):
        """Map source filepath to a  name within object.

        The purpose of the mapping might be normalization, sanitization,
        content distribution, or something else. Parameters:

        filepath - the source filepath
        vdir - the current version directory
        used - disctionary used to check whether a given vfilepath has
          been used already

        Returns:

        vfilepath - the version filepath for this content that starts
          with vdir/content/
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
        vfilepath = os.path.join(vdir, 'content', filepath)  # path relative to root, inc v#/content
        # Check we don't already have this vfilepath from many to one normalization,
        # add suffix to distinguish if necessary
        if vfilepath in used:
            vfilepath = make_unused_filepath(vfilepath, used)
        return vfilepath

    def start_inventory(self):
        """Create inventory start with metadata from self."""
        inventory = {
            'id': self.identifier,
            'type': 'https://ocfl.io/1.0/spec/#inventory',
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
                vfilepath = self.map_filepath(sfilepath, vdir, manifest_to_srcfile)
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
        Namaste(0, 'ocfl_object_1.0').write(objdir)

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

    def build(self, srcdir, metadata=None, objdir=None):
        """Build an OCFL object and write to objdir if set, else print inventories.

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
        num_versions = 0
        for (vdir, inventory, manifest_to_srcfile) in self.build_inventory(srcdir, metadata=metadata):
            num_versions += 1
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
        logging.info("Built object %s with %s versions" % (self.identifier, num_versions))

    def create(self, srcdir, metadata=None, objdir=None):
        """Create a new OCFL object with v1 content from srcdir.

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
        logging.info("Created object %s in %s" % (self.identifier, objdir))

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

    def extract(self, objdir, version, dstdir):
        """Extract version from object at objdir into dstdir."""
        # Read inventory, set up version
        inv = self.parse_inventory(objdir)
        if version == 'head':
            version = inv['head']
            logging.info("Object at %s has head %s" % (objdir, version))
        elif version not in inv['versions']:
            raise ObjectException("Object at %s does not include a version '%s'" % (objdir, version))
        # Sanity check on destination
        if not os.path.isdir(dstdir):
            raise ObjectException("Destination %s does not exist or is not directory" % (dstdir))
        dstdir = os.path.join(dstdir, version)
        if os.path.exists(dstdir):
            raise ObjectException("Target directorty %s already exists, aborting!" % (dstdir))
        os.mkdir(dstdir)
        # Now extract...
        manifest = inv['manifest']
        state = inv['versions'][version]['state']
        for (digest, logical_files) in state.items():
            existing_file = manifest[digest][0]  # FIXME - pick "best" (closest version?) not first?
            for logical_file in logical_files:
                # FIXME -- need to abstract access so we can, for example, implement S3->local extraction
                logging.debug("Copying %s -> %s" % (digest, logical_file))
                dstfile = os.path.join(dstdir, logical_file)
                dstpath = os.path.dirname(dstfile)
                try:
                    os.makedirs(dstpath)  # exist_ok parameter only in Python 3.2+
                except OSError as e:
                    if not os.path.isdir(dstpath):
                        raise
                copyfile(os.path.join(objdir, existing_file), dstfile)
        logging.info("Extracted %s into %s" % (version, dstdir))

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


def make_unused_filepath(filepath, used, separator='__'):
    """Find filepath with string appended that makes it disjoint from those in used."""
    n = 1
    while True:
        n += 1
        f = filepath + separator + str(n)
        if f not in used:
            return f
