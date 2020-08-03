========================
Updating ocfl-py on pypi
========================

  Notes to remind @zimeon...

    * main copy of code is https://github.com/zimeon/ocfl-py
    * on PyPi ocfl-py is at <https://pypi.org/project/ocfl-py>

Putting up a new version
------------------------

    1. Run `extract_codes.py` to update validation status
    2. Run `build_demo_docs.sh` to update demo documents
    3. Check version number working branch in `ocfl/_version.py`
    4. Check all changes described in `CHANGES.md`
    5. Check code is up-to-date with `main` branch on github
    6. Check all tests good (`tox`)
    7. Check out `main` and merge in working branch
    8. Upload new version to PyPI:

      ```
      pip install --upgrade setuptools wheel twine
      python setup.py sdist bdist_wheel; ls dist
      twine upload dist/*1.X.X*
      ```
    9. Check on PyPI at <https://pypi.org/project/ocfl-py>
    10. Finally, in `develop` branch, start new version number by editing `ocfl/_version.py` and `CHANGES.md`
