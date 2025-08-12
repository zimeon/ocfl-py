"""Layout registry.

This registry keeps the mapping between layout names and their classes.

By default it loads the set of layouts supported by ocfl-py (inculding
some alias names) and allows registration of custom layouts. This registry
does not include information about which layouts are officially registered
as OCFL Community Extensions https://ocfl.github.io/extensions/
"""

from .layout_0002_flat_direct import Layout_0002_Flat_Direct
from .layout_0003_hash_and_id_n_tuple import Layout_0003_Hash_And_Id_N_Tuple
from .layout_nnnn_flat_quoted import Layout_NNNN_Flat_Quoted
from .layout_nnnn_tuple_tree import Layout_NNNN_Tuple_Tree
from .layout_nnnn_uuid_quadtree import Layout_NNNN_UUID_Quadtree


_layout_registry = {}


def add_layout(name, layout_cls):
    """Register a new layout class under a given name.

    Arguments:
        name (str): name of the layout to add
        layout_cls (class): Layout class to be associated with the layout name
    """
    _layout_registry[name] = layout_cls


def get_layout(name):
    """Get an instance of the layout class for the given name.

    Arguments:
        name (str): layout name

    Returns:
        instance of layout class

    Raises:
        Exception: if layout is not supported
    """
    if name not in _layout_registry:
        raise Exception("Unknown layout name (%s)" % (name))
    return _layout_registry[name]()


def layout_is_supported(name):
    """Layout with specified name is supported in this registry.

    Arguments:
        name (str): layout name

    Returns:
        bool: True is the layout is supported, False otherwise
    """
    return name in _layout_registry


# Register default layouts
add_layout("0002-flat-direct-storage-layout", Layout_0002_Flat_Direct)
add_layout("0002", Layout_0002_Flat_Direct)
add_layout("flat-direct", Layout_0002_Flat_Direct)
add_layout("0003-hash-and-id-n-tuple-storage-layout", Layout_0003_Hash_And_Id_N_Tuple)
add_layout("0003", Layout_0003_Hash_And_Id_N_Tuple)
add_layout("nnnn-flat-quoted-storage-layout", Layout_NNNN_Flat_Quoted)
add_layout("flat-quoted", Layout_NNNN_Flat_Quoted)
add_layout("nnnn-tuple-tree", Layout_NNNN_Tuple_Tree)
add_layout("nnnn-uuid-quadtree", Layout_NNNN_UUID_Quadtree)
