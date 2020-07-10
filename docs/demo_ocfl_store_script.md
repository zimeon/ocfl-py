# OCFL Object Root Store manipulation script

_Output from `tests/test_demo_ocfl_store_script.py`._

## 1. Test showing version number.

### 1.1 Show version number

The `--version` argument will show version number and exit (but we still tave to specify a root and an action)

```
> python ocfl-store.py --version --root=tmp/root --list
ocfl-store.py is part of ocfl-py version 1.0.1
```


## 2. Test store initialization and object addition.

### 2.1 Create new store

```
> python ocfl-store.py --root=tmp/root --init -v
INFO:root:Created OCFL storage root tmp/root
```


### 2.2 List empty store

```
> python ocfl-store.py --root=tmp/root --list -v
INFO:root:Found 0 OCFL Objects under root tmp/root
```


### 2.3 Add object

```
> python ocfl-store.py --root=tmp/root --add --src fixtures/1.0/good-objects/minimal_one_version_one_file --disposition identity -v
INFO:root:Copying from fixtures/1.0/good-objects/minimal_one_version_one_file to tmp/root/ark%3A123%2Fabc
INFO:root:Copied
```


## 3. Test error cases.

### 3.1 Create new store

```
> python ocfl-store.py --root=tmp/root --init -v
INFO:root:Created OCFL storage root tmp/root
```


### 3.2 Add object

```
> python ocfl-store.py --root=tmp/root --add -v
ERROR:root:Must specify object path with --src
```

(last command exited with return code 1)

