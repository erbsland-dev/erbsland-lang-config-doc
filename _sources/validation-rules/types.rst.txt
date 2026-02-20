..
    Copyright (c) 2025 Tobias Erbsland - Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

*****
Types
*****

Every :term:`Node-Rules` definition requires exactly one effective ``type`` entry.
The type constrains the node to a specific structural or scalar form and determines
which constraints are applicable.

Instead of defining the type directly, a node-rules definition may also reference
a template using ``use_template``. In that case, the template provides the effective
``type`` value.

.. code-block:: erbsland-conf
    :class: validation-rules

    [server.name]
    type: "text"   # Constrains "server.name" to a text value.

See :doc:`node-rules` for additional requirements that apply to all node-rules
definitions.

Rules for the Type Constraint
=============================

#.  **Type Requirement:**
    Every node-rules definition *must* define exactly one effective type, either
    directly or indirectly.

    The only exception is a ``vr_name`` definition, which is always defined as a
    ``text`` node.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [server.name]
        type: "text"

#.  **Indirect Definition via Template:**
    The ``type`` entry may be provided indirectly using ``use_template``, which
    references a template that defines a type.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [vr_template.port]
        type: "integer"
        minimum: 1
        maximum: 65534

        [server.port]
        use_template: "port"

    .. note::

        Templates require a ``type`` entry, as they cannot inherit from another template.

#.  **Exclusive Requirement:**
    A node-rules definition *must not* define both ``type`` and ``use_template``.

    .. code-block:: erbsland-conf
        :class: bad-validation-rules

        [vr_template.port]
        type: "integer"
        minimum: 1
        maximum: 65534

        [server.port]
        type: "integer"
        use_template: "port"  # ERROR: Both entries are defined.

#.  **Value Lists and Matrices Accept Scalar Values:**
    The type ``ValueList`` and ``ValueMatrix`` *must* accept a single :term:`scalar value` and treat it
    as a list containing exactly one element. See :ref:`ref-types-value-lists` for details.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [app.tags]
        type: "ValueList"

        [app.tags.vr_entry]
        type: "text"

    .. code-block:: erbsland-conf
        :class: good-example

        [app]
        tags: "example"  # Treated as a list with one element.

#.  **Type Case Insensitivity and Normalization:**
    Type identifiers are **case-insensitive** and are normalized according to
    the same rules as :term:`names<Name>` in :term:`ELCL`.

    This means comparisons are performed on the normalized form of the
    identifier. For example, ``DateTime``, ``datetime``, and ``DATETIME``
    all refer to the same type.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [app.a]
        type: "INTEGER"

        [app.b]
        type: "integer"

        [app.c]
        type: "Integer"

#.  **Type Aliases:**
    An implementation *may* define additional type identifiers as aliases
    for existing types, separating words with underscores.

    For example, an implementation could define ``date_time`` as an alias
    for ``DateTime``.


Type Identifiers
================

The following table lists all valid type identifiers in a *readable form*.
Unlike reserved names, which are always shown in their normalized form, type
identifiers are written here in **CamelCase** for clarity.

In actual documents, type identifiers are **case-insensitive** and follow the
same normalization rules as :term:`names<Name>` in :term:`ELCL`.
For example, ``DateTime``, ``datetime``, and ``DATETIME`` are all equivalent.

.. list-table::
    :header-rows: 1
    :class: identifier-table

    *   -   Identifier
        -   Description
    *   -   |   Integer
            |   Boolean
            |   Float
            |   Text
            |   Date
            |   Time
            |   DateTime
            |   Bytes
            |   TimeDelta
            |   RegEx
        -   Constrains the node to a :term:`scalar value` of the given type.
    *   -   Value
        -   Allows any :term:`scalar value`.
            This type does *not* include value lists or sections.
            It covers all scalar types listed above.
    *   -   ValueList
        -   Constrains the node to either a single *scalar value* or a *value list*.
            List elements can be validated using ``vr_entry``.
            If omitted, the type ``Value`` is implicitly used for all entries.
    *   -   ValueMatrix
        -   Constrains the node to either a single *scalar value*, a *value list* or a *nested value list*.
            Elements of the lists can be validated using ``vr_entry``.
            If omitted, the type ``Value`` is implicitly used for all matrix entries.
    *   -   Section
        -   Constrains the node to a *section with names*.
            See :ref:`ref-section` for details.
    *   -   SectionList
        -   Constrains the node to a *section list*.
            A ``vr_entry`` rule *must* be provided to define the node-rules for each
            section in the list.
    *   -   SectionWithTexts
        -   Constrains the node to a *section with texts*.
            See :ref:`ref-text-name` for details.
    *   -   NotValidated
        -   Ignores this node and all child nodes.
            Nodes of this type are not validated.
            They are neither required to exist nor forbidden.

.. _ref-types-value-lists:

About Value Lists and Matrices
------------------------------

In Validation Rules, the distinction between a *scalar value*, a *list*, and a
*matrix* describes the **validation intent**, not the concrete syntax used in the
configuration document.

A list or matrix with a single element is always valid, even if it is represented
as a single scalar value in the document.

Value List Example
~~~~~~~~~~~~~~~~~~

The following example defines ``ports`` as a value list:

.. code-block:: erbsland-conf
    :class: validation-rules

    [server.ports]
    type: "ValueList"
    maximum: 5

    [.vr_entry]
    type: "integer"

.. code-block:: erbsland-conf
    :class: good-example

    [server]
    ports: 80, 443   # A classic value list.

.. code-block:: erbsland-conf
    :class: good-example

    [server]
    ports: 80        # Also valid: a list with one element.

.. code-block:: erbsland-conf
    :class: good-example

    [server]
    ports:           # A multi-line list with two elements.
        *   80
        *   443

.. code-block:: erbsland-conf
    :class: bad-example

    [server]
    ports:           # ERROR: A list of lists is not a valid ValueList.
        *   80, 443
        *   8080, 8443

    # By default, list elements have the type "Value", which only allows scalar values.

Value Matrix Example
~~~~~~~~~~~~~~~~~~~~

A value matrix represents a list of lists. The following example defines a matrix
called ``magic_numbers``:

.. code-block:: erbsland-conf
    :class: validation-rules

    [main.magic_numbers]
    type: "ValueMatrix"
    maximum: 5, 5

    [.vr_entry]
    type: "integer"

.. code-block:: erbsland-conf
    :class: good-example

    [main]
    magic_numbers:
        *   1,   9,  -3,  4
        *   14, 15,  19, 27
        *   53, -6,  14, 34

.. code-block:: erbsland-conf
    :class: good-example

    [main]
    magic_numbers: 1  # A valid matrix with one row and one column.

.. code-block:: erbsland-conf
    :class: good-example

    [main]
    # Three rows and one column.
    magic_numbers: 1, 2, 3

.. code-block:: erbsland-conf
    :class: good-example

    [main]
    # The same matrix using a different list syntax.
    magic_numbers:
        *   1
        *   2
        *   3

The API of a configuration parser *should* provide uniform access to values as
lists or matrices, regardless of how they are represented in the configuration
document.


Version History
===============

.. version-changed:: 1.3.1

    Added an explicit rules for ``type`` comparison and aliases with underscores.


