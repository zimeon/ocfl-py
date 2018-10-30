"""Handle different storage dispositions."""
from .identity import Identity
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
    elif disposition == 'identity':
        return Identity()
    else:
        raise Exception("Unsupported disposition %s, aborting!" % (disposition))
