..
    Copyright (c) 2025 Tobias Erbsland - Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

.. include:: _icons.rst

*******************
Minimum and Maximum
*******************

The ``minimum`` and ``maximum`` constraints restrict the allowed range or size of a
node. Both constraints are **inclusive**, meaning the boundary values themselves are
considered valid.

Depending on the node type, these constraints apply to numeric values, textual
lengths, collection sizes, or structural dimensions.

Type Matrix
===========

The following table summarizes which node types support ``minimum`` and ``maximum``
and how the constraint values are interpreted.

.. list-table::
    :header-rows: 1
    :class: type-matrix

    *   -   Node Type
        -   S
        -   Value Type
        -   Details
    *   -   Integer
        -   |constraint-supported|
        -   Integer
        -   Constrains the minimum and maximum allowed integer value.
    *   -   Boolean
        -   |constraint-unsupported|
        -
        -
    *   -   Float
        -   |constraint-supported|
        -   Float
        -   Constrains the minimum and maximum floating-point value.
            If *any* bound is defined, ``NaN`` is disallowed.
            If a bound excludes positive or negative infinity, ``+Inf`` or ``-Inf``
            is disallowed accordingly.
    *   -   Text
        -   |constraint-supported|
        -   Integer
        -   Constrains the number of Unicode code points (characters).
    *   -   Date
        -   |constraint-supported|
        -   Date
        -   Constrains the earliest and/or latest valid date.
    *   -   Time
        -   |constraint-unsupported|
        -
        -
    *   -   DateTime
        -   |constraint-supported|
        -   DateTime
        -   Constrains the earliest and/or latest valid date-time.
    *   -   Bytes
        -   |constraint-supported|
        -   Integer
        -   Constrains the number of bytes.
    *   -   TimeDelta
        -   |constraint-unsupported|
        -
        -
    *   -   RegEx
        -   |constraint-unsupported|
        -
        -
    *   -   Value
        -   |constraint-unsupported|
        -
        -
    *   -   ValueList
        -   |constraint-supported|
        -   Integer
        -   Constrains the minimum and maximum number of list elements.
    *   -   ValueMatrix
        -   |constraint-supported|
        -   |   ValueList
            |   Integer
        -   Constrains the minimum and maximum number of rows and columns.
            The first integer applies to rows, the second to columns.
    *   -   Section
        -   |constraint-supported|
        -   Integer
        -   Constrains the number of child entries when using ``vr_any``.
    *   -   SectionList
        -   |constraint-supported|
        -   Integer
        -   Constrains the number of entries in the section list.
    *   -   SectionWithTexts
        -   |constraint-supported|
        -   Integer
        -   Constrains the number of child entries when using ``vr_any``.
    *   -   NotValidated
        -   |constraint-unsupported|
        -
        -

Rules for Minimum and Maximum
=============================

#.  **Inclusive Boundaries:**
    Both ``minimum`` and ``maximum`` are inclusive.
    A value equal to the specified boundary is valid.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [server.min_port]
        type: "integer"
        minimum: 1
        maximum: 65534

        [server.max_port]
        type: "integer"
        minimum: 1
        maximum: 65534

    .. code-block:: erbsland-conf
        :class: good-example

        [server]
        min_port: 1      # VALID: equals minimum
        max_port: 65534  # VALID: equals maximum

#.  **Type-Specific Semantics:**
    The value type of ``minimum`` and ``maximum`` *must* match the semantic meaning
    of the node type:

    * For numeric types, the constraint limits the numeric value.
    * For ``text``, the integer represents the number of Unicode code points.
    * For ``bytes``, the integer represents the number of bytes.
    * For lists, sections, and matrices, the integer represents the number of
      contained entries.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [client.username]
        type: "text"
        minimum: 3   # At least 3 characters
        maximum: 12  # At most 12 characters

#.  **Special Values for Floats:**
    If either ``minimum`` or ``maximum`` is defined for a ``float`` node, ``NaN``
    values are not permitted.

    Likewise, ``+Inf`` or ``-Inf`` are not permitted if they fall outside the
    specified bounds.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [client.ratio]
        type: "float"
        minimum: 0.001

    .. code-block:: erbsland-conf
        :class: bad-example

        [client]
        ratio: NaN  # ERROR: NaN is not allowed when bounds are defined

#.  **Matrix Constraints:**
    For ``ValueMatrix`` nodes, ``minimum`` and ``maximum`` accept **two integers**.

    The first integer constrains the number of rows, and the second constrains the
    number of columns.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [app.matrix]
        type: "ValueMatrix"
        minimum: 2, 3   # At least 2 rows and 3 columns
        maximum: 5, 8   # At most 5 rows and 8 columns

#.  **Invalid Combinations:**
    If both ``minimum`` and ``maximum`` are defined, validators *must* verify that
    ``minimum`` ≤ ``maximum``.

    If this condition is violated, the Validation Rules document itself is invalid.

    .. code-block:: erbsland-conf
        :class: bad-validation-rules

        [server.port]
        type: "integer"
        minimum: 100
        maximum: 10  # ERROR: minimum is greater than maximum

Examples
========

Numeric Limits
--------------

.. code-block:: erbsland-conf
    :class: validation-rules

    [server.port]
    type: "integer"
    minimum: 1
    maximum: 65534

.. code-block:: erbsland-conf
    :class: good-example

    [server]
    port: 8080  # VALID

.. code-block:: erbsland-conf
    :class: bad-example

    [server]
    port: -1  # ERROR: Must be in the range 1–65534

Text Limits
-----------

.. code-block:: erbsland-conf
    :class: validation-rules

    [client.username]
    type: "text"
    minimum: 1
    maximum: 32

.. code-block:: erbsland-conf
    :class: good-example

    [client]
    username: "example"  # VALID

.. code-block:: erbsland-conf
    :class: bad-example

    [client]
    username: ""  # ERROR: Must contain at least 1 character
