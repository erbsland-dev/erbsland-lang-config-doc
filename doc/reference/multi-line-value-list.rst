..
    Copyright (c) 2024 Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

.. _ref-multi-line-value-list:
.. index::
    single: Multi-line Value List
    single: Value List

Multi-line Value Lists
======================

Multi-line value lists are supported and follow a specific structure. Each list must begin on the line immediately following the value separator, and each entry in the list is prefixed by an asterisk (:cp:`*`). The list ends when a line without an asterisk or indentation is encountered.

.. code-block:: bnf

    ml_value_list       ::= (indentation_pattern ASTERISK spacing sl_value_or_list end_of_line)+

.. code-block:: text
    :class: good-example

    name :
        * value
        * value
        * value

- In the EBNF syntax above, the symbol ``end_of_line`` is defined in :ref:`ref-comment`.
- The symbol ``spacing`` is described in :ref:`ref-spacing`.
- The symbol ``indentation_pattern`` is explained in :ref:`ref-spacing`.
- The symbol ``sl_value_or_list`` is described in :ref:`ref-single-line-value-list`.


.. index::
    pair: Rules; Multi-line Value List
    single: Multi-line Value List

Multi-line Value List Rules
---------------------------

#.  **Asterisk Prefix:** Each entry in a multi-line list must be prefixed with an asterisk (:cp:`*`).

    .. code-block:: erbsland-conf
        :class: good-example
        
        [main]
        value:
            * "one"
            * "two"
            * "three"

#.  **Must Start on the Next Line:** A multi-line list *must* start on the line immediately following the value separator; it cannot begin on the same line as the separator.

    .. code-block:: text
        :class: bad-example

        [main]
        value: * "one"     # ERROR! The list must start on the next line.
            * "two"
            * "three"

#.  **Indentation Required:** Each entry in the list must be indented by at least one space or tab character before the asterisk.

    .. code-block:: text
        :class: bad-example

        [main]
        value:
        * "one"     # ERROR! The list entry must be indented.
        * "two"
        * "three"

#.  **Consistent Indentation Pattern:** The indentation pattern, including the exact combination of spaces and tabs, must be consistent across all list entries. For more details, refer to :ref:`ref-indentation-pattern`.

    .. code-block:: text
        :class: bad-example

        [main]
        value:
        ⎵⎵⎵⎵* "one"
        →    * "two"      # ERROR! Inconsistent indentation pattern.
        ⎵⎵⎵⎵* "three"

#.  **No Multi-line Values Allowed:** Multi-line values are *not allowed* in multi-line value lists. Each value must be on a single line.

    .. code-block:: text
        :class: bad-example

        [main]
        value:
            * """    # ERROR! Multi-line values are not allowed.
            Text
            """

#.  **A Value is Required:** Each entry must have a value after the asterisk. Empty list entries are not allowed.

    .. code-block:: text
        :class: bad-example

        [main]
        value:
            * 105
            *         # ERROR! A value is required.
            * 254

#.  **No Empty Lines:** There must be no empty lines between the name and the first entry, or between two entries. Lines containing only spaces, tabs, and/or comments are treated as empty lines.

    .. code-block:: text
        :class: bad-example

        [main]
        value:
                       # ERROR! Empty lines are not allowed.
            * 105
                       # ERROR! Empty lines are not allowed.
            * 254

Example
~~~~~~~

.. code-block:: erbsland-conf
    :class: good-example

    [main]
    first list:               # Multi-line lists must start on the next line after the separator.
        * "one"               # Each list entry starts with an indented asterisk.
        * "two"               # The indentation pattern must be consistent for all entries.
        * "three"             # No empty lines are allowed between entries.
    second list:
        *   1,   2,   3       # Single-line values can also be part of a multi-line list.
        *   4,   5,   6
        *   7,   8,   9

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
        -   |   No value follows the asterisk in a multi-line list.
            |   A multi-line value list contains a multi-line value, such as multi-line text.
            |   The multi-line value list is interrupted by an empty line.
            |   The multi-line value list starts on the same line as the value separator.
    *   -   :text-code:`Indentation`
        -   |   No space or tab character is present before the asterisk.
            |   The indentation pattern does not match the first entry in the multi-line value list.
