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


class Coverage(Command):
    """Class to allow coverage run from setup."""

    description = "run coverage"
    user_options = []

    def initialize_options(self):
        """Empty initialize_options."""
        pass

    def finalize_options(self):
        """Empty finalize_options."""
        pass

    def run(self):
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
    scripts=['ocfl-build.py'],
    classifiers=["Development Status :: 2 - Pre-Alpha",
                 "Intended Audience :: Developers",
                 "Operating System :: OS Independent",
                 "Programming Language :: Python",
                 "Programming Language :: Python :: 3.5",
                 "Programming Language :: Python :: 3.6",
                 "Topic :: Internet :: WWW/HTTP",
                 "Topic :: Software Development :: "
                 "Libraries :: Python Modules"],
    url='https://github.com/zimeon/ocfl-py',
    description='ocfl-py - A Python implementation of OCFL',
    long_description=open('README.md').read(),
    install_requires=[
    ],
    test_suite="tests",
    cmdclass={
        'coverage': Coverage,
    },
)
