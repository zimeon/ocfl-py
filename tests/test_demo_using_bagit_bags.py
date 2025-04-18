# -*- coding: utf-8 -*-
"""Tests/demo building spec examples."""
from testlib import DemoTestCase


class TestAll(DemoTestCase):
    """TestAll class to run tests."""

    def test00_build_from_bags(self):
        """Test building from bags."""
        text = "Imagine that we have a Bagit bag [`tests/testdata/bags/uaa_v1`]" \
               "(https://github.com/zimeon/ocfl-py/tree/main/tests/testdata/bags/uaa_v1) " \
               "that represents the initial state of an object. We can use `--create` to " \
               "make a new OCFL object `/tmp/obj` with that content as the " \
               "`v1` state:"
        out = self.run_script("Building from a set of bags",
                              ["python", "ocfl-object.py", "create",
                               "--objdir", "TMPDIR/obj",
                               "--srcbag", "tests/testdata/bags/uaa_v1",
                               "-v"],
                              text=text)
        self.assertIn("Created OCFL object info:bb123cd4567 in", out)
        out = self.run_script("Check new object is valid",
                              ["python", "ocfl-validate.py",
                               "TMPDIR/obj"],
                              text="Now that we have the object it is of course valid.")
        self.assertIn("/obj is VALID", out)
        out = self.run_script("Look inside",
                              ["python", "ocfl-object.py", "show",
                               "--objdir", "TMPDIR/obj"],
                              text="Looking inside the object we see `v1` with the expected 2 content files.")
        self.assertIn("├── content (2 files)", out)
        text = "If we have a bag " \
               "[`tests/testdata/bags/uaa_v2`](https://github.com/zimeon/ocfl-py/tree/main/tests/testdata/bags/uaa_v2) " \
               "with updated content we can `--update` the object to create `v2`."
        out = self.run_script("Update with v2",
                              ["python", "ocfl-object.py", "update",
                               "--objdir", "TMPDIR/obj",
                               "--srcbag", "tests/testdata/bags/uaa_v2",
                               "-v"],
                              text=text)
        self.assertIn("Updated object info:bb123cd4567 to v2", out)
        out = self.run_script("Look inside again",
                              ["python", "ocfl-object.py", "show",
                               "--objdir", "TMPDIR/obj"],
                              text="Looking inside the object we now see `v1` and `v2`. There are no content files inside `v2` because although this update added two files they have identical content (and hence digest) as one of the files in `v1`")
        self.assertIn("└── v2 \n    ├── inventory.json \n    └── inventory.json.sha512", out)
        text = "Similarly we can `--update` with " \
               "[`tests/testdata/bags/uaa_v3`](https://github.com/zimeon/ocfl-py/tree/main/tests/testdata/bags/uaa_v3) " \
               "to create `v3`."
        out = self.run_script("Update with v3",
                              ["python", "ocfl-object.py", "update",
                               "--objdir", "TMPDIR/obj",
                               "--srcbag", "tests/testdata/bags/uaa_v3",
                               "-v"],
                              text=text)
        self.assertIn("Updated object info:bb123cd4567 to v3", out)
        out = self.run_script("Look inside again",
                              ["python", "ocfl-object.py", "show",
                               "--objdir", "TMPDIR/obj"],
                              text="Looking inside again we see that `v3` does add another content file.")
        self.assertIn("└── v3 \n    ├── content (1 files)\n    ├── inventory.json \n    └── inventory.json.sha512", out)
        text = "Finally, we can `--update` again with " \
               "[`tests/testdata/bags/uaa_v4`](https://github.com/zimeon/ocfl-py/tree/main/tests/testdata/bags/uaa_v4) " \
               "to create `v4`."
        out = self.run_script("Update with v4",
                              ["python", "ocfl-object.py", "update",
                               "--objdir", "TMPDIR/obj",
                               "--srcbag", "tests/testdata/bags/uaa_v4",
                               "-v"],
                              text=text)
        self.assertIn("Updated object info:bb123cd4567 to v4", out)
        text = "Taking the newly created OCFL object `/tmp/obj` we can `--extract` the `v4` content as a Bagit bag. " \
               "The `--set-bagging-date` means that the created time for v4 will be used to generate the " \
               "Bagging-Date in the Bagit bag's metadata."
        out = self.run_script("Update with v4",
                              ["python", "ocfl-object.py", "extract",
                               "--objver", "v4",
                               "--objdir", "TMPDIR/obj",
                               "--dstbag", "TMPDIR/extracted_v4",
                               "--set-bagging-date",
                               "-v"],
                              text=text)
        self.assertIn("Extracted content for v4 saved as Bagit bag", out)
        text = "We note that the OCFL object had only one `content` file in `v4` but the " \
               "extracted object state for `v4` includes 4 files, two of which have identical " \
               "content (`dracula.txt` and `another_directory/a_third_copy_of_dracula.txt`). We " \
               "can now compare the extracted bag `/tmp/uaa_v4` that with the bag we used to " \
               "create `v4` `tests/testdata/bags/uaa_v4` using a recursive `diff`."
        out = self.run_script("Compare extracted and original v4",
                              ["diff",
                               "--ignore-matching-lines", " bag-info.txt",
                               "-r", "TMPDIR/extracted_v4", "tests/testdata/bags/uaa_v4"],
                              text=text)
        self.demo_text("The only difference that shows in the output of the `diff` is the "
                       "addition of the `Bag-Software-Agent:` line in the newly created bag "
                       "that was no present in the input metadata. Because of this additional "
                       "metadata, the digest for the bag is also different, but this is removed "
                       "from the `diff` output with the `--ignore-matching-lines ' bag-info.txt'` "
                       "parameter. The bag content matches.")


if __name__ == "__main__":
    # Run in demo mode if run directly instead of through py.test
    TestAll.run_as_demo(title="Demonstration of OCFL Object manipulation using Bagit bags to import and export versions")
