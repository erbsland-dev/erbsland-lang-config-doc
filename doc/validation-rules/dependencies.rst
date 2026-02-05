..
    Copyright (c) 2025 Tobias Erbsland - Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

************
Dependencies
************

Dependencies express **conditional relationships** between configuration elements.
They allow you to define rules such as *“if this value exists, that one must also exist”*
without duplicating logic in application code.

Dependencies are declared using the ``vr_dependency`` section list.
They always operate on the **presence or absence** of values or sections, never on
their actual content.

.. important::

    Default values do *not* count as “configured” for dependency checks.
    Only nodes that explicitly exist in the configuration document are considered present.

.. code-block:: erbsland-conf
    :class: validation-rules

    [client.username]
    type: "text"
    is_optional: yes

    [client.password]
    type: "text"
    is_optional: yes

    *[client.vr_dependency]*
    mode: "xnor"
    source: "username"
    target: "password"
    error: "Configure username *and* password, or none of these values"

Rules for Dependencies
======================

#.  **Section List Required:**
    Dependencies *must* be defined using a section list named ``vr_dependency``.

    .. code-block:: erbsland-conf
        :class: validation-rules

        *[vr_dependency]*
        mode: "if"
        source: "server.hostname"
        target: "server.ip_address"

#.  **Placement and Scope:**
    A ``vr_dependency`` may appear either:

    * at the document root, or
    * inside a node-rules definition for a section.

    The dependency applies only within the subtree of the section in which it is defined.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [server]
        type: "section"

        *[server.vr_dependency]*
        mode: "xor"
        source: "hostname"
        target: "ip_address"

#.  **Mode Required:**
    Each dependency *must* define a ``mode`` entry.
    The following modes are supported:

    * ``if`` — Targets may only be configured if the sources are configured.
    * ``if_not`` — Targets may only be configured if the sources are *not* configured.
    * ``xnor`` — Either all sources *and* all targets are configured, or none of them are.
    * ``xor`` — Either the sources *or* the targets are configured, but not both and not neither.

#.  **Source and Target Required:**
    Each dependency *must* define both ``source`` and ``target``.

    * Each entry may be a single text value or a list of text values.
    * Values are :term:`relative name-paths <name path>` resolved within the same section.

    .. code-block:: erbsland-conf
        :class: validation-rules

        *[client.vr_dependency]*
        mode: "if"
        source: "username"
        target: "password"

#.  **Multiple Values (OR Semantics):**
    If multiple name-paths are listed in ``source`` or ``target``,
    that side of the dependency is considered configured if *any*
    of the listed nodes exists.

    .. code-block:: erbsland-conf
        :class: validation-rules

        *[vr_dependency]*
        mode: "if"
        source: "api_key", "token"
        target: "endpoint"

#.  **Custom Error Messages:**
    A dependency *may* define an ``error`` entry to provide a custom validation message.

    .. code-block:: erbsland-conf
        :class: validation-rules

        *[vr_dependency]*
        mode: "xor"
        source: "hostname"
        target: "ip_address"
        error: "Configure either 'hostname' or 'ip_address', not both."

Examples
========

Exclusion (XOR)
---------------

Exactly one of the two values must be configured:

.. code-block:: erbsland-conf
    :class: validation-rules

    [server.hostname]
    type: "text"
    is_optional: yes

    [server.ip_address]
    type: "text"
    is_optional: yes

    *[server.vr_dependency]*
    mode: "xor"
    source: "hostname"
    target: "ip_address"
    error: "Configure either 'hostname' or 'ip_address'"

Bidirectional Dependency (XNOR)
-------------------------------

Either both values must be present, or neither:

.. code-block:: erbsland-conf
    :class: validation-rules

    [window.x]
    type: "integer"
    is_optional: yes

    [window.y]
    type: "integer"
    is_optional: yes

    *[window.vr_dependency]*
    mode: "xnor"
    source: "x"
    target: "y"
    error: "You must either specify both 'x' and 'y' or neither"

Directional Dependency (IF)
---------------------------

A value is required only when a related feature is configured:

.. code-block:: erbsland-conf
    :class: validation-rules

    [api.media_link]
    type: "SectionList"
    is_optional: yes

    [api.media_link.vr_entry.id]
    type: "text"

    *[vr_key]*
    name: "media_link"
    key: "api.media_link.id"

    [app.primary_medialink]
    type: "text"
    key: "media_link"
    is_optional: yes

    *[vr_dependency]*
    mode: "if"
    source: "api.media_link"
    target: "app.primary_medialink"
    error: "You must configure 'primary_medialink' when using this feature"
