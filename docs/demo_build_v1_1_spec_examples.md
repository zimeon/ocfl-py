# Build the v1.1 specification examples

_Output from `tests/test_demo_build_spec_v1_1_examples.py`._

## 1. Test for minimal example.

### 1.1 Minimal example

The digest type sha512-spec-ex is sha512 with most of the content stripped out and replaced with an ellipsis. This is inventory should match the example in <https://ocfl.io/1.1/spec/#example-minimal-object>.

```
> python ocfl-object.py create --src fixtures/1.1/content/spec-ex-minimal --id http://example.org/minimal --spec-version 1.1 --digest sha512-spec-ex --created 2018-10-02T12:00:00Z --message One file --name Alice --address alice@example.org -v
### Inventory for v1
{
  "digestAlgorithm": "sha512-spec-ex",
  "head": "v1",
  "id": "http://example.org/minimal",
  "manifest": {
    "7545b8720a60123...f67": [
      "v1/content/v1/file.txt"
    ]
  },
  "type": "https://ocfl.io/1.1/spec/#inventory",
  "versions": {
    "v1": {
      "created": "2018-10-02T12:00:00Z",
      "message": "One file",
      "state": {
        "7545b8720a60123...f67": [
          "v1/file.txt"
        ]
      },
      "user": {
        "address": "alice@example.org",
        "name": "Alice"
      }
    }
  }
}
```


## 2. Test for versioned example.

### 2.1 Versioned example

This is inventory should match the example with 3 versions in <https://ocfl.io/1.1/spec/#example-versioned-object>.

```
> python ocfl-object.py build --src fixtures/1.1/content/spec-ex-full --spec-version 1.1 --id ark:/12345/bcd987 --fixity md5 --fixity sha1 --digest sha512-spec-ex --metadata extra_fixtures/1.1/content/spec-ex-full-metadata.json -v
### Inventory for v3
{
  "digestAlgorithm": "sha512-spec-ex",
  "fixity": {
    "md5": {},
    "sha1": {}
  },
  "head": "v3",
  "id": "ark:/12345/bcd987",
  "manifest": {
    "4d27c86b026ff70...b53": [
      "v2/content/foo/bar.xml"
    ],
    "7dcc352f96c56dc...c31": [
      "v1/content/foo/bar.xml"
    ],
    "cf83e1357eefb8b...a3e": [
      "v1/content/empty.txt"
    ],
    "ffccf6baa218097...62e": [
      "v1/content/image.tiff"
    ]
  },
  "type": "https://ocfl.io/1.1/spec/#inventory",
  "versions": {
    "v1": {
      "created": "2018-01-01T01:01:01Z",
      "message": "Initial import",
      "state": {
        "7dcc352f96c56dc...c31": [
          "foo/bar.xml"
        ],
        "cf83e1357eefb8b...a3e": [
          "empty.txt"
        ],
        "ffccf6baa218097...62e": [
          "image.tiff"
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
        "4d27c86b026ff70...b53": [
          "foo/bar.xml"
        ],
        "cf83e1357eefb8b...a3e": [
          "empty.txt",
          "empty2.txt"
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
        "4d27c86b026ff70...b53": [
          "foo/bar.xml"
        ],
        "cf83e1357eefb8b...a3e": [
          "empty2.txt"
        ],
        "ffccf6baa218097...62e": [
          "image.tiff"
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


## 3. Test for different paths example.

### 3.1 Versioned example

This is inventory should match the example showing how content paths may differ from logical paths in <https://ocfl.io/1.1/spec/#example-object-diff-paths>.

```
> python ocfl-object.py create --src fixtures/1.1/content/spec-ex-diff-paths/v1 --id http://example.org/diff-paths/v1 --spec-version 1.1 --digest sha512-spec-ex --normalization md5 --created 2019-03-14T20:31:00Z -v
### Inventory for v1
{
  "digestAlgorithm": "sha512-spec-ex",
  "head": "v1",
  "id": "http://example.org/diff-paths/v1",
  "manifest": {
    "7545b8720a60123...f67": [
      "v1/content/3bacb119a98a15c5"
    ],
    "af318dca6b3f5ad...3cd": [
      "v1/content/9f2bab8ef869947d"
    ]
  },
  "type": "https://ocfl.io/1.1/spec/#inventory",
  "versions": {
    "v1": {
      "created": "2019-03-14T20:31:00Z",
      "state": {
        "7545b8720a60123...f67": [
          "a file.wxy"
        ],
        "af318dca6b3f5ad...3cd": [
          "another file.xyz"
        ]
      }
    }
  }
}
```

