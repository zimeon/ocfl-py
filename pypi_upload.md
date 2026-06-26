========================
Updating ocfl-py on pypi
========================

Notes to remind @zimeon...

    * main copy of code is https://github.com/zimeon/ocfl-py
    * on PyPi ocfl-py is at <https://pypi.org/project/ocfl-py>
    * now just working in `main` branch, noting releases via https://github.com/zimeon/ocfl-py/releases

Putting up a new version
------------------------

    1. Check version number working branch in `ocfl/_version.py`
    2. Check all changes described in `CHANGES.md`
    3. Check in as necessary and ensure code is up-to-date with `main` branch on github (`pull`
      again after `commit`/`push` to get update error codes and documentation)
    4. Check all tests good (`pytest`)
    5. Upload new version to PyPI:

      ```
      uv pip install --upgrade build setuptools wheel twine
      python -m build --no-isolation
      ls -lrt dist
      twine upload dist/*2.X.X*
      ```
    6. Check on PyPI at <https://pypi.org/project/ocfl-py>
    7. Mark github release via https://github.com/zimeon/ocfl-py/releases
    8. Start new version number by editing `ocfl/_version.py` and `CHANGES.md`, push to `main`
