# Demonstration of OCFL Object manipulation using Bagit bags to import and export versions

_Output from `tests/test_demo_using_bagit_bags.py`._

## 1. Test building from bags.

### 1.1 Building from a set of bags

Imagine that we have a Bagit bag [`tests/testdata/bags/uaa_v1`](https://github.com/zimeon/ocfl-py/tree/main/tests/testdata/bags/uaa_v1) that represents the initial state of an object. We can use `--create` to make a new OCFL object `/tmp/obj` with that content as the `v1` state:

```
> python ocfl-object.py create --objdir tmp/obj --srcbag tests/testdata/bags/uaa_v1 -v
/Users/sw272/.python_venv/py311/lib/python3.11/site-packages/bagit.py:24: UserWarning: pkg_resources is deprecated as an API. See https://setuptools.pypa.io/en/latest/pkg_resources.html. The pkg_resources package is slated for removal as early as 2025-11-30. Refrain from using this package or pin to Setuptools<81.
  from pkg_resources import DistributionNotFound, get_distribution
INFO:root:Created OCFL object info:bb123cd4567 in tmp/obj
```


### 1.2 Check new object is valid

Now that we have the object it is of course valid.

```
> python ocfl-validate.py tmp/obj
/Users/sw272/.python_venv/py311/lib/python3.11/site-packages/bagit.py:24: UserWarning: pkg_resources is deprecated as an API. See https://setuptools.pypa.io/en/latest/pkg_resources.html. The pkg_resources package is slated for removal as early as 2025-11-30. Refrain from using this package or pin to Setuptools<81.
  from pkg_resources import DistributionNotFound, get_distribution
OCFL v1.1 Object at tmp/obj is VALID
```


### 1.3 Look inside

Looking inside the object we see `v1` with the expected 2 content files.

```
> python ocfl-object.py show --objdir tmp/obj
/Users/sw272/.python_venv/py311/lib/python3.11/site-packages/bagit.py:24: UserWarning: pkg_resources is deprecated as an API. See https://setuptools.pypa.io/en/latest/pkg_resources.html. The pkg_resources package is slated for removal as early as 2025-11-30. Refrain from using this package or pin to Setuptools<81.
  from pkg_resources import DistributionNotFound, get_distribution
INFO:root:OCFL v1.1 Object at tmp/obj has VALID STRUCTURE (DIGESTS NOT CHECKED)
Object tree for None
[tmp/obj]
├── 0=ocfl_object_1.1 
├── inventory.json 
├── inventory.json.sha512 
└── v1 
    ├── content (2 files)
    ├── inventory.json 
    └── inventory.json.sha512 

```


### 1.4 Update with v2

If we have a bag [`tests/testdata/bags/uaa_v2`](https://github.com/zimeon/ocfl-py/tree/main/tests/testdata/bags/uaa_v2) with updated content we can `--update` the object to create `v2`.

```
> python ocfl-object.py update --objdir tmp/obj --srcbag tests/testdata/bags/uaa_v2 -v
/Users/sw272/.python_venv/py311/lib/python3.11/site-packages/bagit.py:24: UserWarning: pkg_resources is deprecated as an API. See https://setuptools.pypa.io/en/latest/pkg_resources.html. The pkg_resources package is slated for removal as early as 2025-11-30. Refrain from using this package or pin to Setuptools<81.
  from pkg_resources import DistributionNotFound, get_distribution
INFO:root:Updated OCFL object info:bb123cd4567 by adding v2
Updated object info:bb123cd4567 to v2
```


### 1.5 Look inside again

Looking inside the object we now see `v1` and `v2`. There are no content files inside `v2` because although this update added two files they have identical content (and hence digest) as one of the files in `v1`

```
> python ocfl-object.py show --objdir tmp/obj
/Users/sw272/.python_venv/py311/lib/python3.11/site-packages/bagit.py:24: UserWarning: pkg_resources is deprecated as an API. See https://setuptools.pypa.io/en/latest/pkg_resources.html. The pkg_resources package is slated for removal as early as 2025-11-30. Refrain from using this package or pin to Setuptools<81.
  from pkg_resources import DistributionNotFound, get_distribution
INFO:root:OCFL v1.1 Object at tmp/obj has VALID STRUCTURE (DIGESTS NOT CHECKED)
Object tree for None
[tmp/obj]
├── 0=ocfl_object_1.1 
├── inventory.json 
├── inventory.json.sha512 
├── v1 
│   ├── content (2 files)
│   ├── inventory.json 
│   └── inventory.json.sha512 
└── v2 
    ├── inventory.json 
    └── inventory.json.sha512 

```


### 1.6 Update with v3

Similarly we can `--update` with [`tests/testdata/bags/uaa_v3`](https://github.com/zimeon/ocfl-py/tree/main/tests/testdata/bags/uaa_v3) to create `v3`.

```
> python ocfl-object.py update --objdir tmp/obj --srcbag tests/testdata/bags/uaa_v3 -v
/Users/sw272/.python_venv/py311/lib/python3.11/site-packages/bagit.py:24: UserWarning: pkg_resources is deprecated as an API. See https://setuptools.pypa.io/en/latest/pkg_resources.html. The pkg_resources package is slated for removal as early as 2025-11-30. Refrain from using this package or pin to Setuptools<81.
  from pkg_resources import DistributionNotFound, get_distribution
INFO:root:Updated OCFL object info:bb123cd4567 by adding v3
Updated object info:bb123cd4567 to v3
```


### 1.7 Look inside again

Looking inside again we see that `v3` does add another content file.

```
> python ocfl-object.py show --objdir tmp/obj
/Users/sw272/.python_venv/py311/lib/python3.11/site-packages/bagit.py:24: UserWarning: pkg_resources is deprecated as an API. See https://setuptools.pypa.io/en/latest/pkg_resources.html. The pkg_resources package is slated for removal as early as 2025-11-30. Refrain from using this package or pin to Setuptools<81.
  from pkg_resources import DistributionNotFound, get_distribution
INFO:root:OCFL v1.1 Object at tmp/obj has VALID STRUCTURE (DIGESTS NOT CHECKED)
Object tree for None
[tmp/obj]
├── 0=ocfl_object_1.1 
├── inventory.json 
├── inventory.json.sha512 
├── v1 
│   ├── content (2 files)
│   ├── inventory.json 
│   └── inventory.json.sha512 
├── v2 
│   ├── inventory.json 
│   └── inventory.json.sha512 
└── v3 
    ├── content (1 files)
    ├── inventory.json 
    └── inventory.json.sha512 

```


### 1.8 Update with v4

Finally, we can `--update` again with [`tests/testdata/bags/uaa_v4`](https://github.com/zimeon/ocfl-py/tree/main/tests/testdata/bags/uaa_v4) to create `v4`.

```
> python ocfl-object.py update --objdir tmp/obj --srcbag tests/testdata/bags/uaa_v4 -v
/Users/sw272/.python_venv/py311/lib/python3.11/site-packages/bagit.py:24: UserWarning: pkg_resources is deprecated as an API. See https://setuptools.pypa.io/en/latest/pkg_resources.html. The pkg_resources package is slated for removal as early as 2025-11-30. Refrain from using this package or pin to Setuptools<81.
  from pkg_resources import DistributionNotFound, get_distribution
INFO:root:Updated OCFL object info:bb123cd4567 by adding v4
Updated object info:bb123cd4567 to v4
```


### 1.9 Update with v4

Taking the newly created OCFL object `/tmp/obj` we can `--extract` the `v4` content as a Bagit bag. The `--set-bagging-date` means that the created time for v4 will be used to generate the Bagging-Date in the Bagit bag's metadata.

```
> python ocfl-object.py extract --objver v4 --objdir tmp/obj --dstbag tmp/extracted_v4 --set-bagging-date -v
/Users/sw272/.python_venv/py311/lib/python3.11/site-packages/bagit.py:24: UserWarning: pkg_resources is deprecated as an API. See https://setuptools.pypa.io/en/latest/pkg_resources.html. The pkg_resources package is slated for removal as early as 2025-11-30. Refrain from using this package or pin to Setuptools<81.
  from pkg_resources import DistributionNotFound, get_distribution
INFO:root:Extracted v4 into tmp/extracted_v4
Extracted content for v4 saved as Bagit bag in tmp/extracted_v4
```


### 1.10 Compare extracted and original v4

We note that the OCFL object had only one `content` file in `v4` but the extracted object state for `v4` includes 4 files, two of which have identical content (`dracula.txt` and `another_directory/a_third_copy_of_dracula.txt`). We can now compare the extracted bag `/tmp/uaa_v4` that with the bag we used to create `v4` `tests/testdata/bags/uaa_v4` using a recursive `diff`.

```
> diff --ignore-matching-lines  bag-info.txt -r tmp/extracted_v4 tests/testdata/bags/uaa_v4
diff --ignore-matching-lines  bag-info.txt -r tmp/extracted_v4/bag-info.txt tests/testdata/bags/uaa_v4/bag-info.txt
1d0
< Bag-Software-Agent: bagit.py v1.8.1 <https://github.com/LibraryOfCongress/bagit-python>
```

(last command exited with return code 1)

The only difference that shows in the output of the `diff` is the addition of the `Bag-Software-Agent:` line in the newly created bag that was no present in the input metadata. Because of this additional metadata, the digest for the bag is also different, but this is removed from the `diff` output with the `--ignore-matching-lines ' bag-info.txt'` parameter. The bag content matches.

