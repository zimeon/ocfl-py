# -*- coding: utf-8 -*-
"""Utility functions for OCFL command line tools."""
import os
import logging
import sys

import fs.path

from ._version import __version__


NORMALIZATIONS = ['uri', 'md5']  # Must match possibilities in map_filepaths()


class ObjectException(Exception):
    """Exception class for OCFL Object."""


def add_version_metadata_args(parser):
    """Add version metadata settings to argparse instance parser."""
    parser.add_argument('--created', default=None,
                        help='creation time to be used with version(s) added, else '
                             'current time will be recorded')
    parser.add_argument('--message', default=None,
                        help='message to be recorded with version(s) added')
    parser.add_argument('--name', default=None,
                        help='name of user adding version(s) to object')
    parser.add_argument('--address', default=None,
                        help='address of user adding version(s) to object')


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
    """Check arguments set with add_shared_args, and also set logging."""
    if args.version:
        print("%s is part of ocfl-py version %s" % (fs.path.basename(sys.argv[0]), __version__))
        sys.exit(0)
    # Set up logging
    logging.basicConfig(level=logging.INFO if args.verbose else logging.WARN)


def get_storage_root(args):
    """Get OCFL storage root from --root argument or from $OCFL_ROOT.

    Returns path string. Will throw error if the root is not set.
    """
    if args.root:
        return args.root
    env_root = os.getenv('OCFL_ROOT')
    if env_root is not None:
        return env_root
    logging.error("The storage root must be set either via --root or $OCFL_ROOT")
    sys.exit(1)
