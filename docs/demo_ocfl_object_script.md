# OCFL Object manipulation script

_Output from `tests/test_demo_ocfl_object_script.py`._

## 1. Test showing version number.

### 1.1 Show version number

The `--version` argument will show version number and exit

```
> python ocfl-object.py --version
ocfl-object.py is part of ocfl-py version 1.1.0
```


## 2. Test object inventory creation with output to stdout.

### 2.1 Inventory for new object with just v1

Without an `--objdir` argument the script just writes out the inventory for the object that would have been created.

```
> python ocfl-object.py --create --id http://example.org/obj1 --src fixtures/1.0/content/cf1/v1
WARNING:ocfl.object:### Inventory for v1
{
  "digestAlgorithm": "sha512",
  "head": "v1",
  "id": "http://example.org/obj1",
  "manifest": {
    "43a43fe8a8a082d3b5343dfaf2fd0c8b8e370675b1f376e92e9994612c33ea255b11298269d72f797399ebb94edeefe53df243643676548f584fb8603ca53a0f": [
      "v1/content/a_file.txt"
    ]
  },
  "type": "https://ocfl.io/1.0/spec/#inventory",
  "versions": {
    "v1": {
      "created": "2020-08-03T14:10:46.870153Z",
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
> python ocfl-object.py --build --id http://example.org/obj2 --src fixtures/1.0/content/cf3
WARNING:ocfl.object:### Inventory for v1
{
  "digestAlgorithm": "sha512",
  "head": "v1",
  "id": "http://example.org/obj2",
  "manifest": {
    "43a43fe8a8a082d3b5343dfaf2fd0c8b8e370675b1f376e92e9994612c33ea255b11298269d72f797399ebb94edeefe53df243643676548f584fb8603ca53a0f": [
      "v1/content/a_file.txt"
    ]
  },
  "type": "https://ocfl.io/1.0/spec/#inventory",
  "versions": {
    "v1": {
      "created": "2020-08-03T14:10:47.751210Z",
      "state": {
        "43a43fe8a8a082d3b5343dfaf2fd0c8b8e370675b1f376e92e9994612c33ea255b11298269d72f797399ebb94edeefe53df243643676548f584fb8603ca53a0f": [
          "a_file.txt"
        ]
      }
    }
  }
}
WARNING:ocfl.object:### Inventory for v2
{
  "digestAlgorithm": "sha512",
  "head": "v2",
  "id": "http://example.org/obj2",
  "manifest": {
    "296e72b8fd5f7f0ac1473993600ae34953d5dab646f17e7b182b8648aff830d7bf01b56490777cb3e72b33fcc1ae520506badea1032252d1a55fd7362e269975": [
      "v2/content/a_file.txt"
    ],
    "43a43fe8a8a082d3b5343dfaf2fd0c8b8e370675b1f376e92e9994612c33ea255b11298269d72f797399ebb94edeefe53df243643676548f584fb8603ca53a0f": [
      "v1/content/a_file.txt"
    ]
  },
  "type": "https://ocfl.io/1.0/spec/#inventory",
  "versions": {
    "v1": {
      "created": "2020-08-03T14:10:47.751210Z",
      "state": {
        "43a43fe8a8a082d3b5343dfaf2fd0c8b8e370675b1f376e92e9994612c33ea255b11298269d72f797399ebb94edeefe53df243643676548f584fb8603ca53a0f": [
          "a_file.txt"
        ]
      }
    },
    "v2": {
      "created": "2020-08-03T14:10:47.752348Z",
      "state": {
        "296e72b8fd5f7f0ac1473993600ae34953d5dab646f17e7b182b8648aff830d7bf01b56490777cb3e72b33fcc1ae520506badea1032252d1a55fd7362e269975": [
          "a_file.txt"
        ]
      }
    }
  }
}
WARNING:ocfl.object:### Inventory for v3
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
  "type": "https://ocfl.io/1.0/spec/#inventory",
  "versions": {
    "v1": {
      "created": "2020-08-03T14:10:47.751210Z",
      "state": {
        "43a43fe8a8a082d3b5343dfaf2fd0c8b8e370675b1f376e92e9994612c33ea255b11298269d72f797399ebb94edeefe53df243643676548f584fb8603ca53a0f": [
          "a_file.txt"
        ]
      }
    },
    "v2": {
      "created": "2020-08-03T14:10:47.752348Z",
      "state": {
        "296e72b8fd5f7f0ac1473993600ae34953d5dab646f17e7b182b8648aff830d7bf01b56490777cb3e72b33fcc1ae520506badea1032252d1a55fd7362e269975": [
          "a_file.txt"
        ]
      }
    },
    "v3": {
      "created": "2020-08-03T14:10:47.753066Z",
      "state": {
        "43a43fe8a8a082d3b5343dfaf2fd0c8b8e370675b1f376e92e9994612c33ea255b11298269d72f797399ebb94edeefe53df243643676548f584fb8603ca53a0f": [
          "a_file.txt"
        ]
      }
    }
  }
}
```


## 3. Test object creation with just v1.

### 3.1 New object with just v1

```
> python ocfl-object.py --create --id http://example.org/obj1 --src fixtures/1.0/content/cf1/v1 --objdir tmp/obj1 -v
INFO:ocfl.object:Created OCFL object http://example.org/obj1 in tmp/obj1
```


## 4. Test object build with three versions.

### 4.1 New object with three versions

```
> python ocfl-object.py --build --id http://example.org/obj2 --src fixtures/1.0/content/cf3 --objdir tmp/obj2 -v
INFO:ocfl.object:Built object http://example.org/obj2 with 3 versions
```


## 5. Test extract of version.

### 5.1 Extract v1

```
> python ocfl-object.py --extract v1 --objdir fixtures/1.0/good-objects/spec-ex-full --dstdir tmp/v1 -v
INFO:ocfl.object:Extracted v1 into tmp/v1
Extracted content for v1 in tmp/v1
```


### 5.2 Extract v2

```
> python ocfl-object.py --extract v2 --objdir fixtures/1.0/good-objects/spec-ex-full --dstdir tmp/v2 -v
INFO:ocfl.object:Extracted v2 into tmp/v2
Extracted content for v2 in tmp/v2
```


## 6. Test error conditions.

### 6.1 No valid command argument

With no argument and error and suggections are shown.

```
> python ocfl-object.py
Error - Exactly one command (create, build, update, show, validate, extract) must be specified
```

(last command exited with return code 1)


### 6.2 No source directory (--srcdir)

The `--create` action requires a source.

```
> python ocfl-object.py --create
Error - Must specify either --srcdir or --srcbag containing v1 files when creating an OCFL object!
```

(last command exited with return code 1)


### 6.3 No identifier

The `--create` action requires an identifier.

```
> python ocfl-object.py --create --srcdir tmp
Error - Identifier is not set!
```

(last command exited with return code 1)

