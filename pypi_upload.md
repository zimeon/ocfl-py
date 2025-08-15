========================
Updating ocfl-py on pypi
========================

Notes to remind @zimeon...

    * main copy of code is https://github.com/zimeon/ocfl-py
    * on PyPi ocfl-py is at <https://pypi.org/project/ocfl-py>
    * now just working in `main` branch, noting releases via https://github.com/zimeon/ocfl-py/releases

Putting up a new version
------------------------

    1. Run `extract_codes.py` to update validation status
    2. Run `build_demo_docs.sh` to update demo documents
    3. Check version number working branch in `ocfl/_version.py`
    4. Check all changes described in `CHANGES.md`
    5. Check in as necessary and ensure code is up-to-date with `main` branch on github
    6. Check all tests good (`py.test`)
    7. Upload new version to PyPI:

      ```
      pip install --upgrade build setuptools wheel twine
      python -m build --no-isolation
      ls -lrt dist
      twine upload dist/*2.X.X*
      ```
    8. Check on PyPI at <https://pypi.org/project/ocfl-py>
    9. Mark github release via https://github.com/zimeon/ocfl-py/releases
    10. Start new version number by editing `ocfl/_version.py` and `CHANGES.md`, push to `main`
