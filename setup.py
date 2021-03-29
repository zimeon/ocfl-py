"""Setup for ocfl-py."""
import os
import re
from setuptools import setup, Command

# Extract version number
verfile = open("ocfl/_version.py", "rt").read()
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

    def finalize_options(self):
        """Empty finalize_options."""


class Coverage(ShellCommand):
    """Class to allow coverage run from setup."""

    description = "run coverage"

    def run(self):  # pylint: disable=no-self-use
        """Run coverage program."""
        os.system("coverage run --source=ocfl setup.py test")
        os.system("coverage report")
        os.system("coverage html")
        print("See htmlcov/index.html for details.")


setup(
    name='ocfl-py',
    version=version,
    author='Simeon Warner',
    author_email='simeon.warner@cornell.edu',
    packages=['ocfl'],
    package_data={'ocfl': ['data/*']},
    scripts=['ocfl-object.py', 'ocfl-sidecar.py', 'ocfl-store.py', 'ocfl-validate.py'],
    classifiers=["Development Status :: 4 - Beta",
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
        'bagit>=1.8.1',
        'dateutils>=0.6.6',
        'fs>2.4.0',
        'fs_s3fs>=1.1.1',
        'pairtree>=0.8.1'
    ],
    test_suite="tests",
    cmdclass={
        'coverage': Coverage
    },
)
