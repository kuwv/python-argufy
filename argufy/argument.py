# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Arguments for inspection based CLI parser.'''

import inspect
from typing import Any, Dict, Type

from docstring_parser.common import DocstringParam


class Argument:
    '''Represent argparse arguments.'''

    def __init__(
        self,
        parameters: Type[inspect.Parameter],
        docstring: Type[DocstringParam],
    ) -> None:
        '''Initialize argparse argument.'''
        self.__docstring = docstring
        self.attributes: Dict[Any, Any] = {}

        # Define attribute defaults
        self.nargs_type = '+'

        self.default = parameters.default
        self.name = parameters.name.replace('_', '-')
        self.__set_attributes(self.__get_annotations(parameters.annotation))
        self.metavar = (parameters.name).upper()
        if self.__docstring:
            self.help = self.__docstring.description

    def __get_annotations(self, annotation: Any) -> Any:
        '''Get parameter types for method/function.'''
        if annotation != inspect._empty:  # type: ignore
            return annotation
        elif self.__docstring and self.__docstring.type_name:
            # TODO: There has to be a cleaner way
            annotation = eval(self.__docstring.type_name)  # nosec
            return annotation
        else:
            return None

    def __set_attributes(self, annotation: Any) -> None:
        '''Define argument attributes.'''
        if type(annotation) == bool:
            # Note: these store type internally
            if self.attributes.get('default'):
                self.action = 'store_false'
            else:
                self.action = 'store_true'
        elif type(annotation) == int:
            self.type = annotation
            self.action = 'append'
        elif type(annotation) == list:
            self.type = annotation
            self.nargs = self.nargs_type
        elif type(annotation) == tuple:
            self.type = annotation[0]
            if type(annotation[1]) == set:
                self.choices = annotation[1]
        else:
            self.type = annotation

    @property
    def name(self):
        '''Get argparse command/argument name.'''
        return self.__name

    @name.setter
    def name(self, name):
        '''Set argparse command/argument name.'''
        if 'default' not in self.attributes:
            self.attributes['name'] = [name]
            self.__name = [name]
        else:
            names = ['--' + name]
            if '-' not in name:
                # TODO: check against default names
                names.append(name[:1])
            self.attributes['name'] = names
            self.__name = names

    @property
    def metavar(self):
        '''Get argparse argument metavar.'''
        return self.__metavar

    @metavar.setter
    def metavar(self, metavar):
        '''Set argparse argument metavar.'''
        if self.attributes['type'] != bool or self.__type != bool:
            self.attributes['metavar'] = metavar
            self.__metavar = metavar

    @property
    def type(self):
        '''Get argparse argument type.'''
        return self.__type

    @type.setter
    def type(self, kind):
        '''Set argparse argument type.'''
        self.attributes['type'] = kind
        self.__type = kind

    @property
    def const(self):
        '''Get argparse argument const.'''
        return self.__const

    @const.setter
    def const(self, const):
        '''Set argparse argument const.'''
        self.attributes['const'] = const
        self.__const = const

    @property
    def dest(self):
        '''Get argparse command/argument dest.'''
        return self.__dest

    @dest.setter
    def dest(self, dest):
        '''Set argparse command/argument dest.'''
        self.attributes['dest'] = dest
        self.__dest = dest

    @property
    def required(self):
        '''Get argparse required argument.'''
        return self.__required

    @required.setter
    def required(self, required):
        '''Set argparse required argument.'''
        self.attributes['required'] = required
        self.__required

    @property
    def action(self):
        '''Get argparse argument action.'''
        return self.__action

    @action.setter
    def action(self, action):
        '''Set argparse argument action.'''
        self.attributes['action'] = action
        self.__action = action

    @property
    def choices(self):
        '''Get argparse argument choices.'''
        return self.__choices

    @choices.setter
    def choices(self, choices):
        '''Set argparse argument choices.'''
        self.attributes['choices'] = choices
        self.__choices = choices

    @property
    def nargs(self):
        '''Get argparse argument nargs.'''
        return self.__nargs

    @nargs.setter
    def nargs(self, nargs):
        '''Set argparse argument nargs.'''
        self.attributes['nargs'] = nargs
        self.__nargs = nargs

    @property
    def default(self):
        '''Get argparse argument default.'''
        return self.__default

    @default.setter
    def default(self, default):
        '''Set argparse argument default.'''
        if default != inspect._empty:  # type: ignore
            self.attributes['default'] = default
            self.__default = default
        else:
            self.__default = None

    @property
    def help(self):
        '''Get argparse command/argument help message.'''
        return self.__help

    @help.setter
    def help(self, description):
        '''Set argparse command/argument help message.'''
        self.attributes['help'] = description
        self.__help = description
