``pyprika`` package
===================

The ``pyprika`` package contains the primary API.

.. module:: pyprika

Input and output
----------------

.. autofunction:: load

.. autofunction:: loads

.. autofunction:: dump

.. autofunction:: dumps

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

:class:`FieldError`
~~~~~~~~~~~~~~~~~~~

.. autoclass:: FieldError 

:class:`ParseError`
~~~~~~~~~~~~~~~~~~~

.. autoclass:: ParseError 

:class:`LoadError`
~~~~~~~~~~~~~~~~~~

.. autoclass:: LoadError
