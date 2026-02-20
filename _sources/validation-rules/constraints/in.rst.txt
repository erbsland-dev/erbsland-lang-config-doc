..
    Copyright (c) 2025 Tobias Erbsland - Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

.. include:: _icons.rst

**
In
**

The ``in`` constraint restricts a node’s value to a **predefined set of allowed
values**. It is most commonly used to limit text or numeric nodes to a controlled
vocabulary or a fixed set of constants.

When applied to text nodes, the behavior of this constraint can be influenced by the
:doc:`case sensitivity <case-sensitive>` flag.

Type Matrix
===========

The following table summarizes which node types support the ``in`` constraint and
how membership is evaluated.

.. list-table::
    :header-rows: 1
    :class: type-matrix

    *   -   Node Type
        -   S
        -   Value Type
        -   Details
    *   -   Integer
        -   |constraint-supported|
        -   ValueList
        -   Valid only if the integer value appears in the list of integers.
    *   -   Boolean
        -   |constraint-unsupported|
        -
        -
    *   -   Float
        -   |constraint-supported|
        -   ValueList
        -   Valid only if the floating-point value appears in the list.
            Equality *must* be evaluated using a platform-consistent strategy
            (for example, with a tolerance that accounts for IEEE rounding).
    *   -   Text
        -   |constraint-supported|
        -   ValueList
        -   Valid only if the text matches one of the listed text values.
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
        -   ValueList
        -   Valid only if the byte sequence matches one of the listed byte sequences.
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
        -   |constraint-unsupported|
        -
        -
    *   -   ValueMatrix
        -   |constraint-unsupported|
        -
        -
    *   -   Section
        -   |constraint-unsupported|
        -
        -
    *   -   SectionList
        -   |constraint-unsupported|
        -
        -
    *   -   SectionWithTexts
        -   |constraint-unsupported|
        -
        -
    *   -   NotValidated
        -   |constraint-unsupported|
        -
        -

Rules
=====

#.  **List Membership:**
    The value of the node *must* exactly match one of the values listed in ``in``.

#.  **Type Alignment:**
    Each value listed in ``in`` *must* have the same type as the constrained node.

    Mixing types (for example, constraining a text node with integers) is invalid
    and *must* be rejected by the validator.

#.  **No Duplicate Entries:**
    Each value in the ``in`` list *must* be unique.

    Duplicate entries provide no additional meaning and *must* be treated as an
    error in the validation rules document.

#.  **Floats and Equality:**
    For floating-point values, equality *must* be determined using a
    platform-consistent strategy that accounts for precision and rounding behavior.

    This ensures that values such as ``0.1`` behave consistently across different
    validators and platforms.

#.  **Case Sensitivity:**
    Text comparisons using ``in`` are case-insensitive by default.

    This behavior can be changed using the ``case_sensitive`` flag.
    See :doc:`case-sensitive` for details.

Example
=======

The following example restricts ``mode`` to one of three predefined text values:

.. code-block:: erbsland-conf
    :class: validation-rules

    [server.mode]
    type: "text"
    in: "idle", "scanning", "connecting"

.. code-block:: erbsland-conf
    :class: good-example

    [server]
    mode: "scanning"

.. code-block:: erbsland-conf
    :class: bad-example

    [server]
    mode: "shutdown"  # ERROR: Must be one of "idle", "scanning", "connecting"
