# Inventory validation

```
(py3) simeon@Cider ocfl-py (master %)> rm -rf tmp/minimal
(py3) simeon@Cider ocfl-py (master %)> ./ocfl-object.py --build --src fixtures/content/spec-ex-minimal --id http://example.org/minimal --created "2018-10-02T12:00:00Z" --message "One file" --name "Alice" --address "alice@example.org" --dst tmp/minimal
(py3) simeon@Cider ocfl-py (master %)> jsonschema -i tmp/minimal/inventory.json ../ocfl-spec/draft/spec/inventory_schema.json
```

```
(py3) simeon@Cider ocfl-py (master %)> rm -rf tmp/full
(py3) simeon@Cider ocfl-py (master %)> ./ocfl-object.py --build --src fixtures/content/spec-ex-full --id ark:/12345/bcd987 --fixity md5 --fixity sha1 --dst tmp/full
INFO:root:Reading metadata for v1 from fixtures/content/spec-ex-full/v1/inventory.json
INFO:root:Reading metadata for v2 from fixtures/content/spec-ex-full/v2/inventory.json
INFO:root:Reading metadata for v3 from fixtures/content/spec-ex-full/v3/inventory.json
(py3) simeon@Cider ocfl-py (master %)> jsonschema -i tmp/full/inventory.json ../ocfl-spec/draft/spec/inventory_schema.json
```
