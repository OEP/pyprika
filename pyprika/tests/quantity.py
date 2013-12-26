import pyprika
from pyprika import Quantity
from .common import BaseTest
from fractions import Fraction

class StaticTest(BaseTest):
  def test_parse_error(self):
    self.assertRaises(pyprika.ParseError, Quantity.parse, "")
    self.assertRaises(pyprika.ParseError, Quantity.parse, "one")
    self.assertRaises(pyprika.ParseError, Quantity.parse, "1.1.1")

class BaseInstanceTest(BaseTest):
  def assertSanity(self):
    i = self.instance
    self.assertEqual(self.amount, i.amount)
    self.assertEqual(self.unit, i.unit)

class UnitlessTest(BaseInstanceTest):
  @classmethod
  def setUpClass(cls):
    cls.instance = Quantity.parse('1')
    cls.amount = 1
    cls.unit = None

class IntegerTest(BaseInstanceTest):
  @classmethod
  def setUpClass(cls):
    cls.instance = Quantity.parse('1 fl oz')
    cls.amount = 1
    cls.unit = 'fl oz'

class FloatTest(BaseInstanceTest):
  @classmethod
  def setUpClass(cls):
    cls.instance = Quantity.parse('1.5 fl oz')
    cls.amount = 1.5
    cls.unit = 'fl oz'

class FractionTest(BaseInstanceTest):
  @classmethod
  def setUpClass(cls):
    cls.instance = Quantity.parse('3/2 fl oz')
    cls.amount = Fraction(3,2)
    cls.unit = 'fl oz'

class MixedTest(BaseInstanceTest):
  @classmethod
  def setUpClass(cls):
    cls.instance = Quantity.parse('1 1/2 fl oz')
    cls.amount = Fraction(3,2)
    cls.unit = 'fl oz'

class BasicTest(object):
  def test_parse(self):
    self.assertSanity()

  def test_mul(self):
    i = self.instance
    expected = Quantity(2 * i.amount,
                        i.unit)
    result = 2 * i
    self.assertEqual(expected, result)
    result = i * 2
    self.assertEqual(expected, result)

class BasicUnitlessTest(UnitlessTest, BasicTest): pass
class BasicIntegerTest(IntegerTest, BasicTest): pass
class BasicFloatTest(FloatTest, BasicTest): pass
class BasicFractionTest(FractionTest, BasicTest): pass
class BasicMixedTest(MixedTest, BasicTest): pass
