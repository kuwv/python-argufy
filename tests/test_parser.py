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

from argufy import Parser

module = sys.modules[__name__]
check_attribute = 'test-attr'


def example_bool(bool_check: bool = False):
    '''Example bool.

    Parameters
    ----------
    bool_check: bool, optional
        list packages and version

    '''
    pass


def example_choice(choice_check: str = 'A'):
    '''Example choice.

    Parameters
    ----------
    choice_check: str, {'A', 'B', 'C'}
        example choice

    '''
    pass


# def test_help():
#     '''Do help function for CLI.'''
#     parser = Parser()
#     parser.add_commands(module, ['test_'])
#     parser.dispatch()


def test_bool():
    '''Do main function for CLI.'''
    parser = Parser()
    parser.add_commands(module, ['test_'])
    parser.dispatch(['example_bool'])


def test_choice():
    '''Do main function for CLI.'''
    parser = Parser()
    parser.add_commands(module, ['test_'])
    parser.dispatch(['example_choice'])
