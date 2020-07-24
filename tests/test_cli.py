import sys
from inspect import getmembers, isfunction, signature

from docstring_parser import parse

from argufier.argufier import Argument, Parser

module = sys.modules[__name__]


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


def test_argument_bool():
    name, fn = [x for x in getmembers(module, isfunction)][0]
    sig = signature(fn)
    docstring = parse(fn.__doc__)
    arguments = []
    for arg in sig.parameters:
        document = next((d for d in docstring.params if d.arg_name == arg), None)
        arguments.append(Argument(parameters=sig.parameters[arg], docstring=document))
    print(arguments[0].__dict__)
    assert arguments[0].attributes['default'] == False


def test_argument_choice():
    name, fn = [x for x in getmembers(module, isfunction)][1]
    sig = signature(fn)
    document = parse(fn.__doc__)
    arguments = []
    for arg in sig.parameters:
        docstring = next((d for d in document.params if d.arg_name == arg), None)
        arguments.append(Argument(parameters=sig.parameters[arg], docstring=docstring))
    assert arguments[0].attributes['default'] == 'A'


def test_subparser():
    '''Do main function for CLI.'''
    parser = Parser()
    parser.add_subcommands(module, 'test_')
    parser.dispatch(['example_choice'])
