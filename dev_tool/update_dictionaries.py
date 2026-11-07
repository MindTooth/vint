#!/usr/bin/env python3
""" Update vint/ast/dictionary/*.py from a Vim source checkout.

usage: python3 dev_tool/update_dictionaries.py /path/to/vim

Entries are only added, never removed, so scripts written for older Vims
(e.g. using the removed 'altkeymap' option) are still recognized.
"""
import ast
import re
import sys
from pathlib import Path

DICTIONARY_DIR = Path(__file__).resolve().parent.parent / 'vint' / 'ast' / 'dictionary'


def read(path):
    return Path(path).read_text(encoding='utf-8', errors='replace')


def vim_functions(vim_src):
    src = read(vim_src / 'evalfunc.c')
    table = src[src.index('global_functions[] ='):]
    table = table[:table.index('\n};')]
    return {name: True for name in re.findall(r'^\s*\{"(\w+)",', table, re.M)}


def vim_variables(vim_src):
    names = re.findall(r'VV_NAME\("(\w+)"', read(vim_src / 'evalvars.c'))
    return {name: True for name in names}


def vim_autocmd_events(vim_src):
    names = re.findall(r'KEYVALUE_ENTRY\(-?EVENT_\w+,\s*"(\w+)"\)', read(vim_src / 'autocmd.c'))
    return {name.upper(): True for name in names}


def vim_option_abbreviations(vim_src):
    pairs = re.findall(r'^\s*\{"(\w+)"\s*,\s*"(\w+)"', read(vim_src / 'optiondefs.h'), re.M)
    return {abbr: name for name, abbr in pairs}


def format_dict_body(entries):
    return ''.join('    {!r}: {!r},\n'.format(k, v) for k, v in sorted(entries.items()))


def update_dict(path, dict_name, new_entries):
    """ Merges new_entries into the top-level `dict_name = {...}` literal in path. """
    text = path.read_text(encoding='utf-8')
    pattern = re.compile(r'^(' + dict_name + r' = \{\n)(.*?)(^\}\n)', re.S | re.M)
    match = pattern.search(text)
    if match is None:
        raise ValueError('{} not found in {}'.format(dict_name, path))

    current = ast.literal_eval('{' + match.group(2) + '}')
    merged = dict(current, **new_entries)
    text = text[:match.start(2)] + format_dict_body(merged) + text[match.end(2):]
    path.write_text(text, encoding='utf-8')
    return len(merged) - len(current)


def main(vim_dir):
    vim_src = Path(vim_dir) / 'src'
    updates = [
        ('builtins.py', 'BuiltinVariables', vim_variables(vim_src)),
        ('builtins.py', 'BuiltinFunctions', vim_functions(vim_src)),
        ('autocmd_events.py', 'AutoCmdEvents', vim_autocmd_events(vim_src)),
        ('abbreviations.py', 'Abbreviations', vim_option_abbreviations(vim_src)),
    ]
    for file_name, dict_name, entries in updates:
        if not entries:
            raise ValueError('No {} found; is {} a Vim source checkout?'.format(dict_name, vim_dir))
        added = update_dict(DICTIONARY_DIR / file_name, dict_name, entries)
        print('{}: +{} entries'.format(dict_name, added))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(__doc__.strip())
    main(sys.argv[1])
