# -*- coding: utf-8 -*-
"""Utility functions to support the OCFL Object library."""
import re

import fs
import fs.path

from ._version import __version__
from .namaste import find_namastes
from .pyfs import pyfs_openfs


NORMALIZATIONS = ["uri", "md5"]  # Must match possibilities in map_filepaths()


class ObjectException(Exception):
    """Exception class for OCFL Object."""


def first_version_directory(zero_padded_width=None):
    """First version directory name with possible zero padding.

    Arguments:
        zero_padded_width: either None (default) to use an unpadded version
            directory name ("v1"), or an integer between 2 and 5 inclusive to
            specify the number of digits used in the version directory name
            (e.g. "v0001" if zero_padded_width=4).

    Returns string of the version directory name.

    Raises Object extension if zero_padded_width is specified but out or range.
    """
    if zero_padded_width is None:
        return "v1"
    # Make appropriate width zero-padded version
    if zero_padded_width < 2 or zero_padded_width > 5:
        raise ObjectException("Width of zero padded version numbers is out of "
                              "range (%d)" % (zero_padded_width))
    return "v" + "0" * (zero_padded_width - 1) + "1"


def next_version_directory(vdir):
    """Next version directory name following existing pattern.

    Arguments:
        vdir: last version directory name string which will follow
            either the recommended unpadded convention (e.g. "v3") or else
            the zero padded convention (e.g. "v00003")

    Returns the next version directory following the existing style of
    zero-padded or non zero-padded.

    Raises an ObjectExtension if the format of version cannot be understood
    or if there is overflow of a zero-padded form.
    """
    m = re.match(r"""v((\d)\d*)$""", vdir)
    if not m:
        raise ObjectException("Bad version directory '%s'" % vdir)
    next_n = int(m.group(1)) + 1
    if m.group(2) == "0":
        # Zero-padded version
        next_v = ("v0%0" + str(len(vdir) - 2) + "d") % next_n
        if len(next_v) != len(vdir):
            raise ObjectException("Version number overflow for zero-padded "
                                  "version directory %s to %s" % (vdir, next_v))
        return next_v
    # Not zero-padded
    return "v" + str(next_n)


def remove_first_directory(path):
    """Remove first directory from input path.

    Aguments:
        path: filesystem path string

    The return value will not have a trailing parh separator, even if
    the input path does. Will return an empty string if the input path
    has just one path segment.
    """
    # FIXME - how to do this efficiently? Current code does complete
    # split and rejoins, excluding the first directory
    rpath = ""
    while True:
        (head, tail) = fs.path.split(path)
        if path in (head, tail):
            break
        path = head
        rpath = tail if rpath == "" else fs.path.join(tail, rpath)
    return rpath


def make_unused_filepath(filepath, used, separator="__"):
    """Find filepath with string appended that makes it disjoint from those in used.

    Arguments:
        filepath: string of filepath to use as basis for one that has not been
            used
        used: dict() or set() that is used to test for filepaths that have
            already be used
        separator: string used to separate the basis filepath from the added
            sequence number in order to build and unused filepath

    Returns filepath string that does not exist in used. Will return the
    supplied filepath if that hasn't been used, otherwise a filepath based
    on that with separator and a sequence integer added.
    """
    print("#USED= " + str(used))
    n = 1
    f = filepath
    while f in used:
        n += 1
        f = filepath + separator + str(n)
    return f


def find_path_type(path):
    """Return a string indicating the type of thing at the given path.

    Arguments:
        path: filesystem path string

    Return values:
        "root" - looks like an OCFL Storage Root
        "object" - looks like an OCFL Object
        "file" - a file, might be an inventory
        other string explains error description

    Looks only at "0=*" Namaste files to determine the directory type.
    """
    try:
        pyfs = pyfs_openfs(path, create=False)
    except (fs.opener.errors.OpenerError, fs.errors.CreateFailed):
        # Failed to open path as a filesystem, try enclosing directory
        # in case path is a file
        (parent, filename) = fs.path.split(path)
        try:
            pyfs = pyfs_openfs(parent, create=False)
        except (fs.opener.errors.OpenerError, fs.errors.CreateFailed) as e:
            return "path cannot be opened, and nor can parent (" + str(e) + ")"
        # Can open parent, is filename a file there?
        try:
            info = pyfs.getinfo(filename)
        except fs.errors.ResourceNotFound:
            return "path does not exist"
        if info.is_dir:
            return "directory that could not be opened as a filesystem, this should not happen"  # pragma: no cover
        return "file"
    namastes = find_namastes(0, pyfs=pyfs)
    if len(namastes) == 0:
        return "no 0= declaration file"
    # Look at the first 0= Namaste file that is of OCFL form to determine type, if there are
    # multiple declarations this will be caught later
    for namaste in namastes:
        m = re.match(r"""ocfl(_object)?_(\d+\.\d+)$""", namaste.tvalue)
        if m:
            return "root" if m.group(1) is None else "object"
    return "unrecognized 0= declaration file or files (first is %s)" % (namastes[0].tvalue)


def parse_version_directory(dirname):
    """Get version number from version directory name.

    Arguments:
        dirname (str): the directory name to parse.

    Returns the integer version number from this version directory name.
    """
    m = re.match(r"""v(\d{1,5})$""", dirname)
    if not m:
        raise ObjectException("Bad version directory name: %s" % (dirname))
    v = int(m.group(1))
    if v == 0:
        raise ObjectException("Bad version directory name: %s, v0 no allowed" % (dirname))
    return v
