"""NAMASTE file support.

NAMASTE spec: http://www.cdlib.org/inside/diglib/namaste/namastespec.html

See also command line tool: http://github.com/mjgiarlo/namaste
"""
import os
import os.path
import re
import fs


def content_to_tvalue(content):
    """Safe and limited length tvalue from content.

    Return string will be at most 40 characters, trimmed of starting or ending
    whitespace, any input characters not word, dot, hyphen, underscore, colon
    will be converted to underscore.
    """
    content = content.strip()
    return re.sub(r'''[^\w\.\-:]''', '_', content[:40])


def find_namastes(d, dir='', pyfs=None, limit=10):
    """Find NAMASTE files with tag d in dir, return list of Namaste objects.

    limit sets a limit on the number of Namaste objects returned, a NamasteException
    will be raised if more than limit files with tag d are found.
    """
    prefix = str(d) + '='
    if pyfs is not None:
        filenames = [f for f in pyfs.listdir(dir) if f.startswith(prefix)]
    else:
        filenames = [f for f in os.listdir(dir) if f.startswith(prefix)]
    if len(filenames) > limit:
        raise NamasteException("Found too many Namaste files with tag %s in %s" % (d, dir))
    return [Namaste(d, tvalue=filename[len(prefix):]) for filename in filenames]


def get_namaste(d, dir):
    """Find NAMASTE file with tag d in dir, return Namaste object.

    Raises NamasteException if not exaclty one.
    """
    namastes = find_namastes(d, dir, limit=1)
    if len(namastes) != 1:
        raise NamasteException("Failed to find one Namaste file with tag %s in %s" % (str(d), dir))
    return namastes[0]


class NamasteException(Exception):
    """Class for exceptions from Namaste."""


class Namaste():
    """Class implementing NAMASTE specification."""

    def __init__(self, d=0, content='', tvalue=None, tr_func=content_to_tvalue):
        """Initialize Namaste object.

        Parameters:
            d - tag name, D in NAMASTE specification
            content - metadata content of NAMASTE file from which tvalue is derived
            tvalue - explicity set tvalue instead of deriving
            tr_func - function reference used to derive a tvalue from content,
                overriding default content_to_tvalue
        """
        self.d = d
        self.content = content
        self._tvalue = tvalue
        self._tr_func = tr_func

    @property
    def filename(self):
        """Filename of Namaste file."""
        return str(self.d) + '=' + self.tvalue

    @property
    def tvalue(self):
        """Tvalue of Namaste file."""
        if self._tvalue is not None:
            return self._tvalue
        return self._tr_func(self.content)

    def write(self, dir='', pyfs=None):
        """Write NAMASTE file to dir, optionally in fs.

        Handle both a dirctory with in a pyfs filesystem (if pyfs is set) or
        else just a directory with plain os file support.

        e.g.
            Namaste(0, 'ocfl_1.0').write(pyfs=obj_fs)
        or
            Namaste(0, 'ocfl_1.0').write(dir)
        """
        if pyfs is not None:
            pyfs.writetext(fs.path.join(dir, self.filename), self.content + "\n")
        else:
            with open(os.path.join(dir, self.filename), 'w') as fh:
                fh.write(self.content + "\n")

    def check_content(self, dir='', pyfs=None):
        """Check that the file content is compatible with the tvalue based on tr_func, else raise NamasteException."""
        filepath = fs.path.join(dir, self.filename)
        if self.tvalue == '':
            raise NamasteException("Cannot check Namaste file %s without tvalue being set!" % (filepath))
        if pyfs is not None:
            try:
                content = pyfs.readtext(filepath)
            except fs.errors.ResourceNotFound:
                raise NamasteException("Namaste file %s cannot be read!" % (filepath))
        else:
            if not os.path.isfile(filepath):
                raise NamasteException("Namaste file %s does not exist!" % (filepath))
            with open(filepath, 'r') as fh:
                content = fh.read()
        if self.tvalue != self._tr_func(content):
            raise NamasteException("Content of Namaste file %s doesn't match tvalue %s" % (filepath, self.tvalue))

    def content_ok(self, dir='', pyfs=None):
        """Return True if check_content() does not raise a NamasteException exception."""
        try:
            self.check_content(dir, pyfs)
        except NamasteException:
            return False
        return True
