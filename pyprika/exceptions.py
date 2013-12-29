class LoadError(Exception):
  """ A blanket exception to catch if there was an error loading a recipe.
  """
  def __init__(self, *args, **kwargs):
    cause = kwargs.pop('cause', None)
    super(LoadError, self).__init__(*args, **kwargs)
    self.cause = cause

  def __str__(self):
    s = ""
    if len(self.args) == 1:
      s = self.args[0]
    elif len(self.args) > 1:
      s = "%s: %s" % (self.args[0], ", ".join(repr(arg)
                                              for arg in self.args[1:]))
    if self.cause and not s:
        s = str(self.cause)
    return s

  def __repr__(self):
    return "<%s: %s>" % (type(self).__name__, self)

class ParseError(Exception):
  """ Raised on invalid syntax.
  """
  pass
