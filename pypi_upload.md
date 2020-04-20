========================
Updating ocfl-py on pypi
========================

  Notes to remind @zimeon...

    * master copy of code is https://github.com/zimeon/ocfl-py
    * on PyPi ocfl-py is at <https://pypi.org/project/ocfl-py>

Putting up a new version
------------------------

    1. Check version number working branch in `ocfl/__init__.py`
    2. Check all changes described in `CHANGES.md`
    3. Check code is up-to-date with master github version
    4. Check out master and merge in working branch
    5. Check all tests good (`tox`)
    6. Check branches are as expected (`git branch -a`)
    7. Check local build and version reported OK (`python setup.py build; python setup.py install`)
    8. Upload new version to PyPI:

      ```
      pip install --upgrade setuptools wheel twine
      python setup.py sdist bdist_wheel
      ls dist
      twine upload dist/*
      ```
    9. Check on PyPI at <https://pypi.org/project/ocfl-py>
    10. Finally, start new version number by editing `ocfl/__init__.py` and `CHANGES.md`
