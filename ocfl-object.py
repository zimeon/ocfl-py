#!/usr/bin/env python
"""OCFL Object and Inventory builder command line tool.

This tool has no awareness of storage roots or the structure
and requirements around them. It is designed to manipulate
OCFL Objects or just Inventory files alone.
"""
import argparse
import logging
import sys

import ocfl
from ocfl.command_line_utils import add_version_arg, check_version_arg, \
    add_version_metadata_args, add_object_args, add_verbosity_args, \
    check_verbosity_args, validate_object


class FatalError(Exception):
    """Exception class for conditions that should abort with message."""


def add_common_args(parser, include_version_metadata=False, objdir_required=True):
    """Add argparse arguments that are common to many commands."""
    add_verbosity_args(parser)
    # Object files
    parser.add_argument("--objdir", "--obj", required=objdir_required,
                        help="read from or write to OCFL object directory objdir")
    # Version metadata and object settings
    obj_params = parser.add_argument_group(title="OCFL object parameters")
    obj_params.add_argument("--spec-version", "--spec", action="store", default="1.1",
                            help="OCFL specification version to adhere to")
    obj_params.add_argument("--digest", default="sha512",
                            help="digest algorithm to use")
    obj_params.add_argument("--fixity", action="append",
                            help="add fixity type to add")
    obj_params.add_argument("--id", default=None,
                            help="identifier of object")
    add_object_args(obj_params)
    if include_version_metadata:
        add_version_metadata_args(obj_params)


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Manipulate or validate an OCFL Object or Inventory.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # The only options at the top level are --help and --version
    add_version_arg(parser)

    subparsers = parser.add_subparsers(
        dest="cmd",
        help="(Show sub-command help with command -h)")

    # Separate sub-parsers for each command
    create_parser = subparsers.add_parser(
        "create",
        help="create a new object from version 1 files in --srcdir or "
             "--srcbag, and metadata optionally specified via arguments")
    add_common_args(create_parser, include_version_metadata=True, objdir_required=False)
    create_parser.add_argument("--srcdir", "--src", action="store",
                               help="source directory path")
    create_parser.add_argument("--srcbag", action="store",
                               help="source Bagit bag path (alternative to --srcdir)")

    build_parser = subparsers.add_parser(
        "build",
        help="build a new object from version directories in --srcdir, and "
             "metadata optionally specified in a JSON file")
    add_common_args(build_parser, objdir_required=False)
    build_parser.add_argument("--srcdir", "--src", action="store",
                              help="source directory path")
    build_parser.add_argument("--metadata", action="store",
                              help="path to inventory format JSON file containing metadata (created, message, user) for each version to build")

    update_parser = subparsers.add_parser(
        "update",
        help="update an object by adding a new version from files in --srcdir "
             "or from --srcbag")
    add_common_args(update_parser, include_version_metadata=True)
    update_parser.add_argument("--srcdir", "--src", action="store",
                               help="source directory path")
    update_parser.add_argument("--srcbag", action="store",
                               help="source Bagit bag path (alternative to --srcdir)")

    add_parser = subparsers.add_parser(
        "show",
        help="show versions and files in an OCFL object")
    add_common_args(add_parser)

    validate_parser = subparsers.add_parser(
        "validate",
        help="validate an OCFL object (use ocfl-validate.py for more control)")
    add_common_args(validate_parser)

    extract_parser = subparsers.add_parser(
        "extract",
        help="extract a specific version (or `head`) into --dstdir")
    add_common_args(extract_parser)
    extract_parser.add_argument("--objver", action="store", default="head",
                                help="object version content to extract (defaults to latest version)")
    extract_parser.add_argument("--dstdir", "--dst", action="store", default="/tmp/ocfl-out",
                                help="destination directory path")
    extract_parser.add_argument("--dstbag", action="store",
                                help="destination Bagit bag path (alternative to --dstdir)")
    extract_parser.add_argument("--logical-path", "--path", action="store", default=None,
                                help="if specified, extract just the file at the specified logical path into --dstdir")

    args = parser.parse_args()
    check_version_arg(args)
    if args.cmd is None:
        raise FatalError("No command, nothing to do (use -h to show help)")
    check_verbosity_args(args)

    return args


def print_inventory(inventory):
    """Print out the inventory."""
    print("### Inventory for %s" % (inventory.head))
    print(inventory.as_json())


def do_object_operation(args):
    """Implement object operations in a way that can be reused by ocfl.py."""
    obj = ocfl.Object(identifier=args.id,
                      spec_version=args.spec_version,
                      digest_algorithm=args.digest,
                      filepath_normalization=args.normalization,
                      forward_delta=not args.no_forward_delta,
                      dedupe=not args.no_dedupe,
                      lax_digests=args.lax_digests,
                      fixity=args.fixity)
    if args.cmd == "create":
        srcdir = args.srcdir
        metadata = ocfl.VersionMetadata(created=args.created,
                                        message=args.message,
                                        name=args.name,
                                        address=args.address)
        if args.srcbag is not None:
            srcdir = ocfl.bag_as_source(args.srcbag, metadata)
            if metadata.id is not None:
                if obj.id is None:
                    obj.id = metadata.id
                elif obj.id != metadata.id:
                    raise FatalError("Identifier specified (%s) and identifier from Bagit bag (%s) do not match!" % (obj.id, metadata.id))
        elif args.srcdir is None:
            raise FatalError("Must specify either --srcdir or --srcbag containing v1 files when creating an OCFL object!")
        inventory = obj.create(srcdir=srcdir,
                               metadata=metadata,
                               objdir=args.objdir)
        if args.objdir is None:
            print_inventory(inventory)
    elif args.cmd == "build":
        if args.srcdir is None:
            raise FatalError("Must specify --srcdir containing version directories when building an OCFL object!")
        # Read in per version metadata if given. This is just like reading an
        # inventory
        versions_metadata = {}
        if args.metadata is not None:
            inv = ocfl.Inventory(filepath=args.metadata)
            for version in inv.versions():
                versions_metadata[version.number] = ocfl.VersionMetadata(inventory=inv, version=version.vdir)
        # Build the object
        inventory = obj.build(srcdir=args.srcdir,
                              versions_metadata=versions_metadata,
                              objdir=args.objdir)
        if args.objdir is None:
            print_inventory(inventory)
    elif args.cmd == "update":
        srcdir = args.srcdir
        metadata = ocfl.VersionMetadata(created=args.created,
                                        message=args.message,
                                        name=args.name,
                                        address=args.address)
        if args.srcbag is not None:
            srcdir = ocfl.bag_as_source(args.srcbag, metadata)
        elif args.srcdir is None:
            raise FatalError("Must specify either --srcdir or --srcbag containing new version files when updating an OCFL object!")
        obj.update(objdir=args.objdir,
                   srcdir=srcdir,
                   metadata=metadata)
    elif args.cmd == "show":
        print("Object tree for %s\n%s" % (obj.id, obj.tree(objdir=args.objdir)))
    elif args.cmd == "validate":
        validate_object(obj, objdir=args.objdir)
    elif args.cmd == "extract":
        if args.logical_path:
            if args.dstbag:
                raise FatalError("Cannot extract a single file to a Bagit bag.")
            metadata = obj.extract_file(objdir=args.objdir,
                                        version=args.objver,
                                        logical_path=args.logical_path,
                                        dstdir=args.dstdir)
            print("Extracted %s in %s to %s" % (args.logical_path, metadata.version, args.dstdir))
        else:
            if args.dstdir and args.dstbag:
                args.dstdir = None  # Override dstdir if dstbag specified
            dst = args.dstdir or args.dstbag
            metadata = obj.extract(objdir=args.objdir,
                                   version=args.objver,
                                   dstdir=dst)
            if args.dstdir:
                print("Extracted content for %s in %s" % (metadata.version, dst))
            else:  # args.dstbag
                ocfl.bag_extracted_version(dst, metadata)
                print("Extracted content for %s saved as Bagit bag in %s" % (metadata.version, dst))
    else:
        logging.error("Unrecognized command!")


if __name__ == "__main__":
    try:
        aargs = parse_arguments()
        do_object_operation(aargs)
    except (FatalError, ocfl.ObjectException) as e:
        logging.error(str(e))
        sys.exit(1)
