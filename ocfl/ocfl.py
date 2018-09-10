"""Core of OCFL library."""
import hashlib
import json
import os
import os.path
import re
import logging
from shutil import copyfile

from .digest import *
from .validator import OCFLValidator


class OCFL(object):
    """Class for handling OCFL data and operations."""

    def __init__(self, digest_type='sha512', skips=None):
        """Initialize OCFL builder."""
        self.digest_type = digest_type
        self.skips = set() if skips is None else set(skips)
        self.validation_codes = None

    def parse_version_directory(self, dirname):
        """Get version number from version directory name."""
        m = re.match(r'''v(\d{1,5})$''', dirname)
        if not m:
            raise Exception("Bad directory name: %s" % (dirname))
        return int(m.group(1))

    def digest(self, filename):
        """Digest for file filename."""
        return file_digest(filename, self.digest_type)

    def add_version(self, inventory, path, vdir, forward_delta=True, dedupe=True, rename=True):
        """Add to inventory data for new version based on files in path/vdir."""
        this_version = {'version': vdir,
                        'type': 'Version'}
        inventory['versions'].append(this_version)
        state = {}
        this_version['state'] = state
        manifest = inventory['manifest']
        # Go through all files to find new files in manifest and state for each version
        for (dirpath, dirnames, filenames) in os.walk(os.path.join(path, vdir), followlinks=True):
            # Go through filenames, in sort order so the it is deterministic
            # which file is included and which is/are referenced in the case
            # of multiple additions with the same digest
            digests_in_version = {}
            for filename in sorted(filenames):
                filepath = os.path.join(dirpath, filename)
                vfilepath = os.path.relpath(filepath, path)  # path relative to roob, inc v#
                sfilepath = os.path.relpath(vfilepath, vdir)  # path relative to this version
                digest = self.digest(filepath)
                # Always add file to state
                if digest not in state:
                    state[digest] = []
                state[digest].append(sfilepath)
                if forward_delta and digest in manifest:
                    # We already have this content in a previous version and we are using
                    # forward deltas so do not need to copy in this one
                    pass
                else:
                    # This is a new digest so an addition in this version and
                    # we save the information for later includes
                    if digest not in digests_in_version:
                        digests_in_version[digest] = [vfilepath]
                    elif not dedupe:
                        digests_in_version[digest].append(vfilepath)
            # Add any new digests in this version to the manifest
            for digest, paths in digests_in_version.items():
                if digest not in manifest:
                    manifest[digest] = paths
                else:
                    for p in paths:
                        manifest[digest].append(p)

    def build_inventory(self, path, forward_delta=True, dedupe=True, rename=True):
        """Generator for building an OCFL inventory.

        Yields (vdir, inventory) for each version in sequence, where vdir is
        the version directory name and inventory is the inventory for that
        version.
        """
        inventory = {
            '@context': 'https://ocfl.io/1.0/context.jsonld',
            'type': 'OCFLObject',
            'digest': self.digest_type,
            'versions': [],
            'manifest': {}
        }
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
            self.add_version(inventory, path, vdir, forward_delta, dedupe, rename)
            yield (vdir, inventory)

    def write_object_declaration(self, dstdir):
        """Write NAMASTE object declaration to dstdir."""
        namastefile = os.path.join(dstdir, '0=ocfl_object_1.0')
        with open(namastefile, 'w') as fh:
            pass  # empty file

    def write_inventory_and_sidecar(self, dstdir, inventory):
        """Write inventory and sidecar to dstdir."""
        invfilename = 'inventory.jsonld'
        if not os.path.exists(dstdir):
            os.makedirs(dstdir)
        invfile = os.path.join(dstdir, invfilename)
        with open(invfile, 'w') as fh:
            json.dump(inventory, fh, sort_keys=True, indent=2)
        sidecar = os.path.join(dstdir, invfilename + '.' + self.digest_type)
        digest = file_digest(invfile, self.digest_type)
        with open(sidecar, 'w') as fh:
            fh.write(digest + ' ' + invfilename + '\n')

    def write_ocfl_object(self, srcdir, forward_delta=True, dedupe=True, rename=True, dstdir=None):
        """Write out OCFL object to dst if set, else print inventory."""
        if dstdir is not None:
            os.makedirs(dstdir)
        for (vdir, inventory) in self.build_inventory(srcdir, forward_delta=True, dedupe=True, rename=True):
            if dstdir is None:
                print("\n\n### Inventory for %s\n" % (vdir))
                print(json.dumps(inventory, sort_keys=True, indent=2))
            else:
                self.write_inventory_and_sidecar(os.path.join(dstdir, vdir), inventory)
        if dstdir is None:
            return
        # Write NAMASTE, inventory and sidecar
        self.write_object_declaration(dstdir)
        self.write_inventory_and_sidecar(dstdir, inventory)
        # Write version files
        for digest, paths in inventory['manifest'].items():
            for path in paths:
                (head, tail) = os.path.split(path)
                srcfile = os.path.join(srcdir, path)
                dstpath = os.path.join(dstdir, head)
                dstfile = os.path.join(dstdir, path)
                if not os.path.exists(dstpath):
                    os.makedirs(dstpath)
                copyfile(srcfile, dstfile)

    def validate(self, path):
        """Validate OCFL object at path."""
        validator = OCFLValidator()
        passed = validator.validate(path)
        if passed:
            print("OCFL object at %s is VALID" % (path))
        else:
            print("OCFL object at %s is INVALID" % (path))
        print(str(validator))
