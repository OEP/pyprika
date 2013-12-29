"""
kit (command-line interface) specific data and code

Importing this module could potentially be a performance hit as it tries to
pre-cache recipes which would be wasteful for a library to do.
"""

from . import load
from .exceptions import LoadError 
import glob
import os
import warnings
import yaml

config_path = os.path.expanduser("~/.pyprika")
if os.path.exists(config_path):
  with open(config_path) as fp:
    config = yaml.load(fp)
else:
  config = {}
if not isinstance(config, dict):
  warnings.warn('invalid user configuration; skipping')
  config = {}

class _Registry(object):
  def __init__(self):
    self.recipes = {}
    self.search(os.path.curdir)
    paths = config.get('paths', [])
    recursive = config.get('recursive', False)
    search = self.search if not recursive else self.recursive_search
    for p in paths:
      search(p)

  def recursive_search(self, path):
    skip_hidden = config.get('skip_hidden', True)
    for root, dirnames, filenames in os.walk(path, topdown=True):
      if skip_hidden:
        dirnames[:] = [d for d in dirnames if not d.startswith('.')]
        filenames[:] = [f for f in filenames if not f.startswith('.')]
      filenames[:] = [f for f in filenames if f.endswith('.yaml')]
      for f in filenames:
        try:
          self.add(os.path.join(root, f))
        except LoadError:
          pass

  def search(self, path):
    files = glob.glob(os.path.join(path, '*.yaml'))
    for f in files:
      try:
        self.add(f)
      except LoadError:
        pass
    
  def add(self, path):
    recipe = load(path)
    self.recipes[recipe.name] = recipe

registry = _Registry()
