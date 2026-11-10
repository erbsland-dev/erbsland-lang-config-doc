..
    Copyright (c) 2025 Tobias Erbsland - Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

*********************
Node-Rules Definition
*********************

A section in a Validation Rules document whose name ends in a regular name or in
``vr_any`` defines the rules for one or more nodes in the validated document.
Such sections are called :term:`Node-Rules` definitions.

Each node-rules definition specifies the expected type of a node, its constraints,
optional default values, and additional metadata such as documentation or dependency
information.

.. code-block:: erbsland-conf
    :class: validation-rules

    [server.name]
    type: "text"
    title: "The name of this server entry"
    description: """
        Specify a unique name for the server, used in logs and diagnostics.
        Only letters, digits, underscores, and hyphens are allowed, up to 60 characters.
        """
    minimum: 1
    maximum: 60
    allowed_chars: "[-A-Za-z0-9_]"

Rules for a Node-Rules Definition
=================================

#.  **Type Requirement:**
    Each node-rules definition *must* have exactly one effective type.
    The type is provided either by:

    * a local ``type`` field, or
    * a ``use_template`` reference that defines a type.

    A node-rules definition must not define both.
    See :doc:`types` for the exact rules governing ``type`` and ``use_template``.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [client.port]
        type: "integer"   # Either "type" or "use_template" is required.

#.  **Defaults:**
    Node-rules definitions for a :term:`scalar value` or a value list *may* define a
    default value using the ``default`` field.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [client.port]
        type: "integer"
        default: 9000

    .. note::

        When a default is applied, only the ``type`` constraint is validated.
        All other constraints are skipped for the default value.

        See :doc:`defaults-and-optionality` for details.

#.  **Optionality:**
    A node-rules definition *may* explicitly mark a node as optional using
    ``is_optional: yes``.

    Optional nodes are not required to exist in the configuration document.
    Optionality can also be achieved implicitly by providing a ``default`` value.

    See :doc:`defaults-and-optionality` for details.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [client]
        type: "section"
        is_optional: yes

#.  **Documentation Fields:**
    A node-rules definition *may* provide documentation metadata using the
    ``title`` and ``description`` fields.

    These fields do not influence validation.
    They are intended for tooling, user interfaces, and generated documentation.
    Parsers *should* expose these values through their APIs.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [client.port]
        type: "integer"
        title: "Port on the server to connect to"
        description: """
            The numeric port where the client connects to the server.
            """
        default: 9000

#.  **Constraints:**
    A node-rules definition can define zero or more constraints that further restrict
    valid values or structures.

    Constraints are evaluated according to the rules defined in
    :doc:`evaluation-order`.

    See :doc:`constraints/index` for the complete list of available constraints,
    including negated constraints and custom error messages.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [client.port]
        type: "integer"
        minimum: 1         # Constraint on the value
        maximum: 65534     # Further constraint

#.  **Custom Error:**
    A node-rules definition *may* define a custom error message for the entire node
    using the ``error`` field.

    This message is used when validation of the node fails and no more specific
    constraint-level error applies.

    See :doc:`diagnostics` for details.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [client.port]
        type: "integer"
        minimum: 1
        maximum: 65534
        error: "Please specify a valid port from 1–65534."

#.  **List Entries:**
    Node-rules definitions for value lists or section lists *must* describe their
    elements using a ``vr_entry`` subsection or section list.

    The ``vr_entry`` rules define the structure and constraints of each list element.

    See :doc:`lists` for details.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [main.tags]
        type: "ValueList"

        [main.tags.vr_entry]
        type: "text"
        minimum: 1

#.  **Dependencies:**
    A node-rules definition *may* express dependencies between child nodes using a
    ``vr_dependency`` section list.

    Dependencies are validated in a later validation stage and can express logical
    relationships such as mutual inclusion or exclusion.

    See :doc:`dependencies` for details.

    .. code-block:: erbsland-conf
        :class: validation-rules

        # ...

        [client]
        type: "section"

        *[client.vr_dependency]*
        mode: "xnor"
        source: "username"
        target: "password"

        # ...

#.  **Variable Names:**
    Node-rules definitions that end in ``vr_any`` *may* restrict the allowed variable
    names using a ``vr_name`` subsection.

    This allows rule authors to constrain the names of dynamically created child
    nodes.

    See :doc:`variable-names` and :doc:`reserved` for details.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [user.vr_any]
        type: "section"

        [user.vr_any.vr_name]
        maximum: 60

#.  **Case Sensitivity:**
    A node-rules definition *may* enable case-sensitive evaluation for text-based
    constraints using the ``case_sensitive`` field.

    If not enabled, text comparisons are case-insensitive by default.

    See :doc:`constraints/case-sensitive` for details.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [app.message]
        type: "text"
        case_sensitive: yes
        starts: "message:"

#.  **Secrets:**
    A node-rules definition *may* mark a node as secret using the ``is_secret`` field.

    Secret nodes should be redacted or masked in diagnostics, logs, and error
    messages.

    See :doc:`security` for details.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [client.secret]
        type: "text"
        is_secret: yes
