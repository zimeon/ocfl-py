# Demonstration of OCFL Object and Storage Root validation script

_Output from `tests/test_demo_ocfl_validate_script.py`._

## 1. Test showing version number.

### 1.1 Show version number

The `--version` argument will show version number and exit

```
> python ocfl-validate.py --version
ocfl-validate.py is part of ocfl-py version 2.0.3
```


## 2. Test simple good case.

### 2.1 Good test

```
> python ocfl-validate.py fixtures/1.0/good-objects/minimal_uppercase_digests
dirpath = /v1/content
fsw_walk: /v1/content v1/content/a_file.txt  type=file
OCFL v1.0 Object at fixtures/1.0/good-objects/minimal_uppercase_digests is VALID
```


## 3. Test warning cases.

### 3.1 Warning test for a v1.0 object

The test shows warning W004 with a link to the v1.0 specification

```
> python ocfl-validate.py fixtures/1.0/warn-objects/W004_uses_sha256
dirpath = /v1/content
fsw_walk: /v1/content v1/content/a_file.txt  type=file
[W004] OCFL Object root inventory SHOULD use sha512 but uses sha256 as the DigestAlgorithm (see https://ocfl.io/1.0/spec/#W004)
OCFL v1.0 Object at fixtures/1.0/warn-objects/W004_uses_sha256 is VALID
```


### 3.2 Warning test with -q (--quiet) flag

The -q or --quiet flag will silence any warning messages

```
> python ocfl-validate.py -q fixtures/1.0/warn-objects/W004_uses_sha256
dirpath = /v1/content
fsw_walk: /v1/content v1/content/a_file.txt  type=file
OCFL v1.0 Object at fixtures/1.0/warn-objects/W004_uses_sha256 is VALID
```


### 3.3 Warning test for a v1.1 object with several warnings

The test shows warning W004 with a link to the v1.0 specification

```
> python ocfl-validate.py fixtures/1.1/warn-objects/W001_W004_W005_zero_padded_versions
dirpath = /v0001/content
fsw_walk: /v0001/content v0001/content/my_content  type=directory
dirpath = /v0001/content/my_content
fsw_walk: /v0001/content/my_content v0001/content/my_content/poe.txt  type=file
fsw_walk: /v0001/content/my_content v0001/content/my_content/dracula.txt  type=file
dirpath = /v0003/content
fsw_walk: /v0003/content v0003/content/my_content  type=directory
dirpath = /v0003/content/my_content
fsw_walk: /v0003/content/my_content v0003/content/my_content/poe-nevermore.txt  type=file
dirpath = /v0004/content
fsw_walk: /v0004/content v0004/content/my_content  type=directory
dirpath = /v0004/content/my_content
fsw_walk: /v0004/content/my_content v0004/content/my_content/dunwich.txt  type=file
[W001] OCFL Object root inventory version numbers SHOULD NOT be zero-padded (see https://ocfl.io/1.1/spec/#W001)
[W001] OCFL Object v0001 inventory version numbers SHOULD NOT be zero-padded (see https://ocfl.io/1.1/spec/#W001)
[W001] OCFL Object v0002 inventory version numbers SHOULD NOT be zero-padded (see https://ocfl.io/1.1/spec/#W001)
[W001] OCFL Object v0003 inventory version numbers SHOULD NOT be zero-padded (see https://ocfl.io/1.1/spec/#W001)
[W004] OCFL Object root inventory SHOULD use sha512 but uses sha256 as the DigestAlgorithm (see https://ocfl.io/1.1/spec/#W004)
[W004] OCFL Object v0001 inventory SHOULD use sha512 but uses sha256 as the DigestAlgorithm (see https://ocfl.io/1.1/spec/#W004)
[W004] OCFL Object v0002 inventory SHOULD use sha512 but uses sha256 as the DigestAlgorithm (see https://ocfl.io/1.1/spec/#W004)
[W004] OCFL Object v0003 inventory SHOULD use sha512 but uses sha256 as the DigestAlgorithm (see https://ocfl.io/1.1/spec/#W004)
[W005] OCFL Object root inventory id SHOULD be a URI (got bb123cd4567) (see https://ocfl.io/1.1/spec/#W005)
[W005] OCFL Object v0001 inventory id SHOULD be a URI (got bb123cd4567) (see https://ocfl.io/1.1/spec/#W005)
[W005] OCFL Object v0002 inventory id SHOULD be a URI (got bb123cd4567) (see https://ocfl.io/1.1/spec/#W005)
[W005] OCFL Object v0003 inventory id SHOULD be a URI (got bb123cd4567) (see https://ocfl.io/1.1/spec/#W005)
OCFL v1.1 Object at fixtures/1.1/warn-objects/W001_W004_W005_zero_padded_versions is VALID
```

