"""
kit (command-line interface) specific data and code

Importing this module could potentially be a performance hit as it tries to
pre-cache recipes which would be wasteful for a library to do.
"""

from .. import load
from ..exceptions import LoadError
import hashlib
import glob
import logging
import os
import warnings
import yaml

config_path = os.path.expanduser("~/.kitrc")
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
    pass

  @property
  def recipes(self):
    try:
      return self._recipes
    except AttributeError:
      self._recipes = {}
      self.search(os.path.curdir)
      paths = config.get('paths', [])
      recursive = config.get('recursive', False)
      search = self.search if not recursive else self.recursive_search
      for p in paths:
        search(p)
      return self._recipes

  @property
  def paths(self):
    try:
      return self._paths
    except AttributeError:
      self._paths = {}
      self.recipes ## attempt to build path dict
      return self._paths

  def recursive_search(self, path):
    skip_hidden = config.get('skip_hidden', True)
    for root, dirnames, filenames in os.walk(path, topdown=True):
      logging.info('crawling %s...', root)
      if skip_hidden:
        dirnames[:] = [d for d in dirnames if not d.startswith('.')]
        filenames[:] = [f for f in filenames if not f.startswith('.')]
      filenames[:] = [f for f in filenames if f.endswith('.yaml')]
      for f in filenames:
        try:
          logging.info('discovered %s...', f)
          self.add(os.path.join(root, f))
        except LoadError as e:
          logging.warning('error loading %s: %s', os.path.join(root, f), e)

  def search(self, path):
    files = glob.glob(os.path.join(path, '*.yaml'))
    for f in files:
      try:
        self.add(f)
      except LoadError as e:
        logging.warning('error loading %s: %s', f, e)

  def select(self, index):
    return [k for k in self.recipes.keys() if k.startswith(index)]
    
  def add(self, path):
    with open(path, 'r') as fp:
      recipe = load(fp)
      if recipe.index is None:
        hasher = hashlib.md5()
        fp.seek(0)
        hasher.update(fp.read())
        recipe.index = hasher.hexdigest()
      self.recipes[recipe.index] = recipe
      self.paths[recipe.index] = path

registry = _Registry()
