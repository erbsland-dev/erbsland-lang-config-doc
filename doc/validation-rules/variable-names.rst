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

Rules for Variable Names
=======================

#.  **Exclusive Mechanism:**
    ``vr_any`` is the *only* mechanism to define rules for variable names.

#.  **Optional Name Constraints:**
    If no ``vr_name`` subsection is defined, all valid names are accepted.

#.  **Text Semantics:**
    Name constraints in ``vr_name`` follow the same rules as text constraints,
    including support for ``starts``, ``ends``, ``matches``, ``chars``, and
    ``case_sensitive``.

#.  **Scope:**
    Constraints defined in ``vr_name`` apply only to the name itself, not to
    the node’s value or children.
