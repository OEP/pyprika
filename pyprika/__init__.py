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

def load(fp):
  """ Load ``fp``, a file-like object 

  The file is assumed to be a pyprika-compliant YAML document. If the document
  contains a sequence, a list of ``Recipe`` objects will be returned.
  Otherwise, a single ``Recipe`` object should be returned.

  Note that this function wraps the underlying exceptions thrown by
  :meth:`Recipe.from_dict` under the assumption it is due to a malformed
  document, but the original traceback is preserved.

  :param file-like fp: the file-like object containing the document to load
  :raises LoadError: if there was an error in the loading of the document,
                     usually indicative of a syntax error
  :returns: the recipe data contained in the stream 
  :rtype: :class:`Recipe` or list of :class:`Recipe`
  """
  try:
    d = yaml.load(fp)
    if isinstance(d, (tuple, list)):
      return [Recipe.from_dict(x) for x in d]
    elif isinstance(d, dict):
      return Recipe.from_dict(d)
    else:
      raise LoadError('Recipe did not decode as expected (got %s)' % type(d).__name__)
  except:
    exc_type, exc, traceback = sys.exc_info()
    raise LoadError, LoadError(*exc.args, cause=exc), traceback
  
def loads(data):
  """ Load recipe from string data.

  This wraps ``data`` in a :class:`cString.StringIO` and calls :func:`load` on
  it.

  See :func:`load` for more information.

  :param str data: recipe document data
  :returns: the recipe data contained in ``data`` 
  :rtype: :class:`Recipe` or list of :class:`Recipe`
  """
  return load(StringIO(data))

def dump(recipe, fp):
  d = recipe.to_dict()
  yaml.dump(d, fp)

def dumps(recipe):
  fp = StringIO()
  dump(recipe, fp)
  return fp.getvalue()
