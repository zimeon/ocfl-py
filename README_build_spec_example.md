# Build spec example inventory

```
> ./ocfl-object.py --build --src fixtures/content/spec-ex --id ark:/12345/bcd987 --fixity md5 --fixity sha1 --digest sha512-spec-ex -v > README_build_spec_example.md
```

to get:

### Inventory for v1

```
{
  "@context": "https://ocfl.io/draft/context.jsonld",
  "digestAlgorithm": "sha512-spec-ex",
  "fixity": {
    "md5": {
      "184f84e28cbe75e050e9c25ea7f2e939": [
        "v1/foo/bar.xml"
      ],
      "c289c8ccd4bab6e385f5afdd89b5bda2": [
        "v1/image.tiff"
      ],
      "d41d8cd98f00b204e9800998ecf8427e": [
        "v1/empty.txt"
      ]
    },
    "sha1": {
      "66709b068a2faead97113559db78ccd44712cbf2": [
        "v1/foo/bar.xml"
      ],
      "b9c7ccc6154974288132b63c15db8d2750716b49": [
        "v1/image.tiff"
      ],
      "da39a3ee5e6b4b0d3255bfef95601890afd80709": [
        "v1/empty.txt"
      ]
    }
  },
  "head": "v1",
  "id": "ark:/12345/bcd987",
  "manifest": {
    "7dcc35...c31": [
      "v1/foo/bar.xml"
    ],
    "cf83e1...a3e": [
      "v1/empty.txt"
    ],
    "ffccf6...62e": [
      "v1/image.tiff"
    ]
  },
  "type": "Object",
  "versions": [
    {
      "created": "2018-01-01T01:01:01Z",
      "message": "Initial import",
      "state": {
        "7dcc35...c31": [
          "foo/bar.xml"
        ],
        "cf83e1...a3e": [
          "empty.txt"
        ],
        "ffccf6...62e": [
          "image.tiff"
        ]
      },
      "type": "Version",
      "user": {
        "address": "alice@example.com",
        "name": "Alice"
      },
      "version": "v1"
    }
  ]
}
```

### Inventory for v2

```
{
  "@context": "https://ocfl.io/draft/context.jsonld",
  "digestAlgorithm": "sha512-spec-ex",
  "fixity": {
    "md5": {
      "184f84e28cbe75e050e9c25ea7f2e939": [
        "v1/foo/bar.xml"
      ],
      "2673a7b11a70bc7ff960ad8127b4adeb": [
        "v2/foo/bar.xml"
      ],
      "c289c8ccd4bab6e385f5afdd89b5bda2": [
        "v1/image.tiff"
      ],
      "d41d8cd98f00b204e9800998ecf8427e": [
        "v1/empty.txt"
      ]
    },
    "sha1": {
      "66709b068a2faead97113559db78ccd44712cbf2": [
        "v1/foo/bar.xml"
      ],
      "a6357c99ecc5752931e133227581e914968f3b9c": [
        "v2/foo/bar.xml"
      ],
      "b9c7ccc6154974288132b63c15db8d2750716b49": [
        "v1/image.tiff"
      ],
      "da39a3ee5e6b4b0d3255bfef95601890afd80709": [
        "v1/empty.txt"
      ]
    }
  },
  "head": "v2",
  "id": "ark:/12345/bcd987",
  "manifest": {
    "4d27c8...b53": [
      "v2/foo/bar.xml"
    ],
    "7dcc35...c31": [
      "v1/foo/bar.xml"
    ],
    "cf83e1...a3e": [
      "v1/empty.txt"
    ],
    "ffccf6...62e": [
      "v1/image.tiff"
    ]
  },
  "type": "Object",
  "versions": [
    {
      "created": "2018-01-01T01:01:01Z",
      "message": "Initial import",
      "state": {
        "7dcc35...c31": [
          "foo/bar.xml"
        ],
        "cf83e1...a3e": [
          "empty.txt"
        ],
        "ffccf6...62e": [
          "image.tiff"
        ]
      },
      "type": "Version",
      "user": {
        "address": "alice@example.com",
        "name": "Alice"
      },
      "version": "v1"
    },
    {
      "created": "2018-02-02T02:02:02Z",
      "message": "Fix bar.xml, remove image.tiff, add empty2.txt",
      "state": {
        "4d27c8...b53": [
          "foo/bar.xml"
        ],
        "cf83e1...a3e": [
          "empty.txt",
          "empty2.txt"
        ]
      },
      "type": "Version",
      "user": {
        "address": "bob@example.com",
        "name": "Bob"
      },
      "version": "v2"
    }
  ]
}
```

### Inventory for v3

```
{
  "@context": "https://ocfl.io/draft/context.jsonld",
  "digestAlgorithm": "sha512-spec-ex",
  "fixity": {
    "md5": {
      "184f84e28cbe75e050e9c25ea7f2e939": [
        "v1/foo/bar.xml"
      ],
      "2673a7b11a70bc7ff960ad8127b4adeb": [
        "v2/foo/bar.xml"
      ],
      "c289c8ccd4bab6e385f5afdd89b5bda2": [
        "v1/image.tiff"
      ],
      "d41d8cd98f00b204e9800998ecf8427e": [
        "v1/empty.txt"
      ]
    },
    "sha1": {
      "66709b068a2faead97113559db78ccd44712cbf2": [
        "v1/foo/bar.xml"
      ],
      "a6357c99ecc5752931e133227581e914968f3b9c": [
        "v2/foo/bar.xml"
      ],
      "b9c7ccc6154974288132b63c15db8d2750716b49": [
        "v1/image.tiff"
      ],
      "da39a3ee5e6b4b0d3255bfef95601890afd80709": [
        "v1/empty.txt"
      ]
    }
  },
  "head": "v3",
  "id": "ark:/12345/bcd987",
  "manifest": {
    "4d27c8...b53": [
      "v2/foo/bar.xml"
    ],
    "7dcc35...c31": [
      "v1/foo/bar.xml"
    ],
    "cf83e1...a3e": [
      "v1/empty.txt"
    ],
    "ffccf6...62e": [
      "v1/image.tiff"
    ]
  },
  "type": "Object",
  "versions": [
    {
      "created": "2018-01-01T01:01:01Z",
      "message": "Initial import",
      "state": {
        "7dcc35...c31": [
          "foo/bar.xml"
        ],
        "cf83e1...a3e": [
          "empty.txt"
        ],
        "ffccf6...62e": [
          "image.tiff"
        ]
      },
      "type": "Version",
      "user": {
        "address": "alice@example.com",
        "name": "Alice"
      },
      "version": "v1"
    },
    {
      "created": "2018-02-02T02:02:02Z",
      "message": "Fix bar.xml, remove image.tiff, add empty2.txt",
      "state": {
        "4d27c8...b53": [
          "foo/bar.xml"
        ],
        "cf83e1...a3e": [
          "empty.txt",
          "empty2.txt"
        ]
      },
      "type": "Version",
      "user": {
        "address": "bob@example.com",
        "name": "Bob"
      },
      "version": "v2"
    },
    {
      "created": "2018-03-03T03:03:03Z",
      "message": "Reinstate image.tiff, delete empty.txt",
      "state": {
        "4d27c8...b53": [
          "foo/bar.xml"
        ],
        "cf83e1...a3e": [
          "empty2.txt"
        ],
        "ffccf6...62e": [
          "image.tiff"
        ]
      },
      "type": "Version",
      "user": {
        "address": "cecilia@example.com",
        "name": "Cecilia"
      },
      "version": "v3"
    }
  ]
}
```
