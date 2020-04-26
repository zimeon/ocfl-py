"""Setup for ocfl-py."""
from setuptools import setup, Command
import os
import re

# Extract version number
verfile = open("ocfl/__init__.py", "rt").read()
match = re.search(r"^__version__ = '(\d\.\d.\d+(\.\d+)?)'",
                  verfile, re.MULTILINE)
if match:
    version = match.group(1)
else:
    raise RuntimeError("Unable to find version string")


class ShellCommand(Command):
    """Class to with defaults for adding extra shell commnads from setup."""

    user_options = []

    def initialize_options(self):
        """Empty initialize_options."""
        pass

    def finalize_options(self):
        """Empty finalize_options."""
        pass


class Coverage(ShellCommand):
    """Class to allow coverage run from setup."""

    description = "run coverage"

    def run(self):
        """Run coverage program."""
        os.system("coverage run --source=ocfl setup.py test")
        os.system("coverage report")
        os.system("coverage html")
        print("See htmlcov/index.html for details.")


class Readmes(ShellCommand):
    """Class to make readme files for demo runs."""

    description = "make README_ files"

    def run(self):
        """Run coverage program."""
        os.system("python tests/test_ocfl_object_script.py > README_object.md")
        os.system("python tests/test_ocfl_store_script.py > README_store.md")
        print("Built README_object.md and README_store.md.")


setup(
    name='ocfl-py',
    version=version,
    author='Simeon Warner',
    author_email='simeon.warner@cornell.edu',
    packages=['ocfl'],
    package_data={'ocfl': ['data/*']},
    scripts=['ocfl-object.py', 'ocfl-store.py', 'ocfl-validate.py'],
    classifiers=["Development Status :: 2 - Pre-Alpha",
                 "Intended Audience :: Developers",
                 "Operating System :: OS Independent",
                 "Programming Language :: Python",
                 "Programming Language :: Python :: 3.6",
                 "Programming Language :: Python :: 3.7",
                 "Programming Language :: Python :: 3.8",
                 "Topic :: Internet :: WWW/HTTP",
                 "Topic :: Software Development :: "
                 "Libraries :: Python Modules"],
    url='https://github.com/zimeon/ocfl-py',
    description='ocfl-py - A Python implementation of OCFL',
    long_description=open('README').read(),
    install_requires=[
        'pairtree>=0.8.1',
        'dateutils>=0.6.6',
        'bagit>=1.7.0'
    ],
    test_suite="tests",
    cmdclass={
        'coverage': Coverage,
        'readmes': Readmes,
    },
)
