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

KIT_ENCODING = os.environ.get('KIT_ENCODING', 'utf-8')
USER_CONFIG_PATH = os.path.expanduser("~/.kitrc")


class ConfigError(Exception):
    pass


class _Registry(object):

    @classmethod
    def from_config(cls, path):
        with open(path, 'r') as fp:
            config = yaml.load(fp)
        if not isinstance(config, dict):
            raise ConfigError('Configuration YAML file is not a mapping')
        kw = {}
        for k in ('encoding', 'paths', 'recursive', 'skip_hidden'):
            if k in config:
                kw[k] = config[k]
        return cls(**kw)

    def __init__(self, encoding=None, paths=(), recursive=False,
                 skip_hidden=True):
        self.encoding = encoding or KIT_ENCODING
        self.search_paths = paths
        self.recursive = recursive
        self.skip_hidden = skip_hidden
        if not isinstance(self.search_paths, (list, tuple)):
            self.search_paths = (self.search_paths,)

    @property
    def recipes(self):
        try:
            return self._recipes
        except AttributeError:
            self._recipes = {}
            self.search(os.path.curdir)
            search = (self.search
                      if not self.recursive
                      else self.recursive_search)
            for p in self.search_paths:
                p = os.path.expanduser(p)
                search(p)
            return self._recipes

    @property
    def paths(self):
        try:
            return self._paths
        except AttributeError:
            self._paths = {}
            self.recipes  # attempt to build path dict
            return self._paths

    def recursive_search(self, path):
        for root, dirnames, filenames in os.walk(path, topdown=True):
            logging.info('crawling %s...', root)
            if self.skip_hidden:
                dirnames[:] = [d for d in dirnames if not d.startswith('.')]
                filenames[:] = [f for f in filenames if not f.startswith('.')]
            filenames[:] = [f for f in filenames if f.endswith('.yaml')]
            for f in filenames:
                try:
                    logging.info('discovered %s...', f)
                    self.add(os.path.join(root, f))
                except LoadError as e:
                    logging.warning('error loading %s: %s',
                                    os.path.join(root, f), e)

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
                hasher.update(fp.read().encode(self.encoding))
                recipe.index = hasher.hexdigest()
        self.recipes[recipe.index] = recipe
        self.paths[recipe.index] = path

registry = None
if os.path.exists(USER_CONFIG_PATH):
    try:
        registry = _Registry.from_config(USER_CONFIG_PATH)
    except ConfigError:
        warnings.warn('invalid user configuration; skipping')
if registry is None:
    registry = _Registry()
