"""Metadata for a version of OCFL Object's content."""
from .w3c_datetime import datetime_to_str


def add_version_metadata_args(parser):
    """Add version metadata settings to argarse instance."""
    parser.add_argument('--created', default=None,
                        help='creation time to be used with version(s) added, else '
                             'current time will be recorded')
    parser.add_argument('--message', default='',
                        help='message to be recorded with version(s) added')
    parser.add_argument('--name', default='someone',
                        help='name of user adding version(s) to object')
    parser.add_argument('--address', default='somewhere',
                        help='address of user adding version(s) to object')


class VersionMetadata(object):
    """Class for metadata for a version of OCFL Object's content."""

    def __init__(self, args):
        """Initialize from command line arguments from argparse."""
        self.created = args.created
        self.message = args.message
        self.name = args.name
        self.address = args.address

    def as_dict(self, **kwargs):
        """Dictionary object with versin metedata."""
        m = {}
        self.add_to_dict(m, **kwargs)
        return m

    def add_to_dict(self, m, **kwargs):
        """Add metadata to dictionary m."""
        m['type'] = 'Version'
        m['created'] = self.created if self.created else datetime_to_str()
        m['message'] = self.message
        m['user'] = {'name': self.name, 'address': self.address}
        # Add any extra values, and they will override instance variables
        for (key, value) in kwargs.items():
            m[key] = value
