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
from argufy.__version__ import __version__

sys.path.append('.')
import subcommands_parser  # noqa: E402


def test_help():
    '''Do help function for CLI.'''
    parser = Parser(version=__version__)
    parser.add_commands(subcommands_parser, ['test_'])

    with pytest.raises(SystemExit) as err:
        parser.dispatch(['subcommands-parser'])
    assert err.type == SystemExit
    # assert err.value.code == 2

    with pytest.raises(SystemExit) as err:
        parser.dispatch(['subcommands-parser', 'example-bool'])
    assert err.type == SystemExit
    # assert err.value.code == 2


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
