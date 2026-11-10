..
    Copyright (c) 2025-2026 Tobias Erbsland - Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

*****
Lists
*****

Validation Rules for lists—*value lists*, *value matrices*, and *section lists*—are
defined in two distinct layers:

* **List-level constraints** — defined in the main node-rules definition and applied
  to the list as a whole (for example, the number of entries or optionality).
* **Entry-level rules** — defined in a ``vr_entry`` subsection (or section list) and
  applied individually to each list entry.

This separation keeps list validation predictable and makes complex structures
easier to reason about.

.. code-block:: erbsland-conf
    :class: validation-rules

    [app.tags]
    type: "ValueList"
    maximum: 10

    [app.tags.vr_entry]
    type: "text"
    minimum: 1
    maximum: 60

    [app.user]
    type: "SectionList"

    [.vr_entry.full_name]
    type: "text"

    [.vr_entry.email]
    type: "text"

.. code-block:: erbsland-conf
    :class: good-example

    [app]
    tags: "red", "orange", "yellow", "green", "blue"

    *[app.user]*
    full_name: "Example User 1"
    email: "user1@example.com"

    *[app.user]*
    full_name: "Example User 2"
    email: "user2@example.com"

About Optionality of Section Lists
==================================

At first glance, the optionality of section lists may appear less intuitive
than for value lists. In practice, however, the rule is exactly the same.

If a node-rules definition declares a list—whether ``ValueList``,
``ValueMatrix``, or ``SectionList``—and it is **not** explicitly marked as
optional, then **at least one entry is required**.

In other words:

* A list definition without ``is_optional: true`` requires at least one entry.
* This rule applies uniformly to value lists, value matrices, and section lists.
* The requirement applies to the *list itself*, not to individual entries.

For section lists, this means that the configuration must contain at least one
corresponding section instance.

In the following minimal example, the ``app.user`` section list must contain at
least one entry because it is not marked as optional.

.. code-block:: erbsland-conf
    :class: validation-rules

    [app.user]
    type: "SectionList"

    [.vr_entry.full_name]
    type: "text"

.. code-block:: erbsland-conf
    :class: bad-example

    [app]
    # ERROR: "app.user" is missing.
    # At least one section entry is required.

If your configuration intentionally allows zero entries, you must explicitly
mark the list definition as optional.

.. code-block:: erbsland-conf
    :class: validation-rules

    [app.user]
    type: "SectionList"
    is_optional: true

    [.vr_entry.full_name]
    type: "text"

.. code-block:: erbsland-conf
    :class: good-example

    [app]
    # VALID: "app.user" is optional and may contain zero entries.

Common Rules for ``vr_entry``
=============================

#.  **Regular Node-Rules Semantics:**
    A ``vr_entry`` definition behaves like a regular :term:`Node-Rules` definition.

    All rules that apply to node-rules definitions—such as constraints, alternatives,
    and documentation fields—also apply to ``vr_entry``.

    The only difference is that the allowed ``type`` values depend on the parent list
    type.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [app.tags]
        type: "ValueList"
        maximum: 10

        [app.tags.vr_entry]
        type: "text"
        minimum: 1
        maximum: 60

#.  **Alternatives Allowed:**
    A ``vr_entry`` definition *may* itself be a section list, enabling the use of
    :doc:`alternatives <alternatives>` for list entries.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [ruler.marks]
        type: "ValueList"
        maximum: 15

        *[.vr_entry]*
        type: "integer"

        *[.vr_entry]*
        type: "float"

#.  **No Defaults and Optionality:**
    A ``vr_entry`` definition *must not* define a default value and *must not* be
    marked as optional.

    A list or matrix itself may define a default value or be marked as optional,
    but individual list entries cannot.

    .. code-block:: erbsland-conf
        :class: bad-validation-rules

        [ruler.marks]
        type: "ValueList"

        [.vr_entry]
        default: 10.0  # ERROR: "default" is not allowed for vr_entry definitions.

    .. code-block:: erbsland-conf
        :class: bad-validation-rules

        [ruler.marks]
        type: "ValueList"

        [.vr_entry]
        is_optional: true  # ERROR: "is_optional" is not allowed for vr_entry definitions.

Rules for Value Lists and Matrices
==================================

Please also refer to :ref:`ref-types-value-lists` for details on how value lists and
value matrices are represented and interpreted.

#.  **Mandatory vr_entry:**
    A node-rules definition for a value list or value matrix *must* include a
    ``vr_entry`` subsection.

    .. code-block:: erbsland-conf
        :class: bad-validation-rules

        [app.tags]
        type: "ValueList"
        maximum: 10

        # ERROR: "app.tags.vr_entry" is missing

#.  **Scalar Entries Only:**
    The ``vr_entry`` definition for a value list or value matrix is limited to
    :term:`scalar values <scalar value>`.

    Nested lists, sections, or structured values are not permitted as list entries.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [server.ports]
        type: "ValueList"
        maximum: 5

        [.vr_entry]
        type: "integer"
        minimum: 1
        maximum: 65534

#.  **Alternatives Are Limited to Scalar Values:**
    If the ``vr_entry`` definition uses :doc:`alternatives <alternatives>`, all
    alternatives *must* define scalar value types.

    .. note::

        Non-scalar alternatives—such as sections—would violate the configuration
        specification and are therefore not permitted.

        Nested lists are defined using ``ValueMatrix`` at the list level.
        In this case, ``vr_entry`` validates individual matrix entries and handles
        nested list structures implicitly through the matrix semantics.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [ruler.marks]
        type: "ValueList"
        maximum: 15

        *[.vr_entry]*
        type: "integer"

        *[.vr_entry]*
        type: "float"

        *[.vr_entry]*
        type: "section"  # ERROR: Alternatives may only contain scalar values.

Rules for Section Lists
=======================

#.  **Mandatory vr_entry:**
    A node-rules definition for a section list *must* include a ``vr_entry``
    subsection.

    The ``vr_entry`` rules describe the structure and constraints of each section
    in the list.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [app.user]
        type: "SectionList"

        [.vr_entry.full_name]
        type: "text"

        [.vr_entry.email]
        type: "text"

#.  **Section-Type Entries:**
    The ``vr_entry`` definition for a section list *must* define a section or a
    section-with-texts.

    Implicit sections are allowed and commonly used.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [app.user]
        type: "SectionList"

        # "vr_entry" is implicitly defined as a section.

        [.vr_entry.full_name]
        type: "text"

        [.vr_entry.email]
        type: "text"

Version History
===============

.. version-changed:: 1.3.1

    Added a section with clarifications about optionality in section lists.