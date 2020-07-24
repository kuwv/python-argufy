'''Argufier is an inspection based CLI parser.'''
import inspect
import textwrap
from argparse import ArgumentParser

from argparse_color_formatter import ColorHelpFormatter, ColorTextWrapper
from docstring_parser import parse

from argufier import __version__

# import re
# import types


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
        if self.attributes.get('default'):
            self.attributes['action'] = 'store_false'
        else:
            self.attributes['action'] = 'store_true'

    def annotation(self, annotation):
        if annotation == list:
            self.attributes['nargs'] = '*'
        if annotation == bool:
            self.action()

    def type(self, annotation):
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
        if self.__doc:
            self.attributes['help'] = self.__doc.description


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
        ''' Check if menu dispatch exists '''
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
        print(args)
        result = self.parse_args(args, namespace)
        fn = vars(result).pop('fn')
        return fn(**vars(result))
