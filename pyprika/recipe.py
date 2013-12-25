from copy import deepcopy
from .ingredient import Ingredient
from .quantity import Quantity, QuantityDescriptor

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
    return {
      'name': self.name,
      'servings': self.servings,
      'source_url': self.source_url,
      'servings': self.servings,
      'source': self.source,
      'source_url': self.source_url,
      'prep_time': (self.prep_time),
      'cook_time': (self.cook_time),
      'on_favorites': self.on_favorites, 
      'categories':  (self.categories),
      'nutritional_info': self.nutritional_info, 
      'difficulty': self.difficulty, 
      'rating': self.rating, 
      'notes': self.notes, 
      'photo': self.photo,
      'ingredients': (self.ingredients),
      'directions': (self.directions),
    }

  def __init__(self, name):
    self.name = name
    self.categories = []
    self.ingredients = []
    self.directions = []

  def __str__(self):
    return self.name

  def __repr__(self):
    return "<Recipe: {}>".format(self)

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
