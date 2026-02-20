.. include:: constraints/_icons.rst

*****************
Constraint Matrix
*****************

This matrix provides a compact overview of **which constraints are applicable
to which node types**.

It is intended as a **quick reference** for rule authors.
For precise semantics, edge cases, and value-type requirements,
always refer to the individual constraint documentation.

Legend
======

* |constraint-supported| — The constraint is defined and meaningful for this node type.
* |constraint-unsupported| — The constraint must not be used with this node type.

.. important::

    “Supported” only indicates that a constraint *may* be used with a given type.
    It does **not** imply that all value forms of the constraint are valid.
    For example, some constraints accept different value types depending on context.

Constraint Applicability Matrix
===============================

.. list-table::
    :header-rows: 1
    :class: constraint-matrix

    *   -   Type → / Constraint ↓
        -   Integer
        -   Boolean
        -   Float
        -   Text
        -   Date
        -   Time
        -   DateTime
        -   Bytes
        -   TimeDelta
        -   RegEx
        -   Value
        -   Value Lists [#valuelists]_
        -   Sections [#sections]_

    *   -   |   chars
            |   not_chars
        -   |constraint-unsupported|
        -   |constraint-unsupported|
        -   |constraint-unsupported|
        -   |constraint-supported|
        -   |constraint-unsupported|
        -   |constraint-unsupported|
        -   |constraint-unsupported|
        -   |constraint-unsupported|
        -   |constraint-unsupported|
        -   |constraint-unsupported|
        -   |constraint-unsupported|
        -   |constraint-unsupported|
        -   |constraint-unsupported|

    *   -   equals
        -   |constraint-supported|
        -   |constraint-supported|
        -   |constraint-supported|
        -   |constraint-supported|
        -   |constraint-unsupported|
        -   |constraint-unsupported|
        -   |constraint-unsupported|
        -   |constraint-supported|
        -   |constraint-unsupported|
        -   |constraint-unsupported|
        -   |constraint-unsupported|
        -   |constraint-supported|
        -   |constraint-supported|

    *   -   in
        -   |constraint-supported|
        -   |constraint-unsupported|
        -   |constraint-supported|
        -   |constraint-supported|
        -   |constraint-unsupported|
        -   |constraint-unsupported|
        -   |constraint-unsupported|
        -   |constraint-supported|
        -   |constraint-unsupported|
        -   |constraint-unsupported|
        -   |constraint-unsupported|
        -   |constraint-unsupported|
        -   |constraint-unsupported|

    *   -   key
        -   |constraint-supported|
        -   |constraint-unsupported|
        -   |constraint-unsupported|
        -   |constraint-supported|
        -   |constraint-unsupported|
        -   |constraint-unsupported|
        -   |constraint-unsupported|
        -   |constraint-unsupported|
        -   |constraint-unsupported|
        -   |constraint-unsupported|
        -   |constraint-unsupported|
        -   |constraint-unsupported|
        -   |constraint-unsupported|

    *   -   matches
        -   |constraint-unsupported|
        -   |constraint-unsupported|
        -   |constraint-unsupported|
        -   |constraint-supported|
        -   |constraint-unsupported|
        -   |constraint-unsupported|
        -   |constraint-unsupported|
        -   |constraint-unsupported|
        -   |constraint-unsupported|
        -   |constraint-unsupported|
        -   |constraint-unsupported|
        -   |constraint-unsupported|
        -   |constraint-unsupported|

    *   -   |   minimum
            |   maximum
        -   |constraint-supported|
        -   |constraint-unsupported|
        -   |constraint-supported|
        -   |constraint-supported|
        -   |constraint-supported|
        -   |constraint-unsupported|
        -   |constraint-supported|
        -   |constraint-supported|
        -   |constraint-unsupported|
        -   |constraint-unsupported|
        -   |constraint-unsupported|
        -   |constraint-supported|
        -   |constraint-supported|

    *   -   multiple
        -   |constraint-supported|
        -   |constraint-unsupported|
        -   |constraint-supported|
        -   |constraint-supported|
        -   |constraint-unsupported|
        -   |constraint-unsupported|
        -   |constraint-unsupported|
        -   |constraint-supported|
        -   |constraint-unsupported|
        -   |constraint-unsupported|
        -   |constraint-unsupported|
        -   |constraint-supported|
        -   |constraint-supported|

    *   -   |   starts
            |   ends
            |   contains
        -   |constraint-unsupported|
        -   |constraint-unsupported|
        -   |constraint-unsupported|
        -   |constraint-supported|
        -   |constraint-unsupported|
        -   |constraint-unsupported|
        -   |constraint-unsupported|
        -   |constraint-unsupported|
        -   |constraint-unsupported|
        -   |constraint-unsupported|
        -   |constraint-unsupported|
        -   |constraint-unsupported|
        -   |constraint-unsupported|

    *   -   |   version
            |   minimum_version
            |   maximum_version
        -   |constraint-supported|
        -   |constraint-supported|
        -   |constraint-supported|
        -   |constraint-supported|
        -   |constraint-supported|
        -   |constraint-supported|
        -   |constraint-supported|
        -   |constraint-supported|
        -   |constraint-supported|
        -   |constraint-supported|
        -   |constraint-supported|
        -   |constraint-supported|
        -   |constraint-supported|

Notes
=====

* Version constraints apply to **node-rules definitions**, not to configuration
  values themselves. They therefore appear as supported for all node types.
* Constraints affecting **entry counts** (e.g. ``minimum``, ``equals``,
  ``multiple``) apply to lists and sections only when those nodes represent
  collections.
* Constraints not listed here (such as ``case_sensitive`` or ``is_optional``)
  are **flags**, not value constraints, and are therefore intentionally excluded
  from this matrix.

.. [#valuelists] Including ``ValueList`` and ``ValueMatrix``.
.. [#sections] Including ``Section``, ``SectionList``, and ``SectionWithTexts``.
