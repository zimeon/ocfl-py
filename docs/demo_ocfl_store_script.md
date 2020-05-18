# Demo output from tests/test_ocfl_store_script.py

## 1. Test store initialization and object addition.


### 1.1 Create new store

```
> python ocfl-store.py --root tmp/store --init -v
INFO:root:Created OCFL storage root tmp/store
```

```
store
└── 0=ocfl_1.0

0 directories, 1 file
```


### 1.2 List empty store

```
> python ocfl-store.py --root tmp/store --list -v
INFO:root:Found 0 OCFL Objects under root tmp/store
```

```
store
└── 0=ocfl_1.0

0 directories, 1 file
```


### 1.3 Add object

```
> python ocfl-store.py --root tmp/store --add --src fixtures/1.0/objects/of1 --disposition identity -v
INFO:root:Copying from fixtures/1.0/objects/of1 to tmp/store/ark%3A123%2Fabc
INFO:root:Copied
```

```
store
├── 0=ocfl_1.0
└── ark%3A123%2Fabc
    ├── 0=ocfl_object_1.0
    ├── inventory.json
    ├── inventory.json.sha512
    └── v1
        ├── a_file.txt
        ├── inventory.json
        └── inventory.json.sha512

2 directories, 7 files
```


## 2. Test error cases.


### 2.1 Create new store

```
> python ocfl-store.py --root tmp/store --init -v
INFO:root:Created OCFL storage root tmp/store
```

```
store
└── 0=ocfl_1.0

0 directories, 1 file
```


### 2.2 Add object

```
> python ocfl-store.py --root tmp/store --add -v
ERROR:root:Must specify object path with --src
```

Exited with code 1
