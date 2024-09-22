# OCFL Sidecar creation and update script

_Output from `tests/test_demo_ocfl_sidecar_script.py`._

## 1. Test showing version number.

### 1.1 Show version number

The `--version` argument will show version number and exit

```
> python ocfl-sidecar.py --version
ocfl-sidecar.py is part of ocfl-py version 1.9.0
```


## 2. Test creation of sidecar file.

### 2.1 Set up directory as object root

```
> mkdir -v tmp/obj
tmp/obj
```


### 2.2 Copy in an inventory from an example

```
> cp -v fixtures/1.0/good-objects/minimal_one_version_one_file/inventory.json tmp/obj
fixtures/1.0/good-objects/minimal_one_version_one_file/inventory.json -> tmp/obj/inventory.json
```


### 2.3 Create sidecar

The digest type will be set by reading the inventory (in this case, sha512)

```
> python ocfl-sidecar.py tmp/obj
INFO:root:Looking at path tmp/obj
INFO:root:Written sidecar file inventory.json.sha512
Done.
```


### 2.4 Create a new sidecar with a different digest

The digest type is set with the --digest parameter

```
> python ocfl-sidecar.py --digest sha256 tmp/obj
INFO:root:Looking at path tmp/obj
INFO:root:Written sidecar file inventory.json.sha256
Done.
```

