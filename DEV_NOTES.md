# Development Notes

## Build

## Test

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
