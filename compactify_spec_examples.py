#!/usr/bin/env python
"""Compactify example JSON for spec."""
import re
import sys

txt = sys.stdin.read()

txt = re.sub(r'''sha512-spec-ex''', 'sha512', txt)
txt = re.sub(r'''\s+\[\s+"''', ' [ "', txt, flags=re.MULTILINE)
txt = re.sub(r'''\s+\](\s+)},''', r''' ]\1},''', txt, flags=re.MULTILINE)
txt = re.sub(r'''\s+],''', ' ],', txt, flags=re.MULTILINE)
txt = re.sub(r'''(\[[^\n,\]]+,)\s+''', r'''\1 ''', txt, flags=re.MULTILINE)

print(txt)

