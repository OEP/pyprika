import pyprika
import yaml
from pyprika import Recipe, ParseError, Ingredient, loads, LoadError
from .common import BaseTest

class StaticTest(BaseTest):
  def test_empty(self):
    d = {}
    self.assertRaises(KeyError, Recipe.from_dict, d)
    self.assertRaises(LoadError, loads, yaml.dump(d))

  def test_invalid_key(self): 
    d = {'name': 'Recipe', 'x': 3}
    self.assertRaises(AttributeError, Recipe.from_dict, d)
    self.assertRaises(LoadError, loads, yaml.dump(d))

  def test_invalid_syntax_1(self):
    d = {'name': 'Recipe', 'prep_time': '1.1.1 days'}
    self.assertRaises(ParseError, Recipe.from_dict, d)
    self.assertRaises(LoadError, loads, yaml.dump(d))

  def test_invalid_type_1(self):
    d = {'name': 'Recipe', 'servings': 'four'}
    self.assertRaises(TypeError, Recipe.from_dict, d)
    self.assertRaises(LoadError, loads, yaml.dump(d))

  def test_invalid_type_2(self):
    d = {'name': 'Recipe', 'servings': (1,)}
    self.assertRaises(TypeError, Recipe.from_dict, d)
    self.assertRaises(LoadError, loads, yaml.dump(d))

  def test_invalid_type_3(self):
    d = {'name': 'Recipe', 'servings': (1,2,3)}
    self.assertRaises(TypeError, Recipe.from_dict, d)
    self.assertRaises(LoadError, loads, yaml.dump(d))

class InstanceTest(BaseTest):
  pass

class ManualInstanceTest(InstanceTest):
  @classmethod
  def setUpClass(cls):
    i = cls.instance = Recipe.from_dict({
      'name': 'My Special Recipe',
      'prep_time': '1 day',
      'cook_time': '1 week',
      'ingredients': [
        '(1) egg',
        'salt',
        '(1 cup) milk',
      ],
      'directions': [
        'Put it in a bowl',
        'Mix \'em up.',
      ],
    })

class BasicTest(object):
  
  def test_to_from_dict(self):
    i = self.instance
    d = i.to_dict()
    result = Recipe.from_dict(d)
    self.assertEqual(i, result)

class ManualBasicTest(ManualInstanceTest, BasicTest):
  pass
