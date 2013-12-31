import shlex
import re
from fractions import Fraction

from .exceptions import ParseError

quantity_rx = re.compile(r'^(((?P<ipart>\d+) )?(?P<fpart>\d+/\d+)|(?P<amount>\d+([.]\d+)?))( (?P<unit>.*))?$')

def _to_number(amount):
  try:
    return int(amount)
  except ValueError:
    pass
  try:
    return float(amount)
  except ValueError:
    pass
  try:
    return Fraction(amount)
  except ValueError:
    pass
  raise ParseError("Can't convert to number", amount)

class Quantity(object):
  """ Class for representing quantity.

  Quantities can either be a measurement (like ``1 cup``) or a dimensionless
  amount (like ``12``).

  :ivar amount: numeric amount of the quantity
  :type amount: int or float or fractions.Fraction
  :ivar str unit: unit of the amount, if any
  """
  amount = None 
  unit = None

  @classmethod
  def parse(cls, s):
    """
    Parse an object from a string. Valid strings are of the form:

    ::

      amount[ unit] 
    
    Where ``unit`` is unconstrained and ``amount`` is one of the following:

    * an integer, like ``4``
    * a decimal number, like ``4.5`` (*not* scientific notation)
    * a fraction, like ``1/2``
    * a mixed number, like ``1 1/2``

    :param str s: string to parse
    :raises ParseError: on invalid syntax
    :returns: the resulting Quantity 
    :rtype: Quantity 
    """
    m = quantity_rx.match(s)
    if not m:
      raise ParseError("Not valid quantity syntax", s)
    amount, unit, ipart, fpart = m.group('amount', 'unit', 'ipart', 'fpart')
    if amount:
      amount = _to_number(amount)
    elif ipart and not fpart:
      amount = int(ipart)
    else:
      assert fpart
      amount = int(ipart or 0) + Fraction(fpart)
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
    def strfrac(s):
      if not isinstance(s, Fraction):
        return s
      ipart = int(s.numerator/s.denominator)
      fpart = s - ipart
      if ipart and fpart:
        return "{} {}".format(ipart, fpart)
      return str(ipart or fpart or 0)
    s = strfrac(self.amount)
    if self.unit is None:
      return str(s)
    else:
      return "{} {}".format(s, self.unit)

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
