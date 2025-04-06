# Demonstration of OCFL Object manipulation script

_Output from `tests/test_demo_ocfl_object_script.py`._

## 1. Test showing version number.

### 1.1 Show version number

The `--version` argument will show version number and exit

```
> python ocfl-object.py --version
ocfl-object.py is part of ocfl-py version 1.9.0
```


## 2. Test object inventory creation with output to stdout.

### 2.1 Inventory for new object with just v1

Without an `--objdir` argument the script just writes out the inventory for the object that would have been created.

```
> python ocfl-object.py create --id http://example.org/obj1 --src fixtures/1.0/content/cf1/v1 --created 2024-10-24T18:30:01Z
### Inventory for v1
{
  "digestAlgorithm": "sha512",
  "head": "v1",
  "id": "http://example.org/obj1",
  "manifest": {
    "43a43fe8a8a082d3b5343dfaf2fd0c8b8e370675b1f376e92e9994612c33ea255b11298269d72f797399ebb94edeefe53df243643676548f584fb8603ca53a0f": [
      "v1/content/a_file.txt"
    ]
  },
  "type": "https://ocfl.io/1.1/spec/#inventory",
  "versions": {
    "v1": {
      "created": "2024-10-24T18:30:01Z",
      "state": {
        "43a43fe8a8a082d3b5343dfaf2fd0c8b8e370675b1f376e92e9994612c33ea255b11298269d72f797399ebb94edeefe53df243643676548f584fb8603ca53a0f": [
          "a_file.txt"
        ]
      }
    }
  }
}
```


### 2.2 Inventory for new object with three versions

Without an `--objdir` argument the script just writes out the inventory for each version in the object that would have been created.

```
> python ocfl-object.py build --id http://example.org/obj2 --src fixtures/1.0/content/cf3 --metadata extra_fixtures/1.0/content/spec-ex-full-metadata.json
### Inventory for v3
{
  "digestAlgorithm": "sha512",
  "head": "v3",
  "id": "http://example.org/obj2",
  "manifest": {
    "296e72b8fd5f7f0ac1473993600ae34953d5dab646f17e7b182b8648aff830d7bf01b56490777cb3e72b33fcc1ae520506badea1032252d1a55fd7362e269975": [
      "v2/content/a_file.txt"
    ],
    "43a43fe8a8a082d3b5343dfaf2fd0c8b8e370675b1f376e92e9994612c33ea255b11298269d72f797399ebb94edeefe53df243643676548f584fb8603ca53a0f": [
      "v1/content/a_file.txt"
    ]
  },
  "type": "https://ocfl.io/1.1/spec/#inventory",
  "versions": {
    "v1": {
      "created": "2018-01-01T01:01:01Z",
      "message": "Initial import",
      "state": {
        "43a43fe8a8a082d3b5343dfaf2fd0c8b8e370675b1f376e92e9994612c33ea255b11298269d72f797399ebb94edeefe53df243643676548f584fb8603ca53a0f": [
          "a_file.txt"
        ]
      },
      "user": {
        "address": "alice@example.com",
        "name": "Alice"
      }
    },
    "v2": {
      "created": "2018-02-02T02:02:02Z",
      "message": "Fix bar.xml, remove image.tiff, add empty2.txt",
      "state": {
        "296e72b8fd5f7f0ac1473993600ae34953d5dab646f17e7b182b8648aff830d7bf01b56490777cb3e72b33fcc1ae520506badea1032252d1a55fd7362e269975": [
          "a_file.txt"
        ]
      },
      "user": {
        "address": "bob@example.com",
        "name": "Bob"
      }
    },
    "v3": {
      "created": "2018-03-03T03:03:03Z",
      "message": "Reinstate image.tiff, delete empty.txt",
      "state": {
        "43a43fe8a8a082d3b5343dfaf2fd0c8b8e370675b1f376e92e9994612c33ea255b11298269d72f797399ebb94edeefe53df243643676548f584fb8603ca53a0f": [
          "a_file.txt"
        ]
      },
      "user": {
        "address": "cecilia@example.com",
        "name": "Cecilia"
      }
    }
  }
}
```


## 3. Test object creation with just v1.

### 3.1 New object with just v1

```
> python ocfl-object.py create --id http://example.org/obj1 --src fixtures/1.0/content/cf1/v1 --objdir tmp/obj1 --created 2024-10-24T18:30:03Z -v
INFO:root:Created OCFL object http://example.org/obj1 in tmp/obj1
```


## 4. Test object build with three versions.

### 4.1 New object with three versions

```
> python ocfl-object.py build --id http://example.org/obj2 --src fixtures/1.0/content/cf3 --objdir tmp/obj2 -v
INFO:root:Built object http://example.org/obj2 at tmp/obj2 with 3 versions
```


## 5. Test extract of version.

### 5.1 Extract v1 of content in an OCFL v1.0 object

Version 1 object with location specified in `--objdir` and the first version specified in `--objver`, extract into tmp/v1:

```
> python ocfl-object.py extract --objdir fixtures/1.0/good-objects/spec-ex-full --objver v1 --dstdir tmp/v1 -v
INFO:root:Extracted v1 into tmp/v1
Extracted content for v1 in tmp/v1
```

and the extracted files are:

```
> find -s tmp/v1 -print
find: unknown predicate `-s'
```

(last command exited with return code 1)


### 5.2 Extract v2 of content in an OCFL v1.1 object

```
> python ocfl-object.py extract --objver v2 --objdir fixtures/1.1/good-objects/spec-ex-full --dstdir tmp/v2 -v
INFO:root:Extracted v2 into tmp/v2
Extracted content for v2 in tmp/v2
```

and the extracted files are:

```
> find -s tmp/v2 -print
find: unknown predicate `-s'
```

(last command exited with return code 1)


### 5.3 Extract head version (v3) of content in the same OCFL v1.1 object

```
> python ocfl-object.py extract --objver head --objdir fixtures/1.1/good-objects/spec-ex-full --dstdir tmp/head -v
INFO:root:Extracted v3 into tmp/head
Extracted content for v3 in tmp/head
```

and the extracted files are:

```
> find -s tmp/v3 -print
find: unknown predicate `-s'
```

(last command exited with return code 1)


### 5.4 Extract foo/bar.xml of v3 into a new directory

```
> python ocfl-object.py extract --objver v3 --objdir fixtures/1.1/good-objects/spec-ex-full --logical-path foo/bar.xml --dstdir tmp/files -v
Extracted foo/bar.xml in v3 to tmp/files
```

and the extracted file is:

```
> find -s tmp/files -print
find: unknown predicate `-s'
```

(last command exited with return code 1)


### 5.5 Extract image.tiff of v3 (default) into the same directory

```
> python ocfl-object.py extract --objdir fixtures/1.1/good-objects/spec-ex-full --logical-path image.tiff --dstdir tmp/files -v
Extracted image.tiff in v3 to tmp/files
```

and the directory now contains two extracted files:

```
> find -s tmp/files -print
find: unknown predicate `-s'
```

(last command exited with return code 1)


## 6. Test error conditions.

### 6.1 No valid command argument

With no argument and error and suggections are shown.

```
> python ocfl-object.py
ERROR:root:No command, nothing to do (use -h to show help)
```

(last command exited with return code 1)


### 6.2 No source directory (--srcdir)

The `create` command requires a source.

```
> python ocfl-object.py create --objdir TMP/v1
ERROR:root:Must specify either --srcdir or --srcbag containing v1 files when creating an OCFL object!
```

(last command exited with return code 1)


### 6.3 No identifier

The `show` command requires --objdir.

```
> python ocfl-object.py show --srcdir tmp
usage: ocfl-object.py show [-h] [--verbose] [--debug] [--quiet] --objdir
                           OBJDIR [--spec-version SPEC_VERSION]
                           [--digest DIGEST] [--fixity FIXITY] [--id ID]
                           [--skip SKIP] [--normalization NORMALIZATION]
                           [--no-forward-delta] [--no-dedupe] [--lax-digests]
ocfl-object.py show: error: the following arguments are required: --objdir/--obj
```

(last command exited with return code 2)

