import shlex
from fractions import Fraction

from .exceptions import ParseError

def _to_number(amount):
  try:
    return int(amount)
  except ValueError:
    pass
  try:
    return float(amount)
  except:
    pass
  try:
    return Fraction(amount)
  except ValueError:
    pass
  raise ParseError("Can't convert to number", amount)

class Quantity(object):
  amount = None 
  unit = None

  @classmethod
  def parse(cls, s):
    parts = shlex.split(s)
    if len(parts) > 2:
      parts[1:] = [" ".join(parts[1:])]
    assert len(parts) <= 2
    amount, unit = (None,) * 2
    if len(parts) == 1:
      amount = _to_number(parts[0])
    else: 
      amount = _to_number(parts[0])
      unit = parts[1]
    return cls(amount=amount, unit=unit)
  
  def __init__(self, amount=None, unit=None):
    self.amount = amount
    self.unit = unit

  def __mul__(self, factor):
    """ Scale amount by a factor. 

    Note: not unit safe. ``factor`` must be dimensionless.
    """
    cls = type(self)
    return cls(factor * self.amount,
               self.unit)

  def __rmul__(self, factor):
    return self * factor

  def __eq__(self, other):
    if type(self) != type(other):
      return False
    return (self.unit == other.unit and
            self.amount == other.amount)

  def __str__(self):
    if self.unit is None:
      return str(self.amount)
    else:
      return "{} {}".format(self.amount, self.unit)

  def __repr__(self):
    return "<Quantity: {}>".format(str(self))

class QuantityDescriptor(object):

  def __init__(self, value=None, convert=False):
    self.convert = convert
    self.default = self._check(value)

  def __get__(self, obj, objtype):
    return obj.__dict__.get(self, self.default)

  def __set__(self, obj, value):
    obj.__dict__[self] = self._check(value)

  def _check(self, value):
    if isinstance(value, basestring) and self.convert:
      value = Quantity.parse(value)
    elif value is None:
      pass
    elif not isinstance(value, Quantity):
      raise TypeError("Not a Quantity", value)
    return value
