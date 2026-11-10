..
    Copyright (c) 2025 Tobias Erbsland - Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

************************
Defaults and Optionality
************************

Validation Rules provide two distinct mechanisms for handling missing elements in a
parsed configuration document:

* **Defaults** — supply a predefined value when a :term:`scalar value` or
  :term:`value list` is missing.
* **Optionality** — explicitly mark a node as optional so it may be omitted entirely,
  along with all of its child nodes.

While both mechanisms address missing data, they serve different purposes and have
different semantics.

.. list-table::
    :header-rows: 1
    :widths: 20, 40, 40
    :class: feature-table

    *   -   Feature
        -   Defaults
        -   Optionality
    *   -   Applies to
        -   :term:`Scalar values <scalar value>`, :term:`Value lists <value list>`
        -   Any node (values, lists, sections)
    *   -   Purpose
        -   Supply a predefined value if the node is missing
        -   Allow the node (and its children) to be omitted entirely
    *   -   Child Nodes
        -   Defaults affect only the node itself
        -   Optionality cascades to all child nodes
    *   -   Constraints
        -   Default values bypass constraints (except ``type``)
        -   Constraints apply only if the node exists
    *   -   Interaction
        -   Must not be combined with ``is_optional``
        -   Must not be combined with ``default``
    *   -   Common Use
        -   Avoid repetitive program logic for common values
        -   Support optional features or configuration sections

.. code-block:: erbsland-conf
    :class: validation-rules

    [api.host]
    type: "text"
    default: "127.0.0.1"

    [api.port]
    type: "integer"
    default: 9000

    [client]
    type: "section"
    is_optional: yes

    [client.name]
    type: "text"

.. code-block:: erbsland-conf
    :class: good-example

    [api]  # The "api" section is required
    # "host" and "port" use their default values
    # The "client" section is optional

.. design-rationale::

    Defaults are intentionally limited to scalar values and value lists to keep their
    behavior simple, predictable, and easy to implement.

    While it might appear useful to provide defaults for entire sections or complete
    configurations, doing so would blur the boundary between **validation** and
    **configuration derivation**. Applications that require a default configuration
    should provide one explicitly (for example, by shipping a base configuration
    file or embedding defaults in code) and then validate user-provided overrides.

    Defaults in Validation Rules are therefore designed as a lightweight, node-level
    convenience. They eliminate repetitive application logic while also serving as
    machine-readable documentation of commonly used values.

Rules for Defaults
==================

#.  **Default Field:**
    A node-rules definition may specify a ``default`` value that is used if the node
    is missing from the configuration document.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [api.host]
        type: "text"
        default: "127.0.0.1"

#.  **Allowed Node Types:**
    Defaults *may only* be defined for :term:`scalar values <scalar value>` and
    :term:`value lists <value list>`.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [article.tags]
        type: "ValueList"
        default: "article", "news"

        [article.tags.vr_entry]
        type: "text"
        minimum: 1
        maximum: 60

#.  **Type Matching:**
    A default value *must* match the declared ``type`` of the node-rules definition.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [api.port]
        type: "integer"
        default: 9000

#.  **Constraints Ignored:**
    Default values are *not* validated against local constraints, except for
    the ``type`` constraint.

    This allows placeholder or empty values to be supplied even if they would not
    be valid as explicit user input.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [server.name]
        type: "text"
        minimum: 1
        default: ""   # Allowed, even though the minimum length is 1

#.  **No Combination with Optionality:**
    A node-rules definition *must not* combine ``default`` with ``is_optional``.

    Validators *must* report this as an error.

    .. code-block:: erbsland-conf
        :class: bad-validation-rules

        [server.name]
        type: "text"
        is_optional: yes
        default: "example"  # ERROR: default and is_optional must not be combined

Rules for Optional Nodes
========================

#.  **Optional Flag:**
    Any node may be marked as optional by setting ``is_optional: yes``.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [client]
        type: "section"
        is_optional: yes

        [client.name]
        type: "text"

#.  **Optionality Includes Child Nodes:**
    If an optional node does not exist, none of its child nodes may exist either.

    Even if child nodes are normally required, they are only validated if the parent
    node itself exists.

    .. code-block:: erbsland-conf
        :class: good-example

        # An empty document is valid because "client" is optional

#.  **No Defaults for Missing Optional Nodes:**
    Defaults are *not* applied when an optional node is missing.

    Child nodes are neither created nor validated unless the optional parent node
    exists.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [client]
        type: "section"
        is_optional: yes

        [client.name]
        type: "text"
        default: "unknown"

    .. code-block:: erbsland-conf
        :class: good-example

        # Empty document — "client" does not exist,
        # so "client.name" is not created.

    .. code-block:: erbsland-conf
        :class: good-example

        [client]
        # "client" exists, so "client.name" is created
        # with the default value "unknown"
