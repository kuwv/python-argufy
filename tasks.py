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

'''Test Task-Runner.'''
from invoke import call, task

from argufy.__version__ import __version__

if 'dev' in __version__ or 'rc' in __version__:
    part = 'build'
else:
    part = 'patch'


@task
def format(ctx, check=True):  # type: ignore
    '''Format project source code to PEP-8 standard.

    :param check: bool, optional
        Check project source code without modification

    '''
    args = ['--skip-string-normalization']
    if check:
        args.append('--check')
    ctx.run('isort --atomic **/*.py')
    ctx.run("black **/*.py {}".format(' '.join(args)))


@task
def doc_lint(ctx):
    '''Check code for documentation errors.'''
    ctx.run('pydocstyle')


@task(post=[doc_lint])
def lint(ctx):  # type: ignore
    '''Check project source code for linting errors.'''
    ctx.run('flake8')


@task
def type_check(ctx, path='.'):  # type: ignore
    '''Check project source types.

    :param path: str, optional
        Include the path to check for type-hints

    '''
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
    ctx.run('safety check')
    ctx.run('bandit -r argufy')


@task
def doc_coverage(ctx):
    '''Ensure all code is documented.'''
    ctx.run('docstr-coverage **/*.py')


@task(post=[doc_coverage])
def coverage(ctx, report=None):  # type: ignore
    '''Perform coverage checks for tests.'''
    args = ['--cov=argufy']
    if report:
        args.append('--cov-report={}'.format(report))
    ctx.run("pytest {} ./tests/".format(' '.join(args)))


@task(pre=[doc_lint], post=[doc_coverage])
def doc_test(ctx):
    '''Test documentation build.'''
    ctx.run('mkdocs build')


@task(pre=[format, lint, unit_test, static_analysis, coverage])
def test(ctx):  # type: ignore
    '''Run all tests.'''
    pass


@task
def doc_build(ctx):
    '''Build documentation site.'''
    ctx.run('mkdocs build')


@task(post=[doc_build])
def build(ctx, format=None):  # type: ignore
    '''Build wheel package.'''
    if format:
        ctx.run("flit build --format={}".format(format))
    else:
        ctx.run('flit build')


@task(pre=[call(build, format='wheel')])
def dev(ctx):  # type: ignore
    '''Perform development runtime environment setup.'''
    ctx.run('flit install --symlink --python python3')


@task
def install(ctx, symlink=True):  # type: ignore
    '''Install in development environment.'''
    ctx.run('flit install -s')


@task
def version(  # type: ignore
    ctx, part=part, tag=False, commit=False, message=None
):
    '''Update project version and apply tags.

    :param tag: bool, optional
        Apply tag to branch using version

    :param commit: bool, optional
        Commit version to branch

    :param message: str, optional
        Add commit message with annotated tag
    '''
    args = [part]
    if tag:
        args.append('--tag')
    if commit:
        args.append('--commit')
    else:
        args.append('--dry-run')
        args.append('--allow-dirty')
        args.append('--verbose')
        print('Add "--commit" to actually bump the version.')
    if message:
        args.append("--tag-message '{}'".format(message))
    ctx.run("bumpversion {}".format(' '.join(args)))


@task
def doc_lint(ctx):
    '''Check code for documentation errors.'''
    ctx.run('pydocstyle')


@task
def doc_publish(ctx):
    '''Publish project documentation.'''
    ctx.run('mkdocs gh-deploy')


@task(post=[doc_publish])
def publish(ctx):  # type: ignore
    '''Publish project distribution.'''
    ctx.run('flit publish')


@task
def clean(ctx):  # type: ignore
    '''Clean project dependencies and build.'''
    paths = ['dist', 'logs']
    paths.append('**/__pycache__')
    paths.append('**/*.pyc')
    paths.append('argufy.egg-info')
    for path in paths:
        ctx.run("rm -rf {}".format(path))
