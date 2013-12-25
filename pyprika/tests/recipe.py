import pyprika
from pyprika import Recipe, ParseError, Ingredient
from .common import BaseTest

class StaticTest(BaseTest):
  def test_from_dict_errors(self):
    d = {}
    self.assertRaises(KeyError, Recipe.from_dict, d)
    d['name'] = 'Recipe'
    d['x'] = 3
    self.assertRaises(AttributeError, Recipe.from_dict, d)
    del d['x']
    d['prep_time'] = '1.1.1 days'
    self.assertRaises(ParseError, Recipe.from_dict, d)
    del d['prep_time']
    d['servings'] = 'four'
    self.assertRaises(TypeError, Recipe.from_dict, d)
    d['servings'] = (1,)
    self.assertRaises(TypeError, Recipe.from_dict, d)
    d['servings'] = (1,2,3)
    self.assertRaises(TypeError, Recipe.from_dict, d)

class InstanceTest(BaseTest):
  pass

class ManualInstanceTest(InstanceTest):
  @classmethod
  def setUpClass(cls):
    i = cls.instance = Recipe('Empty')
    i.ingredients.append(Ingredient.parse('1 egg'))
    i.ingredients.append(Ingredient.parse('salt'))
    i.ingredients.append(Ingredient.parse('1 cup milk'))
    i.directions.append('Put it in a bowl')
    i.directions.append('Mix \'em up.')
    i.prep_time = '1 day'
    i.cook_time = '1 week'

class BasicTest(object):
  
  def test_to_from_dict(self):
    i = self.instance
    d = i.to_dict()
    result = Recipe.from_dict(d)
    self.assertEqual(i, result)

class ManualBasicTest(ManualInstanceTest, BasicTest):
  pass
