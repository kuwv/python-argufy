# Welcome to Argufy

Argufy is a command line interface (CLI) written in Python.

## Overview

## Motivation

Argufy was created because there wasn't a parser that built on what I believed are
some real strenths of Python. Inspection is a really powerfull tool and I wanted
a CLI that would be updated with minimal effort. Argufy does this by building
CLI's from the functions directly. It then parses docstrings to fill in any
additional content to create a parser.

In short, the more code-complete your application is the more complete the CLI.

## Features

- [x] Dispatch commands arguments to requests functions.
- [x] Generate commands from functions within modules
    - [x] Docstrings
        - [x] Arguments
        - [x] Defaults
        - [x] Help
        - [x] Types
    - [x] Type Hints
        - [x] Arguments
        - [x] Defaults
        - [x] Help
        - [x] Types

- [x] Generate subcommands / arguments from modules
    - [ ] Set module arguments
    - [ ] Docstrings
        - [x] Arguments
        - [ ] Defaults
        - [x] Help
        - [ ] Types
    - [ ] Type Hints
        - [ ] Arguments
        - [x] Defaults
        - [ ] Help (N/A)
        - [ ] Types

- [ ] Generate subcommands / arguments from objects
    - [ ] Set instance arguments
    - [ ] Docstrings
        - [ ] Arguments
        - [ ] Defaults
        - [ ] Help
        - [ ] Types
    - [ ] Type Hints
        - [ ] Arguments
        - [ ] Defaults
        - [ ] Help (N/A)
        - [ ] Types

## Alternatives

There are multiple alternatives such as Click and Docpopt. These are
great options but each have their own trade-offs.

=== "Argparse"
    Argparse is a great parser with many built-in features. But, it is an
    additional layer of complexity that needs to be managed when
    developing with it. 

=== "Click"
    Click is a great alternative and is widely used. It is also part of
    the Pallets Projects suite of tools. Click is a decorator based CLI
    parser. Decorators are easy and convenient but prevent inspection
    from being used without a performance and capability hit. It also
    requires that your code be wrapped with the decorators. This is
    less usefull when needing the tools to function also as a library.

=== "Dockopt"
    Docopt is another great option for CLI parsers and is similar in
    scope to Argufy. It works by parsing docstrings directly in the 
    main module of an applications. A CLI is created by adding the 
    syntax directly into docstrings. Updates to an application still 
    requires that the CLI also be updated independently.
