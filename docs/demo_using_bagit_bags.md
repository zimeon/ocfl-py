# OCFL Object manipulation using Bagit bags to import and export versions

_Output from `tests/test_demo_using_bagit_bags.py`._

## 1. Test building from bags.

### 1.1 Building from a set of bags

Imagine that we have a Bagit bag [`tests/testdata/bags/uaa_v1`](https://github.com/zimeon/ocfl-py/tree/main/tests/testdata/bags/uaa_v1) that represents the initial state of an object. We can use `--create` to make a new OCFL object `/tmp/obj` with that content as the `v1` state:

```
> python ocfl-object.py --create --objdir tmp/obj --srcbag tests/testdata/bags/uaa_v1 -v
INFO:bagit:Verifying checksum for file /Users/simeon/src/ocfl-py/tests/testdata/bags/uaa_v1/data/my_content/dracula.txt
INFO:bagit:Verifying checksum for file /Users/simeon/src/ocfl-py/tests/testdata/bags/uaa_v1/data/my_content/poe.txt
INFO:bagit:Verifying checksum for file /Users/simeon/src/ocfl-py/tests/testdata/bags/uaa_v1/bagit.txt
INFO:bagit:Verifying checksum for file /Users/simeon/src/ocfl-py/tests/testdata/bags/uaa_v1/bag-info.txt
INFO:bagit:Verifying checksum for file /Users/simeon/src/ocfl-py/tests/testdata/bags/uaa_v1/manifest-sha512.txt
INFO:root:Created OCFL object info:bb123cd4567 in tmp/obj
```


### 1.2 Check new object is valid

Now that we have the object it is of course valid.

```
> python ocfl-validate.py tmp/obj
INFO:ocfl.object:OCFL object at tmp/obj is VALID
```


### 1.3 Look inside

Looking inside the object we see `v1` with the expected 2 content files.

```
> python ocfl-object.py --show --objdir tmp/obj
WARNING:ocfl.object:OCFL object at tmp/obj has VALID STRUCTURE (DIGESTS NOT CHECKED) 
WARNING:ocfl.object:Object tree
[tmp/obj]
├── 0=ocfl_object_1.0 
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
> python ocfl-object.py --update --objdir tmp/obj --srcbag tests/testdata/bags/uaa_v2 -v
INFO:bagit:Verifying checksum for file /Users/simeon/src/ocfl-py/tests/testdata/bags/uaa_v2/data/my_content/a_second_copy_of_dracula.txt
INFO:bagit:Verifying checksum for file /Users/simeon/src/ocfl-py/tests/testdata/bags/uaa_v2/data/my_content/dracula.txt
INFO:bagit:Verifying checksum for file /Users/simeon/src/ocfl-py/tests/testdata/bags/uaa_v2/data/my_content/poe-nevermore.txt
INFO:bagit:Verifying checksum for file /Users/simeon/src/ocfl-py/tests/testdata/bags/uaa_v2/data/my_content/another_directory/a_third_copy_of_dracula.txt
INFO:bagit:Verifying checksum for file /Users/simeon/src/ocfl-py/tests/testdata/bags/uaa_v2/bagit.txt
INFO:bagit:Verifying checksum for file /Users/simeon/src/ocfl-py/tests/testdata/bags/uaa_v2/bag-info.txt
INFO:bagit:Verifying checksum for file /Users/simeon/src/ocfl-py/tests/testdata/bags/uaa_v2/manifest-sha512.txt
INFO:root:Will update info:bb123cd4567 v1 -> v2
INFO:root:Updated OCFL object info:bb123cd4567 in tmp/obj by adding v2
```


### 1.5 Look inside again

Looking inside the object we now see `v1` and `v2`. There are no content files inside `v2` because although this update added two files they have identical content (and hence digest) as one of the files in `v1`

```
> python ocfl-object.py --show --objdir tmp/obj
WARNING:ocfl.object:OCFL object at tmp/obj has VALID STRUCTURE (DIGESTS NOT CHECKED) 
WARNING:ocfl.object:Object tree
[tmp/obj]
├── 0=ocfl_object_1.0 
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
> python ocfl-object.py --update --objdir tmp/obj --srcbag tests/testdata/bags/uaa_v3 -v
INFO:bagit:Verifying checksum for file /Users/simeon/src/ocfl-py/tests/testdata/bags/uaa_v3/data/my_content/dracula.txt
INFO:bagit:Verifying checksum for file /Users/simeon/src/ocfl-py/tests/testdata/bags/uaa_v3/data/my_content/poe-nevermore.txt
INFO:bagit:Verifying checksum for file /Users/simeon/src/ocfl-py/tests/testdata/bags/uaa_v3/data/my_content/another_directory/a_third_copy_of_dracula.txt
INFO:bagit:Verifying checksum for file /Users/simeon/src/ocfl-py/tests/testdata/bags/uaa_v3/bagit.txt
INFO:bagit:Verifying checksum for file /Users/simeon/src/ocfl-py/tests/testdata/bags/uaa_v3/bag-info.txt
INFO:bagit:Verifying checksum for file /Users/simeon/src/ocfl-py/tests/testdata/bags/uaa_v3/manifest-sha512.txt
INFO:root:Will update info:bb123cd4567 v2 -> v3
INFO:root:Updated OCFL object info:bb123cd4567 in tmp/obj by adding v3
```


### 1.7 Look inside again

Looking inside again we see that `v3` does add another content file.

```
> python ocfl-object.py --show --objdir tmp/obj
WARNING:ocfl.object:OCFL object at tmp/obj has VALID STRUCTURE (DIGESTS NOT CHECKED) 
WARNING:ocfl.object:Object tree
[tmp/obj]
├── 0=ocfl_object_1.0 
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
> python ocfl-object.py --update --objdir tmp/obj --srcbag tests/testdata/bags/uaa_v4 -v
INFO:bagit:Verifying checksum for file /Users/simeon/src/ocfl-py/tests/testdata/bags/uaa_v4/data/my_content/dracula.txt
INFO:bagit:Verifying checksum for file /Users/simeon/src/ocfl-py/tests/testdata/bags/uaa_v4/data/my_content/dunwich.txt
INFO:bagit:Verifying checksum for file /Users/simeon/src/ocfl-py/tests/testdata/bags/uaa_v4/data/my_content/poe-nevermore.txt
INFO:bagit:Verifying checksum for file /Users/simeon/src/ocfl-py/tests/testdata/bags/uaa_v4/data/my_content/another_directory/a_third_copy_of_dracula.txt
INFO:bagit:Verifying checksum for file /Users/simeon/src/ocfl-py/tests/testdata/bags/uaa_v4/bagit.txt
INFO:bagit:Verifying checksum for file /Users/simeon/src/ocfl-py/tests/testdata/bags/uaa_v4/bag-info.txt
INFO:bagit:Verifying checksum for file /Users/simeon/src/ocfl-py/tests/testdata/bags/uaa_v4/manifest-sha512.txt
INFO:root:Will update info:bb123cd4567 v3 -> v4
INFO:root:Updated OCFL object info:bb123cd4567 in tmp/obj by adding v4
```


### 1.9 Update with v4

Taking the newly created OCFL object `/tmp/obj` we can `--extract` the `v4` content as a Bagit bag.

```
> python ocfl-object.py --extract v4 --objdir tmp/obj --dstbag tmp/extracted_v4 -v
INFO:root:Extracted v4 into tmp/extracted_v4
INFO:bagit:Creating bag for directory tmp/extracted_v4
INFO:bagit:Creating data directory
INFO:bagit:Moving my_content to /privatetmp/extracted_v4/tmp3ky3u9tv/my_content
INFO:bagit:Moving /privatetmp/extracted_v4/tmp3ky3u9tv to data
INFO:bagit:Using 1 processes to generate manifests: sha512
INFO:bagit:Generating manifest lines for file data/my_content/dracula.txt
INFO:bagit:Generating manifest lines for file data/my_content/dunwich.txt
INFO:bagit:Generating manifest lines for file data/my_content/poe-nevermore.txt
INFO:bagit:Generating manifest lines for file data/my_content/another_directory/a_third_copy_of_dracula.txt
INFO:bagit:Creating bagit.txt
INFO:bagit:Creating bag-info.txt
INFO:bagit:Creating tmp/extracted_v4/tagmanifest-sha512.txt
Extracted content for v4 saved as Bagit bag in tmp/extracted_v4
```


### 1.10 Compare extracted and original v4

We note that the OCFL object had only one `content` file in `v4` but the extracted object state for `v4` includes 4 files, two of which have identical content (`dracula.txt` and `another_directory/a_third_copy_of_dracula.txt`). We can now compare the extracted bag `/tmp/uaa_v4` that with the bag we used to create `v4` `tests/testdata/bags/uaa_v4` using a recursive `diff`.

```
> diff -r tmp/extracted_v4 tests/testdata/bags/uaa_v4
diff -r tmp/extracted_v4/bag-info.txt tests/testdata/bags/uaa_v4/bag-info.txt
1,2c1
< Bag-Software-Agent: bagit.py v1.7.1.dev15+g6e14a50 <https://github.com/LibraryOfCongress/bagit-python>
< Bagging-Date: 2020-07-10
---
> Bagging-Date: 2020-01-04
diff -r tmp/extracted_v4/tagmanifest-sha512.txt tests/testdata/bags/uaa_v4/tagmanifest-sha512.txt
2c2
< 14fd538ee8c8c0d3b636b1d664b699f649610c21b03f120de00cf15e70e514275c38d2dc7b5c89f07521ad7d8d9f4015e91cec567a1d344e124cb21ee7a4d85c bag-info.txt
---
> 10624e6d45462def7af66d1a0d977606c7b073b01809c1d42258cfab5c34a275480943cbe78044416aee1f23822cc3762f92247b8f39b5c6ddc5ae32a8f94ce5 bag-info.txt
```

(last command exited with return code 1)

The only differences are in the `bag-info.txt` file and the checksum file for that file (`tagmanifest-sha512.txt`). The content matches.

