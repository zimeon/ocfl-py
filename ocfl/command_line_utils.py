# -*- coding: utf-8 -*-
"""Utility functions for OCFL command line tools."""
import logging
import sys

import fs.path

from ._version import __version__


NORMALIZATIONS = ['uri', 'md5']  # Must match possibilities in map_filepaths()


class ObjectException(Exception):
    """Exception class for OCFL Object."""


def add_version_arg(parser):
    """Add --version argument."""
    parser.add_argument('--version', action='store_true',
                        help='show version number and exit')


def check_version_arg(args):
    """Check for --version argument."""
    if args.version:
        print("%s is part of ocfl-py version %s" % (fs.path.basename(sys.argv[0]), __version__))
        sys.exit(0)


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


def add_verbosity_args(parser):
    """Add arguments controlling verbosity that are shared by many ocfl-py scripts.

    Parameters:
        parser - and argparse.Parser object
    """
    parser.add_argument('--verbose', '-v', action='store_true',
                        help="be more verbose")
    parser.add_argument('--debug', action='store_true',
                        help="show debugging messages (more verbose than -v)")
    parser.add_argument('--quiet', '-q', action='store_true',
                        help="be quiet, do not show warnings")


def check_verbosity_args(args):
    """Check verbosity arguments and set root logging level.

    Parameters:
        args - arguments from argparse
    """
    level = logging.WARN
    if args.debug:
        level = logging.DEBUG
    elif args.verbose:
        level = logging.INFO
    elif args.quiet:
        level = logging.ERROR
    logging.basicConfig(level=level)


def validate_object(obj, objdir, show_warnings=True, show_errors=True, check_digests=True):
    """Validate object with control of console output.

    Parameters:
        obj - Object() instance
        path - Path to object

    Returns True if passed, False if failed.
    """
    passed, validator = obj.validate(objdir=objdir, show_warnings=show_warnings, show_errors=show_errors, check_digests=check_digests)
    messages = str(validator)
    if messages != '':
        print(messages)
    obj.log.info("OCFL v%s Object at %s is %s",
                 validator.spec_version, objdir,
                 'VALID' if passed else 'INVALID')
    return passed
