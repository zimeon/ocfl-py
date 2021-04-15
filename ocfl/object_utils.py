# -*- coding: utf-8 -*-
"""Utility functions to support the OCFL Object library."""
import re
import sys

import fs
import fs.path

from ._version import __version__
from .namaste import find_namastes
from .pyfs import open_fs


NORMALIZATIONS = ['uri', 'md5']  # Must match possibilities in map_filepaths()


class ObjectException(Exception):
    """Exception class for OCFL Object."""


def add_object_args(parser):
    """Add Object settings to argparse or argument group instance parser."""
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
    # Validation settings
    parser.add_argument('--lax-digests', action='store_true',
                        help='allow use of any known digest')
    # Object files
    parser.add_argument('--objdir', '--obj',
                        help='read from or write to OCFL object directory objdir')


def add_shared_args(parser):
    """Add arguments to be shared by any ocfl-py scripts."""
    parser.add_argument('--verbose', '-v', action='store_true',
                        help="be more verbose")
    parser.add_argument('--version', action='store_true',
                        help='Show version number and exit')


def check_shared_args(args):
    """Check arguments set with add_shared_args."""
    if args.version:
        print("%s is part of ocfl-py version %s" % (fs.path.basename(sys.argv[0]), __version__))
        sys.exit(0)


def next_version(version):
    """Next version identifier following existing pattern.

    Must deal with both zero-prefixed and non-zero prefixed versions.
    """
    m = re.match(r'''v((\d)\d*)$''', version)
    if not m:
        raise ObjectException("Bad version '%s'" % version)
    next = int(m.group(1)) + 1
    if m.group(2) == '0':
        # Zero-padded version
        next_v = ('v0%0' + str(len(version) - 2) + 'd') % next
        if len(next_v) != len(version):
            raise ObjectException("Version number overflow for zero-padded version %d to %d" % (version, next_v))
        return next_v
    # Not zero-padded
    return 'v' + str(next)


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
        (head, tail) = fs.path.split(path)
        if path in (head, tail):
            break
        path = head
        rpath = tail if rpath == '' else fs.path.join(tail, rpath)
    return rpath


def make_unused_filepath(filepath, used, separator='__'):
    """Find filepath with string appended that makes it disjoint from those in used."""
    n = 1
    while True:
        n += 1
        f = filepath + separator + str(n)
        if f not in used:
            return f


def find_path_type(path):
    """Return a string indicating the type of thing at the given path.

    Return values:
        'root' - looks like an OCFL Storage Root
        'object' - looks like an OCFL Object
        'file' - a file, might be an inventory
        other string explains error description

    Looks only at "0=*" Namaste files to determine the directory type.
    """
    try:
        pyfs = open_fs(path, create=False)
    except (fs.opener.errors.OpenerError, fs.errors.CreateFailed):
        # Failed to open path as a filesystem, try enclosing directory
        # in case path is a file
        (parent, filename) = fs.path.split(path)
        try:
            pyfs = open_fs(parent, create=False)
        except (fs.opener.errors.OpenerError, fs.errors.CreateFailed) as e:
            return "path cannot be opened, and nor can parent (" + str(e) + ")"
        # Can open parent, is filename a file there?
        try:
            info = pyfs.getinfo(filename)
        except fs.errors.ResourceNotFound:
            return "path does not exist"
        if info.is_dir:
            return "directory that could not be opened as a filesystem, this should not happen"  # pragma: no cover
        return 'file'
    namastes = find_namastes(0, pyfs=pyfs)
    if len(namastes) == 0:
        return "no 0= declaration file"
    if len(namastes) > 1:
        return "more than one 0= declaration file"
    m = re.match(r'''ocfl(_object)?_(\d+\.\d+)$''', namastes[0].tvalue)
    if m:
        return 'root' if m.group(1) is None else 'object'
    return "unrecognized 0= declaration file 0=%s" % (namastes[0].tvalue)
