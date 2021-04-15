"""Digest handling for OCFL."""
import hashlib
import fs
from .pyfs import open_fs

BUFSIZE = 64 * 1024  # 64kB for want of better info...


def _fs_digest(pyfs, filename, digester):
    """Update digester reading from fh."""
    with pyfs.openbin(filename, 'r') as fh:
        for b in iter(lambda: fh.read(BUFSIZE), b''):
            digester.update(b)


def _file_digest(pyfs, filename, digester):
    """Generate a digest for filename using the supplied digester object.

    Like haslib.sha256 and hashlib.sha512, the digester object must
    support the .update() and .hexdigest() methods.
    """
    if pyfs is None:
        (dir, name) = fs.path.split(filename)
        with open_fs(dir) as dir_fs:
            _fs_digest(dir_fs, name, digester)
    else:
        _fs_digest(pyfs, filename, digester)
    return digester.hexdigest()


def file_digest(filename, digest_type='sha512', pyfs=None):
    """Digest of digest_type for file filename in normalized form.

    Supports digest_type values from OCFL spec:
        'md5', 'sha1', 'sha256', 'sha512', 'blake2b-512'
    and from OCFL extensions
        'blake2b-160', 'blake2b-256', 'blake2b-384'
    and a truncated sha512 and sha256 useful for examples
        'sha512-spec-ex',  'sha256-spec-ex'

    Raises an exception if the digest_type is not supported.
    """
    # From spec
    if digest_type == 'sha512':
        return _file_digest(pyfs, filename, hashlib.sha512())
    if digest_type == 'sha256':
        return _file_digest(pyfs, filename, hashlib.sha256())
    if digest_type == 'sha1':
        return _file_digest(pyfs, filename, hashlib.sha1())
    if digest_type == 'md5':
        return _file_digest(pyfs, filename, hashlib.md5())
    if digest_type == 'blake2b-512':
        return _file_digest(pyfs, filename, hashlib.blake2b())
    # From extensions
    if digest_type == 'blake2b-160':
        return _file_digest(pyfs, filename, hashlib.blake2b(digest_size=20))
    if digest_type == 'blake2b-256':
        return _file_digest(pyfs, filename, hashlib.blake2b(digest_size=32))
    if digest_type == 'blake2b-384':
        return _file_digest(pyfs, filename, hashlib.blake2b(digest_size=48))
    # Specification examples: 15/6 chars ... 3 chars. The truncated
    # sha512 is twice as many chars as the truncated sha256 to give
    # a appropriate impression in examples
    if digest_type == 'sha512-spec-ex':
        d = _file_digest(pyfs, filename, hashlib.sha512())
        return d[:15] + '...' + d[-3:]
    if digest_type == 'sha256-spec-ex':
        d = _file_digest(pyfs, filename, hashlib.sha256())
        return d[:6] + '...' + d[-3:]
    raise ValueError("Unsupport digest type %s" % (digest_type))


DIGEST_REGEXES = {
    'sha512': r'''^[0-9a-fA-F]{128}$''',
    'sha256': r'''^[0-9a-fA-F]{64}$''',
    'sha1': r'''^[0-9a-fA-F]{40}$''',
    'md5': r'''^[0-9a-fA-F]{32}$''',
    'blake2b-512': r'''^[0-9a-fA-F]{128}$''',
    'blake2b-384': r'''^[0-9a-fA-F]{96}$''',
    'blake2b-256': r'''^[0-9a-fA-F]{64}$''',
    'blake2b-160': r'''^[0-9a-fA-F]{40}$''',
    'sha512-spec-ex': r'''^[0-9a-f]{15}\.\.\.[0-9a-f]{3}$''',
    'sha256-spec-ex': r'''^[0-9a-f]{6}\.\.\.[0-9a-f]{3}$'''
}


def digest_regex(digest_type='sha512'):
    """Regex to be used to check the un-normalized form of a digest string."""
    try:
        return DIGEST_REGEXES[digest_type]
    except KeyError:
        raise ValueError("Unsupport digest type %s" % (digest_type))


def normalized_digest(digest, digest_type='sha512'):
    """Normalize the digest to return version that enables string comparison.

    All forms (except the spec example forms) are case insensitive. We
    use lowercase as the normalized form.
    """
    if digest_type in ('sha512-spec-ex', 'sha256-spec-ex'):
        return digest
    return digest.lower()
