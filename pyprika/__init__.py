"""
A Python package for recipe parsing and management.
"""

__version__ = '1.0.0'
__author__ = 'Paul Kilgo'

import yaml
import sys
from cStringIO import StringIO
from .exceptions import LoadError, ParseError
from .ingredient import Ingredient
from .quantity import Quantity
from .recipe import Recipe

def load(fp, loader=None, **kw):
  """ Load ``fp``, a file-like object 

  The file is assumed to be a pyprika-compliant YAML document. If the document
  contains a sequence, a list of ``Recipe`` objects will be returned.
  Otherwise, a single ``Recipe`` object should be returned.

  Note that this function wraps the underlying exceptions thrown by
  :meth:`Recipe.from_dict` under the assumption it is due to a malformed
  document, but the original traceback is preserved.

  :param file-like fp: the file-like object containing the document to load
  :param callable loader: takes one positional argument and optional arguments
                          and returns a dict (defaults to ``yaml.load``)
  :param **kw: passed through to loader
  :raises LoadError: if there was an error in the loading of the document,
                     usually indicative of a syntax error
  :returns: the recipe data contained in the stream 
  :rtype: :class:`Recipe` or list of :class:`Recipe`
  """
  loader = loader or yaml.load
  try:
    d = loader(fp)
    if isinstance(d, (tuple, list)):
      return [Recipe.from_dict(x) for x in d]
    elif isinstance(d, dict):
      return Recipe.from_dict(d)
    else:
      raise LoadError('Recipe did not decode as expected (got %s)' % type(d).__name__)
  except:
    exc_type, exc, traceback = sys.exc_info()
    raise LoadError, LoadError(*exc.args, cause=exc), traceback
  
def loads(data, loader=None, **kw):
  """ Load recipe from string data.

  This wraps ``data`` in a :class:`cString.StringIO` and calls :func:`load` on
  it.

  See :func:`load` for more information.

  :param str data: recipe document data
  :returns: the recipe data contained in ``data`` 
  :rtype: :class:`Recipe` or list of :class:`Recipe`
  """
  return load(StringIO(data), loader=loader, **kw)

def dump(recipe, fp, dumper=None, **kw):
  dumper = dumper or yaml.dump
  d = recipe.to_dict(serialize=True)
  dumper(d, fp, **kw)

def dumps(recipe, dumper=None, **kw):
  fp = StringIO()
  dump(recipe, fp, dumper=dumper, **kw)
  return fp.getvalue()
