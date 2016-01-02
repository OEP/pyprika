from .registry import registry as GLOBAL_REGISTRY
from ..pprint import pprint_recipe
from ..exceptions import LoadError
from ..quantity import _to_number
from .. import load
from abc import ABCMeta, abstractmethod, abstractproperty
import argparse
import sys
import os
import re


def _suggest(matches, cutoff=3, conjunct=' or ', sep=', ', ellipsis='...'):
    assert len(matches) > 1
    suggestions = matches[:cutoff]
    prefix = os.path.commonprefix(suggestions)
    suggestions = [s[:len(prefix) + 1] for s in suggestions]
    if len(matches) > len(suggestions):
        return sep.join(suggestions) + ellipsis
    else:
        return sep.join(suggestions[:-1]) + conjunct + suggestions[-1]


def _fetch_unique(index, registry):
    keys = registry.select(index)
    if len(keys) > 1:
        raise CommandError('multiple matches for `%s` (did you mean %s?)' %
                           (index, _suggest(keys)))
    elif len(keys) == 0:
        raise CommandError('no matches for `%s`' % index)
    return keys[0]


class CommandError(Exception):
    def __init__(self, message, exitcode=1):
        self.message = message
        self.exitcode = exitcode
        self.args = (message, exitcode)


class Command(object):
    __metaclass__ = ABCMeta

    def __init__(self, stdout=None, stderr=None):
        self.stdout = stdout or sys.stdout
        self.stderr = stderr or sys.stderr
        self.registry = GLOBAL_REGISTRY

    @abstractproperty
    def help(self):
        raise NotImplementedError

    @abstractproperty
    def name(self):
        raise NotImplementedError

    @abstractmethod
    def execute(self, ns):
        raise NotImplementedError

    @abstractmethod
    def setup_parser(self, subparsers):
        raise NotImplementedError

    def run(self, *argv):
        '''Simulate calling this command with given sys.argv
        '''
        parser = argparse.ArgumentParser()
        self.setup_parser(parser)
        args = parser.parse_args(argv)
        self.execute(args)


class Edit(Command):
    name = 'edit'
    help = 'edit a recipe'

    DEFAULT_EDITOR = 'pico'

    def _kit_editor(self):
        cls = type(self)
        editor = None
        if editor is None:
            editor = os.getenv('KIT_EDITOR')
        if editor is None:
            editor = os.getenv('EDITOR')
        if editor is None:
            editor = cls.DEFAULT_EDITOR
        return editor

    def execute(self, ns):
        k = _fetch_unique(ns.index, self.registry)
        path = self.registry.paths[k]
        editor = self._kit_editor()
        try:
            os.execvp(editor, [editor, path])
        except OSError as e:
            raise CommandError("error launching '%s': %s"
                               % (editor, os.strerror(e.errno)))

    def setup_parser(self, parser):
        parser.add_argument('index', type=str,
                            help='index of recipe to edit')


class List(Command):
    name = 'ls'
    help = 'list all recipes'

    def execute(self, ns):
        for r in self.registry.recipes.values():
            self.stdout.write('{0} {1}\n'.format(r.index, r.name))
        return 0

    def setup_parser(self, parser):
        pass


class Search(Command):
    name = 'search'
    help = 'look up recipes by name'

    def execute(self, ns):
        flags = 0
        if ns.ignore_case:
            flags |= re.I

        recipes = [r for r in self.registry.recipes.values()
                   if re.search(ns.term, r.name, flags)]
        for r in recipes:
            self.stdout.write('{0} {1}\n'.format(r.index, r.name))
        return 0

    def setup_parser(self, parser):
        parser.add_argument('term', type=str,
                            help='what to search for in recipe')
        parser.add_argument('-i', '--ignore-case', action='store_true',
                            help='ignore text case while searching')


class Show(Command):
    name = 'show'
    help = 'show recipe contents'

    def execute(self, ns):
        key = _fetch_unique(ns.index, self.registry)
        try:
            scale = _to_number(ns.scale)
        except ValueError:
            raise CommandError("not a valid number: %s" % ns.scale)
        recipe = scale * self.registry.recipes[key]
        pprint_recipe(recipe, os=self.stdout)
        return 0

    def setup_parser(self, parser):
        parser.add_argument('--scale', '-s', type=str, default='1',
                            help='scale the recipe by a constant factor')
        parser.add_argument('index', type=str,
                            help='index (or prefix of index) of recipe to '
                                 'show')


class Validate(Command):
    name = 'validate'
    help = 'validate an input recipe'

    def execute(self, ns):
        exit_code = 0
        for f in ns.filenames:
            try:
                with open(f, 'r') as fp:
                    load(fp)
            except (LoadError, IOError) as e:
                exit_code = 1
                if len(ns.filenames) > 1:
                    self.stdout.write('{0}: {1}\n'.format(f, e))
                else:
                    self.stdout.write('{0}\n'.format(e))
        return exit_code

    def setup_parser(self, parser):
        parser.add_argument('filenames', type=str, nargs='+',
                            help='path to recipe file(s) to validate')


class Which(Command):
    name = 'which'
    help = 'print path to recipe'

    def execute(self, ns):
        k = _fetch_unique(ns.index, self.registry)
        path = self.registry.paths[k]
        self.stdout.write('{0}\n'.format(path))
        return 0

    def setup_parser(self, parser):
        parser.add_argument('index', type=str,
                            help='index of recipe to find')
