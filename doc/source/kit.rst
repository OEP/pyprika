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

Since it's often inconsistent to refer to recipes by their name, ``kit``
indexes each recipe by taking the MD5 hash of the source file's contents. This
has its obvious flaws (the index changes when the file contents does), so this
is only done if a index has not been manually assigned in the source file.

Edit
~~~~

Edits a recipe, using the first editor found in the environment variables
``KIT_EDITOR``, ``EDITOR``, and falling back on ``pico``.

Usage:

.. code::

  kit edit index

List
~~~~

Lists recipes in the registry by their index and name.

Usage:

.. code::

  kit ls

Show
~~~~

Pretty-print a recipe to the command line. The recipe can optionally be
scaled.

Usage:

.. code::

  kit show [-s|--scale SCALE] index

Search
~~~~~~

Search for a recipe by terms in the title. The search can be case-insensitive
when the ``-i`` flag is specified.

.. code::

  kit search [-i] search-term

Validate
~~~~~~~~

Validate one or more input Pyprika recipes to verify it is correctly formed.

.. code::

  kit validate filename [filename...]

Which
~~~~~

Print the path to a recipe given its index.

.. code::

  kit which index
