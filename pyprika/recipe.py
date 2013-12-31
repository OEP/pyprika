from copy import deepcopy
from .ingredient import Ingredient
from .quantity import Quantity, QuantityDescriptor

RECIPE_ATTRIBUTES = (
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

  servings = None
  source = ''
  source_url = ''
  prep_time = QuantityDescriptor(convert=True) 
  cook_time = QuantityDescriptor(convert=True) 
  notes = ''
  ingredients = ()
  directions = ()

  @classmethod
  def from_dict(cls, d):
    """ Creates a new recipe from a dictionary.

    :param dict d: the dictionary to convert
    :raises KeyError: if a required field is missing
    :raises AttributeError: if an invalid field is specified
    :returns: the resulting recipe
    :rtype: Recipe
    """
    i = cls(name=d['name'])
    for key in d.iterkeys():
      if not hasattr(i, key):
        raise AttributeError(key)
      v = deepcopy(d[key])
      setattr(i, key, v)
    return i

  def to_dict(self):
    """ Return a dictionary representing the Recipe.

    :returns: a dictionary mapping attribute names to values
    :rtype: dict
    """
    return dict((x, getattr(self, x)) for x in RECIPE_ATTRIBUTES)

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

  @property
  def servings(self):
    return getattr(self, '_servings', None)

  @servings.setter
  def servings(self, value):
    if isinstance(value, (float, int)) or value is None:
      self._servings = value
    elif (isinstance(value, (list, tuple)) and len(value) == 2 and
          all(isinstance(x, (int, float)) for x in value)):
      self._servings = tuple(value)
    else:
      raise TypeError("Not a number or 2-item tuple/list", value)
    return value

  @property
  def ingredients(self):
    return getattr(self, '_ingredients', None)

  @ingredients.setter
  def ingredients(self, value):
    self._ingredients = [Ingredient.parse(x)
                         if not isinstance(x, Ingredient) else x
                         for x in value]
