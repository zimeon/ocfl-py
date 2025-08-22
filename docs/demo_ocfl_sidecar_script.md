# Demonstration of OCFL Sidecar creation and update script

_Output from `tests/test_demo_ocfl_sidecar_script.py`._

## 1. Test showing version number.

### 1.1 Show version number

The `--version` argument will show version number and exit

```
> python ocfl-sidecar.py --version
ocfl-sidecar.py is part of ocfl-py version 2.0.3
```


## 2. Test creation of a sidecar file.

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


### 2.3 Create sidecar for inventory in specified object

The digest type will be set by reading the inventory (in this case, sha512)

```
> python ocfl-sidecar.py tmp/obj
Written sidecar file tmp/obj/inventory.json.sha512
```


### 2.4 Create sidecar for specified inventory

The digest type will be set by reading the inventory (in this case, sha512)

```
> python ocfl-sidecar.py tmp/obj/inventory.json
Written sidecar file tmp/obj/inventory.json.sha512
```


### 2.5 Create a new sidecar with a different digest

The digest type is set with the --digest parameter

```
> python ocfl-sidecar.py --digest sha256 tmp/obj
Written sidecar file tmp/obj/inventory.json.sha256
```


## 3. Test creation of multiple sidecar files.

### 3.1 Set up directory as object 1 root

```
> mkdir -v tmp/obj1
tmp/obj1
```


### 3.2 Set up directory as object 2 root

```
> mkdir -v tmp/obj2
tmp/obj2
```


### 3.3 Set up directory as object 3 root

```
> mkdir -v tmp/obj3
tmp/obj3
```


### 3.4 Copy in an inventory from an example for object 1

```
> cp -v fixtures/1.1/good-objects/minimal_uppercase_digests/inventory.json tmp/obj1
fixtures/1.1/good-objects/minimal_uppercase_digests/inventory.json -> tmp/obj1/inventory.json
```


### 3.5 Copy in an inventory from an example for object 2

```
> cp -v fixtures/1.1/good-objects/minimal_mixed_digests/inventory.json tmp/obj2
fixtures/1.1/good-objects/minimal_mixed_digests/inventory.json -> tmp/obj2/inventory.json
```


### 3.6 Copy in an inventory from an example for object 3

```
> cp -v fixtures/1.1/good-objects/minimal_no_content/inventory.json tmp/obj3
fixtures/1.1/good-objects/minimal_no_content/inventory.json -> tmp/obj3/inventory.json
```


### 3.7 Create sidecars for all 3 inventory files

```
> python ocfl-sidecar.py tmp/obj1 tmp/obj2 tmp/obj3
Written sidecar file tmp/obj1/inventory.json.sha512
Written sidecar file tmp/obj2/inventory.json.sha512
Written sidecar file tmp/obj3/inventory.json.sha512
```

