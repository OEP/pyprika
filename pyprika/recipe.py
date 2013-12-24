import shlex

from .exceptions import ParseError

def _to_number(value):
  try:
    return int(value)
  except ValueError:
    try:
      return float(value)
    except:
      raise ParseError("Can't convert to number", value)

class Ingredient(object):
  label = None
  quantity = None
  unit = None

  @classmethod
  def parse(cls, s):
    parts = shlex.split(s)
    if len(parts) > 3:
      parts[2:] = [" ".join(parts[2:])]
    assert len(parts) <= 3
    label, value, unit = (None,) * 3
    if len(parts) == 1:
      label = parts[0]
    elif len(parts) == 2:
      value = _to_number(parts[0])
      label = parts[1]
    else: # len(parts) == 3
      value = _to_number(parts[0])
      unit = parts[1]
      label = parts[2]
    return cls(label=label, value=value, unit=unit)
  
  def __init__(self, label, value=None, unit=None):
    self.label = label
    self.value = value
    self.unit = unit

  def __mul__(self, factor):
    """ Scale ingredient by some factor.

    Note: not unit safe. ``factor`` must be dimensionless.
    """
    cls = type(self)
    return cls(self.label,
               factor * self.value if self.value is not None else None,
               self.unit)

  def __rmul__(self, factor):
    return self * factor

  def __eq__(self, other):
    return (self.label == other.label and
            self.unit == other.unit and
            self.value == other.value)

class Recipe(object):
  pass
