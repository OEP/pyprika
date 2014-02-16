from .commands import Edit, Show, Search, Validate, List, Which, CommandError
from argparse import ArgumentParser
import os
import logging
import sys

COMMANDS = [
  Edit(),
  List(),
  Show(),
  Search(),
  Validate(),
  Which(),
]

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
    head, tail = os.path.split(sys.argv[0])
    sys.stderr.write("%s: %s\n" % (tail, e.message))
    sys.exit(e.exitcode)

def get_parser():
  parser = ArgumentParser(description='Recipe management utility')
  parser.add_argument('--quiet', '-q', action='count', default=0)
  parser.add_argument('--verbose', '-v', action='count', default=0)
  return parser

if __name__ == "__main__":
  main()
