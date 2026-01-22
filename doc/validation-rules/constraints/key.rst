..
    Copyright (c) 2025 Tobias Erbsland - Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

.. include:: _icons.rst

***
Key
***

The ``key`` constraint restricts a value to one of the **keys stored in a named
index**. These indexes are declared using ``vr_key``, as described in
:doc:`../keys-and-references`.

This constraint is primarily used to enforce **referential integrity** within a
configuration document—for example, ensuring that a reference in one section
corresponds to a defined identifier in another section.

Type Matrix
===========

The following table summarizes how the ``key`` constraint applies to different
node types.

.. list-table::
    :header-rows: 1
    :class: type-matrix

    *   -   Node Type
        -   S
        -   Value Type
        -   Details
    *   -   Integer
        -   |constraint-supported|
        -   |   Text
            |   ValueList[Text]
        -   Constrains the integer value to reference a key from one of the
            specified indexes.
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
        -   Constrains the text value to reference a key from one of the
            specified indexes.
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

Rules for Key
=============

#.  **Index Reference:**
    The ``key`` constraint takes one or more text values.
    Each value names an index that the node value is allowed to reference.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [app.start_filter]
        type: "text"
        key: "filter"

#.  **Index Must Exist:**
    Each referenced index *must* be defined elsewhere in the same Validation Rules
    document using ``vr_key``.

    .. code-block:: erbsland-conf
        :class: validation-rules

        *[vr_key]*
        name: "filter"
        key: "filter.identifier"

        [filter]
        type: "SectionList"

        [filter.vr_entry.identifier]
        type: "text"

        [app.start_filter]
        type: "text"
        key: "filter"

#.  **Multiple Indexes (OR Semantics):**
    If multiple index names are specified, the value is valid if it exists in
    *any* of the listed indexes.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [app.start]
        type: "text"
        key: "remote_action", "local_action"

#.  **Type Alignment:**
    The type of the referencing node *must* match the type of the keys stored in
    the referenced index.

    For example, an index built from text identifiers cannot be referenced by a
    node of type ``date``.

    .. code-block:: erbsland-conf
        :class: bad-validation-rules

        *[vr_key]*
        name: "filter"
        key: "filter.identifier"

        [filter]
        type: "SectionList"

        [filter.vr_entry.identifier]
        type: "text"

        [app.start_filter]
        type: "date"
        key: "filter"   # ERROR: Referenced keys are text, not date

#.  **Case Sensitivity:**
    Key comparisons are case-insensitive by default.

    If the :doc:`case-sensitive` flag is set on the referencing node, the key match
    *must* be performed case-sensitively.

    .. code-block:: erbsland-conf
        :class: good-example

        *[filter]*
        identifier: "first"

        *[filter]*
        identifier: "second"

        [app]
        start_filter: "First"  # VALID: matches "first" (case-insensitive)

Example
=======

In the following example, ``start_filter`` must reference one of the identifiers
defined in the ``filter`` section list:

.. code-block:: erbsland-conf
    :class: validation-rules

    *[vr_key]*
    name: "filter"
    key: "filter.identifier"

    [filter]
    type: "SectionList"

    [filter.vr_entry.identifier]
    type: "text"

    [app.start_filter]
    type: "text"
    key: "filter"

.. code-block:: erbsland-conf
    :class: good-example

    *[filter]*
    identifier: "first"

    *[filter]*
    identifier: "second"

    [app]
    start_filter: "first"

.. code-block:: erbsland-conf
    :class: bad-example

    *[filter]*
    identifier: "first"

    *[filter]*
    identifier: "second"

    [app]
    start_filter: "third"  # ERROR: "third" is not defined
