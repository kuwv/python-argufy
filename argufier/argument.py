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
# -*- coding: utf-8 -*-

'''Argufier is an inspection based CLI parser.'''

import inspect
import textwrap
from argparse import ArgumentParser

from argparse_color_formatter import ColorHelpFormatter, ColorTextWrapper
from docstring_parser import parse


class Argument:
    '''Represent argparse arguments.'''

    def __init__(self, parameters, docstring):
        '''Initialize argparse argument.'''
        self.attributes = {}
        default = parameters.default
        annotation = parameters.annotation

        if default == inspect._empty:
            self.attributes['name'] = [parameters.name]
        else:
            self.attributes['flags'] = ['--' + parameters.name]
            self.attributes['default'] = default

        self.__doc = docstring
        self.annotation(annotation)
        self.type(annotation)
        self.help(annotation)

    # const
    # dest
    # metavar
    # required
    # help

    def action(self, annotation=None):
        '''Define argument action.'''
        if self.attributes.get('default'):
            self.attributes['action'] = 'store_false'
        else:
            self.attributes['action'] = 'store_true'

    def annotation(self, annotation):
        '''Define argument nargs.'''
        if annotation == list:
            self.attributes['nargs'] = '*'
        if annotation == bool:
            self.action()

    def type(self, annotation):
        '''Define argument type.'''
        if annotation != inspect._empty:
            self.attributes['type'] = annotation
        elif self.__doc and self.__doc.type_name:
            type_name = eval(self.__doc.type_name)
            if type(type_name) == tuple:
                self.attributes['type'] = type_name[0]
                if type(type_name[1]) == set:
                    self.attributes['choices'] = type_name[1]
            else:
                self.attributes['type'] = type_name

    def help(self, help):
        '''Define argument helm.'''
        if self.__doc:
            self.attributes['help'] = self.__doc.description
