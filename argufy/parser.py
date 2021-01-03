# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Argufy is an inspection based CLI parser.'''

import inspect
import logging
import sys
from argparse import ArgumentParser, Namespace, _SubParsersAction
from inspect import _ParameterKind
from types import ModuleType
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
)

from docstring_parser import parse

from .argument import Argument
from .formatter import ArgufyHelpFormatter

log = logging.getLogger(__name__)

# Define function as parameters for MyPy
F = TypeVar('F', bound=Callable[..., Any])


class Parser(ArgumentParser):
    '''Provide CLI parser for function.'''

    exclude_prefixes = ('@', '_')

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
        # TODO: handle environment variables

        module = self.__get_parent_module()
        if module:
            docstring = parse(module.__doc__)
            if not kwargs.get('description'):
                kwargs['description'] = docstring.short_description

        if module and 'prog' not in kwargs:
            kwargs['prog'] = module.__name__.split('.')[0]

        # if 'prefix' in kwargs:
        #     self.prefix = kwargs.pop('prefix')
        # else:
        #     self.prefix = kwargs['prog'].upper()
        # print(self.prefix)

        if 'formatter_class' not in kwargs:
            self.formatter_class = ArgufyHelpFormatter

        if 'log_level' in kwargs:
            log.setLevel(getattr(logging, kwargs.pop('log_level').upper()))

        if 'version' in kwargs:
            self.prog_version = kwargs.pop('version')

        self.command_type = kwargs.pop('command_type', None)

        super().__init__(**kwargs)  # type: ignore
        # if not hasattr(self, '_commands'):
        #     self._commands = None

        # TODO: move to formatter
        self._positionals.title = ArgufyHelpFormatter.font(
            self._positionals.title or 'arguments'
        )
        self._optionals.title = ArgufyHelpFormatter.font(
            self._optionals.title or 'flags'
        )

        if hasattr(self, 'prog_version'):
            self.add_argument(
                '--version',
                action='version',
                version=f"%(prog)s {self.prog_version}",
                help='display package version'
            )

    @staticmethod
    def __get_parent_module() -> Optional[ModuleType]:
        '''Get parent name importing this module.'''
        stack = inspect.stack()
        # TODO: need way to better identify calling module
        stack_frame = stack[2]
        result = inspect.getmodule(stack_frame[0]) or None
        return result

    @staticmethod
    def __get_args(argument: Argument) -> Dict[Any, Any]:
        '''Retrieve arguments from argument.'''
        return {
            k[len('_Argument__') :]: v  # noqa
            for k, v in vars(argument).items()
            if k.startswith('_Argument__')
        }

    def __get_excludes(
        self, exclude_prefixes: tuple = tuple()
    ) -> tuple:
        if exclude_prefixes != []:
            return (
                tuple(exclude_prefixes) +
                Parser.exclude_prefixes
            )
        else:
            return Parser.exclude_prefixes

    def add_arguments(
        self, obj: Any, parser: Optional[ArgumentParser] = None
    ) -> 'Parser':
        '''Add arguments to parser/subparser.'''
        if not parser:
            parser = self
        docstring = parse(obj.__doc__)
        signature = inspect.signature(obj)
        for arg in signature.parameters:
            description = next(
                (d for d in docstring.params if d.arg_name == arg),
                None,
            )
            argument = Argument(signature.parameters[arg], description)
            arguments = self.__get_args(argument)
            log.warning('arguments', arguments)
            name = arguments.pop('name')
            parser.add_argument(*name, **arguments)
        return self

    def add_commands(
        self,
        module: ModuleType,
        parser: Optional[ArgumentParser] = None,
        exclude_prefixes: tuple = tuple(),
        command_type: Optional[str] = None,
    ) -> 'Parser':
        '''Add commands.'''
        module_name = module.__name__.split('.')[-1]
        docstring = parse(module.__doc__)
        if not parser:
            parser = self
        if not any(isinstance(x, _SubParsersAction) for x in parser._actions):
            parser.add_subparsers(dest=module_name, parser_class=Parser)
        command = next(
            (x for x in parser._actions if isinstance(x, _SubParsersAction)),
            None,
        )

        excludes = self.__get_excludes(exclude_prefixes)
        if command_type is None:
            command_type = self.command_type

        for name, value in inspect.getmembers(module):
            # TODO: Possible singledispatch candidate
            if not name.startswith(excludes):
                if inspect.isclass(value):
                    continue  # pragma: no cover
                elif inspect.isfunction(value):  # or inspect.ismethod(value):
                    # TODO: Turn argumentless function into switch
                    if (
                        module.__name__ == value.__module__
                        and not name.startswith(
                            (', '.join(excludes))
                        )
                    ):
                        if command:
                            if command_type == 'chain':
                                cmd_name = module_name + '.' + name
                            else:
                                cmd_name = name
                            msg = parse(value.__doc__).short_description
                            cmd = command.add_parser(
                                cmd_name.replace('_', '-'),
                                description=msg,
                                formatter_class=ArgufyHelpFormatter,
                                help=msg,
                            )
                            cmd.set_defaults(fn=value)
                            parser.formatter_class = ArgufyHelpFormatter
                        # print('command', name, value, cmd)
                        log.debug(f"command {name} {value} {cmd}")
                        self.add_arguments(value, cmd)
                elif isinstance(value, (float, int, str, list, dict, tuple)):
                    # TODO: Reconcile inspect parameters with dict
                    parameters = inspect.Parameter(
                        name,
                        _ParameterKind.POSITIONAL_OR_KEYWORD,  # type: ignore
                        default=getattr(module, name),
                        annotation=inspect._empty,  # type: ignore
                    )
                    description = next(
                        (d for d in docstring.params if d.arg_name == name),
                        None,
                    )
                    argument = Argument(parameters, description)
                    arguments = self.__get_args(argument)
                    name = arguments.pop('name')
                    parser.add_argument(*name, **arguments)
        return self

    def add_subcommands(
        self,
        module: ModuleType,
        parser: Optional[ArgumentParser] = None,
        exclude_prefixes: tuple = tuple(),
    ) -> 'Parser':
        '''Add subcommands.'''
        module_name = module.__name__.split('.')[-1]
        docstring = parse(module.__doc__)

        if not parser:
            parser = self
        if not any(isinstance(x, _SubParsersAction) for x in parser._actions):
            parser.add_subparsers(dest=module_name, parser_class=Parser)
        command = next(
            (x for x in parser._actions if isinstance(x, _SubParsersAction)),
            None,
        )

        excludes = self.__get_excludes(exclude_prefixes)

        if command:
            msg = docstring.short_description
            subcommand = command.add_parser(
                module_name.replace('_', '-'),
                description=msg,
                formatter_class=ArgufyHelpFormatter,
                help=msg,
            )
            subcommand.set_defaults(mod=module)
            parser.formatter_class = ArgufyHelpFormatter
        self.add_commands(
            module=module, parser=subcommand, exclude_prefixes=excludes
        )
        return self

    def __set_module_arguments(
        self, fn: Callable[[F], F], ns: Namespace
    ) -> Namespace:
        '''Separe module arguments from functions.'''
        if 'mod' in ns:
            mod = vars(ns).pop('mod')
        else:
            mod = None
        signature = inspect.signature(fn)
        # Separate namespace from other variables
        args = [
            {k: vars(ns).pop(k)}
            for k in list(vars(ns).keys()).copy()
            if not signature.parameters.get(k)
        ]
        if mod:
            for arg in args:
                for k, v in arg.items():
                    mod.__dict__[k] = v
        return ns

    def retrieve(
        self,
        args: Sequence[str] = sys.argv[1:],
        ns: Optional[Namespace] = None,
    ) -> Tuple[List[str], Namespace]:
        '''Retrieve values from CLI.'''
        # TODO: handle invalid argument
        if args == []:
            args = ['--help']  # pragma: no cover
        main_ns, main_args = self.parse_known_args(args, ns)
        if main_args == [] and 'fn' in vars(main_ns):
            return main_args, main_ns
        else:
            # NOTE: default to help message for subcommand
            if 'mod' in vars(main_ns):
                a = []
                a.append(vars(main_ns)['mod'].__name__.split('.')[-1])
                a.append('--help')
                self.parse_args(a)
            return main_args, main_ns

    def dispatch(
        self,
        args: Sequence[str] = sys.argv[1:],
        ns: Optional[Namespace] = None,
    ) -> Optional[Callable[[F], F]]:
        '''Call command with arguments.'''
        # TODO: support command chaining at same level
        arguments, namespace = self.retrieve(args, ns)
        if 'fn' in namespace:
            fn = vars(namespace).pop('fn')
            namespace = self.__set_module_arguments(fn, namespace)
            return fn(**vars(namespace))
        return None
