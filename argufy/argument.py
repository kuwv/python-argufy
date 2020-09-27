# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Arguments for inspection based CLI parser.'''

import inspect
from typing import Any, Dict, List, Type

from docstring_parser.common import DocstringParam

types = ('float', 'int', 'str', 'list', 'dict', 'tuple', 'set')


class Argument:
    '''Represent argparse arguments.'''

    def __init__(
        self,
        parameters: Type[inspect.Parameter],
        docstring: Type[DocstringParam],
    ) -> None:
        '''Initialize argparse argument.'''
        self.attributes: Dict[Any, Any] = {}

        self.default = parameters.default
        self.name = parameters.name.replace('_', '-')  # type: ignore

        annotation = None
        if parameters.annotation != inspect._empty:  # type: ignore
            annotation = parameters.annotation
            self.type = annotation
        if docstring and docstring.type_name:
            # print(docstring.type_name)
            if ',' in docstring.type_name:
                args = docstring.type_name.split(',', 1)
                if not annotation:
                    a = args.pop(0)
                    if a in types:
                        # NOTE: Limit input that eval will parse
                        annotation = eval(a)  # nosec
                        self.type = annotation
            if not annotation:
                # NOTE: Limit input that eval will parse
                if docstring.type_name in types:
                    annotation = eval(docstring.type_name)  # nosec

        # if docstring:
        #     print('docstring:', docstring.__dict__)

        if annotation:
            print('metavar annotation:', annotation)
            self.metavar = (annotation.__name__).upper()

        if docstring:
            self.help = docstring.description

    @property
    def name(self) -> List[str]:
        '''Get argparse command/argument name.'''
        return self.__name

    @name.setter
    def name(self, name: str) -> None:
        '''Set argparse command/argument name.'''
        if 'default' not in self.attributes:
            self.attributes['name'] = [name]
            self.__name = [name]
            self.__positional_argument = True
        else:
            names = ['--' + name]
            # TODO: Need to check other conflicting variables
            # if '-' not in name:
            #     # TODO: check against default names
            #     names.append('-' + name[:1])
            self.attributes['name'] = names
            self.__name = names
            self.__positional_argument = False

    @property
    def metavar(self) -> str:
        '''Get argparse argument metavar.'''
        return self.__metavar

    @metavar.setter
    def metavar(self, metavar: str) -> None:
        '''Set argparse argument metavar.'''
        # if self.attributes.get('type', None) != bool:
        print(self.__positional_argument)
        if self.__positional_argument:
            self.attributes['metavar'] = metavar
            self.__metavar = metavar
            print('metavar:', self.__metavar)

    @property
    def type(self) -> Any:
        '''Get argparse argument type.'''
        return self.__type

    @type.setter
    def type(self, annotation: Any) -> None:
        '''Set argparse argument type.'''
        # print('prematched annotation:', annotation)
        if annotation == bool:
            # NOTE: these store bool type internally
            if self.attributes.get('default'):
                self.action = 'store_false'
            else:
                self.action = 'store_true'
        elif annotation == int:
            self.attributes['type'] = annotation
            self.__type = annotation
            self.action = 'append'
        elif annotation == list:
            self.attributes['type'] = annotation
            self.__type = annotation
            self.nargs = '+'
        elif annotation == tuple:
            self.attributes['type'] = annotation
            self.__type = annotation
        elif annotation == set:
            self.attributes['type'] = annotation
            self.__type = annotation
        else:
            # print('unmatched annotation:', annotation)
            self.attributes['type'] = annotation
            self.__type = annotation

    @property
    def const(self) -> str:
        '''Get argparse argument const.'''
        return self.__const

    @const.setter
    def const(self, const: str) -> None:
        '''Set argparse argument const.'''
        self.attributes['const'] = const
        self.__const = const

    @property
    def dest(self) -> str:
        '''Get argparse command/argument dest.'''
        return self.__dest

    @dest.setter
    def dest(self, dest: str) -> None:
        '''Set argparse command/argument dest.'''
        self.attributes['dest'] = dest
        self.__dest = dest

    @property
    def required(self) -> bool:
        '''Get argparse required argument.'''
        return self.__required

    @required.setter
    def required(self, required: bool) -> None:
        '''Set argparse required argument.'''
        self.attributes['required'] = required
        self.__required = required

    @property
    def action(self) -> str:
        '''Get argparse argument action.'''
        return self.__action

    @action.setter
    def action(self, action: str) -> None:
        '''Set argparse argument action.'''
        self.attributes['action'] = action
        self.__action = action

    @property
    def choices(self) -> str:
        '''Get argparse argument choices.'''
        return self.__choices

    @choices.setter
    def choices(self, choices: str) -> None:
        '''Set argparse argument choices.'''
        self.attributes['choices'] = choices
        self.__choices = choices

    @property
    def nargs(self) -> str:
        '''Get argparse argument nargs.'''
        return self.__nargs

    @nargs.setter
    def nargs(self, nargs: str) -> None:
        '''Set argparse argument nargs.'''
        self.attributes['nargs'] = nargs
        self.__nargs = nargs

    @property
    def default(self) -> Any:
        '''Get argparse argument default.'''
        return self.__default

    @default.setter
    def default(self, default: Any) -> None:
        '''Set argparse argument default.'''
        if default != inspect._empty:  # type: ignore
            self.attributes['default'] = default
            self.__default = default
        else:
            self.__default = None

    @property
    def help(self) -> str:
        '''Get argparse command/argument help message.'''
        return self.__help

    @help.setter
    def help(self, description: str) -> None:
        '''Set argparse command/argument help message.'''
        self.attributes['help'] = description
        self.__help = description
