..
    Copyright (c) 2024 Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

.. _ref-named-value:
.. index::
    single: Value
    single: Named Values

Named Values
============

In :term:`ELCL`, each section can have zero or more named values assigned to it. Named values follow a specific syntax that supports various data types and list structures.

The basic syntax consists of the value name, followed by a value separator, then the value assignment, and is finally terminated by an end-of-line sequence. The end-of-line sequence may include optional spacing, an optional comment, and a line break.

.. code-block:: bnf

    value_line          ::= value_name value_separator value_assignment end_of_line

    value_name          ::= meta_name | name | text_name
    meta_name           ::= AT_SIGN name

    value_separator     ::= spacing (COLON | EQUAL) spacing

.. code-block:: text

    name : value [#comment]

The value assignment can appear directly after the value separator on the same line, or it can be indented on the next line. While both forms support single-line value lists, multi-line lists can only begin when the value is placed on the next line.

.. code-block:: bnf

    value_assignment    ::= value_on_same_line | value_on_next_line

    value_on_same_line  ::= ml_value | sl_value_or_list
    value_on_next_line  ::= end_of_line (ml_value_list | indentation_pattern (ml_value | sl_value_or_list))

.. code-block:: text

    name : value [#comment]
    ... or ...
    name : [#comment]
        value [#comment]

The distinction between single-line and multi-line values is important because multi-line values cannot be used in lists.

.. code-block:: bnf

    sl_value            ::= datetime | date | time | float | integer |
                            boolean | text_value | code | binary | regex | time_delta
    ml_value            ::= multi_line_text | multi_line_code |
                            multi_line_binary | multi_line_regex

- In the EBNF syntax above, the symbol ``end_of_line`` is described in :ref:`ref-comment`.
- Single-line and multi-line value lists, with the symbols ``sl_value_or_list`` and ``ml_value_list`` are described in :ref:`ref-single-line-value-list` and :ref:`ref-multi-line-value-list`.
- The symbols for specific value types, like ``datetime``, are described in later chapters.


.. index::
    pair: Rules; Named Values

Named Value Rules
-----------------

#.  **Start at the Beginning:** The name of a value, whether a regular name or a text name, *must* always start at the beginning of a line.

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        value 1: 123       # OK!

    .. code-block:: erbsland-conf
        :class: bad-example
        :force:

        [main]
            value 2: 123   # ERROR! The value name must start at the beginning of the line.

#.  **Value Separator:** A value separator, either a colon (:cp:`:`) or an equal sign (:cp:`=`), must follow the name. Optional spaces are allowed around the separator.

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        value 1: 123       # OK!
        value 2   =  123   # OK!

#.  **Value on the Same or Next Line:** The value must either follow the separator on the same line or start on the next line.

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        value 1: 123       # OK!
        value 2:
            123            # OK!

#.  **Indentation Required:** If the value starts on the next line, it *must* be indented by at least one space or tab character.

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        value:
            123           # OK!

    .. code-block:: text
        :class: bad-example
        :force:

        [main]
        value:
        123               # ERROR! The value is not indented.

#.  **No Empty Line:** There must be no empty line between the name and its value. Lines that contain only spaces, tabs and/or a comment are treated as empty lines.

    .. code-block:: text
        :class: bad-example
        :force:

        [main]
        value:
                            # Empty line (spaces, tabs and/or a comment)
            123             # ERROR! No empty line is allowed.

#.  **Handling Name Conflicts:** The guidelines for resolving name conflicts are detailed in :ref:`ref-name-path`.

Example
~~~~~~~

.. code-block:: erbsland-conf

    [main]
    first value: 123             # Simple case: name and value on the same line.
    second value   : 123         # Extra spacing is allowed between the name and separator.
    third value:                 # Value can start on the next line.
        123                      # Indentation is required when the value continues on the next line.
    # Comments or lines with only spacing are allowed between value assignments.
    fourth value: 123

    fifth value: 123

    [text values]
    "text" : 123                 # Quoted names follow the same rules as unquoted names.


Features
--------

.. list-table::
    :header-rows: 1
    :width: 100%
    :widths: 25, 75

    *   -   Feature
        -   Coverage
    *   -   :text-code:`core`
        -   Regular names, meta values and the value assignment are part of the core language.
    *   -   :text-code:`text-names`
        -   Text names are a standard feature.
    *   -   :text-code:`multi-line`
        -   Multi-line values are a standard feature.
    *   -   :text-code:`value-list`
        -   Value lists are a standard feature.
    *   -   :text-code:`float`
        -   Floating point values are a standard feature.
    *   -   :text-code:`date-time`
        -   Date-time values are a standard feature.
    *   -   :text-code:`code`
        -   Code text values are a standard feature.
    *   -   :text-code:`byte-data`
        -   Byte-data values are a standard feature.
    *   -   :text-code:`regex`
        -   Regular expression values are an advanced feature. 
    *   -   :text-code:`time-delta`
        -   Time delta values are an advanced feature.


Errors
------

.. list-table::
    :header-rows: 1
    :width: 100%
    :widths: 25, 75

    *   -   Error Code
        -   Causes
    *   -
        -   All errors from invalid names. See :ref:`ref-name`.
    *   -   :text-code:`NameConflict`
        -   Raised if a value name causes a name conflict as described in :ref:`ref-name-conflict`.
    *   -   :text-code:`Syntax`
        -   |   No value separator follows the name or text name.
            |   No value follows a value separator on the same or the next line.
    *   -   :text-code:`Indentation`
        -   |   There is spacing before the name.
            |   There is no spacing before the value if the value is defined on the next line.