..
    Copyright (c) 2025-2026 Tobias Erbsland - Erbsland DEV. https://erbsland.dev
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

        # ...

        [app.start_filter]
        type: "text"
        key: "filter"

    .. code-block:: erbsland-conf
        :class: validation-rules

        # ...

        [app.start_action]
        type: "text"
        key: "local_action_id", "remote_action_id"

#.  **Index Must Exist:**
    Each referenced index *must* be defined and visible within *the same
    Validation Rules branch* using ``vr_key``.

    .. code-block:: erbsland-conf
        :class: validation-rules

        *[vr_key]*
        name: "filter"
        key: "filter.vr_entry.identifier"

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
        key: "filter.vr_entry.identifier"

        [filter]
        type: "SectionList"

        [filter.vr_entry.identifier]
        type: "text"

        [app.start_filter]
        type: "date"
        key: "filter"   # ERROR: Referenced keys are text, not date

#.  **Case Sensitivity:**
    Key comparison semantics are determined exclusively by the
    case-sensitivity configuration of the referenced index.

    Any :doc:`case_sensitive <case-sensitive>` flag defined on the
    referencing node is ignored for the purpose of key resolution.

    .. code-block:: erbsland-conf
        :class: validation-rules

        *[vr_key]*
        name: "filter"
        key: "filter.vr_entry.identifier"
        case_sensitive: false

        [filter]
        type: "SectionList"

        [filter.vr_entry.identifier]
        type: "text"

        [app.start_filter]
        type: "text"
        case_sensitive: true
        key: "filter"

    .. code-block:: erbsland-conf
        :class: good-example

        *[filter]*
        identifier: "first"

        *[filter]*
        identifier: "second"

        [app]
        start_filter: "First"
        # VALID: matches "first"
        # The index is case-insensitive.
        # The referencing node's case_sensitive flag is ignored.

#.  **Index Scope Is Hierarchical:**
    Indexes defined in sibling branches are not visible to the
    referencing node.

    An index is resolved by searching upward in the Validation Rules
    tree from the referencing node. Only indexes defined in the same
    branch or in ancestor branches are visible.

    .. code-block:: erbsland-conf
        :class: bad-validation-rules

        [server.connections]
        type: "SectionList"

        # ...

        *[server.vr_key]*
        name: "connection_id"
        key: "connections.vr_entry.id"

        [app.main_connection]
        type: "text"
        key: "connection_id"  # ERROR: No such index in this scope

#.  **Nearest Ancestor Resolution:**
    If multiple indexes with the same ``name`` exist in accessible
    branches, the index defined in the nearest ancestor branch
    is used.

    Index resolution proceeds upward from the referencing node
    until a matching index name is found. Once found, that index
    is used and the search stops.

    In the following example, two indexes named ``id`` are defined.
    The reference resolves to the index defined at ``server.vr_key``,
    because it is closer in the tree than the index defined at
    the document root.

    .. code-block:: erbsland-conf
        :class: validation-rules

        # ...

        *[vr_key]*
        name: "id"
        key: "log.vr_entry.id"

        [server.connections]
        type: "SectionList"

        *[server.vr_key]*
        name: "id"
        key: "connections.vr_entry.id"

        # ...

        [server.filter.vr_entry.connection_id]
        type: "text"
        key: "id"   # Resolves to 'server.vr_key'


Example
=======

In the following example, ``start_filter`` must reference one of the identifiers
defined in the ``filter`` section list:

.. code-block:: erbsland-conf
    :class: validation-rules

    *[vr_key]*
    name: "filter"
    key: "filter.vr_entry.identifier"

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

Version History
===============

.. version-changed:: 1.3.0

    Clarified that key comparison behavior is determined exclusively
    by the referenced index.

    The ``case_sensitive`` setting of the referencing node is ignored.
    Uniqueness checks and ``key`` constraint comparisons now consistently
    follow the case-sensitivity defined by the index.

