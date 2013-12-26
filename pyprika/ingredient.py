import shlex
import re
from copy import deepcopy

from .quantity import Quantity
from .exceptions import ParseError

ingredient_rx = re.compile(r'^([(](?P<quantity>[^)]+)[)] )?(?P<label>.+)$')

class Ingredient(object):
  label = None
  quantity = None

  @classmethod
  def parse(cls, s):
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
