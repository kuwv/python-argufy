# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
'''Argufier is an inspection based CLI parser.'''
# -*- coding: utf-8 -*-

import inspect
import textwrap
from argparse import ArgumentParser

from argparse_color_formatter import ColorHelpFormatter, ColorTextWrapper
from docstring_parser import parse

from argufier import __version__
from .argument import Argument

# import re
# import types


class Parser(ArgumentParser):
    '''Provide CLI parser for function.'''

    _parser = None
    __settings = None

    def __init__(self, **kwargs):
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
            A list of ArgumentParser objects whose arguments should also be included
        formatter_class: Object
            A class for customizing the help output
        prefix_chars: char
            The set of characters that prefix optional arguments
        fromfile_prefix_chars: None
            The set of characters that prefix files from which additional arguments should be read
        argument_default: None
            The global default value for arguments
        conflict_handler: Object
            The strategy for resolving conflicting optionals
        add_help: str
            Add a -h/--help option to the parser
        allow_abbrev: bool
            Allows long options to be abbreviated if the abbreviation is unambiguous
        
        '''
        # self.__log = Logger(__name__)
        # self.__log.info("Loading command line tool settings")
        super().__init__(**kwargs)

    @staticmethod
    def message(msgs):
        '''Generate CLI menu message.'''
        usg = textwrap.dedent(
            '''\
            command [OPTIONS] [SUB-COMMAND] [ARGUMENTS]
   
            Sub-Commands to manage the setup of lunar:
            '''
        )
        for msg in msgs:
            usg += "  {c}\t{d}\n".format(c=msg['cmd'], d=msg['desc'])
        return usg

    @staticmethod
    def usage_message(instance):
        '''Generate usage message.'''
        msgs = [
            {
                'cmd': fn + ' ',
                'desc': getattr(getattr(instance, fn), '__doc__'.splitlines()[0]),
            }
            for fn in dir(instance)
            if not fn.startswith('_')
        ]
        return message(msgs)

    def check_menu(self, menu, command):
        '''Check if menu dispatch exists.'''
        if not hasattr(menu, command):
            self.__log.warning('Unrecognized command')
            self.print_help()
            exit(1)

    def add_subcommands(self, module, exclude_prefix='_'):
        '''Add subparsers.'''
        self.subparsers = self.add_subparsers()
        for name, fn in inspect.getmembers(module, inspect.isfunction):
            subparser = None
            if fn.__module__ == module.__name__ and not name.startswith(exclude_prefix):
                help = parse(fn.__doc__).short_description
                subparser = self.subparsers.add_parser(name, help=help)
                subparser.set_defaults(fn=fn)
                self.add_arguments(fn)

    def add_arguments(self, fn):
        '''Add arguments to parser/subparser.'''
        signature = inspect.signature(fn)
        docstring = parse(fn.__doc__)
        for arg in signature.parameters:
            description = next((d for d in docstring.params if d.arg_name == arg), None)
            argument = Argument(signature.parameters[arg], description)

    def dispatch(self, args=None, namespace=None):
        '''Dispatch CLI command.'''
        result = self.parse_args(args, namespace)
        fn = vars(result).pop('fn')
        return fn(**vars(result))
