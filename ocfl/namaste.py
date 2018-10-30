"""NAMASTE file support.

NAMASTE spec: http://www.cdlib.org/inside/diglib/namaste/namastespec.html

See also command line tool: http://github.com/mjgiarlo/namaste
"""


class Namaste(object):
    """Class implementing NAMASTE specification."""

    def __init__(self, d=None, tvalue=None, content=None):
        """Initialize Namaste object."""
        self.d = d
        self.tvalue = tvalue
        self.content = content

    @property
    def filename(self):
        """Filename of Namaste file."""
        return self.d + '=' + self.tvalue

    @property
    def content(self):
        """Content of Namaste file."""
        if self.content is not None:
            return self.content
        else:
            return self.tvalue

    def write(self, dir):
        """Write NAMASTE file to dir.

        e.g.
            Namaste(0, 'ocfl_1.0').write(dir)
        """
        with open(os.path.join(dir, self.filename), 'w') as fh:
            fh.write(self.content)

    def find(self, d):
        """Find NAMASTE files with given d."""
        pass

    def get(self, d):
        """Get NAMASTE file with given d.

        raise NamasteException if more than one.
        """
        pass
