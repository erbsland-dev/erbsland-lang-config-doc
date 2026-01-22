..
    Copyright (c) 2025 Tobias Erbsland - Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

************
Alternatives
************

Alternatives allow you to define **multiple possible node-rules definitions for the
same node**. They are typically used when a configuration element may appear in
different forms, such as different types or distinct structural layouts.

Alternatives are created by defining a **section list** instead of a regular section.
Each entry in the section list represents one alternative.

.. important::

    **Alternatives are evaluated linearly and without backtracking.**

    An alternative is considered fulfilled as soon as its *own constraints* are valid.
    Validation of child nodes happens afterwards.

    If an alternative matches at the top level but a child node fails validation,
    **the entire document validation fails immediately**.
    No further alternatives are considered.

    This behavior is intentional and must be taken into account when designing
    alternative definitions.

.. code-block:: erbsland-conf
    :class: validation-rules

    *[main.interface]*
    type: "text"
    default: "localhost"

    *[main.interface]*
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

.. code-block:: erbsland-conf
    :class: good-example

    [main]
    interface: "10.120.14.17"

.. code-block:: erbsland-conf
    :class: good-example

    [main.interface]
    address: "10.120.14.17"
    protocol: "http"
    port: 80

Rules for Alternatives
======================

#.  **Section List Required:**
    Alternatives *must* be defined using a section list.

    Each section list entry represents one complete alternative.

    .. code-block:: erbsland-conf
        :class: validation-rules

        *[app.service]*
        type: "integer"

        *[app.service]*
        type: "text"
        in: "http", "https", "smtp", "smtps"

#.  **Complete Definitions:**
    Each alternative *must* be a complete and valid node-rules definition.

    .. code-block:: erbsland-conf
        :class: bad-validation-rules

        *[app.threads]*
        type: "integer"
        minimum: 1
        maximum: 100

        *[app.threads]*
        minimum: 20     # ERROR: Missing "type"

#.  **Order of Definition:**
    Alternatives *must* be evaluated strictly in the order in which they are defined.

    .. code-block:: erbsland-conf
        :class: validation-rules

        *[server.initial_response]*
        type: "text"
        starts: "response:{"
        ends: "}"

        *[server.initial_response]*
        type: "text"
        starts: "response:"

#.  **First Match Wins:**
    The first alternative that fulfills all of its own constraints is selected.
    Even if later alternatives would also match, they are not considered.

    .. code-block:: erbsland-conf
        :class: good-example

        [server]
        initial_response: "response:{demo}"  # Matches the first alternative

#.  **Missing Required Node:**
    If a node defined using alternatives is required but missing, the error message
    *must* list all valid types declared by the alternatives that *match the nodes version
    constraints*.

    .. rubric:: Example

    .. code-block:: text

        The 'app.service' value is missing. It must be an Integer or Text value.

#.  **Error Handling When No Alternative Matches:**
    If no alternative fulfills all constraints, validators *must* apply the following
    algorithm:

    #.  Scan all alternatives for matching ``type`` and ``version`` constraints.
    #.  If none match, raise an error listing all valid types.

        .. rubric:: Example

        .. code-block:: text

            The 'app.service' must be an Integer or Text value.

    #.  If exactly one alternative matches, handle errors as for a regular node-rules
        definition.
    #.  If multiple alternatives match, use the **first matching alternative** for
        error reporting.

#.  **Defaults:**
    If a ``default`` value is defined in any alternative and the node is missing,
    the first default encountered is used.

    Validators *must* raise an error if multiple alternatives define a ``default``.

    .. code-block:: erbsland-conf
        :class: validation-rules

        *[app.service]*
        type: "integer"

        *[app.service]*
        type: "text"
        default: "https"

    .. code-block:: erbsland-conf
        :class: good-example

        [app]
        # "service" defaults to "https"

#.  **Optionality:**
    If ``is_optional`` is present in any alternative, the node is considered optional.

    -   Validators *must* raise an error if multiple alternatives define ``is_optional``.
    -   Validators *must* raise an error if ``is_optional`` is not defined in the first alternative.

    .. code-block:: erbsland-conf
        :class: validation-rules

        *[app.service]*
        type: "integer"
        is_optional: yes

        *[app.service]*
        type: "text"

#.  **Sections in Alternatives:**
    When alternatives define sections, their child node-rules are validated
    individually *after* the alternative has been selected.

    An alternative is considered fulfilled if its own constraints are valid,
    **even if required child nodes are missing**.

    .. code-block:: erbsland-conf
        :class: bad-validation-rules

        *[app.screen]*
        type: "section"

        [app.screen.size]
        type: "integer"

        *[app.screen]*   # Does not work as expected
        type: "section"

        [app.screen.width]
        type: "integer"

        *[app.screen]*
        type: "text"

    .. code-block:: erbsland-conf
        :class: bad-example

        [app.screen]
        width: 10    # ERROR: Missing "size"

    Alternatives that differ only in their child layout must be distinguished by
    constraints at the same level, such as ``version``.

    .. code-block:: erbsland-conf
        :class: validation-rules

        *[app.screen]*
        type: "section"
        version: 1

        [app.screen.size]
        type: "integer"

        *[app.screen]*
        type: "section"
        version: 2

        [app.screen.width]
        type: "integer"

        *[app.screen]*
        type: "text"

    .. code-block:: erbsland-conf
        :class: good-example

        # Assuming version 2 is in effect:
        [app.screen]
        width: 10

    .. design-rationale::

        Alternatives are evaluated linearly without backtracking.
        This model is predictable, efficient to implement, and avoids ambiguous
        validation outcomes that would otherwise arise from structural lookahead.
