"""Handle different storage dispositions."""
from .identity import Identity
from .ntree import Ntree
from .uuid_quadtree import UUIDQuadtree


def get_dispositor(disposition=None):
    """Find Dispositor object for the given disposition."""
    if disposition == 'pairtree':
        return Ntree(n=2)
    if disposition == 'tripletree':
        return Ntree(n=3)
    if disposition == 'quadtree':
        return Ntree(n=4)
    if disposition == 'uuid_quadtree':
        return UUIDQuadtree()
    if disposition == 'identity':
        return Identity()
    raise Exception("Unsupported disposition %s, aborting!" % (disposition))
