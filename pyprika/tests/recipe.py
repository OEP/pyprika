import pyprika
import yaml
from pyprika import (Recipe, ParseError, Ingredient, loads, dumps, LoadError,
                     FieldError)
from .common import BaseTest

STANDARD_DICT = {
  'name': 'My Special Recipe',
  'index': 'MSR0001',
  'prep_time': '1 day',
  'cook_time': '1 week',
  'servings': [2, 4],
  'source': 'Source Person',
  'source_url': 'http://example.com/',
  'notes': 'some notes',
  'ingredients': [
    '(1.5 cup) milk',
    '(1 1/2 cup) milk',
    '(1 cup) milk',
    '(1) egg',
    'salt',
  ],
  'directions': [
    'Put it in a bowl',
    'Mix \'em up.',
  ],
}

class StaticTest(BaseTest):
  def test_empty(self):
    d = {}
    self.assertRaises(FieldError, Recipe.from_dict, d)
    self.assertRaises(LoadError, loads, yaml.dump(d))

  def test_invalid_key(self): 
    d = {'name': 'Recipe', 'x': 3}
    self.assertRaises(FieldError, Recipe.from_dict, d)
    self.assertRaises(LoadError, loads, yaml.dump(d))

  def test_invalid_syntax_1(self):
    d = {'name': 'Recipe', 'prep_time': '1.1.1 days'}
    self.assertRaises(ParseError, Recipe.from_dict, d)
    self.assertRaises(LoadError, loads, yaml.dump(d))

  def test_invalid_type_1(self):
    d = {'name': 'Recipe', 'servings': 'four'}
    self.assertRaises(FieldError, Recipe.from_dict, d)
    self.assertRaises(LoadError, loads, yaml.dump(d))

  def test_invalid_type_2(self):
    d = {'name': 'Recipe', 'servings': (1,)}
    self.assertRaises(FieldError, Recipe.from_dict, d)
    self.assertRaises(LoadError, loads, yaml.dump(d))

  def test_invalid_type_3(self):
    d = {'name': 'Recipe', 'servings': (1,2,3)}
    self.assertRaises(FieldError, Recipe.from_dict, d)
    self.assertRaises(LoadError, loads, yaml.dump(d))

class InstanceTest(BaseTest):
  pass

class ManualInstanceTest(InstanceTest):
  @classmethod
  def setUpClass(cls):
    i = cls.instance = Recipe.from_dict(STANDARD_DICT)

class BasicTest(object):

  def test_copy(self):
    from copy import deepcopy
    i = self.instance
    result = deepcopy(i)
    self.assertEqual(i, result)

  def test_mul(self):
    i = self.instance
    result = i * 2
    result = result * 0.5
    self.assertEqual(i, result)

  def test_to_from_dict(self):
    i = self.instance
    d = i.to_dict()
    result = Recipe.from_dict(d)
    self.assertEqual(i, result)
  
  def test_to_from_dict_serialize(self):
    i = self.instance
    d = i.to_dict(serialize=True)
    result = Recipe.from_dict(d)
    self.assertEqual(i, result)

  def test_dump_load_default(self):
    i = self.instance
    s = dumps(i)
    result = loads(s)
    self.assertEqual(i, result)
  
  def test_dump_load_yaml(self):
    i = self.instance
    s = dumps(i, dumper=yaml.dump)
    result = loads(s, loader=yaml.load)
    self.assertEqual(i, result)
  
  def test_dump_load_json(self):
    import json
    i = self.instance
    s = dumps(i, dumper=json.dump)
    result = loads(s, loader=json.load)
    self.assertEqual(i, result)
  
  def test_dump_load_simplejson(self):
    try:
      import simplejson
      i = self.instance
      s = dumps(i, dumper=simplejson.dump)
      result = loads(s, loader=simplejson.load)
      self.assertEqual(i, result)
    except ImportError:
      pass

class ManualBasicTest(ManualInstanceTest, BasicTest):
  pass
