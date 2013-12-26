import unittest

import pyprika
from pyprika import Ingredient, Quantity
from .common import BaseTest

class BaseInstanceTest(BaseTest):
  def assertSanity(self):
    i = self.instance
    self.assertEqual(self.label, i.label)
    self.assertEqual(i.quantity, self.quantity)

class ValuelessInstanceTest(BaseInstanceTest):
  @classmethod
  def setUpClass(cls):
    cls.instance = Ingredient.parse('sea salt')
    cls.label = 'sea salt'
    cls.quantity = None

class DimensionlessInstanceTest(BaseInstanceTest):
  @classmethod
  def setUpClass(cls):
    cls.instance = Ingredient.parse('(2) eggs')
    cls.label = 'eggs'
    cls.quantity = Quantity(2)

class FullInstanceTest(BaseInstanceTest):
  @classmethod
  def setUpClass(cls):
    cls.instance = Ingredient.parse('(16 fl oz) distilled water')
    cls.label = 'distilled water'
    cls.quantity = Quantity(16, 'fl oz')

class BasicInstanceTest(object):

  def test_parse(self):
    self.assertSanity()

  def test_mul(self):
    i = self.instance
    correct = Ingredient(i.label,
                         i.quantity * 2 if i.quantity is not None else None)
    self.assertEqual(correct, i * 2)
    self.assertEqual(correct, 2 * i)

class ValuelessBasicTest(ValuelessInstanceTest, BasicInstanceTest):
  pass

class DimensionlessBasicTest(DimensionlessInstanceTest, BasicInstanceTest):
  pass

class FullBasicTest(FullInstanceTest, BasicInstanceTest):
  pass
