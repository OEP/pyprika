from pyprika import Ingredient, Quantity
from .common import BaseTest


class BaseInstanceTest(BaseTest):
    def assertSanity(self):
        i = self.instance
        self.assertEqual(self.label, i.label)
        self.assertEqual(i.quantity, self.quantity)


class ValuelessInstanceTest(BaseInstanceTest):
    def setUp(self):
        self.instance = Ingredient.parse('sea salt')
        self.label = 'sea salt'
        self.quantity = None


class DimensionlessInstanceTest(BaseInstanceTest):
    def setUp(self):
        self.instance = Ingredient.parse('(2) eggs')
        self.label = 'eggs'
        self.quantity = Quantity(2)


class FullInstanceTest(BaseInstanceTest):
    def setUp(self):
        self.instance = Ingredient.parse('(16 fl oz) distilled water')
        self.label = 'distilled water'
        self.quantity = Quantity(16, 'fl oz')


class BasicInstanceTest(object):

    def test_parse(self):
        self.assertSanity()

    def test_mul(self):
        i = self.instance
        correct = Ingredient(i.label,
                             i.quantity * 2
                             if i.quantity is not None else None)
        self.assertEqual(correct, i * 2)
        self.assertEqual(correct, 2 * i)


class ValuelessBasicTest(ValuelessInstanceTest, BasicInstanceTest):
    pass


class DimensionlessBasicTest(DimensionlessInstanceTest, BasicInstanceTest):
    pass


class FullBasicTest(FullInstanceTest, BasicInstanceTest):
    pass
