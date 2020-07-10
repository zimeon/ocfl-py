# ocfl-py changelog

## ??? v1.0.3

  * ???

## 2020-07-10 v1.0.2

  * Use `main` as default branch in git repository, fix links and documentation

## 2020-07-07 v1.0.1

  * Add table of implementation status (https://github.com/zimeon/ocfl-py/blob/main/docs/validation_status.md)

## 2020-07-07 v1.0.0

  * OCFL v1.0 released (https://ocfl.io/1.0/spec/), change links from draft to 1.0
  * Add checks for paths in manifest (https://ocfl.io/1.0/spec/#E098, https://ocfl.io/1.0/spec/#E099, https://ocfl.io/1.0/spec/#E100, https://ocfl.io/1.0/spec/#E101)
  * Separate message not a string test (https://ocfl.io/1.0/spec/#E094) from others
  * Sort out version sequence tests (https://ocfl.io/1.0/spec/#E008, https://ocfl.io/1.0/spec/#E009, https://ocfl.io/1.0/spec/#E010, https://ocfl.io/1.0/spec/#E011)
  * Refine checks for logical paths (https://ocfl.io/1.0/spec/#E052, https://ocfl.io/1.0/spec/#E053)
  * Fix code for missing sidecar (https://ocfl.io/1.0/spec/#E058)
  * Add --version for ocfl-sidecar.py

## 2020-05-21 v0.0.8

  * Add checks for paths in manifest (https://ocfl.io/1.0/spec/#E098, https://ocfl.io/1.0/spec/#E099, https://ocfl.io/1.0/spec/#E100, https://ocfl.io/1.0/spec/#E101)
  * Separate message not a string test (https://ocfl.io/1.0/spec/#E094) from others
  * Sort out version sequence tests (https://ocfl.io/1.0/spec/#E008, https://ocfl.io/1.0/spec/#E009, https://ocfl.io/1.0/spec/#E010, https://ocfl.io/1.0/spec/#E011)
  * Refine checks for logical paths (https://ocfl.io/1.0/spec/#E052, https://ocfl.io/1.0/spec/#E053)
  * Fix code for missing sidecar (https://ocfl.io/1.0/spec/#E058)
  * Add ocfl-sidecar.py script to generate inventory sidecar

## 2020-05-18 v0.0.7

  * Validator now checks fixity block structure, additional fixity values in fixity block
  * Validator now checks for repeated digests in manifest, fixity and state blocks (https://ocfl.io/1.0/spec/#E096, https://ocfl.io/1.0/spec/#E097, https://ocfl.io/1.0/spec/#E098) 
  * Move all the many README_*.md demos into docs folder
  * Add build_demo_docs.sh to build demo descriptions in docs folder

## 2020-05-15 v0.0.6

  * ocfl-validate.py script now handles storage roots and objects
  * When validating, show warnings and errors by default (https://github.com/zimeon/ocfl-py/issues/22)
  * Handle case of no versions https://ocfl.io/1.0/spec/#E008
  * Handle case of bad JSON inventory https://ocfl.io/1.0/spec/#E033
  * Handle case of no manifest https://ocfl.io/1.0/spec/#E041
  * Handle case of conflicting paths https://ocfl.io/1.0/spec/#E095


## 2020-05-05 v0.0.5

  * Renumber errors to align somewhat with the canonical code set extracted 
    at https://github.com/OCFL/spec/blob/main/validation/validation-codes.md
  * Add --version parameter to scripts to show version number

## 2020-05-02 v0.0.4

  * Actually check digests for content during validation!
  * Add --validate to ocfl-store.py to check all of storage root

## 2020-04-26 v0.0.3

  * Add missing package data to install
  * Deal with tests for warnings https://ocfl.io/1.0/spec/#W003,
    https://ocfl.io/1.0/spec/#W009 and https://ocfl.io/1.0/spec/#W010

## 2020-04-20 v0.0.2

  * Two in a day...
  * Support for version creation from and extraction as Bagit bags

## 2020-04-20 v0.0.1

  * Push up first version to PyPI
