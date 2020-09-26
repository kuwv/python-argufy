# -*- coding: utf-8 -*-
# :copyright: (c) 2020 by Jesse Johnson.
# :license: Apache 2.0, see LICENSE for more details.
'''Test arguments.'''

import sys
from inspect import getmembers, isfunction, signature

from docstring_parser import parse

from argufy import Argument

module = sys.modules[__name__]


def argument_simple(check):
    '''Example demonstrating minimal CLI.'''
    pass


def test_argument_simple():
    '''Test simple argument.'''
    name, fn = [
        x for x in getmembers(module, isfunction) if x[0] == 'argument_simple'
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
    # print('Arguments: ', arguments[0].__dict__)
    # assert arguments[0].attributes.get('metavar') == 'CHECK'
    assert arguments[0].attributes.get('default', None) is None


def argument_bool(bool_check: bool = False):
    '''Example bool.

    Parameters
    ----------
    bool_check: bool, optional
        list packages and version

    '''
    pass


def test_argument_bool():
    '''Test simple boolean.'''
    name, fn = [
        x for x in getmembers(module, isfunction) if x[0] == 'argument_bool'
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
    # print(arguments[0].__dict__)
    assert arguments[0].default is False


def argument_choice(choice_check: str = 'A'):
    '''Example choice.

    Parameters
    ----------
    choice_check: str, {'A', 'B', 'C'}
        argument choice

    '''
    pass


def test_argument_choice():
    '''Test simple character.'''
    name, fn = [
        x for x in getmembers(module, isfunction) if x[0] == 'argument_choice'
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
    # print(arguments[0].__dict__)
    # assert arguments[0].metavar == 'CHOICE_CHECK'
    assert arguments[0].help == 'argument choice'
    assert arguments[0].default == 'A'


def argument_full(
    string_check: str = 'A',
    bool_check: bool = False,
    integer_check: int = 1,
    float_check: float = 1.5,
    list_check: list = ['A'],
    set_check: set = {'a'},
    tuple_check: tuple = ('A',),
    # file_check: open = 'test.toml',
):
    '''Example full.

    Parameters
    ----------
    string_check: str, {'A', 'B', 'C'}
        argument string
    bool_check:
        argument bool
    integer_check:
        argument int
    float_check:
        argument float
    list_check:
        argument list
    set_check:
        argument set
    tuple_check:
        argument tuple

    '''
    pass


def test_argument_full():
    '''Test full type set.'''
    name, fn = [
        x for x in getmembers(module, isfunction) if x[0] == 'argument_full'
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
    # assert arguments[0].metavar == 'STRING_CHECK'
    assert arguments[0].help == 'argument string'
    assert arguments[0].default == 'A'

    print(arguments[1].__dict__)
    # assert arguments[1].metavar == 'BOOL_CHECK'
    assert arguments[1].help == 'argument bool'
    assert arguments[1].default is False

    print(arguments[2].__dict__)
    # assert arguments[2].metavar == 'INTEGER_CHECK'
    assert arguments[2].help == 'argument int'
    assert arguments[2].default == 1

    print(arguments[3].__dict__)
    # assert arguments[3].metavar == 'FLOAT_CHECK'
    assert arguments[3].help == 'argument float'
    assert arguments[3].default == 1.5

    print(arguments[4].__dict__)
    # assert arguments[4].metavar == 'LIST_CHECK'
    assert arguments[4].help == 'argument list'
    assert arguments[4].default == ['A']

    print(arguments[5].__dict__)
    # assert arguments[5].metavar == 'SET_CHECK'
    assert arguments[5].help == 'argument set'
    assert arguments[5].default == {'a'}

    print(arguments[6].__dict__)
    # assert arguments[6].metavar == 'TUPLE_CHECK'
    assert arguments[6].help == 'argument tuple'
    assert arguments[6].default == ('A',)
