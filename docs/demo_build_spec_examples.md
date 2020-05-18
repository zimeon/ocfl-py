# Build spec example inventory

## Minimal example

```
> ./ocfl-object.py --build --src fixtures/1.0/content/spec-ex-minimal --id http://example.org/minimal --digest sha512 --created "2018-10-02T12:00:00Z" --message "One file" --name "Alice" --address "alice@example.org" -v | ./compactify_spec_examples.py > examples/spec-minimal.txt
```

to get <examples/spec-minimal.txt>

## Full example

```
./ocfl-object.py --build --src fixtures/1.0/content/spec-ex-full --id ark:/12345/bcd987 --fixity md5 --fixity sha1 --digest sha512 -v | ./compactify_spec_examples.py > examples/spec-full.txt
```

to get <examples/spec-full.txt>

## Different paths example

```
./ocfl-object.py --build --src fixtures/1.0/content/spec-ex-diff-paths --id http://example.org/diff-paths --digest sha512 --normalization md5 --created "2019-03-14T20:31:00Z" -v | ./compactify_spec_examples.py > examples/spec-diff-paths.txt
```

to get <examples/spec-diff-paths.txt>
