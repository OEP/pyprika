import sys

def pprint_recipe(recipe, os=sys.stdout):
  def writeif(cond, s):
    if cond:
      os.write(s)
  os.write("Name: %s\n" % recipe.name)
  if recipe.servings:
    if isinstance(recipe.servings, (list, tuple)):
      s = "-".join(str(x) for x in recipe.servings)
    else:
      s = str(recipe.servings)
    os.write("Servings: %s\n" % s)
  writeif(recipe.source or recipe.source_url, "Source: ")
  if recipe.source:
    os.write(recipe.source)
    writeif(recipe.source_url, " <%s>" % recipe.source_url)
    os.write("\n")
  else:
    writeif(recipe.source_url, "%s\n" % recipe.source_url)
  writeif(recipe.prep_time, "Prep time: %s\n" % recipe.prep_time)
  writeif(recipe.cook_time, "Cook time: %s\n" % recipe.cook_time)
  os.write("\nIngredients:\n\n")
  for i in recipe.ingredients:
    os.write("  - %s\n" % i)
  os.write("\nDirections:\n\n")
  for num, d in enumerate(recipe.directions, 1):
    os.write("  %d. %s\n" % (num, d))

  writeif(recipe.notes, "\nNotes:\n\n%s" % recipe.notes)
