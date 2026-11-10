..
    Copyright (c) 2025 Tobias Erbsland - Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

.. include:: _icons.rst

*******
Version
*******

The ``version``, ``minimum_version``, and ``maximum_version`` constraints allow
node-rules definitions to be **conditionally enabled or disabled** depending on
the version of the validation context.

The version number is *not* read from the configuration document itself.
Instead, it is explicitly provided to the validator by the application.

Unlike constraints such as ``minimum`` or ``maximum``, which validate configuration
*values*, version constraints operate at the **definition level**.
If a version constraint does not match, the entire node-rules definition is ignored
as if it were never declared.

Type Matrix
===========

The following table summarizes support for version constraints across node types.

.. list-table::
    :header-rows: 1
    :class: type-matrix

    *   -   Node Type
        -   S
        -   Value Type
        -   Details
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
            |   Value
            |   ValueList
            |   ValueMatrix
            |   Section
            |   SectionList
            |   SectionWithTexts
            |   NotValidated
        -   |constraint-supported|
        -   |   Integer
            |   ValueList[Integer]
        -   Constraints are evaluated against the version number supplied to
            the validator, not against configuration values.

Rules for Version Constraints
=============================

#.  **Value Type:**
    All version constraints use integer values.

    * ``version`` accepts either a single integer or a list of integers.
    * ``minimum_version`` and ``maximum_version`` accept exactly one integer.

#.  **Exact Version Match:**
    ``version`` passes only if the validator’s version number equals the specified value.

    If a list of integers is provided, the constraint passes if the version matches
    *any* value in the list (OR semantics).

    All version values in the list *must* be unique.

#.  **Version Ranges:**

    * ``minimum_version`` passes if the validator’s version is **greater than or equal to** the specified value.
    * ``maximum_version`` passes if the validator’s version is **less than or equal to** the specified value.

#.  **Combining Version Constraints:**
    When multiple version constraints are present, they are combined using **AND semantics**.

    Example:
    ``version: 1, 2, 3`` combined with ``minimum_version: 4`` matches *no* version.

#.  **Ignored Definitions:**
    If any version constraint fails, the entire node-rules definition is ignored.
    It behaves exactly as if it were not present in the Validation Rules document.

#.  **Error Messages:**
    Custom error messages for version constraints are *not* supported.
    Attempting to define one *must* result in a parser error.

    .. design-rationale::

        Version constraints exist to manage schema evolution, not to produce
        validation errors.

        Ignoring non-matching definitions makes it possible to support
        backward- and forward-compatible rule sets within a single document,
        without complicating validation logic or error reporting.

Examples
========

Schema Evolution
----------------

In the following example, ``port`` may be defined either as an integer or as a named
text value. Text-based ports were introduced in **schema version 2**:

.. code-block:: erbsland-conf
    :class: validation-rules

    *[server.port]*
    type: "integer"
    minimum: 1
    maximum: 65534

    *[server.port]*
    type: "text"
    in: "http", "https", "smtp", "smtps"
    minimum_version: 2

Good Examples
-------------

.. code-block:: erbsland-conf
    :class: good-example

    [server]
    port: 8080  # VALID in all versions

.. code-block:: erbsland-conf
    :class: good-example

    [server]
    port: "https"  # VALID only in version 2 or higher
