# Demo output from tests/test_ocfl_object_script.py

## 1. Test object inventory creation with output to stdout.

### 1.1 Inventory for new object with just v1

Without an `--objdir` argument the script just writes out the inventory for the object that would have been created.

```
> python ocfl-object.py --create --id http://example.org/obj1 --src fixtures/1.0/content/cf1/v1


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
  "type": "Object",
  "versions": {
    "v1": {
      "created": "2018-11-29T13:10:44.286323Z",
      "message": "",
      "state": {
        "43a43fe8a8a082d3b5343dfaf2fd0c8b8e370675b1f376e92e9994612c33ea255b11298269d72f797399ebb94edeefe53df243643676548f584fb8603ca53a0f": [
          "a_file.txt"
        ]
      },
      "type": "Version",
      "user": {
        "address": "somewhere",
        "name": "someone"
      }
    }
  }
}
```

Exited with code 0

### 1.2 Inventory for new object with three versions

Without an `--objdir` argument the script just writes out the inventory for each version in the object that would have been created.

```
> python ocfl-object.py --build --id http://example.org/obj2 --src fixtures/1.0/content/cf3


### Inventory for v1

{
  "digestAlgorithm": "sha512",
  "head": "v1",
  "id": "http://example.org/obj2",
  "manifest": {
    "43a43fe8a8a082d3b5343dfaf2fd0c8b8e370675b1f376e92e9994612c33ea255b11298269d72f797399ebb94edeefe53df243643676548f584fb8603ca53a0f": [
      "v1/content/a_file.txt"
    ]
  },
  "type": "Object",
  "versions": {
    "v1": {
      "created": "2018-11-29T13:10:44.403391Z",
      "message": "",
      "state": {
        "43a43fe8a8a082d3b5343dfaf2fd0c8b8e370675b1f376e92e9994612c33ea255b11298269d72f797399ebb94edeefe53df243643676548f584fb8603ca53a0f": [
          "a_file.txt"
        ]
      },
      "type": "Version",
      "user": {
        "address": "somewhere",
        "name": "someone"
      }
    }
  }
}


### Inventory for v2

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
  "type": "Object",
  "versions": {
    "v1": {
      "created": "2018-11-29T13:10:44.403391Z",
      "message": "",
      "state": {
        "43a43fe8a8a082d3b5343dfaf2fd0c8b8e370675b1f376e92e9994612c33ea255b11298269d72f797399ebb94edeefe53df243643676548f584fb8603ca53a0f": [
          "a_file.txt"
        ]
      },
      "type": "Version",
      "user": {
        "address": "somewhere",
        "name": "someone"
      }
    },
    "v2": {
      "created": "2018-11-29T13:10:44.403774Z",
      "message": "",
      "state": {
        "296e72b8fd5f7f0ac1473993600ae34953d5dab646f17e7b182b8648aff830d7bf01b56490777cb3e72b33fcc1ae520506badea1032252d1a55fd7362e269975": [
          "a_file.txt"
        ]
      },
      "type": "Version",
      "user": {
        "address": "somewhere",
        "name": "someone"
      }
    }
  }
}


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
  "type": "Object",
  "versions": {
    "v1": {
      "created": "2018-11-29T13:10:44.403391Z",
      "message": "",
      "state": {
        "43a43fe8a8a082d3b5343dfaf2fd0c8b8e370675b1f376e92e9994612c33ea255b11298269d72f797399ebb94edeefe53df243643676548f584fb8603ca53a0f": [
          "a_file.txt"
        ]
      },
      "type": "Version",
      "user": {
        "address": "somewhere",
        "name": "someone"
      }
    },
    "v2": {
      "created": "2018-11-29T13:10:44.403774Z",
      "message": "",
      "state": {
        "296e72b8fd5f7f0ac1473993600ae34953d5dab646f17e7b182b8648aff830d7bf01b56490777cb3e72b33fcc1ae520506badea1032252d1a55fd7362e269975": [
          "a_file.txt"
        ]
      },
      "type": "Version",
      "user": {
        "address": "somewhere",
        "name": "someone"
      }
    },
    "v3": {
      "created": "2018-11-29T13:10:44.404128Z",
      "message": "",
      "state": {
        "43a43fe8a8a082d3b5343dfaf2fd0c8b8e370675b1f376e92e9994612c33ea255b11298269d72f797399ebb94edeefe53df243643676548f584fb8603ca53a0f": [
          "a_file.txt"
        ]
      },
      "type": "Version",
      "user": {
        "address": "somewhere",
        "name": "someone"
      }
    }
  }
}
```

Exited with code 0

## 2. Test object creation with just v1.

### 2.1 New object with just v1

```
> python ocfl-object.py --objdir tmp/object --create --id http://example.org/obj1 --src fixtures/1.0/content/cf1/v1 -v
INFO:root:Created object http://example.org/obj1 in tmp/object
```

```
object
├── 0=ocfl_object_1.0
├── inventory.json
├── inventory.json.sha512
└── v1
    ├── content
    │   └── a_file.txt
    ├── inventory.json
    └── inventory.json.sha512

2 directories, 6 files
```


## 3. Test object build with three versions.

### 3.1 New object with three versions

```
> python ocfl-object.py --objdir tmp/object --build --id http://example.org/obj2 --src fixtures/1.0/content/cf3 -v
INFO:root:Built object http://example.org/obj2 with 3 versions
```

```
object
├── 0=ocfl_object_1.0
├── inventory.json
├── inventory.json.sha512
├── v1
│   ├── content
│   │   └── a_file.txt
│   ├── inventory.json
│   └── inventory.json.sha512
├── v2
│   ├── content
│   │   └── a_file.txt
│   ├── inventory.json
│   └── inventory.json.sha512
└── v3
    ├── inventory.json
    └── inventory.json.sha512

5 directories, 11 files
```


## 4. Test extract of version.

### 4.1 Extract v1

```
> python ocfl-object.py --dstdir tmp --extract v1 --objdir fixtures/1.0/objects/spec-ex-full -v
INFO:root:Extracted v1 into tmp/v1
```

```
.
└── v1
    ├── empty.txt
    ├── foo
    │   └── bar.xml
    └── image.tiff

2 directories, 3 files
```


### 4.2 Extract v2

```
> python ocfl-object.py --dstdir tmp --extract v2 --objdir fixtures/1.0/objects/spec-ex-full -v
INFO:root:Extracted v2 into tmp/v2
```

```
.
├── v1
│   ├── empty.txt
│   ├── foo
│   │   └── bar.xml
│   └── image.tiff
└── v2
    ├── empty.txt
    ├── empty2.txt
    └── foo
        └── bar.xml

4 directories, 6 files
```


## 5. Test error conditions.

### 5.1 No valid command argument

```
> python ocfl-object.py
usage: ocfl-object.py [-h] [--srcdir SRCDIR] [--digest DIGEST]
                      [--fixity FIXITY] [--id ID] [--dstdir DSTDIR]
                      (--create | --build | --show | --validate | --extract EXTRACT)
                      [--created CREATED] [--message MESSAGE] [--name NAME]
                      [--address ADDRESS] [--skip SKIP] [--no-forward-delta]
                      [--no-dedupe] [--objdir OBJDIR]
                      [--ocfl-version OCFL_VERSION] [--verbose]
ocfl-object.py: error: one of the arguments --create --build --show --validate --extract is required
```

Exited with code 2

### 5.2 No identifier

```
> python ocfl-object.py --create
Traceback (most recent call last):
  File "ocfl-object.py", line 76, in <module>
    do_object_operation(args)
  File "ocfl-object.py", line 55, in do_object_operation
    objdir=args.objdir)
  File "/Users/simeon/src/ocfl-py/ocfl/object.py", line 255, in create
    raise ObjectException("Identifier is not set!")
ocfl.object.ObjectException: Identifier is not set!
```

Exited with code 1
