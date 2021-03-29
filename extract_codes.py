#!/usr/bin/env python
"""Extract list of currently implemented error and warning codes."""
import datetime
import logging
import os.path
import re
import requests
import fs

from ocfl.validation_logger import ValidationLogger

SPEC_URL = 'https://ocfl.io/1.0/spec'
GITHUB_REPO = 'https://github.com/zimeon/ocfl-py'
VALIDATION_CODES_URL = 'https://raw.githubusercontent.com/OCFL/spec/master/validation/validation-codes.md'
VALIDATION_STATUS_MD = 'docs/validation_status.md'


class Code():
    """Class for details of one error or warning code."""

    def __init__(self, code, desc):
        """Initialize Code object."""
        self.code = code
        self.desc = desc
        self.suffixes = dict()

    def add_suffix(self, suffix, link=None, desc=None):
        """Add details for one code suffix, which may be None."""
        if suffix is None:
            suffix = ''
        if suffix not in self.suffixes:
            self.suffixes[suffix] = {'link': set(), 'desc': None}
        if link is not None:
            self.suffixes[suffix]['link'].add(link)
        if desc is not None:
            self.suffixes[suffix]['desc'] = desc

    def desc_links(self, suffix):
        """Description and link for this suffix in code."""
        if len(self.suffixes[suffix]['link']) > 0:
            links = ' '.join(self.suffixes[suffix]['link'])
        else:
            links = "_Not implemented_"
        desc = self.suffixes[suffix]['desc'] or "**Missing description**"
        return "%s \\[%s\\]" % (desc, links)

    def as_str(self):
        """String output for markdown."""
        status = "_See multiple cases identified with suffixes below_"
        if len(self.suffixes) == 0:
            status = "_Not implemented_"
        elif '' in self.suffixes:
            status = self.desc_links('')
        desc = self.desc
        linked_code = self.code
        if self.desc is None:
            desc = "**Not in specification**"
        else:
            linked_code = "[%s](%s#%s)" % (self.code, SPEC_URL, self.code)
        s = '| %s | %s | %s |\n' % (linked_code, desc, status)
        for suffix in sorted(self.suffixes.keys()):
            if suffix == '':
                continue
            s += '| | %s%s | %s |\n' % (self.code, suffix, self.desc_links(suffix))
        return s


class Codes():
    """Class for the complete set of error and warning codes."""

    def __init__(self):
        """Initialize Codes object."""
        self.codes = dict()

    def add_spec(self, code, desc):
        """Add a code from the specification."""
        self.codes[code] = Code(code, desc)

    def add_impl(self, code, suffix, link=None, desc=None):
        """Add a code from the ocfl-py implementation."""
        if code not in self.codes:
            self.codes[code] = Code(code, None)
        self.codes[code].add_suffix(suffix, link=link, desc=desc)

    def as_str(self, exclude=''):
        """String output for markdown."""
        s = ''
        for code in sorted(self.codes.keys()):
            if code.startswith(exclude):
                s += self.codes[code].as_str()
        return s

def main():
    """Run from command line."""
    # 0. Assemble all data in codes
    codes = Codes()

    # 1. Get validation codes from github
    md = requests.get(VALIDATION_CODES_URL).text
    for line in md.split('\n'):
        m = re.match(r'''\|\s*([EW]\d\d\d)\s*\|\s*([^\|]+)\|''', line)
        if m:
            code = m.group(1)
            desc = m.group(2).rstrip()
            codes.add_spec(code, desc)

    # 2. Get validation codes and messages from strings file
    vl = ValidationLogger()
    for code_suffix in vl.validation_codes:
        try:
            desc = vl.validation_codes[code_suffix]['description']['en']
        except KeyError:
            desc = "MISSING ENGLISH DESCRIPTION"
        m = re.match(r'''([EW]\d\d\d)(\w?)$''', code_suffix)
        if m:
            codes.add_impl(m.group(1), m.group(2), desc=desc)
        else:
            logging.error("Bad entry for code+suffix '%s' in strings file", code_suffix)

    # 3. Get validation codes from ocfl-py Python codes
    code_fs = fs.open_fs('ocfl')
    for file in code_fs.walk.files(filter=['*.py']):
        with code_fs.open(file) as fh:
            n = 0
            for line in fh:
                n += 1
                m = re.search(r'''(["'])([EW]\d\d\d)(\w)?\1''', line)
                if m:
                    file_line = 'ocfl%s#L%d' % (file, n)
                    link = '[' + file_line + '](' + GITHUB_REPO + '/blob/main/' + file_line + ')'
                    codes.add_impl(m.group(2), m.group(3), link=link)

    # 4. Write table of what is implemented and raise warnings
    logging.info("Writing summary to %s", VALIDATION_STATUS_MD)
    with open(VALIDATION_STATUS_MD, "w") as fh:
        fh.write("# Implementation status for errors and warnings\n\n")
        fh.write("The following tables show the implementation status of all errors and warnings in the OCFL v1.0 specification, with links to the specification and into the code repository.\n\n")
        fh.write("## Errors\n\n")
        fh.write("| Code | Specification text (or suffixed code) | Implementation status and message/links |\n")
        fh.write("| --- | --- | --- |\n")
        fh.write(codes.as_str(exclude='E') + "\n")
        fh.write("## Warnings\n\n")
        fh.write("| Code | Specification text (or suffixed code) | Implementation status and message/links |\n")
        fh.write("| --- | --- | --- |\n")
        fh.write(codes.as_str(exclude='W') + "\n")
        fh.write("_Generated by `%s` at %s_" % (os.path.basename(__file__), datetime.datetime.now()))

if __name__ == "__main__":
    main()
