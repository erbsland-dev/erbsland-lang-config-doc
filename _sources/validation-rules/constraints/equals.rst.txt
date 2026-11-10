..
    Copyright (c) 2025 Tobias Erbsland - Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

.. include:: _icons.rst

******
Equals
******

The ``equals`` constraint requires a node to have an **exact value or size**.
While it may appear simple at first glance, ``equals`` becomes particularly
powerful when combined with :doc:`alternatives <../alternatives>`.

Typical use cases include:

* constraining a node to a single, fixed value,
* enforcing an exact length or size, and
* combining strict matches with more flexible alternatives.

When applied to text values, ``equals`` can be influenced by the
:doc:`case sensitivity <case-sensitive>` setting.

Type Matrix
===========

The following table summarizes how ``equals`` behaves for different node types.

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
        -   Constrains the integer value to the given constant.
    *   -   Boolean
        -   |constraint-supported|
        -   Boolean
        -   Constrains the boolean value to the given constant.
    *   -   Float
        -   |constraint-supported|
        -   Float
        -   Constrains the floating-point value to the given constant.
            Equality *must* be evaluated using a platform-consistent strategy
            (for example, with a tolerance that accounts for IEEE rounding).
    *   -   Text
        -   |constraint-supported|
        -   |   Text
            |   Integer
        -   If a text value is given, constrains the node to that exact text.
            If an integer is given, constrains the text length in Unicode
            code points.
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
        -   |   Bytes
            |   Integer
        -   If a byte sequence is given, constrains the value to that exact
            sequence.
            If an integer is given, constrains the length of the byte sequence.
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
        -   Constrains the list to exactly *n* elements.
    *   -   ValueMatrix
        -   |constraint-supported|
        -   ValueList
        -   Constrains the matrix to exactly *n* rows and *m* columns.
            The first integer applies to rows, the second to columns.
    *   -   Section
        -   |constraint-supported|
        -   Integer
        -   Constrains the number of child entries when using ``vr_any``.
    *   -   SectionList
        -   |constraint-supported|
        -   Integer
        -   Constrains the section list to exactly *n* entries.
    *   -   SectionWithTexts
        -   |constraint-supported|
        -   Integer
        -   Constrains the number of child entries when using ``vr_any``.
    *   -   NotValidated
        -   |constraint-unsupported|
        -
        -

Rules
=====

#.  **Exact Match Required:**
    The value or size of the node *must* be exactly equal to the value specified
    by ``equals``.

#.  **Type Alignment for Scalar Types:**
    For :term:`scalar values <Scalar Value>`, the type of the ``equals`` value
    *must* match the node type.

#.  **Text and Bytes Length Special Case:**
    If an integer is used with a ``text`` or ``bytes`` node, the constraint applies
    to the number of Unicode code points or bytes, respectively—not to the exact
    content.

#.  **List and Matrix Scope:**
    For lists and matrices, ``equals`` constrains the number of elements, rows, or
    columns, not their contents.

#.  **Floats and Equality:**
    For floating-point values, equality *must* be determined using a
    platform-consistent strategy that accounts for precision and rounding issues.

    For example, ``equals: 0.1`` must behave consistently across validators even
    if floating-point representations differ internally.

#.  **Case Sensitivity:**
    Text comparisons using ``equals`` are case-insensitive by default.

    This behavior can be changed using the ``case_sensitive`` flag.
    See :doc:`case-sensitive` for details.

Examples
========

Numeric Example
---------------

In the following example, ``header`` must contain exactly five bytes:

.. code-block:: erbsland-conf
    :class: validation-rules

    [message.header]
    type: "bytes"
    equals: 5

Alternatives Example
--------------------

In this example, ``allowed_action`` may either reference a valid ``action_id`` key
defined elsewhere in the document, or be the literal asterisk ``*``.

The ``equals`` constraint enables the second case:

.. code-block:: erbsland-conf
    :class: validation-rules

    *[app.allowed_action]*
    type: "text"
    key: "action_id"

    *[app.allowed_action]*
    type: "text"
    equals: "*"
