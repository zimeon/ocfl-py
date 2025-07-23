"""Layout registry.

This file keeps the mapping between layout names and their classes.

It has a set of default options and allows registration of custom layouts.
"""

_layout_registry = {}

def register_layout(name, layout_cls):
    """Register a new layout class under a given name."""
    _layout_registry[name] = layout_cls

def get_layout(name):
    """Get an instance of the layout class for the given name."""
    if name not in _layout_registry:
        raise StorageRootException("E069a Storage root %s lacks required 0= declaration file" % (self.root))
    return _layout_registry[name]()

def layout_is_registered(name):
    return name in _layout_registry

# Register default layouts
from .layout_0002_flat_direct import Layout_0002_Flat_Direct
from .layout_0003_hash_and_id_n_tuple import Layout_0003_Hash_And_Id_N_Tuple
from .layout_nnnn_flat_quoted import Layout_NNNN_Flat_Quoted
from .layout_nnnn_tuple_tree import Layout_NNNN_Tuple_Tree
from .layout_nnnn_uuid_quadtree import Layout_NNNN_UUID_Quadtree

register_layout("0002-flat-direct-storage-layout", Layout_0002_Flat_Direct)
register_layout("0002", Layout_0002_Flat_Direct)
register_layout("flat-direct", Layout_0002_Flat_Direct)
register_layout("0003-hash-and-id-n-tuple-storage-layout", Layout_0003_Hash_And_Id_N_Tuple)
register_layout("0003", Layout_0003_Hash_And_Id_N_Tuple)
register_layout("nnnn-flat-quoted-storage-layout", Layout_NNNN_Flat_Quoted)
register_layout("flat-quoted", Layout_NNNN_Flat_Quoted)
register_layout("nnnn-tuple-tree", Layout_NNNN_Tuple_Tree)
register_layout("nnnn-uuid-quadtree", Layout_NNNN_UUID_Quadtree)
