# Build the specification examples

_Output from `tests/test_demo_build_spec_examples.py`._

## 1. Test for minumal example.

### 1.1 Minimal example

The digest type sha512-spec-ex is sha512 with most of the content stripped out and replaced with an ellipsis. This is inventory should match the example in <https://ocfl.io/1.0/spec/#example-minimal-object>.

```
> python ocfl-object.py --build --src fixtures/1.0/content/spec-ex-minimal --id http://example.org/minimal --digest sha512-spec-ex --created 2018-10-02T12:00:00Z --message One file --name Alice --address alice@example.org -v
WARNING:ocfl.object:### Inventory for v1{
  "digestAlgorithm": "sha512-spec-ex",
  "head": "v1",
  "id": "http://example.org/minimal",
  "manifest": {
    "7545b8720a60123...f67": [
      "v1/content/file.txt"
    ]
  },
  "type": "https://ocfl.io/1.0/spec/#inventory",
  "versions": {
    "v1": {
      "created": "2018-10-02T12:00:00Z",
      "message": "One file",
      "state": {
        "7545b8720a60123...f67": [
          "file.txt"
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

This is inventory should match the example with 3 versions in <https://ocfl.io/1.0/spec/#example-versioned-object>.

```
> python ocfl-object.py --build --src fixtures/1.0/content/spec-ex-full --id ark:/12345/bcd987 --fixity md5 --fixity sha1 --digest sha512-spec-ex -v
WARNING:ocfl.object:### Inventory for v1{
  "digestAlgorithm": "sha512-spec-ex",
  "fixity": {
    "md5": {
      "184f84e28cbe75e050e9c25ea7f2e939": [
        "v1/content/foo/bar.xml"
      ],
      "c289c8ccd4bab6e385f5afdd89b5bda2": [
        "v1/content/image.tiff"
      ],
      "d41d8cd98f00b204e9800998ecf8427e": [
        "v1/content/empty.txt"
      ]
    },
    "sha1": {
      "66709b068a2faead97113559db78ccd44712cbf2": [
        "v1/content/foo/bar.xml"
      ],
      "b9c7ccc6154974288132b63c15db8d2750716b49": [
        "v1/content/image.tiff"
      ],
      "da39a3ee5e6b4b0d3255bfef95601890afd80709": [
        "v1/content/empty.txt"
      ]
    }
  },
  "head": "v1",
  "id": "ark:/12345/bcd987",
  "manifest": {
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
  "type": "https://ocfl.io/1.0/spec/#inventory",
  "versions": {
    "v1": {
      "created": "2021-04-26T13:25:35.957146Z",
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
      }
    }
  }
}

WARNING:ocfl.object:### Inventory for v2{
  "digestAlgorithm": "sha512-spec-ex",
  "fixity": {
    "md5": {
      "184f84e28cbe75e050e9c25ea7f2e939": [
        "v1/content/foo/bar.xml"
      ],
      "2673a7b11a70bc7ff960ad8127b4adeb": [
        "v2/content/foo/bar.xml"
      ],
      "c289c8ccd4bab6e385f5afdd89b5bda2": [
        "v1/content/image.tiff"
      ],
      "d41d8cd98f00b204e9800998ecf8427e": [
        "v1/content/empty.txt"
      ]
    },
    "sha1": {
      "66709b068a2faead97113559db78ccd44712cbf2": [
        "v1/content/foo/bar.xml"
      ],
      "a6357c99ecc5752931e133227581e914968f3b9c": [
        "v2/content/foo/bar.xml"
      ],
      "b9c7ccc6154974288132b63c15db8d2750716b49": [
        "v1/content/image.tiff"
      ],
      "da39a3ee5e6b4b0d3255bfef95601890afd80709": [
        "v1/content/empty.txt"
      ]
    }
  },
  "head": "v2",
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
  "type": "https://ocfl.io/1.0/spec/#inventory",
  "versions": {
    "v1": {
      "created": "2021-04-26T13:25:35.957146Z",
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
      }
    },
    "v2": {
      "created": "2021-04-26T13:25:35.958734Z",
      "state": {
        "4d27c86b026ff70...b53": [
          "foo/bar.xml"
        ],
        "cf83e1357eefb8b...a3e": [
          "empty.txt",
          "empty2.txt"
        ]
      }
    }
  }
}

WARNING:ocfl.object:### Inventory for v3{
  "digestAlgorithm": "sha512-spec-ex",
  "fixity": {
    "md5": {
      "184f84e28cbe75e050e9c25ea7f2e939": [
        "v1/content/foo/bar.xml"
      ],
      "2673a7b11a70bc7ff960ad8127b4adeb": [
        "v2/content/foo/bar.xml"
      ],
      "c289c8ccd4bab6e385f5afdd89b5bda2": [
        "v1/content/image.tiff"
      ],
      "d41d8cd98f00b204e9800998ecf8427e": [
        "v1/content/empty.txt"
      ]
    },
    "sha1": {
      "66709b068a2faead97113559db78ccd44712cbf2": [
        "v1/content/foo/bar.xml"
      ],
      "a6357c99ecc5752931e133227581e914968f3b9c": [
        "v2/content/foo/bar.xml"
      ],
      "b9c7ccc6154974288132b63c15db8d2750716b49": [
        "v1/content/image.tiff"
      ],
      "da39a3ee5e6b4b0d3255bfef95601890afd80709": [
        "v1/content/empty.txt"
      ]
    }
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
  "type": "https://ocfl.io/1.0/spec/#inventory",
  "versions": {
    "v1": {
      "created": "2021-04-26T13:25:35.957146Z",
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
      }
    },
    "v2": {
      "created": "2021-04-26T13:25:35.958734Z",
      "state": {
        "4d27c86b026ff70...b53": [
          "foo/bar.xml"
        ],
        "cf83e1357eefb8b...a3e": [
          "empty.txt",
          "empty2.txt"
        ]
      }
    },
    "v3": {
      "created": "2021-04-26T13:25:35.959946Z",
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
      }
    }
  }
}

```


## 3. Test for different paths example.

### 3.1 Versioned example

This is inventory should match the example showing how content paths may differ from logical paths in <https://ocfl.io/1.0/spec/#example-object-diff-paths>.

```
> python ocfl-object.py --build --src fixtures/1.0/content/spec-ex-diff-paths --id http://example.org/diff-paths --digest sha512-spec-ex --normalization md5 --created 2019-03-14T20:31:00Z -v
WARNING:ocfl.object:### Inventory for v1{
  "digestAlgorithm": "sha512-spec-ex",
  "head": "v1",
  "id": "http://example.org/diff-paths",
  "manifest": {
    "7545b8720a60123...f67": [
      "v1/content/3bacb119a98a15c5"
    ],
    "af318dca6b3f5ad...3cd": [
      "v1/content/9f2bab8ef869947d"
    ]
  },
  "type": "https://ocfl.io/1.0/spec/#inventory",
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

