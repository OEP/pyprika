Pyprika's YAML specification
============================

Pyprika's YAML format was developed from an `export syntax
<http://www.paprikaapp.com/help/android/>`_ used by the Paprika smartphone
application with some modifications primarily to make the syntax more rigid.

The following are the design goals of the syntax in order of importance:

- As little markup as possible
- Support the "natural" way of expressing cooking concepts
- Easily machine-processible where possible

This documentation will work from an example which utilizes all of the
features to touch on:

.. code:: yaml

  name: Dumplings

  index: DMP0001
  servings: [4, 6] 
  source: The Internet 
  source_url: http://www.example.com/
  prep_time: 5 min
  cook_time: 45 min
  notes: |
    Piping hot!
 
  ingredients:
    - (1/2 tsp) baking powder 
    - (1 1/2 cup) flour 
    - salt
    - pepper
    - (2 tbsp) olive oil
    - (4.5 cups) water 

  directions:
    - Put it in a bowl.
    - Mix 'em up.
    - Bake.

Though it looks verbose, the only required field is ``name``. The rest can
safely be left as their defaults.

Field descriptions
------------------

  name
    The name of the recipe.

  index
    An indexing field which is not used internally by the library, but can be
    used by applications to refer to the recipe.

  servings
    The number of servings the recipe produces. This may be an integer, or can
    be a 2-item list to represent a range (e.g. 2 servings or 2-4 servings).

  source
    An unrestricted field for noting the source of the recipe.

  source_url
    An unrestricted field for noting the URL from which the recipe originates.
    No validation is performed to ensure this is a URL.

  prep_time
    The total time of preparation for the recipe. Must conform to `quantity syntax`_.

  cook_time
    The amount of cooking time for the recipe. Must conform to `quantity syntax`_.

  notes
    An unconstrained field for providing miscellaneous notes.

  ingredients
    A list of ingredients needed for the recipe. Each item in the list must
    conform to `ingredient syntax`_.

  directions
    A list of directions (in order) for preparing the recipe. The items of
    the list are unconstrained.

_`Ingredient syntax`
-----------------

Ingredient syntax has two primary forms: unquantified and quantified. The
unquantified form simply means the ingredient does not have an associated
quantity, whereas the quantified form does.

Unquantified form
~~~~~~~~~~~~~~~~~

The unquantified form is the easiest to understand. The only restriction is
the start of the string cannot contain parenthesis. So all of the following
are examples of the unquantified form:

- ``salt``
- ``water (optional)``
- ``black pepper``

Quantified form
~~~~~~~~~~~~~~~

The quantified form has a quantity or measurement associated with it. They
look the same as the unquantified form, but with a measurement in parenthesis
on the left. The following are all examples of the quantified form:

- ``(1 cup) water``
- ``(1 1/2 cup) unbleached flour``
- ``(1) apple (optional)``

The text in the leading set of parantheses must follow the `quantity syntax`_.

_`Quantity syntax`
---------------

The quantity syntax is a means of expressing amounts, whether it be dimensionless (like a count)
or dimensioned (like ``1 cup``). In general, the quantity syntax follows this form:

::

  number [unit]

Where ``number`` is one of the following:

* a non-negative integer (e.g. ``0``, ``12``)
* a decimal point number (e.g. ``1.5``, ``2.75``)
* a fraction (e.g. ``1/2``, ``3/4``)
* a mixed number (e.g. ``1 1/2``, ``2 3/4``)

Scientific notation is not supported for decimal point numbers.

``unit`` is optional, and any text found after the number is considered a part
of the unit. As an example, for ``1 1/2 fl oz``, then ``1 1/2`` would be
interpreted as the number and ``fl oz`` would be interpreted as the unit.

