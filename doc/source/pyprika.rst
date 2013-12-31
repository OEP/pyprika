``pyprika`` package
===================

The ``pyprika`` package contains the primary API.

.. module:: pyprika

Input and output
----------------

.. autofunction:: load

.. autofunction:: loads

API classes
-----------

:class:`Recipe`
~~~~~~~~~~~~~~~

.. autoclass:: Recipe
   :members: from_dict, to_dict 

:class:`Ingredient`
~~~~~~~~~~~~~~~~~~~

.. autoclass:: Ingredient
   :members: parse

:class:`Quantity`
~~~~~~~~~~~~~~~~~

.. autoclass:: Quantity 
   :members: parse

Exceptions
----------

:class:`ParseError`
~~~~~~~~~~~~~~~~~~

.. autoclass:: ParseError 

:class:`LoadError`
~~~~~~~~~~~~~~~~~~

.. autoclass:: LoadError
