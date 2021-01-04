# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Arguments for inspection based CLI parser.'''

import inspect
import re
import typing
from ast import literal_eval
from typing import Any, List, Union

from docstring_parser.common import DocstringParam

types = {'bool', 'dict', 'float', 'int', 'list', 'str', 'set', 'tuple'}


class Argument:
    '''Represent argparse arguments.'''

    __short_flags: List[str] = ['-h']

    def __init__(
        self, parameters: inspect.Parameter, docstring: DocstringParam,
    ) -> None:
        '''Initialize argparse argument.'''
        # self.attributes: Dict[Any, Any] = {}

        self.default = parameters.default
        self.name = parameters.name.replace('_', '-')  # type: ignore

        if parameters.annotation != inspect._empty:  # type: ignore
            if typing.get_origin(parameters.annotation) is Union:
                annotation = typing.get_args(parameters.annotation)
                for x in annotation:
                    if x is None:
                        self.nargs = '?'
                    else:
                        self.type = x
            else:
                self.type = parameters.annotation
        elif docstring and docstring.type_name:
            if ',' in docstring.type_name:
                for arg in docstring.type_name.split(',', 1):
                    if not hasattr(self, 'type'):
                        # NOTE: Limit input that eval will parse
                        if arg in types:
                            self.type = (
                                literal_eval(arg) if arg != 'str' else str
                            )
                    if arg.lower() == 'optional' and not hasattr(
                        self, 'default'
                    ):
                        self.default = None
                    if re.search(r'^\s*\{.*\}\s*$', arg):
                        self.choices = literal_eval(arg.strip())
            if not hasattr(self, 'type'):
                # NOTE: Limit input that eval will parse
                if docstring.type_name in types:
                    self.type = eval(docstring.type_name)  # nosec
        elif self.default is not None:
            self.type = type(self.default)

        # if hasattr(self, 'type'):
        #     self.metavar = (self.type.__name__)

        if docstring:
            self.help = docstring.description

    @property
    def name(self) -> List[str]:
        '''Get argparse command/argument name.'''
        return self.__name

    @name.setter
    def name(self, name: str) -> None:
        '''Set argparse command/argument name.'''
        if not hasattr(self, 'default'):
            self.__name = [name]
        else:
            flags = ['--' + name]
            # NOTE: check for conflicting flags
            if '-' not in name:
                # TODO: check if common short flag (ex: version)
                n = name[:1]
                if n not in Argument.__short_flags:
                    Argument.__short_flags.append(n)
                    flags.append('-' + n)
                elif n.upper() not in Argument.__short_flags:
                    Argument.__short_flags.append(n.upper())
                    flags.append('-' + n.upper())
            self.__name = flags

    @property
    def metavar(self) -> str:
        '''Get argparse argument metavar.'''
        return self.__metavar

    @metavar.setter
    def metavar(self, metavar: str) -> None:
        '''Set argparse argument metavar.'''
        # NOTE: Only positional arguments use metavars
        if not hasattr(self, 'default'):
            self.__metavar = metavar

    @property
    def type(self) -> Any:
        '''Get argparse argument type.'''
        return self.__type  # type: ignore

    @type.setter
    def type(self, annotation: Any) -> None:
        '''Set argparse argument type.'''
        # print('prematched annotation:', annotation)
        if annotation == bool:
            # NOTE: these store bool type internally
            if self.default or not hasattr(self, 'default'):
                self.action = 'store_false'
            else:
                self.action = 'store_true'
        elif annotation == int:
            self.__type = annotation
            self.action = 'append'
        elif annotation == list:
            self.__type = annotation
            self.nargs = '*'
        elif annotation == tuple:
            self.__type = annotation
            self.nargs = '+'
        elif annotation == set:
            self.__type = annotation
            self.nargs = '+'
        else:
            # print('unmatched annotation:', annotation)
            self.__type = annotation
            # self.nargs = 1

    # @property
    # def const(self) -> str:
    #     '''Get argparse argument const.'''
    #     return self.__const

    # @const.setter
    # def const(self, const: str) -> None:
    #     '''Set argparse argument const.'''
    #     self.__const = const

    # @property
    # def dest(self) -> str:
    #     '''Get argparse command/argument dest.'''
    #     return self.__dest

    # @dest.setter
    # def dest(self, dest: str) -> None:
    #     '''Set argparse command/argument dest.'''
    #     self.__dest = dest

    # @property
    # def required(self) -> bool:
    #     '''Get argparse required argument.'''
    #     return self.__required

    # @required.setter
    # def required(self, required: bool) -> None:
    #     '''Set argparse required argument.'''
    #     self.__required = required

    @property
    def action(self) -> str:
        '''Get argparse argument action.'''
        return self.__action

    @action.setter
    def action(self, action: str) -> None:
        '''Set argparse argument action.'''
        self.__action = action

    @property
    def choices(self) -> List[str]:
        '''Get argparse argument choices.'''
        return self.__choices

    @choices.setter
    def choices(self, choices: set) -> None:
        '''Set argparse argument choices.'''
        self.__choices = list(choices)

    @property
    def nargs(self) -> Union[int, str]:
        '''Get argparse argument nargs.'''
        return self.__nargs

    @nargs.setter
    def nargs(self, nargs: Union[int, str]) -> None:
        '''Set argparse argument nargs.'''
        # TODO: map nargs to argparse with typing
        # 1: set number of values
        # ?: a single optional value
        # *: a flexible list of values
        # +: like * requiring at least one value
        # REMAINDER: unused args
        self.__nargs = nargs

    @property
    def default(self) -> Any:
        '''Get argparse argument default.'''
        return self.__default

    @default.setter
    def default(self, default: Any) -> None:
        '''Set argparse argument default.'''
        if default != inspect._empty:  # type: ignore
            self.__default = default
        # else:
        #     self.__default = None

    @property
    def help(self) -> str:
        '''Get argparse command/argument help message.'''
        return self.__help

    @help.setter
    def help(self, description: str) -> None:
        '''Set argparse command/argument help message.'''
        self.__help = description
