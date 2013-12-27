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
  'on_favorites',
  'categories',
  'nutritional_info',
  'difficulty',
  'rating',
  'notes',
  'photo',
  'ingredients',
  'directions',
)

class Recipe(object):
  name = None

  servings = None
  source = ''
  source_url = ''
  prep_time = QuantityDescriptor(convert=True) 
  cook_time = QuantityDescriptor(convert=True) 
  on_favorites = False
  categories = ()
  nutritional_info = ''
  difficulty = None
  rating = None
  notes = ''
  photo = None
  ingredients = ()
  directions = ()

  @classmethod
  def from_dict(cls, d):
    i = cls(name=d['name'])
    for key in d.iterkeys():
      if not hasattr(i, key):
        raise AttributeError(key)
      v = deepcopy(d[key])
      setattr(i, key, d[key])
    return i

  def to_dict(self):
    return dict((x, getattr(self, x)) for x in RECIPE_ATTRIBUTES)

  def __init__(self, name):
    self.name = name
    self.categories = []
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
