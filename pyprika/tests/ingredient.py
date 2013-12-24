import unittest

import pyprika
from pyprika import Recipe, Ingredient
from .common import BaseTest

class StaticTest(BaseTest):
  def test_parse_error(self):
    self.assertRaises(pyprika.ParseError, Ingredient.parse, "one egg")
    self.assertRaises(pyprika.ParseError, Ingredient.parse, "1.1.1 egg")

class BaseInstanceTest(BaseTest):
  def assertSanity(self):
    i = self.instance
    self.assertEqual(self.label, i.label)
    self.assertEqual(self.unit, i.unit)
    self.assertEqual(self.value, i.value)

class ValuelessInstanceTest(BaseInstanceTest):
  @classmethod
  def setUpClass(cls):
    cls.instance = Ingredient.parse('salt')
    cls.label = 'salt'
    cls.unit = None
    cls.value = None

class DimensionlessInstanceTest(BaseInstanceTest):
  @classmethod
  def setUpClass(cls):
    cls.instance = Ingredient.parse('2 eggs')
    cls.label = 'eggs'
    cls.unit = None
    cls.value = 2 

class FullInstanceTest(BaseInstanceTest):
  @classmethod
  def setUpClass(cls):
    cls.instance = Ingredient.parse('16 "fl oz" water')
    cls.label = 'water' 
    cls.unit = 'fl oz'
    cls.value = 16

class BasicInstanceTest(object):

  def test_parse(self):
    self.assertSanity()

  def test_mul(self):
    i = self.instance
    correct = Ingredient(i.label,
                         i.value * 2 if i.value is not None else None,
                         i.unit)
    result = i * 2
    self.assertEqual(correct, result)

class ValuelessBasicTest(ValuelessInstanceTest, BasicInstanceTest):
  pass

class DimensionlessBasicTest(DimensionlessInstanceTest, BasicInstanceTest):
  pass

class FullBasicTest(FullInstanceTest, BasicInstanceTest):
  pass
