..
    Copyright (c) 2024-2025 Tobias Erbsland - Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

.. _ref-boolean-value:
.. index::
    single: Boolean
    single: Boolean Value

Boolean Value
=============

Boolean values are a fundamental type in the language, represented by several different literals that are case-insensitive.

.. code-block:: bnf

    boolean             ::= "true" | "false" | "yes" | "no" |
                            "on" | "off" | "enabled" | "disabled"   /* All literals are case-insensitive */

In the example below, you can see valid boolean values using different literals:

.. code-block:: erbsland-conf
    :class: good-example

    [main]
    value a: True
    value b: off
    value c: YES
    value d: Disabled


.. index::
    pair: Rules; Boolean

Rules
-----

#.  **Boolean Literals:** A boolean value is created using one of the predefined literals from the list below. All literals are case-insensitive, meaning that any combination of upper or lower case letters is valid.

    .. list-table::
        :header-rows: 1
        :widths: 25 25
    
        *   - True Value
            - False Value
        *   - :text-code:`true`
            - :text-code:`false`
        *   - :text-code:`yes`
            - :text-code:`no`
        *   - :text-code:`on`
            - :text-code:`off`
        *   - :text-code:`enabled`
            - :text-code:`disabled`

Features
--------

.. list-table::
    :header-rows: 1
    :width: 100%
    :widths: 25, 75

    *   -   Feature
        -   Coverage
    *   -   :text-code:`core`
        -   Boolean values are part of the core language.
