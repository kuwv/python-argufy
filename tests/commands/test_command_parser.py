# -*- coding: utf-8 -*-
# :copyright: (c) 2020 by Jesse Johnson.
# :license: Apache 2.0, see LICENSE for more details.
'''Test parser.

Attributes
----------
check_attribute: bool
    Check document attributes

'''

import os
import pytest
import sys

from argufy import Parser

sys.path.append('.')
import command_parser  # noqa: E402
# module = sys.modules[__name__]


def test_help():
    '''Do help function for CLI.'''
    parser = Parser()
    parser.add_commands(command_parser, ['test_'])
    with pytest.raises(SystemExit) as err:
        parser.dispatch()
    assert err.type == SystemExit
    assert err.value.code == 0


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
