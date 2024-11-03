# Inventory validation

The current draft [JSON Schema](https://json-schema.org/specification) for validating [OCFL Inventory files](https://ocfl.io/draft/spec/#inventory) is located at <https://ocfl.io/draft/spec/inventory_schema.json> (see also <https://github.com/OCFL/spec/tree/main/draft/spec>). The instructions below show how to generate example inventory files using `ocfl-py` and then validate them against the JSON Schema.

## Minimal example from specification

```
(py3) simeon@Cider ocfl-py (main %)> rm -rf tmp/minimal
(py3) simeon@Cider ocfl-py (main %)> ./ocfl-object.py --build --src fixtures/content/spec-ex-minimal --id http://example.org/minimal --created "2018-10-02T12:00:00Z" --message "One file" --name "Alice" --address "alice@example.org" --objdir tmp/minimal
(py3) simeon@Cider ocfl-py (main %)> jsonschema -i tmp/minimal/inventory.json ../ocfl-spec/draft/spec/inventory_schema.json
```

## Full example from specification

```
(py3) simeon@Cider ocfl-py (main %)> rm -rf tmp/full
(py3) simeon@Cider ocfl-py (main %)> ./ocfl-object.py --build --src fixtures/content/spec-ex-full --id ark:/12345/bcd987 --fixity md5 --fixity sha1 --objdir tmp/full
INFO:root:Reading metadata for v1 from fixtures/content/spec-ex-full/v1/inventory.json
INFO:root:Reading metadata for v2 from fixtures/content/spec-ex-full/v2/inventory.json
INFO:root:Reading metadata for v3 from fixtures/content/spec-ex-full/v3/inventory.json
(py3) simeon@Cider ocfl-py (main %)> jsonschema -i tmp/full/inventory.json ../ocfl-spec/draft/spec/inventory_schema.json
```

## All OCFL JSON schema

* OCFL v1.0: <https://ocfl.io/1.0/spec/inventory_schema.json>
* OCFL v1.1: <https://ocfl.io/1.1/spec/inventory_schema.json>
* Current draft: <https://ocfl.io/draft/spec/inventory_schema.json>
