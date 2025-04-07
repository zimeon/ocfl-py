# Demonstration of OCFL Object manipulation using Bagit bags to import and export versions

_Output from `tests/test_demo_using_bagit_bags.py`._

## 1. Test building from bags.

### 1.1 Building from a set of bags

Imagine that we have a Bagit bag [`tests/testdata/bags/uaa_v1`](https://github.com/zimeon/ocfl-py/tree/main/tests/testdata/bags/uaa_v1) that represents the initial state of an object. We can use `--create` to make a new OCFL object `/tmp/obj` with that content as the `v1` state:

```
> python ocfl-object.py create --objdir tmp/obj --srcbag tests/testdata/bags/uaa_v1 -v
INFO:root:Created OCFL object info:bb123cd4567 in tmp/obj
```


### 1.2 Check new object is valid

Now that we have the object it is of course valid.

```
> python ocfl-validate.py tmp/obj
OCFL v1.1 Object at tmp/obj is VALID
```


### 1.3 Look inside

Looking inside the object we see `v1` with the expected 2 content files.

```
> python ocfl-object.py show --objdir tmp/obj
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
INFO:root:Updated OCFL object info:bb123cd4567 by adding v2
Updated object info:bb123cd4567 to v2
```


### 1.5 Look inside again

Looking inside the object we now see `v1` and `v2`. There are no content files inside `v2` because although this update added two files they have identical content (and hence digest) as one of the files in `v1`

```
> python ocfl-object.py show --objdir tmp/obj
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
INFO:root:Updated OCFL object info:bb123cd4567 by adding v3
Updated object info:bb123cd4567 to v3
```


### 1.7 Look inside again

Looking inside again we see that `v3` does add another content file.

```
> python ocfl-object.py show --objdir tmp/obj
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
INFO:root:Updated OCFL object info:bb123cd4567 by adding v4
Updated object info:bb123cd4567 to v4
```


### 1.9 Update with v4

Taking the newly created OCFL object `/tmp/obj` we can `--extract` the `v4` content as a Bagit bag.

```
> python ocfl-object.py extract --objver v4 --objdir tmp/obj --dstbag tmp/extracted_v4 -v
INFO:root:Extracted v4 into tmp/extracted_v4
Extracted content for v4 saved as Bagit bag in tmp/extracted_v4
```


### 1.10 Compare extracted and original v4

We note that the OCFL object had only one `content` file in `v4` but the extracted object state for `v4` includes 4 files, two of which have identical content (`dracula.txt` and `another_directory/a_third_copy_of_dracula.txt`). We can now compare the extracted bag `/tmp/uaa_v4` that with the bag we used to create `v4` `tests/testdata/bags/uaa_v4` using a recursive `diff`.

```
> diff -r tmp/extracted_v4 tests/testdata/bags/uaa_v4
diff -r tmp/extracted_v4/bag-info.txt tests/testdata/bags/uaa_v4/bag-info.txt
1,2c1
< Bag-Software-Agent: bagit.py v1.8.1 <https://github.com/LibraryOfCongress/bagit-python>
< Bagging-Date: 2025-04-07
---
> Bagging-Date: 2020-01-04
diff -r tmp/extracted_v4/tagmanifest-sha512.txt tests/testdata/bags/uaa_v4/tagmanifest-sha512.txt
1,2d0
< 5c2e2b9cacc93cb315d57f09fac6d199c3378313b6cf918bb0a70e1839c4e4c0c2e5a7f9ae869cf7755e09a196a835be1af7c510d3d5faa5d0c0b3f6be9f816a manifest-sha512.txt
< 765b6cfcfaf7f909c087b55c6035438f16f5814cf1787df7bcfd44933b1366a633b0e6fdd37534bdd860915acefeabdc104aeae35ad8cd89c0e3949e3d73d28f bag-info.txt
3a2,3
> 10624e6d45462def7af66d1a0d977606c7b073b01809c1d42258cfab5c34a275480943cbe78044416aee1f23822cc3762f92247b8f39b5c6ddc5ae32a8f94ce5 bag-info.txt
> 5c2e2b9cacc93cb315d57f09fac6d199c3378313b6cf918bb0a70e1839c4e4c0c2e5a7f9ae869cf7755e09a196a835be1af7c510d3d5faa5d0c0b3f6be9f816a manifest-sha512.txt
```

(last command exited with return code 1)

The only differences are in the `bag-info.txt` file and the checksum file for that file (`tagmanifest-sha512.txt`). The content matches.

