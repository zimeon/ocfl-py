========================
Updating ocfl-py on pypi
========================

  Notes to remind @zimeon...

    * master copy of code is https://github.com/zimeon/ocfl-py
    * on PyPi ocfl-py is at <https://pypi.org/project/ocfl-py>

Putting up a new version
------------------------

    1. Check version number working branch in `ocfl/_version.py`
    2. Check all changes described in `CHANGES.md`
    3. Check code is up-to-date with master github version
    4. Check all tests good (`tox`)
    5. Check out master and merge in working branch
    6. Upload new version to PyPI:

      ```
      pip install --upgrade setuptools wheel twine
      python setup.py sdist bdist_wheel
      ls dist
      twine upload dist/*
      ```
    7. Check on PyPI at <https://pypi.org/project/ocfl-py>
    8. Finally, in develop, start new version number by editing `ocfl/_version.py` and `CHANGES.md`
