"""Wrapper for PyFilesystem2 to deal with ocfl-py needs.

S3FS documentation: https://fs-s3fs.readthedocs.io/en/latest/

But note limitations: https://fs-s3fs.readthedocs.io/en/latest/#limitations
which points out that by default the S3FS implementation creates and requires
empty objects with names ending in slash that record that a directory
exists.

It seems to be the case the using `strict=False` avoids checks for these empty
directories. There is no way to pass the `strict` parameter via the open_fs()
function so we need to call the S3FS creator method directly.
"""
import fs
import fs.base
import fs.opener
from fs.osfs import OSFS
from fs_s3fs import S3FS


def _pyfs_or_local(pyfs):
    """Open local filesytem is pyfs not set.

    Arguments:
        pyfs: an fs filesystem else None

    Simply returns pyfs if set, else if pyfs is None then we open a local
    filesystem and return that.
    """
    return fs.open_fs(".") if pyfs is None else pyfs


def pyfs_openfs(fs_url, **kwargs):
    """Open a pyfs filesystem.

    Arguments:
        fs_url: filesystem url to open, use "." for local filesystem rooted
            in current working directory

    Like fs.open_fs will simply return FS if an instance is given as
    the fs_url parameter. Otherwise will attempt to open the fs_url
    as either a local filesystem path (no `://` in string) or else
    as a FS filesystem with special handling for the case of an S3
    filesystem which has
    """
    if isinstance(fs_url, fs.base.FS):
        return fs_url

    # Now assume a string that may be a path (no ://) or else a filesystem URL
    if "://" not in fs_url:
        # A path, assume this is not URI escaped which is what the OSFS(..)
        # creator assumes (as opposed to open_fs(..))
        return OSFS(fs_url, **kwargs)

    # We have a URL, parse it
    parse_result = fs.opener.parse(fs_url)
    if parse_result.protocol == "s3":
        # And S3 URL, mostly repeat
        # https://github.com/PyFilesystem/s3fs/blob/master/fs_s3fs/opener.py
        # but adjust the handling of strict to default to strict=False
        bucket_name, _, dir_path = parse_result.resource.partition("/")
        if not bucket_name:
            raise fs.opener.errors.OpenerError("invalid bucket name in '{}'".format(fs_url))
        # Instead of the default opener behavior where strict is True unless
        # explicitly set !=1 in the URL query paremeter, we set False unless
        # explicity set via strict=1 in the URL query params
        strict = (
            parse_result.params["strict"] == "1"
            if "strict" in parse_result.params
            else False
        )
        s3fs = S3FS(
            bucket_name,
            dir_path=dir_path or "/",
            aws_access_key_id=parse_result.username or None,
            aws_secret_access_key=parse_result.password or None,
            endpoint_url=parse_result.params.get("endpoint_url", None),
            acl=parse_result.params.get("acl", None),
            cache_control=parse_result.params.get("cache_control", None),
            strict=strict)
        # Patch in version of getinfo method that doesn't check parent directory
        s3fs.getinfo = s3fs._getinfo  # pylint: disable=protected-access
        return s3fs
    # Non-S3 URL
    return fs.open_fs(fs_url, **kwargs)


def pyfs_walk(pyfs, dir="/", is_storage_root=False):
    """Walk that works on pyfs filesystems including S3 without the need for directory objects.

    Arguments:
        pyfs: fs filesytem to use
        dir: string of directory to start from (default /)
        is_storage_root: boolean that affects behaviour according to whether
            this is a storage root, default False

    Assumes that f.getinfo() will work for a file/resource that exists and
    that fs.errors.ResourceNotFound might be raised if called on a filesystem
    without directories (and no directory objects).

    For walking storage roots (is_storage_root=True) then the condition to
    descend is:
        1) this is the root (dirpath == "/"), or
        2) there are no files in this directory (see
           https://ocfl.io/1.0/spec/#root-structure)

    For each directory will yield (dirpath, dirs, files) as does os.walk. The
    value of dirs my be pruned to avoid descending into particular directories.

    FIXME - QUICK AND DIRTY HACK, CAN DO BETTER!
    """
    if not dir.startswith("/"):
        dir = "/" + dir
    stack = [dir]
    while len(stack) > 0:
        dirpath = stack.pop()
        entries = pyfs.listdir(dirpath)
        files = []
        dirs = []
        for entry in entries:
            entry_path = fs.path.join(dirpath, entry)
            is_dir = True
            try:
                info = pyfs.getinfo(entry_path)
                is_dir = info.is_dir
            except fs.errors.ResourceNotFound:
                pass  # Assume to be a directory
            if is_dir:
                dirs.append(entry)
            else:
                files.append(entry)
        yield (dirpath, dirs, files)
        # dirs may have been modified to prune
        if not is_storage_root or dirpath == "/" or len(files) == 0:
            # If this is not the storage root itself and there are files
            # present then we should not descend further
            for entry in dirs:
                stack.append(fs.path.join(dirpath, entry))


def pyfs_opendir(*, pyfs=None, dir="/", **kwargs):
    """Open directory while handling the case of S3 without directory objects.

    Arguments:
        pyfs: fs filesytem to use, else None for local
        dir: string of directory to open
        **kwargs: additional arguments to pass to fs.opendir

    Returns an fs filesystem for the new directory within pyfs. Has special
    handling to deal with S3 filesystems which don't have directory objects.
    """
    pyfs = _pyfs_or_local(pyfs)
    if isinstance(pyfs, S3FS):
        # Hack for S3 because the standard opendir(..) fails when there
        # isn't a directory object (even with strict=False)
        new_dir_path = fs.path.join(pyfs.dir_path, dir)
        s3fs = S3FS(
            pyfs._bucket_name,  # pylint: disable=protected-access
            dir_path=new_dir_path,
            aws_access_key_id=pyfs.aws_access_key_id,
            aws_secret_access_key=pyfs.aws_secret_access_key,
            endpoint_url=pyfs.endpoint_url,
            # acl=pyfs.acl,
            # cache_control=pyfs.cache_control),
            strict=pyfs.strict)
        # Patch in version of getinfo method that doesn't check parent directory
        s3fs.getinfo = s3fs._getinfo  # pylint: disable=protected-access
        return s3fs
    # Not S3, just use regular opendir(..)
    return pyfs.opendir(dir, **kwargs)


def pyfs_openfile(filepath, mode, pyfs=None, **kwargs):
    """Open file on either local filesystem or fs filesystem.

    Arguments:
        filepath: string of file path
        mode: file mode
        pyfs: fs filesystem to use, else None (default) will use the
            local file
        **kwargs: additional arguments to pass to fs.open

    Returns open fs filehandle.
    """
    pyfs = _pyfs_or_local(pyfs)
    return pyfs.open(filepath, mode, **kwargs)


def pyfs_openbin(filepath, mode, pyfs=None):
    """Open binary file on either local filesystem or fs filesystem.

    Arguments:
        filepath: string of file path
        mode: file mode
        pyfs: fs filesystem to use, else None (default) will use the
            local file
    """
    pyfs = _pyfs_or_local(pyfs)
    return pyfs.openbin(filepath, mode)


def pyfs_files_identical(pyfs, file1, file2):
    """Compare files on one filesystem pyfs.

    Arguments:
        pyfs: fs filesytem to use
        file1: string filepath for first file
        file2: string filepath for second file

    Returns True if the files are identical, False otherwise.

    FIXME - Make this more efficient by comparing stat info first, then only
    comparing content in chunks if necessary.
    """
    with pyfs.open(file1, "r") as fh1:
        c1 = fh1.read()
    with pyfs.open(file2, "r") as fh2:
        c2 = fh2.read()
    return c1 == c2
