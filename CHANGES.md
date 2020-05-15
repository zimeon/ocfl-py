# ocfl-py changelog

## ??? v0.0.7

  * Validator now checks fixity block structure, additional fixity values in fixity block
  * Validator now checks for repeated digests in manifest, fixity and state blocks (https://ocfl.io/draft/spec/#E096, https://ocfl.io/draft/spec/#E097, https://ocfl.io/draft/spec/#E098) 

## 2020-05-15 v0.0.6

  * ocfl-validate.py script now handles storage roots and objects
  * When validating, show warnings and errors by default (https://github.com/zimeon/ocfl-py/issues/22)
  * Handle case of no versions https://ocfl.io/draft/spec/#E008
  * Handle case of bad JSON inventory https://ocfl.io/draft/spec/#E033
  * Handle case of no manifest https://ocfl.io/draft/spec/#E041
  * Handle case of conflicting paths https://ocfl.io/draft/spec/#E095


## 2020-05-05 v0.0.5

  * Renumber errors to align somewhat with the canonical code set extracted 
    at https://github.com/OCFL/spec/blob/master/validation/validation-codes.md
  * Add --version parameter to scripts to show version number

## 2020-05-02 v0.0.4

  * Actually check digests for content during validation!
  * Add --validate to ocfl-store.py to check all of storage root

## 2020-04-26 v0.0.3

  * Add missing package data to install
  * Deal with tests for warnings https://ocfl.io/draft/spec/#W003,
    https://ocfl.io/draft/spec/#W009 and https://ocfl.io/draft/spec/#W010

## 2020-04-20 v0.0.2

  * Two in a day...
  * Support for version creation from and extraction as Bagit bags

## 2020-04-20 v0.0.1

  * Push up first version to PyPI
