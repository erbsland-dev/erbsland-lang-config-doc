**************
Variable Names
**************

A common configuration pattern is to use **names as keys**.

Typical examples include:

* user accounts, where the *user name* identifies a section,
* feature flags or tags, where the *tag name* identifies a value,
* dynamically named resources such as queues, profiles, or environments.

For these use cases, Validation Rules provide the reserved name ``vr_any``.
It acts as a **placeholder for arbitrary names** in the validated document.

Using ``vr_any`` allows you to define rules for nodes whose names are not known
in advance, while still enforcing structure and constraints.

The ``vr_any`` placeholder is also the *only* mechanism that allows validation
of **text-names**, which are intended by :term:`ELCL` to be used as keys.

Basic Use of ``vr_any``
=======================

Used on its own, ``vr_any`` matches any valid name (or text-name) at that
position in the document tree.

.. code-block:: erbsland-conf
    :class: validation-rules

    [user.vr_any]
    type: "section"

    [user.vr_any.age]
    type: "integer"

This definition allows an arbitrary number of user sections, each with an
``age`` value.

.. code-block:: erbsland-conf
    :class: good-example

    [user.alice]
    age: 32

    [user.benjamin]
    age: 48

    [user.charlotte]
    age: 56

Constraining Variable Names with ``vr_name``
=============================================

To restrict which names are allowed, a ``vr_name`` subsection can be added
under ``vr_any``. The ``vr_name`` section behaves like a regular text
node-rules definition and supports the same constraints.

This allows you to enforce naming conventions, prefixes, formats, or lengths.

.. code-block:: erbsland-conf
    :class: validation-rules

    [user.vr_any]
    type: "section"

    [.vr_name]
    starts: "u_"

    [user.vr_any.age]
    type: "integer"

Only user names starting with ``u_`` are now allowed.

.. code-block:: erbsland-conf
    :class: good-example

    [user.u_alice]
    age: 32

    [user.u_benjamin]
    age: 48

    [user.u_charlotte]
    age: 56

Variable Names as Values
========================

Variable names can also be constrained to *carry values themselves*.
This is useful when the name is the primary identifier and the value
provides metadata such as a priority, weight, or order.

In this example, tag names are used as keys and their integer values
represent priorities:

.. code-block:: erbsland-conf
    :class: validation-rules

    [tags]
    type: "section"

    [tags.vr_any]
    type: "integer"

.. code-block:: erbsland-conf
    :class: good-example

    [tags]
    feature: 1
    bugfix: 2
    enhancement: 3
    documentation: 4
    misc: 5

Rules for ``vr_any``
====================

#.  **Same Semantics as Node-Rules Definitions:**
    ``vr_any`` behaves like a regular :doc:`node-rules definition <node-rules>`.

    It requires a ``type`` field and supports constraints, documentation fields,
    and alternatives. The only difference is that it does *not* restrict the
    name of the matched node in the document tree.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [numbers.vr_any]
        type: "integer"

    .. code-block:: erbsland-conf
        :class: good-example

        [numbers]
        one: 1
        two: 2
        three: 3

    .. code-block:: erbsland-conf
        :class: validation-rules

        *[numbers.vr_any]*
        type: "integer"

        *[numbers.vr_any]*
        type: "float"

    .. code-block:: erbsland-conf
        :class: good-example

        [numbers]
        half: 0.5
        one: 1
        pi: 3.14159265359

#.  **Text Names Allowed:**
    ``vr_any`` can be used to validate text-names, which are intended by
    :term:`ELCL` to be used as keys.

    This makes ``vr_any`` the only mechanism that allows validation of nodes
    addressed by text-names.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [user.vr_any]
        type: "section_with_texts"

        [user.vr_any.name]
        type: "text"

    .. code-block:: erbsland-conf
        :class: good-example

        [users."User 1"]
        name: "Peter"

        [users."User 2"]
        name: "Peter"

#.  **No Default Value and No Optionality:**
    A ``vr_any`` node-rules definition *must not* define a default value and
    *must not* be marked as optional.

    .. design-rationale::

        ``vr_any`` definitions are inherently optional, as they allow zero or
        more values or sections. Marking them as optional would therefore be
        redundant and potentially confusing.

        Default values are not permitted because, when no matching nodes are
        present, there is no well-defined name to which a default value could
        be assigned.

    .. code-block:: erbsland-conf
        :class: bad-validation-rules

        [user.vr_any]
        type: "integer"
        default: 0   # ERROR: default value not allowed for vr_any

    .. code-block:: erbsland-conf
        :class: bad-validation-rules

        [user.vr_any]
        type: "integer"
        is_optional: true   # ERROR: vr_any must not be optional

#.  **Zero to Many Values:**
    A ``vr_any`` node-rules definition allows zero or more values or sections,
    unless additional cardinality constraints are defined.

    .. note::

        Use constraints such as ``minimum`` and ``maximum`` to restrict the
        number of allowed values.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [numbers.vr_any]
        type: "integer"

    .. code-block:: erbsland-conf
        :class: good-example

        [numbers]
        # Zero values are valid.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [numbers]
        type: "section"
        minimum: 1

        [numbers.vr_any]
        type: "integer"

    .. code-block:: erbsland-conf
        :class: bad-example

        [numbers]
        # ERROR: minimum is 1, but no values are present.

#.  **Name Constraints:**
    An optional ``vr_name`` subsection can be defined to restrict the set of
    allowed names.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [users.vr_any]
        type: "integer"

        [.vr_name]
        starts: "u_"

    .. code-block:: erbsland-conf
        :class: good-example

        [users]
        u_001: 1
        u_002: 2

    .. code-block:: erbsland-conf
        :class: bad-example

        [users]
        alice: 1   # ERROR: name does not start with "u_"

#.  **Unrestricted Names by Default:**
    If no ``vr_name`` subsection is defined, all valid names are accepted.

    In this case, only the naming rules defined by :term:`ELCL` apply.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [users.vr_any]
        type: "integer"

    .. code-block:: erbsland-conf
        :class: good-example

        [users]
        any_valid_name: 1
        is_accepted: 2


Rules for ``vr_name``
=====================

#.  **Type Is Locked to Text:**
    The type of ``vr_name`` *must* be ``Text``.

    The ``type`` field is optional, but if present, it *must* be set to ``Text``.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [users.vr_any]
        type: "integer"

        [.vr_name]   # Omitting the 'type' field is allowed for vr_name
        starts: "u_"

    .. code-block:: erbsland-conf
        :class: validation-rules

        [users.vr_any]
        type: "integer"

        [.vr_name]
        type: "text"
        starts: "u_"

    .. code-block:: erbsland-conf
        :class: bad-validation-rules

        [users.vr_any]
        type: "integer"

        [.vr_name]
        type: "integer"  # ERROR: type must be "text"

#.  **Text Semantics:**
    Constraints defined in ``vr_name`` follow the same semantics as text
    constraints.

    This includes support for ``starts``, ``ends``, ``matches``, ``chars``,
    and ``case_sensitive``.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [user]
        type: "section_with_texts"

        [user.vr_any]
        type: "integer"

        [user.vr_any.vr_name]
        case_sensitive: yes
        starts: "u_"
        ends: "_x"
        chars: "(a-z)", "[_]"

#.  **Scope:**
    Constraints defined in ``vr_name`` apply *only* to the node name itself.

    They do not affect the node’s value, its children, or any nested validation
    rules.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [user]
        type: "section_with_texts"

        [user.vr_any]
        type: "text"

        [user.vr_any.vr_name]
        case_sensitive: yes
        starts: "u_"
        ends: "_x"
        chars: "(a-z)", "[_]"

    .. code-block:: erbsland-conf
        :class: good-example

        [user]
        u_alice: "unrestricted"
        u_bob_x: "vr_name does not affect this text"

