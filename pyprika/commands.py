from . import load
from .pprint import pprint_recipe
from .exceptions import ParseError
from abc import ABCMeta, abstractmethod, abstractproperty
from argparse import ArgumentParser
import glob
import os
import sys
import yaml
import re

def _suggest(matches, cutoff=5, conjunct=' or ', sep=', ', ellipsis='...'):
  assert len(matches) > 1
  suggestions = matches[:cutoff]
  if len(matches) > len(suggestions):
    return sep.join(suggestions) + ellipsis
  elif len(suggestions) == 1:
    return suggestions[0]
  else:
    return sep.join(suggestions[:-1]) + conjunct + suggestions[-1]

class _Registry(object):
  def __init__(self):
    self.recipes = {}
    self.search(os.path.curdir)
    config_path = os.path.expanduser("~/.pyprika")
    if os.path.exists(config_path):
      with open(config_path) as fp:
        self.config = yaml.load(fp)
    else:
      self.config = {}
    if not isinstance(self.config, dict):
      sys.stderr.write("warning: invalid user configuration; skipping")
      self.config = {}
    paths = self.config.get('paths', [])
    recursive = self.config.get('recursive', False)
    search = self.search if not recursive else self.recursive_search
    for p in paths:
      search(p)

  def recursive_search(self, path):
    skip_hidden = self.config.get('skip_hidden', True)
    for root, dirnames, filenames in os.walk(path, topdown=True):
      if skip_hidden:
        dirnames[:] = [d for d in dirnames if not d.startswith('.')]
        filenames[:] = [f for f in filenames if not f.startswith('.')]
      filenames[:] = [f for f in filenames if f.endswith('.yaml')]
      for f in filenames:
        self.add(os.path.join(root, f))

  def search(self, path):
    files = glob.glob(os.path.join(path, '*.yaml'))
    for f in files:
      try:
        self.add(f)
      except ParseError:
        pass
    
  def add(self, path):
    recipe = load(path)
    self.recipes[recipe.name] = recipe
registry = _Registry()

class CommandError(Exception):
  def __init__(self, message, exitcode=1):
    self.message = message
    self.exitcode = exitcode
    self.args = (message, exitcode)

class Command(object):
  __metaclass__ = ABCMeta

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

class Search(Command):
  name = 'search'
  help = 'look up recipes by name'

  def execute(self, ns):
    flags = 0
    if ns.ignore_case:
      flags |= re.I

    recipes = [r for r in registry.recipes.itervalues()
               if re.search(ns.term, r.name, flags)]
    for r in recipes:
      print r.name

  def setup_parser(self, parser):
    parser.add_argument('term', type=str,
                        help='what to search for in recipe')
    parser.add_argument('-i', '--ignore-case', action='store_true',
                        help='ignore text case while searching')

class Show(Command):
  name = 'show'
  help = 'show recipe contents'

  def execute(self, ns):
    keys = [k for k in registry.recipes.keys() if k.startswith(ns.name)]
    if len(keys) == 1:
      pprint_recipe(registry.recipes[keys[0]])
    elif len(keys) > 1:
      raise CommandError("not prefix-free (did you mean %s)?" % _suggest(keys))
    else:
      raise CommandError("no match found for '%s'" % ns.name)

  def setup_parser(self, parser):
    parser.add_argument('name', type=str,
                        help='name (or prefix of name) of recipe to show')

COMMANDS = (
  Show(),
  Search(),
)

def main():
  try:
    parser = get_parser()
    subparsers = parser.add_subparsers()
    for cmd in COMMANDS:
      p = subparsers.add_parser(cmd.name, help=cmd.help)
      cmd.setup_parser(p)
      p.set_defaults(func=cmd.execute)
    ns = parser.parse_args()
    ns.func(ns)
  except CommandError as e:
    sys.stderr.write(e.message + "\n")
    sys.exit(e.exitcode)

def get_parser():
  parser = ArgumentParser(description='Recipe management utility')
  return parser

if __name__ == "__main__":
  main()
