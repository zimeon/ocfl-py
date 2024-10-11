# OCFL Object and Storage Root validation script

_Output from `tests/test_demo_ocfl_validate_script.py`._

## 1. Test showing version number.

### 1.1 Show version number

The `--version` argument will show version number and exit

```
> python ocfl-validate.py --version
ocfl-validate.py is part of ocfl-py version 1.9.0
```


## 2. Test simple good case.

### 2.1 Good test

```
> python ocfl-validate.py fixtures/1.0/good-objects/minimal_uppercase_digests
OCFL v1.0 Object at fixtures/1.0/good-objects/minimal_uppercase_digests is VALID
```


## 3. Test warning cases.

### 3.1 Warning test with -q

```
> python ocfl-validate.py -q fixtures/1.0/warn-objects/W004_uses_sha256
OCFL v1.0 Object at fixtures/1.0/warn-objects/W004_uses_sha256 is VALID
```


### 3.2 Warning test without -q

```
> python ocfl-validate.py fixtures/1.0/warn-objects/W004_uses_sha256
[W004] OCFL Object root inventory SHOULD use sha512 but uses sha256 as the DigestAlgorithm (see https://ocfl.io/1.0/spec/#W004)
OCFL v1.0 Object at fixtures/1.0/warn-objects/W004_uses_sha256 is VALID
```

