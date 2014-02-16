from copy import deepcopy
from fractions import Fraction
from .ingredient import Ingredient
from .quantity import Quantity, QuantityDescriptor
from .exceptions import FieldError

RECIPE_ATTRIBUTES = (
  'index',
  'name',
  'servings',
  'source',
  'source_url',
  'prep_time',
  'cook_time',
  'notes',
  'ingredients',
  'directions',
)

class Recipe(object):
  """Class for representing a recipe.

  :ivar str name: human-friendly name of recipe
  :ivar index: optional application-specific indexing value
  :ivar servings: number of servings or a range (a 2-item tuple) 
  :type servings int or tuple or None:
  :ivar str source: human-friendly source of recipe
  :ivar str source_url: URL source to for recipe
  :ivar Quantity prep_time: total preparation time for recipe
  :ivar Quantity cook_time: total cooking time for recipe
  :ivar str notes: miscellaneous data about recipe
  :ivar list ingredients: list of Ingredient objects
  :ivar list directions: list of instructions to prepare recipe
  """

  name = None

  index = None
  servings = None
  source = ''
  source_url = ''
  prep_time = QuantityDescriptor('prep_time', convert=True) 
  cook_time = QuantityDescriptor('cook_time', convert=True) 
  notes = ''
  ingredients = ()
  directions = ()

  @classmethod
  def from_dict(cls, d):
    """ Creates a new recipe from a dictionary.

    :param dict d: the dictionary to convert
    :raises FieldError: if a field is missing, invalid, or not well-formed
    :raises ParseError: if a Pyprika syntax error is present
    :returns: the resulting recipe
    :rtype: Recipe
    """
    if not 'name' in d:
      raise FieldError('Field is required', 'name')
    i = cls(name=d['name'])
    for key in d.iterkeys():
      if not hasattr(i, key):
        raise FieldError('Unknown field for recipe', key)
      v = deepcopy(d[key])
      setattr(i, key, v)
    return i

  def to_dict(self, serialize=False):
    """ Return a dictionary representing the Recipe.

    :param bool serialize: convert as much as possible to primitive types
    :returns: a dictionary mapping attribute names to values
    :rtype: dict
    """
    def _serialize(value):
      if not serialize:
        return value
      if isinstance(value, (Quantity, Ingredient)):
        return str(value)
      elif isinstance(value, (tuple, list)):
        cls = type(value)
        return cls(_serialize(x) for x in value)
      return value
    return dict((x, _serialize(getattr(self, x))) 
                for x in RECIPE_ATTRIBUTES)

  def __init__(self, name):
    self.name = name
    self.ingredients = []
    self.directions = []

  def __str__(self):
    return self.name

  def __repr__(self):
    return "<Recipe: {}>".format(self)

  def __eq__(self, o):
    if not isinstance(o, type(self)):
      return False
    return all(getattr(self, x) == getattr(o, x)
               for x in RECIPE_ATTRIBUTES)

  def __mul__(self, o):
    result = deepcopy(self)
    if isinstance(result.servings, (list, tuple)):
      result.servings = [o * x for x in result.servings]
    elif result.servings is None:
      pass
    else:
      result.servings = o * result.servings if result.servings else None
    result.ingredients = [o * i for i in result.ingredients]
    return result

  def __rmul__(self, o):
    return self * o

  @property
  def servings(self):
    return getattr(self, '_servings', None)

  @servings.setter
  def servings(self, value):
    if isinstance(value, (Fraction, long, float, int)) or value is None:
      self._servings = value
    elif isinstance(value, (list, tuple)) and len(value) == 2:
      self._servings = tuple(value)
    else:
      raise FieldError("Not a number or 2-item tuple/list", value)
    return value

  @property
  def ingredients(self):
    return getattr(self, '_ingredients', None)

  @ingredients.setter
  def ingredients(self, value):
    self._ingredients = [Ingredient.parse(x)
                         if not isinstance(x, Ingredient) else x
                         for x in value]
