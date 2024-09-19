#!/usr/bin/env python
"""Compactify example JSON for OCFL specification.

Takes the long digests and replaces them with first 6 characters,
an ellipsis, and then the last 6 characters. Input from stdin
and output to stdout.
"""
import re
import sys

txt = sys.stdin.read()

txt = re.sub(r'''sha512-spec-ex''', 'sha512', txt)
txt = re.sub(r'''"([\da-f]{6})([\da-f]{119})([\da-f]{3})"''', r'''"\1...\3"''', txt)
txt = re.sub(r'''\s+\[\s+"''', ' [ "', txt, flags=re.MULTILINE)
txt = re.sub(r'''"\s+\](\s+)}(,)?''', r'''" ]\1}\2''', txt, flags=re.MULTILINE)
txt = re.sub(r'''\s+],''', ' ],', txt, flags=re.MULTILINE)
txt = re.sub(r'''(\[[^\n,\]]+,)\s+''', r'''\1 ''', txt, flags=re.MULTILINE)

print(txt)
