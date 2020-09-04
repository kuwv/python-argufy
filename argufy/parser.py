# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Argufier is an inspection based CLI parser.'''

import inspect
import sys
from argparse import ArgumentParser
from types import ModuleType
from typing import Any, Callable, Optional, Sequence, Type, TypeVar

# from argparse_color_formatter import ColorHelpFormatter, ColorTextWrapper
from docstring_parser import parse

from .argument import Argument

# Define function as parameters for MyPy
F = TypeVar('F', bound=Callable[..., Any])

__exclude_prefixes__ = ('@', '_')


class Parser(ArgumentParser):
    '''Provide CLI parser for function.'''

    def __init__(self, *args: str, **kwargs: str) -> None:
        '''Initialize parser.

        Parameters
        ----------
        prog: str
            The name of the program
        usage: str
            The string describing the program usage
        description: str
            Text to display before the argument help
        epilog: str
            Text to display after the argument help
        parents: list
            A list of ArgumentParser objects whose arguments should also
            be included
        formatter_class: Object
            A class for customizing the help output
        prefix_chars: char
            The set of characters that prefix optional arguments
        fromfile_prefix_chars: None
            The set of characters that prefix files from which additional
            arguments should be read
        argument_default: None
            The global default value for arguments
        conflict_handler: Object
            The strategy for resolving conflicting optionals
        add_help: str
            Add a -h/--help option to the parser
       allow_abbrev: bool
            Allows long options to be abbreviated if the abbreviation is
            unambiguous

        '''
        if 'version' in kwargs:
            self.version = kwargs.pop('version')

        module = None
        stack = inspect.stack()
        stack_frame = stack[1]

        # TODO: subparsers should have the same capability later
        if stack_frame.function != 'add_parser':
            module = inspect.getmodule(stack_frame[0])
            docstring = parse(module.__doc__)
            if not kwargs.get('description'):
                kwargs['description'] = docstring.short_description

        super().__init__(**kwargs)  # type: ignore
        if not hasattr(self, 'subcommands'):
            self._subcommands = {}

        if module:
            self.add_parser_arguments(module, docstring)

    def add_parser_arguments(self, module: Any, docstring):
        parameters = {}
        for name, value in inspect.getmembers(module):
            if not name.startswith(__exclude_prefixes__):
                if inspect.ismodule(value):
                    continue
                elif inspect.isclass(value):
                    continue
                elif inspect.isfunction(value):
                    continue
                elif isinstance(value, (float, int, str, list, dict, tuple)):
                    parameters['default'] = getattr(module, name)
                    description = next(
                        (
                            d.description
                            for d in docstring.params
                            if d.arg_name == name
                        ),
                        None,
                    )
                    # print(name, parameters, description)
                    # argument = Argument(parameters, description)
                    self.add_argument('--' + name, help=description)

    def add_arguments(
        self, obj: Any, parser: Optional[Type[ArgumentParser]] = None
    ) -> None:
        '''Add arguments to parser/subparser.'''
        if not parser:
            parser = self  # type: ignore
        docstring = parse(obj.__doc__)
        signature = inspect.signature(obj)
        for arg in signature.parameters:
            description = next(
                (d for d in docstring.params if d.arg_name == arg), None
            )
            argument = Argument(
                signature.parameters[arg], description  # type: ignore
            )
            # print('sig:', signature.parameters[arg])
            name = argument.attributes.pop('name')
            parser.add_argument(*name, **argument.attributes)  # type: ignore
        return self

    def __add_commands(
        self,
         module: ModuleType,
         parser: ArgumentParser,
         exclude_prefix: list = ['@', '_']
    ) -> None:
        '''Add command.'''
        if inspect.isclass(module):
            inspect_type = inspect.ismodule
        else:
            inspect_type = inspect.isfunction

        for name, fn in inspect.getmembers(module, inspect_type):
            if module.__name__ == fn.__module__ and not name.startswith(
                (', '.join(exclude_prefix))
            ):
                command = parser.add_parser(
                    name, help=parse(fn.__doc__).short_description
                )
                command.set_defaults(fn=fn)
                self.add_arguments(fn, command)  # type: ignore

    def add_commands(
        self, module: ModuleType, exclude_prefix: list = ['@', '_']
    ) -> None:
        '''Add subparsers.'''
        commands = self.add_subparsers()
        self.__add_commands(module, commands, exclude_prefix)
        # print(self._commands)
        return self

    def add_subcommands(
        self, module: ModuleType, exclude_prefix: list = ['@', '_']
    ) -> None:
        '''Add subparsers.'''
        # print(module)
        self._subcommands[module.__name__] = Parser()
        subcommands = self._subcommands[module.__name__].add_subparsers()
        self.__add_commands(module, subcommands, exclude_prefix)
        return self

    def __set_module_arguments(self, obj, ns):
        '''Separe module arguments from functions.'''
        args = []
        signature = inspect.signature(obj)
        # Separate namespace from other variables
        args = [
            vars(ns).pop(k)
            for k in list(vars(ns).keys()).copy()
            if not signature.parameters.get(k)
        ]
        # print('set_vars:', args)
        return ns

    def retrieve(
        self, args: Sequence[str] = None, ns: Optional[str] = None,
    ) -> Callable[[F], F]:
        '''Retrieve values from CLI call.'''
        if sys.argv[1:] == [] and args is None:
            args = ['--help']
        main_ns, main_args = self.parse_known_args(args, ns)
        print(main_ns, main_args)
        if main_args == []:
            namespace = main_ns
            arguments = main_args
        else:
            sub_ns, sub_args = self._subcommands[
                'example.example'
            ].parse_known_args(main_args)
            namespace = sub_ns
            arguments = sub_args
        fn = vars(namespace).pop('fn')
        namespace = self.__set_module_arguments(fn, namespace)
        return fn, arguments, namespace

    def dispatch(
        self, args: Sequence[str] = None, ns: Optional[str] = None,
    ) -> Callable[[F], F]:
        '''Call command with arguments.'''
        fn, arguments, namespace = self.retrieve(args, ns)
        return fn(**vars(namespace))
