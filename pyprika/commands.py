from .kit import registry
from .pprint import pprint_recipe
from .exceptions import LoadError
from . import load
from abc import ABCMeta, abstractmethod, abstractproperty
from argparse import ArgumentParser
import logging
import os
import sys
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
          print "%s: %s" % (f, e)
        else:
          print str(e)
    sys.exit(exit_code)

  def setup_parser(self, parser):
    parser.add_argument('filenames', type=str, nargs='+',
                        help='path to recipe file(s) to validate')

COMMANDS = (
  Show(),
  Search(),
  Validate(),
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
    log_level = logging.WARNING - 10 * (ns.verbose - ns.quiet)
    logging.basicConfig(level=log_level)
    ns.func(ns)
  except CommandError as e:
    sys.stderr.write(e.message + "\n")
    sys.exit(e.exitcode)

def get_parser():
  parser = ArgumentParser(description='Recipe management utility')
  parser.add_argument('--quiet', '-q', action='count', default=0)
  parser.add_argument('--verbose', '-v', action='count', default=0)
  return parser

if __name__ == "__main__":
  main()
