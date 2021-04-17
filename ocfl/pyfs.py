"""Wrapper for PyFilesystem2 to deal with ocfl-py needs.

S3FS documentation: https://fs-s3fs.readthedocs.io/en/latest/

But note limitations: https://fs-s3fs.readthedocs.io/en/latest/#limitations
which points out that by default the S3FS implementation creates and requires
empty objects with names ending in slash that record that a directory
exists.

It seems to be the case the using `strict=False` avoids checks for these empty
directories. There is no way to pass the `strict` parameter via the open_fs()
function so we need to call the SF3
"""
import fs
import fs.base
import fs.opener
from fs.osfs import OSFS
from fs_s3fs import S3FS


def open_fs(fs_url, **kwargs):
    """Open a pyfs filesystem.

    Like fs.open_fs will simply return FS if an instance if given as
    the fs_url parameter.
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
    if parse_result.protocol == 's3':
        # And S3 URL, mostly repeat
        # https://github.com/PyFilesystem/s3fs/blob/master/fs_s3fs/opener.py
        # but adjust the handling of strict to default to strict=False
        bucket_name, _, dir_path = parse_result.resource.partition("/")
        if not bucket_name:
            raise fs.opener.errors.OpenerError("invalid bucket name in '{}'".format(fs_url))
        # Instead of allowing this to be turned on by a strict=1 in the
        # URL query params, allow it to be turned off by strict!=1
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


def ocfl_walk(f, dir='/', is_storage_root=False):
    """Walk that works on pyfs filesystems including S3 without the need for directory objects.

    Assumes that f.getinfo() will work for a file/resource that exists and
    that fs.errors.ResourceNotFound might be raised if called on a filesystem
    without directories (and no directory objects).

    For walking storage roots (is_storage_root=True) then the condition to
    descend is:
        1) this is the root (dirpaht == '/'), or
        2) there are no files in this directory (see https://ocfl.io/1.0/spec/#root-structure)

    FIXME - QUICK AND DIRTY HACK, CAN DO BETTER!
    """
    if not dir.startswith('/'):
        dir = '/' + dir
    stack = [dir]
    while len(stack) > 0:
        # print("Stack " + str(stack))
        dirpath = stack.pop()
        entries = f.listdir(dirpath)
        files = []
        dirs = []
        dirpaths = []
        for entry in entries:
            entry_path = fs.path.join(dirpath, entry)
            is_dir = True
            try:
                info = f.getinfo(entry_path)
                # print(entry_path + " info: " + str(info))
                is_dir = info.is_dir
            except fs.errors.ResourceNotFound:
                pass  # Assume to be a directory
            if is_dir:
                dirs.append(entry)
                dirpaths.append(entry_path)
            else:
                files.append(entry)
        if not is_storage_root or dirpath == '/' or len(files) == 0:
            # If this is not the storage root itself and there are files
            # present then we should not descend further
            stack.extend(dirpaths)
        yield(dirpath, dirs, files)


def ocfl_opendir(pyfs, dir, **kwargs):
    """Open directory while handling the case of S3 without directory objects.

    FIXME - DIRTY HACK
    """
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


def ocfl_files_identical(pyfs, file1, file2):
    """Compare file1 and file2 on the filesystem pyfs.

    Returns True if the files are identical, False otherwise.

    FIXME - Make this more efficient by comparing stat info first, then only
    comparing content in chunks if necessary.
    """
    with pyfs.open(file1, 'r') as fh1:
        c1 = fh1.read()
    with pyfs.open(file2, 'r') as fh2:
        c2 = fh2.read()
    return c1 == c2
