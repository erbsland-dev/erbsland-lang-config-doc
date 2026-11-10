..
    Copyright (c) 2025 Tobias Erbsland - Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

.. include:: _icons.rst

***********************
The Case Sensitive Flag
***********************

By default, all constraints that perform text comparisons operate in a
**case-insensitive** manner.

If the flag ``case_sensitive: yes`` is specified in a node-rules definition,
all applicable text comparisons for that node become **case-sensitive**.

.. rubric:: Exceptions

-   The ``matches`` constraint is exempt from this rule, as its behavior is entirely
    defined by the regular expression engine in use.
-   The ``chars`` and ``not_chars`` constraints are also exempt from this rule, as they are always case-sensitive.

Rules for the Case Sensitive Flag
=================================

#.  **Default Behavior:**
    Text comparisons *must* be case-insensitive unless explicitly overridden.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [api.name]
        type: "text"
        starts: "system"

    .. code-block:: erbsland-conf
        :class: good-example

        [api]
        name: "System"  # VALID: case-insensitive match

#.  **Extent of Case Folding:**
    Implementations *must* support case folding for the ASCII range
    (``a-z`` / ``A-Z``).

    * Single-character Unicode case folding is *recommended*.
    * Full Unicode case folding is *optional*.

    Implementations *should* clearly document the exact extent of their
    case-handling behavior.

#.  **Boolean Flag:**
    The ``case_sensitive`` field requires a boolean value.

    * If omitted, the default value is ``no``.
    * Explicitly specifying ``case_sensitive: no`` *must* be supported.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [api.name]
        type: "text"
        starts: "system"
        case_sensitive: no  # Redundant, but valid

#.  **Effect of Enabling Case Sensitivity:**
    If ``case_sensitive: yes`` is set, all applicable text constraints in the
    node-rules definition *must* be evaluated case-sensitively.

    -   The flag does *not* affect ``matches`` constraints, as its behavior is entirely
        defined by the regular expression engine in use.
    -   The flag does *not* affect ``chars`` or ``not_chars`` constraints, which are
        always case-sensitive by definition.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [api.name]
        type: "text"
        starts: "system"
        case_sensitive: yes

    .. code-block:: erbsland-conf
        :class: bad-example

        [api]
        name: "System"  # ERROR: uppercase "S" does not match in case-sensitive mode

.. design-rationale::

    Case-insensitive comparison is the default because most configuration values
    (such as identifiers, modes, or keywords) are not intended to be case-sensitive.

    The ``case_sensitive`` flag provides an explicit and localized way to enforce
    strict casing rules where required, without complicating constraint semantics
    or validator implementations.
