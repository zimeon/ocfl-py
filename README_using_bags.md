# OCFL 

## Building from a set of bags 

Imagine that we have a Bagit bag [`tests/testdata/bags/uaa_v1`](https://github.com/zimeon/ocfl-py/tree/master/tests/testdata/bags/uaa_v1) that represents the initial state
of an object. We can use `--create` to make a new OCFL object `/tmp/obj` with that content as the
`v1` state:

```
(py38) simeon@RottenApple ocfl-py> rm -rf /tmp/obj
(py38) simeon@RottenApple ocfl-py> ./ocfl-object.py -v --create --objdir /tmp/obj --srcbag tests/testdata/bags/uaa_v1
INFO:bagit:Verifying checksum for file /Users/simeon/src/ocfl-py/tests/testdata/bags/uaa_v1/data/my_content/dracula.txt
INFO:bagit:Verifying checksum for file /Users/simeon/src/ocfl-py/tests/testdata/bags/uaa_v1/data/my_content/poe.txt
INFO:bagit:Verifying checksum for file /Users/simeon/src/ocfl-py/tests/testdata/bags/uaa_v1/bagit.txt
INFO:bagit:Verifying checksum for file /Users/simeon/src/ocfl-py/tests/testdata/bags/uaa_v1/bag-info.txt
INFO:bagit:Verifying checksum for file /Users/simeon/src/ocfl-py/tests/testdata/bags/uaa_v1/manifest-sha512.txt
-o-> tests/testdata/bags/uaa_v1/data/my_content/dracula.txt
... v1/content/my_content/dracula.txt -> tests/testdata/bags/uaa_v1/data/my_content/dracula.txt
-o-> tests/testdata/bags/uaa_v1/data/my_content/poe.txt
... v1/content/my_content/poe.txt -> tests/testdata/bags/uaa_v1/data/my_content/poe.txt
INFO:root:Created OCFL object info:bb123cd4567 in /tmp/obj
```

Now that we have the object `/tmp/obj` it is of course valid and looking inside we see `v1` with the expected 2 content files:

```
(py38) simeon@RottenApple ocfl-py> ./ocfl-validate.py /tmp/obj

OCFL object at /tmp/obj is VALID

(py38) simeon@RottenApple ocfl-py> ./ocfl-object.py --show --objdir /tmp/obj
OCFL object at /tmp/obj has VALID STRUCTURE (DIGESTS NOT CHECKED) 

[/tmp/obj]
├── 0=ocfl_object_1.0 
├── inventory.json 
├── inventory.json.sha512 
└── v1 
    ├── content (2 files)
    ├── inventory.json 
    └── inventory.json.sha512 
```

If we have a bag [`tests/testdata/bags/uaa_v2`](https://github.com/zimeon/ocfl-py/tree/master/tests/testdata/bags/uaa_v2) with updated content we can `--update` the object to create v2:

```
(py38) simeon@RottenApple ocfl-py> ./ocfl-object.py -v --update --objdir /tmp/obj --srcbag tests/testdata/bags/uaa_v2
INFO:bagit:Verifying checksum for file /Users/simeon/src/ocfl-py/tests/testdata/bags/uaa_v2/data/my_content/a_second_copy_of_dracula.txt
INFO:bagit:Verifying checksum for file /Users/simeon/src/ocfl-py/tests/testdata/bags/uaa_v2/data/my_content/dracula.txt
INFO:bagit:Verifying checksum for file /Users/simeon/src/ocfl-py/tests/testdata/bags/uaa_v2/data/my_content/poe-nevermore.txt
INFO:bagit:Verifying checksum for file /Users/simeon/src/ocfl-py/tests/testdata/bags/uaa_v2/data/my_content/another_directory/a_third_copy_of_dracula.txt
INFO:bagit:Verifying checksum for file /Users/simeon/src/ocfl-py/tests/testdata/bags/uaa_v2/bagit.txt
INFO:bagit:Verifying checksum for file /Users/simeon/src/ocfl-py/tests/testdata/bags/uaa_v2/bag-info.txt
INFO:bagit:Verifying checksum for file /Users/simeon/src/ocfl-py/tests/testdata/bags/uaa_v2/manifest-sha512.txt
INFO:root:Will update info:bb123cd4567 v1 -> v2
-o-> tests/testdata/bags/uaa_v2/data/my_content/a_second_copy_of_dracula.txt
... already have content for digest ffc150e7944b5cf5ddb899b2f48efffbd490f97632fc258434aefc4afb92aef2e3441ddcceae11404e5805e1b6c804083c9398c28f061c9ba42dd4bac53d5a2e
-o-> tests/testdata/bags/uaa_v2/data/my_content/dracula.txt
... already have content for digest ffc150e7944b5cf5ddb899b2f48efffbd490f97632fc258434aefc4afb92aef2e3441ddcceae11404e5805e1b6c804083c9398c28f061c9ba42dd4bac53d5a2e
-o-> tests/testdata/bags/uaa_v2/data/my_content/poe-nevermore.txt
... already have content for digest 69f54f2e9f4568f7df4a4c3b07e4cbda4ba3bba7913c5218add6dea891817a80ce829b877d7a84ce47f93cbad8aa522bf7dd8eda2778e16bdf3c47cf49ee3bdf
-o-> tests/testdata/bags/uaa_v2/data/my_content/another_directory/a_third_copy_of_dracula.txt
... already have content for digest ffc150e7944b5cf5ddb899b2f48efffbd490f97632fc258434aefc4afb92aef2e3441ddcceae11404e5805e1b6c804083c9398c28f061c9ba42dd4bac53d5a2e
m2s {}
INFO:root:Updated OCFL object info:bb123cd4567 in /tmp/obj by adding v2
```

Looking inside the object we now see `v1` and `v2`. There are no content files inside `v2` because although this update added two files they have identical content (and hence digest) as one of the files in `v1`:

```
(py38) simeon@RottenApple ocfl-py> ./ocfl-object.py --show --objdir /tmp/obj
OCFL object at /tmp/obj has VALID STRUCTURE (DIGESTS NOT CHECKED) 

[/tmp/obj]
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

Similarly we can `--update` to create `v3`:

```
(py38) simeon@RottenApple ocfl-py> ./ocfl-object.py -v --update --objdir /tmp/obj --srcbag tests/testdata/bags/uaa_v3
INFO:bagit:Verifying checksum for file /Users/simeon/src/ocfl-py/tests/testdata/bags/uaa_v3/data/my_content/dracula.txt
INFO:bagit:Verifying checksum for file /Users/simeon/src/ocfl-py/tests/testdata/bags/uaa_v3/data/my_content/poe-nevermore.txt
INFO:bagit:Verifying checksum for file /Users/simeon/src/ocfl-py/tests/testdata/bags/uaa_v3/data/my_content/another_directory/a_third_copy_of_dracula.txt
INFO:bagit:Verifying checksum for file /Users/simeon/src/ocfl-py/tests/testdata/bags/uaa_v3/bagit.txt
INFO:bagit:Verifying checksum for file /Users/simeon/src/ocfl-py/tests/testdata/bags/uaa_v3/bag-info.txt
INFO:bagit:Verifying checksum for file /Users/simeon/src/ocfl-py/tests/testdata/bags/uaa_v3/manifest-sha512.txt
INFO:root:Will update info:bb123cd4567 v2 -> v3
-o-> tests/testdata/bags/uaa_v3/data/my_content/dracula.txt
... already have content for digest ffc150e7944b5cf5ddb899b2f48efffbd490f97632fc258434aefc4afb92aef2e3441ddcceae11404e5805e1b6c804083c9398c28f061c9ba42dd4bac53d5a2e
-o-> tests/testdata/bags/uaa_v3/data/my_content/poe-nevermore.txt
... v3/content/my_content/poe-nevermore.txt -> tests/testdata/bags/uaa_v3/data/my_content/poe-nevermore.txt
-o-> tests/testdata/bags/uaa_v3/data/my_content/another_directory/a_third_copy_of_dracula.txt
... already have content for digest ffc150e7944b5cf5ddb899b2f48efffbd490f97632fc258434aefc4afb92aef2e3441ddcceae11404e5805e1b6c804083c9398c28f061c9ba42dd4bac53d5a2e
m2s {'v3/content/my_content/poe-nevermore.txt': 'tests/testdata/bags/uaa_v3/data/my_content/poe-nevermore.txt'}
--s-> v3/content/my_content/poe-nevermore.txt tests/testdata/bags/uaa_v3/data/my_content/poe-nevermore.txt
INFO:root:Updated OCFL object info:bb123cd4567 in /tmp/obj by adding v3
```

And we see that `v3` does add another file:

```
(py38) simeon@RottenApple ocfl-py> ./ocfl-object.py --show --objdir /tmp/obj
OCFL object at /tmp/obj has VALID STRUCTURE (DIGESTS NOT CHECKED) 

[/tmp/obj]
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

Finally we can `--update` again to create `v4`:

```
(py38) simeon@RottenApple ocfl-py> ./ocfl-object.py -v --update --objdir /tmp/obj --srcbag tests/testdata/bags/uaa_v4
INFO:bagit:Verifying checksum for file /Users/simeon/src/ocfl-py/tests/testdata/bags/uaa_v4/data/my_content/dracula.txt
INFO:bagit:Verifying checksum for file /Users/simeon/src/ocfl-py/tests/testdata/bags/uaa_v4/data/my_content/dunwich.txt
INFO:bagit:Verifying checksum for file /Users/simeon/src/ocfl-py/tests/testdata/bags/uaa_v4/data/my_content/poe-nevermore.txt
INFO:bagit:Verifying checksum for file /Users/simeon/src/ocfl-py/tests/testdata/bags/uaa_v4/data/my_content/another_directory/a_third_copy_of_dracula.txt
INFO:bagit:Verifying checksum for file /Users/simeon/src/ocfl-py/tests/testdata/bags/uaa_v4/bagit.txt
INFO:bagit:Verifying checksum for file /Users/simeon/src/ocfl-py/tests/testdata/bags/uaa_v4/bag-info.txt
INFO:bagit:Verifying checksum for file /Users/simeon/src/ocfl-py/tests/testdata/bags/uaa_v4/manifest-sha512.txt
INFO:root:Will update info:bb123cd4567 v3 -> v4
-o-> tests/testdata/bags/uaa_v4/data/my_content/dracula.txt
... already have content for digest ffc150e7944b5cf5ddb899b2f48efffbd490f97632fc258434aefc4afb92aef2e3441ddcceae11404e5805e1b6c804083c9398c28f061c9ba42dd4bac53d5a2e
-o-> tests/testdata/bags/uaa_v4/data/my_content/dunwich.txt
... v4/content/my_content/dunwich.txt -> tests/testdata/bags/uaa_v4/data/my_content/dunwich.txt
-o-> tests/testdata/bags/uaa_v4/data/my_content/poe-nevermore.txt
... already have content for digest 242a60b18a716f1e88ebbb3a546a119009671dc210317be1cca206650db471c8d84769d495b4e169bfe8200b4d6d60520aa75fe99e401bd7738107b7b0ca0bcd
-o-> tests/testdata/bags/uaa_v4/data/my_content/another_directory/a_third_copy_of_dracula.txt
... already have content for digest ffc150e7944b5cf5ddb899b2f48efffbd490f97632fc258434aefc4afb92aef2e3441ddcceae11404e5805e1b6c804083c9398c28f061c9ba42dd4bac53d5a2e
m2s {'v4/content/my_content/dunwich.txt': 'tests/testdata/bags/uaa_v4/data/my_content/dunwich.txt'}
--s-> v4/content/my_content/dunwich.txt tests/testdata/bags/uaa_v4/data/my_content/dunwich.txt
INFO:root:Updated OCFL object info:bb123cd4567 in /tmp/obj by adding v4
```

The complete object now has the expected 4 versions with 1 new file in `v4`:

```
(py38) simeon@RottenApple ocfl-py> ./ocfl-validate.py /tmp/obj

OCFL object at /tmp/obj is VALID

(py38) simeon@RottenApple ocfl-py> ./ocfl-object.py --show --objdir /tmp/obj
OCFL object at /tmp/obj has VALID STRUCTURE (DIGESTS NOT CHECKED) 

[/tmp/obj]
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
├── v3 
│   ├── content (1 files)
│   ├── inventory.json 
│   └── inventory.json.sha512 
└── v4 
    ├── content (1 files)
    ├── inventory.json 
    └── inventory.json.sha512 
```

## Extracting a version as a bag

Taking the newly created OCFL object `/tmp/obj` we can `--extract` the `v4` content as a Bagit bag:

```
(py38) simeon@RottenApple ocfl-py> ./ocfl-object.py -v --extract v4 --objdir /tmp/obj --dstbag /tmp/uaa_v4 
INFO:root:Extracted v4 into /tmp/uaa_v4
INFO:bagit:Creating bag for directory /tmp/uaa_v4
INFO:bagit:Creating data directory
INFO:bagit:Moving my_content to /private/tmp/uaa_v4/tmpotio30m7/my_content
INFO:bagit:Moving /private/tmp/uaa_v4/tmpotio30m7 to data
INFO:bagit:Using 1 processes to generate manifests: sha512
INFO:bagit:Generating manifest lines for file data/my_content/dracula.txt
INFO:bagit:Generating manifest lines for file data/my_content/dunwich.txt
INFO:bagit:Generating manifest lines for file data/my_content/poe-nevermore.txt
INFO:bagit:Generating manifest lines for file data/my_content/another_directory/a_third_copy_of_dracula.txt
INFO:bagit:Creating bagit.txt
INFO:bagit:Creating bag-info.txt
INFO:bagit:Creating /tmp/uaa_v4/tagmanifest-sha512.txt
Extracted content for v4 saved as Bagit bag in /tmp/uaa_v4
```

We note that the OCFL object had only one `content` file in `v4` but the extracted object state for `v4` includes 4 files, two of which have identical content (`dracula.txt` and `another_directory/a_third_copy_of_dracula.txt`). We can now compare the extracted bag `/tmp/uaa_v4` that with the bag we used to create `v4` `tests/testdata/bags/uaa_v4` using a recursive `diff`:

```
(py38) simeon@RottenApple ocfl-py> diff -r /tmp/uaa_v4 tests/testdata/bags/uaa_v4
diff -r /tmp/uaa_v4/bag-info.txt tests/testdata/bags/uaa_v4/bag-info.txt
1,2c1
< Bag-Software-Agent: bagit.py v1.7.1.dev15+g6e14a50 <https://github.com/LibraryOfCongress/bagit-python>
< Bagging-Date: 2020-04-20
---
> Bagging-Date: 2020-01-04
diff -r /tmp/uaa_v4/tagmanifest-sha512.txt tests/testdata/bags/uaa_v4/tagmanifest-sha512.txt
2c2
< eb48cbfc4aad4278b073638958db8ee4102af42ebc543a8f67e8aa73da2770d756a50ca308b824eff80ac2b30a28bdb76f2eb50b8c0dc3963ac45153535f9aae bag-info.txt
---
> 10624e6d45462def7af66d1a0d977606c7b073b01809c1d42258cfab5c34a275480943cbe78044416aee1f23822cc3762f92247b8f39b5c6ddc5ae32a8f94ce5 bag-info.txt
```

The only differences are in the `bag-info.txt` file and the checksum file for that file (`tagmanifest-sha512.txt`). The content matches.
