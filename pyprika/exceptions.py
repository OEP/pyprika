class LoadError(Exception):
  """ A blanket exception to catch if there was an error loading a recipe.
  """
  def __init__(self, *args, **kwargs):
    cause = kwargs.pop('cause', None)
    super(LoadError, self).__init__(*args, **kwargs)
    self.cause = cause

class ParseError(Exception):
  """ Raised on invalid syntax.
  """
  pass
