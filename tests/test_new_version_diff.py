import pytest
from ocfl.inventory import Inventory
from ocfl.new_version import NewVersion

def make_inventory_with_state(state, head="v2", prev_state=None):
    inv = Inventory()
    inv.spec_version = "1.1"
    inv.id = "test"
    inv.digest_algorithm = "sha512"
    inv.init_manifest_and_versions()
    # Add previous version if provided
    if prev_state is not None:
        inv.add_version("v1", state=prev_state)
        inv.head = "v1"
    inv.add_version(head, state=state)
    inv.head = head
    return inv

def test_add_delete():
    # Previous version: one file
    prev_state = {
        "digestA": ["fileA.txt"]
    }
    # Current version: fileA.txt deleted, fileB.txt added, fileC.txt added with same digest as fileA.txt
    curr_state = {
        "digestB": ["fileB.txt"],
        "digestA": ["fileC.txt"]
    }
    inv = make_inventory_with_state(curr_state, head="v2", prev_state=prev_state)
    # Instead of creating a new version, just set head to v2 and use NewVersion with carry_content_forward=True
    nv = NewVersion.next_version(inventory=inv)
    nv.inventory.head = "v2"
    diff = nv.diff_with_previous()
    ops = { (op["op"], op["digest"], op["logical_path"]) for op in diff }
    assert ("add", "digestB", "fileB.txt") in ops
    assert ("add", "digestA", "fileC.txt") in ops
    assert ("delete", "digestA", "fileA.txt") in ops
    assert len(diff) == 3

def test_no_previous_version_all_adds():
    curr_state = {
        "digestA": ["fileA.txt"],
        "digestB": ["fileB.txt"]
    }
    inv = make_inventory_with_state(curr_state, head="v1")
    nv = NewVersion.next_version(inventory=inv)
    nv.inventory.head = "v1"
    diff = nv.diff_with_previous()
    ops = { (op["op"], op["digest"], op["logical_path"]) for op in diff }
    assert ("add", "digestA", "fileA.txt") in ops
    assert ("add", "digestB", "fileB.txt") in ops
    assert len(diff) == 2

def test_multiple_logical_paths_same_digest():
    # Previous version: two logical paths for same digest
    prev_state = {
        "digestX": ["file1.txt", "file2.txt"]
    }
    # Current version: file2.txt deleted, file3.txt added for same digest
    curr_state = {
        "digestX": ["file1.txt", "file3.txt"]
    }
    inv = make_inventory_with_state(curr_state, head="v2", prev_state=prev_state)
    nv = NewVersion.next_version(inventory=inv)
    nv.inventory.head = "v2"
    diff = nv.diff_with_previous()
    ops = { (op["op"], op["digest"], op["logical_path"]) for op in diff }
    assert ("delete", "digestX", "file2.txt") in ops
    assert ("add", "digestX", "file3.txt") in ops
    assert all(op[0] in ("add", "delete") for op in ops)

def test_multiple_adds_and_deletes():
    # Previous version: two logical paths for same digest
    prev_state = {
        "digestY": ["a.txt", "b.txt"]
    }
    # Current version: both logical paths deleted, two new added
    curr_state = {
        "digestY": ["c.txt", "d.txt"]
    }
    inv = make_inventory_with_state(curr_state, head="v2", prev_state=prev_state)
    nv = NewVersion.next_version(inventory=inv)
    nv.inventory.head = "v2"
    diff = nv.diff_with_previous()
    ops = { (op["op"], op["digest"], op["logical_path"]) for op in diff }
    assert ("delete", "digestY", "a.txt") in ops
    assert ("delete", "digestY", "b.txt") in ops
    assert ("add", "digestY", "c.txt") in ops
    assert ("add", "digestY", "d.txt") in ops
    assert len(diff) == 4
