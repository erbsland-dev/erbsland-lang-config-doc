..
    Copyright (c) 2024-2025 Tobias Erbsland - Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

.. _ref-text-value:
.. index::
    single: Text
    single: Text Value

Text Values
===========

Text values are one of the core language value types. 

.. code-block:: bnf

    text_value          ::= text

The *EBNF* syntax and accompanying rules for the ``text`` symbol are described in chapter :ref:`ref-text`.

.. code-block:: erbsland-conf
    :class: good-example

    [main]
    value: "おはようございます！"


Features
--------

.. list-table::
    :header-rows: 1
    :width: 100%
    :widths: 25, 75

    *   -   Feature
        -   Coverage
    *   -   :text-code:`core`
        -   Text values are part of the core language.


Errors
------

.. list-table::
    :header-rows: 1
    :width: 100%
    :widths: 25, 75

    *   -   Error Code
        -   Causes
    *   -   
        -   All errors related to text (see :ref:`ref-text`).

