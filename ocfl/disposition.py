"""Handle different storage dispositions."""
from .ntree import Ntree
from .uuid_quadtree import UUIDQuadtree


def get_dispositor(disposition=None):
    """Find Dispositor object for the given disposition."""
    if disposition == 'pairtree':
        return Ntree(n=2)
    elif disposition == 'tripletree':
        return Ntree(n=3)
    elif disposition == 'quadtree':
        return Ntree(n=4)
    elif disposition == 'uuid_quadtree':
        return UUIDQuadtree()
    else:
        raise Exception("Unsupported disposition %s, aborting!" % (disposition))
