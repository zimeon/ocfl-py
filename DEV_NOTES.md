# Development Notes

## Test

The test suite is in `tests` with some test data in `tests/data`
as well as in `fixtures` (submodule <https://github.com/OCFL/fixtures.git>)
and `extra_fixtres` (local, some should eventually migrate into
`fixtures`). The test suite is run with `pytest`:

```
> ocfl-py> pytest
==================== test session starts =======================
platform darwin -- Python 3.11.6, pytest-8.3.3, pluggy-1.5.0
rootdir: /Users/sw272/src/ocfl-py
configfile: pyproject.toml
plugins: anyio-4.6.2.post1
collected 166 items                                                                                                            

tests/test_bagger.py ...            [1%]
...
tests/test_w3c_datetime.py .....  [100%]

==================== 166 passed in 9.90s =======================
```

Filters for warnings from external modules are written in the
`[tool.pytest.ini_options]` section of `pyproject.toml`.

## Coverage

I track test coverage for the code in the ocfl module. I use `coverage`
which has documentation <https://coverage.readthedocs.io/en> and there is
a script `run_coverage.sh` to run coverage assessment and produce HTML
report:

```
> ./run_coverage.sh
================== test session starts =====================
...
ocfl/validator.py                           296     11    96%
ocfl/version_metadata.py                     47      0   100%
ocfl/w3c_datetime.py                         48      0   100%
-------------------------------------------------------------
TOTAL                                      2400    163    93%
Wrote HTML report to htmlcov/index.html
See htmlcov/index.html for details
```

## Testing Sphinx documentation build

```
> sphinx-autobuild docs docs/_build
```

Then access <http://127.0.0.1:8000/>

Some RTD examples using sphinx:
* <https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_numpy.html>
* <https://simpy.readthedocs.io/en/latest/index.html>
* <https://apt-team.pages.debian.net/python-apt/library/index.html>

## Build

Building for upload to pypi is described in `pypi_upload.md`.

FIXME - Having migrated to `pyproject.toml` I'm not sure how to get
`python -m build --no-isolation` working with `--no-isolation`. 