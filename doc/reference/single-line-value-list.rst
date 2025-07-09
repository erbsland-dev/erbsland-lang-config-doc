..
    Copyright (c) 2024-2025 Tobias Erbsland - Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

.. _ref-single-line-value-list:
.. index::
    single: Value List

Single-Line Value Lists
=======================

Single-line values can always be combined into a list using a comma (:cp:`,`) as a separator.

.. code-block:: bnf

    sl_value_or_list    ::= sl_value (sl_list_separator sl_value)+ 
    sl_list_separator   ::= spacing COMMA spacing

.. code-block:: text
    :class: good-example

    value
    value , value
    value , value , value , value , ...

- In the EBNF syntax above, the symbol ``sl_value`` is described in :ref:`ref-named-value`.
- The symbol ``spacing`` is described in :ref:`ref-spacing`.


.. index::
    pair: Rules; Value List
    single: Single-Line Value List

Single-Line Value List Rules
----------------------------

#.  **Commas Form a List:** Values separated by commas (:cp:`,`) form a value list.

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        value list: 1, 2, 3, 4, 5

#.  **Spacing Around Separator:** Optional spacing is allowed before and after the comma.

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        value list 1:   7 ,   1 ,   9
        value list 2: 105 , 722 , 817

#.  **No Prefixing/Trailing Comma:** A value list must not start or end with a comma.

    .. code-block:: erbsland-conf
        :class: bad-example
        :force:

        [main]
        value list 1: ,1 , 2      # ERROR! Value list must not start with comma
        value list 2: 1, 2,       # ERROR! Value list must not end with comma.

#.  **No Consecutive Commas:** Consecutive commas, with no value between them, are *not allowed*.

    .. code-block:: erbsland-conf
        :class: bad-example
        :force:

        [main]
        value list: 1, , 2        # ERROR! Consecutive commas are not allowed.

#.  **No Multi-line Values:** Multi-line values are *not allowed* in single-line value lists.

    .. code-block:: erbsland-conf
        :class: bad-example
        :force:

        [main]
        value list: """
            text
            """, """        # ERROR! Multi-line values are not allowed in lists.
            text
            """

Example
~~~~~~~

.. code-block:: erbsland-conf
    :class: good-example

    [main]
    first list: 1, 2, 3, 4     # Value lists are created by separating values with commas.
    second list: 1  , 2  ,  3  # Spacing is allowed around the comma.

Features
--------

.. list-table::
    :header-rows: 1
    :width: 100%
    :widths: 25, 75

    *   -   Feature
        -   Coverage
    *   -   :text-code:`value-list`
        -   The syntax outlined in this chapter is part of the standard feature *value lists*.

Errors
------

.. list-table::
    :header-rows: 1
    :width: 100%
    :widths: 25, 75

    *   -   Error Code
        -   Causes
    *   -   :text-code:`Syntax`
        -   |   Raised if a single line value list contains a multi-line value, such as multi-line text.
            |   Raised if a value list contains prefixed, trailing, or consecutive commas.

