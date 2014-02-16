The ``kit`` utility
===================

``kit`` is a simple command line application of the pyprika library. It's meant
for recipe management via the command line. It does require a little setup so
that it knows where to find your recipes.

The name is somewhat a play on "kitchen" and "Git".

The ``~/.kitrc`` file
---------------------

Your ``.kitrc`` governs the behavior of ``kit``. Upon startup, ``kit`` searches
the paths defined in this configuration file for recipes as well as the current
directory.

For example, if this is in ``~/.kitrc``:

.. code:: yaml

  paths:
    - /home/paul/recipes
    - /usr/local/share/recipes

Then it will search the paths ``/home/paul/recipes`` and
``/usr/local/share/recipes`` upon startup. The default behavior is to do a
shallow search. If you want it to do a recursive search:

.. code:: yaml

  recursive: True
  paths:
    - /home/paul/recipes
    - /usr/local/share/recipes

That's the basics. The reference should be enough.

Commands
--------

``kit`` is organized into subcommands, similar to a lot of other popular
utilities you're used to using.
