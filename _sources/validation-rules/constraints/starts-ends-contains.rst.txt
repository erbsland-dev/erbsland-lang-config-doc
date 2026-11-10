..
    Copyright (c) 2025 Tobias Erbsland - Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

.. include:: _icons.rst

*************************
Starts, Ends and Contains
*************************

The ``starts``, ``ends``, and ``contains`` constraints validate whether a text value
begins with, ends with, or contains a specified substring.

These constraints provide a lightweight and portable alternative to regular
expressions and are often sufficient for enforcing simple naming conventions.
They apply **only to text values** and can be combined with the
:doc:`case sensitivity <case-sensitive>` flag.

Type Matrix
===========

The following table summarizes how these constraints apply to different node types.

.. list-table::
    :header-rows: 1
    :class: type-matrix

    *   -   Node Type
        -   S
        -   Value Type
        -   Details
    *   -   Integer
        -   |constraint-unsupported|
        -
        -
    *   -   Boolean
        -   |constraint-unsupported|
        -
        -
    *   -   Float
        -   |constraint-unsupported|
        -
        -
    *   -   Text
        -   |constraint-supported|
        -   |   Text
            |   ValueList[Text]
        -   Constrains the text to start with, end with, or contain one of the
            specified values.
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
        -   |constraint-unsupported|
        -
        -
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

Rules for Starts, Ends and Contains
===================================

#.  **Starts:**
    The ``starts`` constraint succeeds if the text begins with the specified
    substring.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [server.identifier]
        type: "text"
        starts: "id"

    .. code-block:: erbsland-conf
        :class: good-example

        [server]
        identifier: "id5000"  # VALID

#.  **Ends:**
    The ``ends`` constraint succeeds if the text ends with the specified substring.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [server.identifier]
        type: "text"
        ends: "_id"

    .. code-block:: erbsland-conf
        :class: good-example

        [server]
        identifier: "example_id"  # VALID

#.  **Contains:**
    The ``contains`` constraint succeeds if the text includes the specified
    substring anywhere.

    The negated form ``not_contains`` ensures that the substring does *not* appear.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [server.identifier]
        type: "text"
        not_contains: "example"

    .. code-block:: erbsland-conf
        :class: bad-example

        [server]
        identifier: "one_example_id"  # ERROR: Must not contain "example"

#.  **Multiple Values (OR Semantics):**
    If a value list is provided, the constraint is satisfied if the text matches
    *any* of the listed values.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [server.identifier]
        type: "text"
        starts: "server_", "client_"

    .. code-block:: erbsland-conf
        :class: good-example

        [server]
        identifier: "server_001"

    .. design-rationale::

        OR semantics keep these constraints simple and predictable.
        More complex matching scenarios that require logical AND combinations
        or pattern grouping should instead be implemented using
        ``matches`` (regular expressions).

#.  **Case Sensitivity:**
    By default, comparisons are case-insensitive.

    This behavior applies equally to ``starts``, ``ends``, and ``contains`` and
    can be changed using the ``case_sensitive`` flag.
    See :doc:`case-sensitive` for details.

Example
=======

.. code-block:: erbsland-conf
    :class: validation-rules

    [api.function]
    type: "text"
    starts: "fn"
    ends: "(x)", "(x,y)"

.. code-block:: erbsland-conf
    :class: good-example

    [api]
    function: "fnAdd(x,y)"  # VALID

.. code-block:: erbsland-conf
    :class: bad-example

    [server]
    function: "sub(x)"  # ERROR: Must start with "fn"
