..
    Copyright (c) 2025 Tobias Erbsland - Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

.. include:: _icons.rst

********
Multiple
********

The ``multiple`` constraint requires a node’s value—or its size—to be evenly
divisible by a given number ``n``. In mathematical terms, validation succeeds if::

    value mod n == 0

This constraint applies not only to numeric values, but also to:

* the length of text values,
* the size of byte sequences,
* the number of elements in lists or matrices, and
* the number of child nodes in sections.

Negative values are supported and evaluated using the same rule.

Type Matrix
===========

The following table summarizes how ``multiple`` is interpreted for each node type.

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
        -   Valid only if ``value mod n == 0``.
    *   -   Boolean
        -   |constraint-unsupported|
        -
        -
    *   -   Float
        -   |constraint-supported|
        -   Float
        -   Valid only if ``value mod n == 0`` within a platform-consistent
            floating-point tolerance.
    *   -   Text
        -   |constraint-supported|
        -   Integer
        -   The text length (in Unicode code points) must be a multiple of ``n``.
    *   -   Date
        -   |constraint-unsupported|
        -
        -
    *   -   Time
        -   |constraint-unsupported|
        -
        -
    *   -   DateTime
        -   |constraint-unsupported|
        -
        -
    *   -   Bytes
        -   |constraint-supported|
        -   Integer
        -   The number of bytes must be a multiple of ``n``.
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
        -   The number of list elements must be a multiple of ``n``.
    *   -   ValueMatrix
        -   |constraint-supported|
        -   |   ValueList
            |   Integer
        -   Both dimensions must be multiples of ``n``.
            The first integer applies to rows, the second to columns.
    *   -   Section
        -   |constraint-supported|
        -   Integer
        -   The number of child nodes (when using ``vr_any``) must be a multiple of ``n``.
    *   -   SectionList
        -   |constraint-supported|
        -   Integer
        -   The number of list entries must be a multiple of ``n``.
    *   -   SectionWithTexts
        -   |constraint-supported|
        -   Integer
        -   The number of child nodes (when using ``vr_any``) must be a multiple of ``n``.
    *   -   NotValidated
        -   |constraint-unsupported|
        -
        -

Rules for Multiple
==================

#.  **Modulo Rule:**
    Validation *must* test whether ``value mod n == 0``.

    For example, ``multiple: 8`` allows the values 0, ±8, ±16, and so on.

#.  **Negative Values:**
    Negative values *must* be handled consistently.
    Validation succeeds if the absolute value is divisible by ``n``.

    For example, ``-16`` is valid for ``multiple: 8``.

#.  **Floating-Point Precision:**
    For floating-point values, validators *must* use a platform-consistent
    tolerance when testing for zero remainder.

    This ensures that values such as ``0.9`` validate correctly with
    ``multiple: 0.1`` despite binary rounding differences.

#.  **Length-Based Evaluation:**
    For text values, byte sequences, lists, matrices, and sections, the constraint
    applies to the *length or size* of the node—not to its contents.

Examples
========

Numeric Constraint
------------------

.. code-block:: erbsland-conf
    :class: validation-rules

    [app.buffer_size]
    type: "integer"
    multiple: 1024

.. code-block:: erbsland-conf
    :class: good-example

    [app]
    buffer_size: 4096

.. code-block:: erbsland-conf
    :class: bad-example

    [app]
    buffer_size: 2000  # ERROR: Not a multiple of 1024

Length-Based Constraint
-----------------------

.. code-block:: erbsland-conf
    :class: validation-rules

    [app.key_block]
    type: "bytes"
    multiple: 16

.. code-block:: erbsland-conf
    :class: good-example

    [app]
    key_block: <00 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f>

.. code-block:: erbsland-conf
    :class: bad-example

    [app]
    key_block: <00 01 02 03 04 05 06 07 08>  # ERROR: Length not a multiple of 16
