import shlex

from .quantity import Quantity

class Ingredient(object):
  label = None
  quantity = None

  @classmethod
  def parse(cls, s):
    parts = shlex.split(s)
    if len(parts) > 3:
      parts[2:] = [" ".join(parts[2:])]
    assert len(parts) <= 3
    label, quantity = None, None
    if len(parts) == 1:
      label = parts[0]
    else:
      label = parts[-1]
      quantity = Quantity.parse(" ".join(parts[:-1]))
    return cls(label=label, quantity=quantity)

  def __init__(self, label, quantity=None):
    self.label = label;
    self.quantity = quantity

  def __str__(self):
    if self.quantity is None:
      return self.label
    else:
      return "{} {}".format(self.quantity, self.label)
  
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
