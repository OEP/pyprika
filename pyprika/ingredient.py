import shlex
import re
from copy import deepcopy

from .quantity import Quantity
from .exceptions import ParseError

ingredient_rx = re.compile(r'^([(](?P<quantity>[^)]+)[)] )?(?P<label>.+)$')

class Ingredient(object):
  """ Class for representing ingredients.

  :ivar str label: the label of the ingredient (like ``egg``)
  :ivar Quantity quantity: the amount of the ingredient, if any
  """
  label = None
  quantity = None

  @classmethod
  def parse(cls, s):
    """
    Parse an object from a string. Valid strings are of the form:

    ::

      [(quantity) ]label

    Where ``quantity`` must be valid syntax to :meth:`Quantity.parse` and
    ``label`` is any text not beginning with a value enclosed in
    parenthesis.

    :param str s: string to parse
    :raises ParseError: on invalid syntax
    :returns: the resulting Ingredient
    :rtype: Ingredient
    """
    m = ingredient_rx.match(s)
    if not m:
      raise ParseError("Invalid ingredient syntax", s)
    quantity, label = m.group('quantity', 'label')
    if quantity:
      quantity = Quantity.parse(quantity)
    return cls(label=label, quantity=quantity)

  def __init__(self, label, quantity=None):
    self.label = label;
    self.quantity = quantity

  def __str__(self):
    if self.quantity is None:
      return self.label
    else:
      return "({}) {}".format(self.quantity, self.label)
  
  def __repr__(self):
    return "<Ingredient: {}>".format(self)

  def __mul__(self, other):
    cls = type(self)
    return cls(label=self.label,
               quantity=(self.quantity * other
                         if self.quantity is not None else None))
  
  def __rmul__(self, other):
    return self * other

  def __eq__(self, other):
    return (type(other) == type(self) and
            self.label == other.label and
            self.quantity == other.quantity)
