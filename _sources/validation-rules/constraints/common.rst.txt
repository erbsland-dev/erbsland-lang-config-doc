..
    Copyright (c) 2025 Tobias Erbsland - Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

.. include:: _icons.rst

***********************
Common Constraint Rules
***********************

To simplify constraint semantics and reduce implementation complexity,
Validation Rules define a **uniform mechanism** for:

* **negating constraints**, and
* **attaching custom error messages** to individual constraints.

These mechanisms are shared by all constraints that support them.

.. code-block:: erbsland-conf
    :class: validation-rules

    [server.port]
    type: "integer"
    minimum: 1024
    minimum_error: "System ports are not allowed"

    [app.username]
    type: "text"
    not_starts: "@"  # Negation of the "starts" constraint

.. design-rationale::

    Not all constraints support negation or custom error messages.
    However, using a consistent naming scheme across constraints keeps
    implementations simple and predictable.

    Instead of requiring special handling for each constraint, validators
    only need to recognize name prefixes and suffixes. This significantly
    reduces the already high implementation effort for constraint handling.

Rules for Negating Constraints
==============================

#.  **Negation Prefix:**
    If a constraint name is prefixed with ``not_``, the result of the constraint
    evaluation is logically negated.

    The negated constraint uses the same value and semantics as the original
    constraint.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [server.name]
        type: "text"
        not_starts: "@"  # The name must not start with "@"

#.  **No Combination with Positive Form:**
    A negated constraint *must not* be combined with its non-negated form
    in the same node-rules definition.

    Validators *must* report this as an error.

    .. code-block:: erbsland-conf
        :class: bad-validation-rules

        [server.name]
        type: "text"
        chars: "[a-z]"
        not_chars: "x"  # ERROR: "chars" is already defined

Rules for Custom Constraint Errors
==================================

#.  **Error Suffix:**
    If a constraint name is suffixed with ``_error``, the entry defines a
    custom error message for that specific constraint.

    The message replaces the default error message when the constraint fails.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [server.name]
        type: "text"
        ends: "_server"
        ends_error: "The server name must end with '_server'."

#.  **Corresponding Constraint Required:**
    A custom error message *must* only be defined if the corresponding
    constraint is present.

    Validators *must* report an error if an ``_error`` entry exists without
    its associated constraint.

    .. code-block:: erbsland-conf
        :class: bad-validation-rules

        [server.name]
        type: "text"
        ends_error: "Message..."  # ERROR: "ends" constraint is missing

#.  **Exact Name Matching:**
    The custom error entry *must* use the exact name of the associated
    constraint, including any ``not_`` prefix.

    This ensures an unambiguous mapping between constraints and their
    error messages.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [server.name]
        type: "text"
        not_starts: "@"
        not_starts_error: "The server name must not start with '@'."
