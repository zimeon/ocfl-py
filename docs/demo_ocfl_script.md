# OCFL Object Root Store manipulation script

_Output from `tests/test_demo_ocfl_store_script.py`._

## 1. Test showing version number.

### 1.1 Show version number

The `--version` argument will show version number and exit (but we still tave to specify a root and an action)

```
> python ocfl.py --version
ocfl.py is part of ocfl-py version 1.9.0
```


## 2. Test store initialization and object addition.

### 2.1 Create new store

```
> python ocfl.py init --root=tmp/root --layout=nnnn-flat-quoted-storage-layout -v
Created OCFL storage root tmp/root
```


### 2.2 List empty store

```
> python ocfl.py list --root=tmp/root -v
INFO:root:Storage root layout is nnnn-flat-quoted-storage-layout
Found 0 OCFL Objects under root tmp/root
```


### 2.3 Add object

```
> python ocfl.py add --root=tmp/root --src fixtures/1.0/good-objects/minimal_one_version_one_file -v
INFO:root:Storage root layout is nnnn-flat-quoted-storage-layout
Added object ark:123/abc at path ark%3A123%2Fabc
```


### 2.4 Error if we try to add the same object again

```
> python ocfl.py add --root=tmp/root --src fixtures/1.0/good-objects/minimal_one_version_one_file -v
INFO:root:Storage root layout is nnnn-flat-quoted-storage-layout
ERROR:root:Add object failed because path ark%3A123%2Fabc exists
```

(last command exited with return code 1)


## 3. Test exploration of a simple OCFL object root.

### 3.1 List objects

```
> python ocfl.py list --root=extra_fixtures/good-storage-roots/simple-root
http%3A%2F%2Fexample.org%2Fminimal_mixed_digests -- id=http://example.org/minimal_mixed_digests
ark%3A123%2Fabc -- id=ark:123/abc
ark%3A%2F12345%2Fbcd987 -- id=ark:/12345/bcd987
Found 3 OCFL Objects under root extra_fixtures/good-storage-roots/simple-root
```


## 4. Test error cases.

### 4.1 Create new store

```
> python ocfl.py init --root=tmp/root --layout=0002-flat-direct-storage-layout -v
Created OCFL storage root tmp/root
```


### 4.2 Add object

```
> python ocfl.py add --root=tmp/root -v
ERROR:root:Must specify object path with --src
```

(last command exited with return code 1)


## 5. Build examples from storage root extension 0003.

### 5.1 Create new store

```
> python ocfl.py init --root=tmp/ex2 --spec-version=1.0 --layout=0003-hash-and-id-n-tuple-storage-layout --layout-params={"digestAlgorithm":"md5", "tupleSize":2, "numberOfTuples":15} -v
Created OCFL storage root tmp/ex2
```


### 5.2 Create add object-01

```
> python ocfl.py add --root=tmp/ex2 --src=extra_fixtures/1.0/good-objects/root_ext0003_object-01
INFO:root:Storage root layout is 0003-hash-and-id-n-tuple-storage-layout
Added object object-01 at path ff/75/53/44/92/48/5e/ab/b3/9f/86/35/67/28/88/object-01
```


### 5.3 Create add horrible-obj

```
> python ocfl.py add --root=tmp/ex2 --src=extra_fixtures/1.0/good-objects/root_ext0003_horrible-obj
INFO:root:Storage root layout is 0003-hash-and-id-n-tuple-storage-layout
Added object ..hor/rib:le-$id at path 08/31/97/66/fb/6c/29/35/dd/17/5b/94/26/77/17/%2e%2ehor%2frib%3ale-%24id
```
