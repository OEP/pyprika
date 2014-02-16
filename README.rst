pyprika
=======

A recipe management library and command line tool.

Primary features:

* A YAML file format for encoding recipes.
* Parser written for human-friendly syntax.

See `the documentation <http://pyprika.readthedocs.org/>`_ for a more complete
discussion.

Example
-------

    >>> import pyprika
    >>> recipe = pyprika.load(open('example.yaml'))
    >>> recipe.name
    'Salt Water'
    >>> recipe.ingredients
    [<Ingredient: (1 cup) water>, <Ingredient: (1 cup) salt>, <Ingredient: pepper>]
    >>> recipe.directions
    ['Put it in a pot.', 'Boil it up.', 'Glug glug glug.']
    >>> more_recipe = 2 * recipe
    >>> more_recipe.ingredients
    [<Ingredient: (2 cup) water>, <Ingredient: (2 cup) salt>, <Ingredient: pepper>]
