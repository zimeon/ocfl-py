

Clear out any existing store

```
> rm -r tmp/s
```

Create new store:

```
> ./ocfl-store.py --root tmp/s --create -v
INFO:root:Created OCFL storage root tmp/s
```

```
> tree tmp/s
tmp/s
└── 0=ocfl_1.0

0 directories, 1 file
```

List empty store:

```
> ./ocfl-store.py --root tmp/s --list -v
INFO:root:Found 0 OCFL Objects under root tmp/s
```