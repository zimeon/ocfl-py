"""Support for use of Bagit bags with OCFL.

Two scenarios:

1) A Bagit bag is used as the source for the content of one version of an
OCFL object.

2) A Bagit bag is used as the output destination for the content extracted
from one version of an OCFL object.

This code relies upon the https://github.com/LibraryOfCongress/bagit-python
library code to implement "The BagIt File Packaging Format" specification
https://tools.ietf.org/html/rfc8493 . Unlike OCFL, BagIt does not natively
support versioning but is widely used as a transfer format and is thus well
suited to transferring content that might be used to update an OCLF object
or disseminate a particular version.
"""
import os.path
import bagit


class BaggerError(Exception):
    """Exception class for conditions that should abort with message."""


def bag_as_source(srcbag, metadata):
    """Validate and read metadata from srcbag as input.

    The notion of a bag being valid includes it being complete, ie. not having
    a fetch.txt to provide URLs for files that are not included in local
    filesystem. We thus don't need to test for that case, bagit.is_valid() is
    enough.

    Parameters:
        srcbag - The directory of the bag on disk
        metadata - A VersionMetadata object that will be updated with metadata
            from the bag

    Returns the srcdir for OCFL object content within the bag as it should be
    expressed in the state block.
    """
    bag = bagit.Bag(srcbag)
    if not bag.is_valid():
        raise BaggerError("Source Bagit bag at %s is not valid" % (srcbag))
    # Local arguments override but otherwise take metadata from bag-info.txt
    if not metadata.id and 'External-Identifier' in bag.info:
        metadata.id = bag.info['External-Identifier']
    if not metadata.created and 'Bagging-Date' in bag.info:
        metadata.created = bag.info['Bagging-Date'] + 'T00:00:00Z'  # FIXME - timezone fudge
    if not metadata.message and 'External-Description' in bag.info:
        metadata.message = bag.info['External-Description']
    if not metadata.name and 'Contact-Name' in bag.info:
        metadata.name = bag.info['Contact-Name']
    if not metadata.address and 'Contact-Email' in bag.info:
        metadata.address = 'mailto:' + bag.info['Contact-Email']
    return os.path.join(srcbag, 'data')


def bag_extracted_version(dst, metadata):
    """Bag the extracted files in dst using metadata from metadata.

    Paramaters:
        dst - Destination location for the bag that initially contains the
            content to be bagged (ie. end up in the data directory)
        metadata - A VersionMetadata object that has metadata to add into
            the bag information
    """
    tags = {}
    if metadata.id:
        tags['External-Identifier'] = metadata.id
    if metadata.message:
        tags['External-Description'] = metadata.message
    if metadata.name:
        tags['Contact-Name'] = metadata.name
    if metadata.address and metadata.address.startswith('mailto:'):
        tags['Contact-Email'] = metadata.address[7:]
    bagit.make_bag(dst, bag_info=tags, checksums=['sha512'])
