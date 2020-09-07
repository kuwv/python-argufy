# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Argufy is an inspection based CLI parser.'''

import inspect
import sys
from argparse import ArgumentParser, Namespace
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

        module = self.__get_parent_module()
        if module:
            docstring = parse(module.__doc__)
            if not kwargs.get('description'):
                kwargs['description'] = docstring.short_description

        super().__init__(**kwargs)  # type: ignore
        if not hasattr(self, 'subcommands'):
            self._subcommands = {}

        if module:
           self.__update_parser(module)

    def __update_parser(
        self,
        obj: Any,
        parser: Optional[Type[ArgumentParser]] = None,
        exclude_prefix: list = ['@', '_'],
    ):
        '''Add arguments to parser/subparser.'''
        if not parser:
            parser = self  # type: ignore
        docstring = parse(obj.__doc__)
        for name, value in inspect.getmembers(obj):
            # TODO: Possible singledispatch candidate
            if not name.startswith(__exclude_prefixes__):
                if inspect.ismodule(value):
                    # print('module', value.__name__)
                    continue
                elif inspect.isclass(value):
                    # print('class:', value.__name__)
                    continue
                elif inspect.isfunction(value) or inspect.ismethod(value):
                    # print('function:', value.__name__)
                    self.__add_command(
                        name, value, obj, parser, exclude_prefix
                    )
                elif isinstance(value, (float, int, str, list, dict, tuple)):
                    '''Add module arguments.'''
                    # TODO: Turn module attributes to inspect.parameters
                    print('attribute:', name, value)
                    self.__add_module_arguments(
                        name, value, obj, parser, docstring, exclude_prefix
                    )

    def __add_command_arguments(
        self, obj: Any, parser: Optional[Type[ArgumentParser]] = None
    ) -> None:
        '''Add arguments to parser/subparser.'''
        if not parser:
            parser = self  # type: ignore
        docstring = parse(obj.__doc__)
        signature = inspect.signature(obj)
        for name in signature.parameters:
            description = next(
                (d for d in docstring.params if d.arg_name == name), None
            )
            argument = Argument(
                signature.parameters[name], description  # type: ignore
            )
            # print('sig:', signature.parameters[name])
            name = argument.attributes.pop('name')
            parser.add_argument(*name, **argument.attributes)  # type: ignore
        return self

    def __add_command(
        self,
        name,
        value,
        obj: Any,
        parser: Optional[Type[ArgumentParser]] = None,
        exclude_prefix: list = ['@', '_'],
    ):
        '''Add command.'''
        if (
            obj.__name__ == value.__module__
            and not name.startswith(
                (', '.join(__exclude_prefixes__))
            )
        ):
            command = parser.add_parser(
                name.replace('_', '-'),
                help=parse(value.__doc__).short_description,
            )
            command.set_defaults(fn=value)
            self.__add_command_arguments(value, command)  # type: ignore

    def add_commands(
        self, module: ModuleType, exclude_prefix: list = ['@', '_']
    ) -> None:
        '''Add commands.'''
        commands = self.add_subparsers()
        self.__update_parser(module, commands, exclude_prefix)
        return self

    def __add_module_arguments(
        self, name, value, obj, parser, docstring, exclude_prefix
    ):
        parameters = {}
        description = next(
            (
                d.description
                for d in docstring.params
                if d.arg_name == name
            ),
            None,
        )
        parameters['default'] = getattr(obj, name)
        # argument = Argument(parameters, description)
        self.add_argument('--' + name.replace('_', '-'), help=description)
        # print('isinstance', name, parameters, description)

    def __add_module_command(
        self,
        obj: Any,
        parser: Optional[Type[ArgumentParser]] = None,
        exclude_prefix: list = ['@', '_'],
    ):
        print('add module command')
        name = obj.__name__.split('.')[1]
        docstring = parse(obj.__doc__)
        if not name.startswith(', '.join(__exclude_prefixes__)):
            command = parser.add_parser(
                name.replace('_', '-'),
                help=docstring.short_description,
            )
            command.set_defaults(mod=obj)
            # self.__add_command_arguments(value, command)  # type: ignore

    def add_subcommands(
        self, module: ModuleType, exclude_prefix: list = ['@', '_']
    ) -> None:
        '''Add subparsers.'''
        # TODO: need to append modules as commands
        # print(module)
        commands = self.add_subparsers()
        self.__add_module_command(module, commands, exclude_prefix)

        module_name = module.__name__.split('.')[-1]
        self._subcommands[module_name] = Parser()
        self._subcommands[module_name].add_commands(module)
        # subcommands = self._subcommands[module_name].add_subparsers()
        # self.__update_parser(module, subcommands, exclude_prefix)
        return self

    # def __set_module_arguments(self, obj: Any, ns: Optional[Namespace] = None):
    #     '''Separate module arguments from functions.'''
    #     args = []
    #     signature = inspect.signature(obj)
    #     # Separate namespace from other variables
    #     args = [
    #         vars(ns).pop(k)
    #         for k in list(vars(ns).keys()).copy()
    #         if not signature.parameters.get(k)
    #     ]
    #     # print('set_vars:', args)
    #     return ns

    def __set_module_arguments(self, obj: Any, ns: Optional[Namespace] = None):
        '''Separate module arguments from functions.'''
        args = []
        for k, v in inspect.getmembers(obj):
            if not k.startswith(__exclude_prefixes__):
                if inspect.isclass(v):
                    # print('class:', v.__name__)
                    continue
                elif inspect.isfunction(v) or inspect.ismethod(v):
                    print('functions:', v.__name__)
                    signature = inspect.signature(obj)
                    # Separate namespace from other variables
                    args = [ 
                        vars(ns).pop(k)
                        for k in list(vars(ns).keys()).copy()
                        if not signature.parameters.get(k)
                    ]
                    # print('set_vars:', args)
                elif isinstance(v, (float, int, str, list, dict, tuple)):
                    args.append({k: v})
        # if inspect.ismodule(obj):
        # Separate namespace from other variables
        print('module', obj.__name__, args)
        results = [
            vars(ns).pop(k)
            for k in list(vars(ns).keys()).copy()
            if k not in args
        ]
        print('set_vars:', results)
        # for k, v in results:
        #     obj[k] = v
        return ns

    @staticmethod
    def __get_parent_module():
        module = None
        stack = inspect.stack()
        stack_frame = stack[1]

        # TODO: subparsers should have the same capability later
        if stack_frame.function != 'add_parser':
            module = inspect.getmodule(stack_frame[0])
        return module

    def retrieve(
        self, args: Sequence[str] = None,
        ns: Optional[Namespace] = None,
        parser: Optional[Type[ArgumentParser]] = None
    ):
        main_ns, main_args = self.parse_known_args(args, ns)
        print('parsed:', main_ns, main_args)
        if main_args == []:
            namespace = main_ns
            arguments = main_args
        else:
            # TODO: implement iterator for CLI paths
            sub_ns, sub_args = self._subcommands[
                vars(main_ns)['fn'].__module__.split('.')[-1]
            ].parse_known_args(main_args)
            namespace = sub_ns
            arguments = sub_args
        print('parsed:', namespace, arguments)
        return arguments, namespace

    def dispatch(
        self, args: Sequence[str] = None, ns: Optional[Namespace] = None,
    ) -> Callable[[F], F]:
        '''Call command with arguments.'''
        if sys.argv[1:] == [] and args is None:
            args = ['--help']
        arguments, namespace = self.retrieve(args, ns)
        if 'fn' in namespace:
            obj = vars(namespace).pop('fn')
        elif 'mod' in namespace:
            obj = vars(namespace).pop('mod')
        ### testing
        if inspect.isfunction(obj) or inspect.ismethod(obj):
            print(obj.__module__)
        ###
        namespace = self.__set_module_arguments(obj, namespace)
        return obj(**vars(namespace))
