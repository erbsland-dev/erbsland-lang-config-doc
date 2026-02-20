..
    Copyright (c) 2025-2026 Tobias Erbsland - Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

*********
Templates
*********

Templates provide a mechanism to define **reusable node-rules definitions**.
They allow you to centralize commonly used constraints and apply them consistently
across multiple nodes.

Templates are defined as subsections or section lists of the reserved section
``vr_template`` at the document root. The name of each subsection is the identifier
used by ``use_template`` in node-rules definitions.

.. code-block:: erbsland-conf
    :class: validation-rules

    [vr_template.interface]
    type: "section"

    [.address]
    type: "text"
    default: "localhost"

    [.protocol]
    type: "text"
    default: "https"

    [.port]
    type: "integer"
    default: 443

    [server.interface]
    use_template: "interface"

    [client.interface]
    use_template: "interface"

    [.port]
    default: 9000

In this example, the same template is applied to both ``server.interface`` and
``client.interface``, while the client overrides the default port.

Rules for Templates
===================

#.  **Templates in Root:**
    Templates *must* be defined as subsections or section lists under ``vr_template``
    at the document root.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [vr_template.interface]
        type: "integer"

    .. code-block:: erbsland-conf
        :class: validation-rules

        *[vr_template.service]*
        type: "integer"
        minimum: 1
        maximum: 65534

        *[vr_template.service]*
        type: "text"
        in_list: "http", "https", "smtp"

#.  **Root Restriction:**
    The name ``vr_template`` *must* only appear at the document root and *must*
    define a section with regular names.

    .. code-block:: erbsland-conf
        :class: bad-example

        [server.vr_template.interface]  # ERROR: "vr_template" must be in the document root
        type: "integer"

#.  **Template Identifier:**
    The name of a subsection or section list under ``vr_template`` is the identifier
    used to reference the template via ``use_template``.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [vr_template.port]  # Defines the template "port"
        type: "integer"
        minimum: 1
        maximum: 65534

        [server.port]
        use_template: "port"  # References the template "port"

#.  **Same Structure as Node-Rules:**
    A template is defined exactly like a regular node-rules definition.
    All rules that apply to node-rules definitions also apply to templates.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [vr_template.port]
        type: "integer"
        minimum: 1
        maximum: 65534

#.  **Direct Type Definition Only:**
    A template *must* define its own ``type`` and *must not* reference another
    template using ``use_template``.

    Templates cannot be composed or chained.

    .. code-block:: erbsland-conf
        :class: bad-example

        [vr_template.port]
        type: "integer"
        minimum: 1
        maximum: 65534

        [vr_template.client_port]
        use_template: "port"   # ERROR: Templates must not reference other templates.
        minimum: 1024

#.  **Copy Semantics:**
    When a template is applied using ``use_template``, its contents are
    **copied** into the node-rules definition at the usage location.

    From that point on, the node-rules definition behaves exactly as if the copied
    rules had been written inline.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [vr_template.port]
        type: "integer"
        minimum: 1
        maximum: 65534

        [server.port]
        use_template: "port"  # Contains a copy of the "port" template.

#.  **Overrides Allowed:**
    Constraints defined at the usage location *overwrite* constraints copied from
    the template.

    This allows templates to define sensible defaults while still permitting
    context-specific adjustments.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [vr_template.port]
        type: "integer"
        minimum: 1
        maximum: 65534

        [server.port]
        use_template: "port"
        minimum: 1024  # Overrides the "minimum" from the template.

#.  **Alternatives Cannot Be Overwritten:**
    Templates defined as alternatives (using section lists) *must not* be
    overwritten or extended at the usage location.

    When a template defines multiple alternatives, the complete set of alternatives
    is copied as-is. You cannot modify individual constraints inside an alternative
    or add additional alternatives.

    .. design-rationale::

        Alternatives represent a deliberate, self-contained choice between
        multiple valid rule structures. Allowing partial overrides would require
        addressing individual alternatives explicitly, which would significantly
        increase complexity and reduce readability.
        For clarity and safety, alternative-based templates are therefore treated
        as atomic and reusable building blocks.

    .. code-block:: erbsland-conf
        :class: bad-example

        *[vr_template.service]*
        type: "integer"
        minimum: 1

        *[vr_template.service]*
        type: "text"
        minimum: 1

        [server.port]
        use_template: "service"
        minimum: 1024   # ERROR: Alternatives from a template must not be modified or extended.

#.  **Order of Overrides and Additions:**
    Constraints from a template are merged with additional constraints in a predictable and stable order:

    *   Constraint overrides *replace* the corresponding constraint **at the same position**
        where the original constraint appeared in the template.
    *   New constraints that do not exist in the template are **appended to the end**
        of the resulting constraint list.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [vr_template.port]
        type: "integer"
        minimum: 1
        maximum: 65534

        [server.port]
        use_template: "port"
        minimum: 10       # Overrides the template's 'minimum' and keeps its original position.
        not_equals: 80    # New constraint, appended to the end of the constraint list.

#.  **Template Validation Timing:**
    Templates are validated **only when they are used** by a node-rules definition.
    During validation, a template is checked together with the node-rules definition
    that applies it.

    Templates that are never referenced via ``use_template`` are ignored entirely and
    may contain errors without affecting validation.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [vr_template.with_error]
        type: "integer"
        unknown_field: 10    # This error is ignored because the template is unused.

        [main.port]
        type: "integer"
