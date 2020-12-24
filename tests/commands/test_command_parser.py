# -*- coding: utf-8 -*-
# :copyright: (c) 2020 by Jesse Johnson.
# :license: Apache 2.0, see LICENSE for more details.
# type: ignore
'''Test parser.

Attributes
----------
check_attribute: bool
    Check document attributes

'''

import pytest
import sys

from argufy import Parser
from argufy.__version__ import __version__

sys.path.append('.')
import command_parser  # noqa: E402
# module = sys.modules[__name__]


def test_help():
    '''Do help function for CLI.'''
    parser = Parser(version=__version__)
    parser.add_commands(command_parser, ['test_'])
    with pytest.raises(SystemExit) as err:
        parser.dispatch()
    assert err.type == SystemExit
    # assert err.value.code == 2


def test_bool():
    '''Do main function for CLI.'''
    parser = Parser()
    parser.add_commands(command_parser, ['test_'])
    parser.dispatch(['example-bool', '--bool-check'])


def test_choice():
    '''Do main function for CLI.'''
    parser = Parser()
    parser.add_commands(command_parser, ['test_'])
    parser.dispatch(['example-choice', '--choice-check', 'B'])
