# -*- coding: utf-8 -*-
# :copyright: (c) 2020 by Jesse Johnson.
# :license: Apache 2.0, see LICENSE for more details.
'''Test parser.

Attributes
----------
check_attribute: bool
    Check document attributes

'''

import sys
import pytest

from argufy import Parser

sys.path.append('.')
import subcommands_parser  # noqa: E402


def test_help():
    '''Do help function for CLI.'''
    parser = Parser()
    parser.add_commands(subcommands_parser, ['test_'])
    with pytest.raises(SystemExit):
        parser.dispatch(['subcommands-parser', 'example-bool'])


def test_bool():
    '''Do main function for CLI.'''
    parser = Parser()
    parser.add_subcommands(subcommands_parser, ['test_'])
    parser.dispatch([
        'subcommands-parser',
        'example-bool',
        '--bool-check'
    ])


def test_choice():
    '''Do main function for CLI.'''
    parser = Parser()
    parser.add_subcommands(subcommands_parser, ['test_'])
    parser.dispatch([
        'subcommands-parser',
        'example-choice',
        '--choice-check',
        'B'
    ])
