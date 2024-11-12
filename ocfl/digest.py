"""Digest handling for OCFL."""
import hashlib

from .pyfs import pyfs_openbin

BUFSIZE = 64 * 1024  # 64kB for want of better info...


def _file_digest(pyfs, filename, digester):
    """Generate a digest for filename using the supplied digester object.

    Like haslib.sha256 and hashlib.sha512, the digester object must
    support the .update() and .hexdigest() methods.
    """
    with pyfs_openbin(filename, "r", pyfs=pyfs) as fh:
        for b in iter(lambda: fh.read(BUFSIZE), b""):
            digester.update(b)
    return digester.hexdigest()


def file_digest(filename, digest_type="sha512", pyfs=None):
    """Digest of digest_type for file filename in normalized form.

    Supports digest_type values from OCFL spec:
        "md5", "sha1", "sha256", "sha512", "blake2b-512"
    and from OCFL extensions
        "blake2b-160", "blake2b-256", "blake2b-384"
    and a truncated sha512 and sha256 useful for examples
        "sha512-spec-ex",  "sha256-spec-ex"

    Arguments:
        filename: string with name of file to calculate digest for
        digest_type: string of digest type
        pyfs: None for local file, else a PyFilesystem2() object within
            which filename exists

    Returns digest string.

    Raises a ValueError exception if the digest_type is not supported.
    """
    # From spec
    if digest_type == "sha512":
        return _file_digest(pyfs, filename, hashlib.sha512())
    if digest_type == "sha256":
        return _file_digest(pyfs, filename, hashlib.sha256())
    if digest_type == "sha1":
        return _file_digest(pyfs, filename, hashlib.sha1())
    if digest_type == "md5":
        return _file_digest(pyfs, filename, hashlib.md5())
    if digest_type == "blake2b-512":
        return _file_digest(pyfs, filename, hashlib.blake2b())
    # From extensions
    if digest_type == "blake2b-160":
        return _file_digest(pyfs, filename, hashlib.blake2b(digest_size=20))
    if digest_type == "blake2b-256":
        return _file_digest(pyfs, filename, hashlib.blake2b(digest_size=32))
    if digest_type == "blake2b-384":
        return _file_digest(pyfs, filename, hashlib.blake2b(digest_size=48))
    # Specification examples: 15/6 chars ... 3 chars. The truncated
    # sha512 is twice as many chars as the truncated sha256 to give
    # a appropriate impression in examples
    if digest_type == "sha512-spec-ex":
        d = _file_digest(pyfs, filename, hashlib.sha512())
        return d[:15] + "..." + d[-3:]
    if digest_type == "sha256-spec-ex":
        d = _file_digest(pyfs, filename, hashlib.sha256())
        return d[:6] + "..." + d[-3:]
    raise ValueError("Unsupport digest type %s" % (digest_type))


def string_digest(txt, digest_type="sha512"):
    """Digest of txt string with given digest in normalized form.

    Argument:
        txt: string value for which digest is calculated
        digest_type: string of digest type

    Returns digest string of the txt input using specified digest type.

    Raises ValueError if the digest type is not supported.
    """
    txt_enc = txt.encode("utf8")
    if digest_type == "sha512":
        return hashlib.sha512(txt_enc).hexdigest()
    if digest_type == "sha256":
        return hashlib.sha256(txt_enc).hexdigest()
    if digest_type == "sha1":
        return hashlib.sha1(txt_enc).hexdigest()
    if digest_type == "md5":
        return hashlib.md5(txt_enc).hexdigest()
    raise ValueError("Unsupport digest type %s" % (digest_type))


DIGEST_REGEXES = {
    "sha512": r"""^[0-9a-fA-F]{128}$""",
    "sha256": r"""^[0-9a-fA-F]{64}$""",
    "sha1": r"""^[0-9a-fA-F]{40}$""",
    "md5": r"""^[0-9a-fA-F]{32}$""",
    "blake2b-512": r"""^[0-9a-fA-F]{128}$""",
    "blake2b-384": r"""^[0-9a-fA-F]{96}$""",
    "blake2b-256": r"""^[0-9a-fA-F]{64}$""",
    "blake2b-160": r"""^[0-9a-fA-F]{40}$""",
    "sha512-spec-ex": r"""^[0-9a-f]{6}\.\.\.[0-9a-f]{3}$""",
    "sha256-spec-ex": r"""^[0-9a-f]{6}\.\.\.[0-9a-f]{3}$"""
}


def digest_regex(digest_type="sha512"):
    """Regex to be used to check the un-normalized form of a digest string.

    Argument:
        digest_type: string of digest type

    Returns regex if the digest type is recognized.

    Raises a ValueError otherwise.
    """
    try:
        return DIGEST_REGEXES[digest_type]
    except KeyError:
        raise ValueError("Unsupport digest type %s" % (digest_type))


def normalized_digest(digest, digest_type="sha512"):
    """Normalize the digest to return version that enables string comparison.

    Arguments:
        digest: digest string
        digest_type: string with digest type

    At present, digest types supported (except the spec example forms) are case
    insensitive. We use lowercase as the normalized form.
    """
    if digest_type in ("sha512-spec-ex", "sha256-spec-ex"):
        return digest
    return digest.lower()
