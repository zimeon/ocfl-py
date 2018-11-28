# Demo output from tests/test_ocfl_object_script.py

## 1. Test object inventory creation with output to stdout.


### 1.1 Inventory for new object with just v1

```
> python ocfl-object.py --create --id http://example.org/obj1 --src fixtures/content/cf1/v1


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
      "created": "2018-11-28T08:31:38.295169Z",
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

```
> python ocfl-object.py --build --id http://example.org/obj2 --src fixtures/content/cf3


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
      "created": "2018-11-28T08:31:38.401260Z",
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
      "created": "2018-11-28T08:31:38.401260Z",
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
      "created": "2018-11-28T08:31:38.401650Z",
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
      "created": "2018-11-28T08:31:38.401260Z",
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
      "created": "2018-11-28T08:31:38.401650Z",
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
      "created": "2018-11-28T08:31:38.402021Z",
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
