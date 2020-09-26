# -*- coding: utf-8 -*-
# :copyright: (c) 2020 by Jesse Johnson.
# :license: Apache 2.0, see LICENSE for more details.
'''Test arguments.'''

import sys
from inspect import getmembers, isfunction, signature

from docstring_parser import parse

from argufy import Argument

module = sys.modules[__name__]


def example_simple(check):
    '''Example demonstrating minimal CLI.'''
    pass


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


def test_argument_simple():
    '''Test simple argument.'''
    name, fn = [
        x for x in getmembers(module, isfunction) if x[0] == 'example_simple'
    ][0]
    sig = signature(fn)
    docstring = parse(fn.__doc__)
    arguments = []
    for arg in sig.parameters:
        document = next(
            (d for d in docstring.params if d.arg_name == arg), None
        )
        arguments.append(
            Argument(parameters=sig.parameters[arg], docstring=document)
        )
    print('Arguments: ', arguments[0].__dict__)
    assert arguments[0].attributes.get('metavar') == 'CHECK'
    assert arguments[0].attributes.get('default', None) is None


def test_argument_bool():
    '''Test simple boolean.'''
    name, fn = [
        x for x in getmembers(module, isfunction) if x[0] == 'example_bool'
    ][0]
    sig = signature(fn)
    docstring = parse(fn.__doc__)
    arguments = []
    for arg in sig.parameters:
        document = next(
            (d for d in docstring.params if d.arg_name == arg), None
        )
        arguments.append(
            Argument(parameters=sig.parameters[arg], docstring=document)
        )
    print(arguments[0].__dict__)
    assert arguments[0].attributes['default'] is False


def test_argument_choice():
    '''Test simple character.'''
    name, fn = [
        x for x in getmembers(module, isfunction) if x[0] == 'example_choice'
    ][0]
    sig = signature(fn)
    document = parse(fn.__doc__)
    arguments = []
    for arg in sig.parameters:
        docstring = next(
            (d for d in document.params if d.arg_name == arg), None
        )
        arguments.append(
            Argument(parameters=sig.parameters[arg], docstring=docstring)
        )
    print(arguments[0].__dict__)
    assert arguments[0].metavar == 'CHOICE_CHECK'
    assert arguments[0].help == 'example choice'
    assert arguments[0].attributes['default'] == 'A'
