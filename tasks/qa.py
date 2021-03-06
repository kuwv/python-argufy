# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Test Task-Runner.'''

from invoke import task


@task
def autoformat(ctx, check=True):  # type: ignore
    '''Format project source code to PEP-8 standard.'''
    args = ['--skip-string-normalization']
    if check:
        args.append('--check')
    ctx.run('isort --atomic **/*.py')
    ctx.run("black **/*.py {}".format(' '.join(args)))


@task
def lint(ctx):  # type: ignore
    '''Check project source code for linting errors.'''
    ctx.run('flake8')


@task
def type_check(ctx, path='.'):  # type: ignore
    '''Check project source types.'''
    ctx.run("mypy {}".format(path))


@task
def unit_test(ctx, capture=None):  # type: ignore
    '''Perform unit tests.'''
    args = []
    if capture:
        args.append('--capture=' + capture)
    ctx.run("pytest {}".format(' '.join(args)))


@task
def static_analysis(ctx):  # type: ignore
    '''Perform static code analysis on imports.'''
    # TODO: ignore tornado vulnurability due to no update
    ctx.run('safety check --ignore=39462')
    ctx.run('bandit -r argufy')


@task
def coverage(ctx, report=None):  # type: ignore
    '''Perform coverage checks for tests.'''
    args = ['--cov=argufy']
    if report:
        args.append('--cov-report={}'.format(report))
    ctx.run("pytest {} ./tests/".format(' '.join(args)))


@task(pre=[lint, unit_test, static_analysis, coverage])
def test(ctx):  # type: ignore
    '''Run all tests.'''
    pass
