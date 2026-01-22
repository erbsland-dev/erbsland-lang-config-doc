..
    Copyright (c) 2025 Tobias Erbsland - Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

**************
Document Model
**************

This section defines the fundamental structure and interpretation rules for
Validation Rules (:term:`ELCL-VR`) documents. These rules describe how validation
rules map onto a parsed configuration document and how the resulting *value tree*
is interpreted during validation.

Rules for Validation Rules Documents
------------------------------------

#.  **Valid ELCL Document:**
    A Validation Rules document *must* itself be a valid :term:`ELCL` document and
    support all features provided by the parser.

    Validation rules use the same syntax and structural concepts as regular
    configuration documents.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [server.name]
        type: "text"

#.  **Sections Define Nodes:**
    Each section in a Validation Rules document *defines* the rules for exactly one
    :term:`Node` in the validated document.

    The section name represents the :term:`Name Path` of the node being validated.
    When validation is applied to only a subtree of a configuration, the name path
    is interpreted as *relative* to the validated root.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [server.name]
        type: "text"

    The example above defines rules for the node at ``server.name``, which corresponds
    to the following configuration:

    .. code-block:: erbsland-conf
        :class: good-example

        [server]
        name: "example"

    See :doc:`node-rules` for details about the contents of a node-rules definition.

#.  **Implicit Ancestors:**
    Elements of a name path that are not explicitly defined are treated as
    *implicit* ancestor sections.

    To reduce redundancy in validation rules documents, missing path elements
    implicitly create node-rules definitions for **required sections with names**.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [server.name]
        type: "text"
        default: "unknown"

    In this example, the section ``server`` is not explicitly defined in the rules.
    It is therefore implicitly created as a required section with names.

    .. code-block:: erbsland-conf
        :class: bad-example

        # ERROR: The required section "server" is missing.

#.  **Existence Requirement:**
    If a node-rules definition has no ``default`` value and is not explicitly marked
    as optional, the corresponding node *must* exist in the configuration document.

    By default, every node defined by validation rules is required to appear in the
    value tree. A node can be made optional in exactly one of the following ways:

    * by providing a ``default`` value, or
    * by setting ``is_optional: yes``.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [server.name]
        type: "text"

    .. code-block:: erbsland-conf
        :class: good-example

        [server]
        name: ""  # VALID: The node exists, even if the value is empty.

#.  **Closed by Default:**
    A configuration document *must not* contain nodes for which no matching
    node-rules definition exists.

    A Validation Rules document is considered authoritative for the validated
    document or :term:`Value Tree`. As a result, any value, section, or list that
    is not explicitly covered by validation rules is forbidden.

    .. important::

        Nodes are only exempt from the closed-by-default rule if they are explicitly
        covered by a node-rules definition of type ``NotValidated``.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [server.name]
        type: "text"

    .. code-block:: erbsland-conf
        :class: bad-example

        [server]
        name: "example"

        [client]  # ERROR: "client" is not defined in the validation rules.
