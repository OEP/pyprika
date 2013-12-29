import yaml
import sys
from cStringIO import StringIO
from .exceptions import LoadError, ParseError
from .ingredient import Ingredient
from .quantity import Quantity
from .recipe import Recipe

def _loadfp(fp):
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

def load(resource):
  """ Load ``resource``, some mixed type.

  If ``resource`` is a string it will be treated as a file path. Otherwise, it
  will be treated as a file-like object.

  The file is assumed to be a pyprika-compliant YAML document. If the document
  contains a sequence, a list of ``Recipe`` objects will be returned.
  Otherwise, a single ``Recipe`` object should be returend.
  """
  if isinstance(resource, basestring):
    with open(resource, 'r') as fp:
      return _loadfp(fp)
  else:
    return _loadfp(resource)
  
def loads(data):
  """ Load recipe from string data.

  See ``load`` for more information.
  """
  return load(StringIO(data))
