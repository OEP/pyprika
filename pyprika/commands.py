from . import load
from .pprint import pprint_recipe
from .exceptions import ParseError
from abc import ABCMeta, abstractmethod
from argparse import ArgumentParser
import glob
import os
import sys
import yaml

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
    with open(config_path) as fp:
      self.config = yaml.load(fp)
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

  @abstractmethod
  def execute(self, argv):
    raise NotImplementedError

class Show(Command):

  def execute(self, argv):
    parser = self._get_parser()
    ns = parser.parse_args(argv)
    keys = [k for k in registry.recipes.keys() if k.startswith(ns.name)]
    if len(keys) == 1:
      pprint_recipe(registry.recipes[keys[0]])
    elif len(keys) > 1:
      raise CommandError("not prefix-free (did you mean %s)?" % _suggest(keys))
    else:
      raise CommandError("no match found for '%s'" % ns.name)

  def _get_parser(self):
    parser = ArgumentParser()
    parser.add_argument('name', type=str)
    return parser

COMMANDS = {
  'show': Show(),
}

def main():
  try:
    parser = get_parser()
    ns = parser.parse_args()
    cmd = COMMANDS.get(ns.subcommand)
    if cmd is None:
      raise CommandError("No such command: %s" % ns.subcommand)
    cmd.execute(ns.argv)
  except CommandError as e:
    sys.stderr.write(e.message + "\n")
    sys.exit(e.exitcode)

def get_parser():
  parser = ArgumentParser(description='Recipe management utility')
  parser.add_argument('subcommand', type=str)
  parser.add_argument('argv', type=str, nargs='*')
  return parser

if __name__ == "__main__":
  main()
