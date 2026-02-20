..
    Copyright (c) 2025 Tobias Erbsland - Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

**************
Reserved Names
**************

Validation Rules documents define a set of *reserved names* with predefined
semantics. These names are interpreted specially by validators and must not be
used as regular configuration or rule identifiers.

All reserved names start with the prefix ``vr_``.

.. design-rationale::

    Reserved names are used instead of extending the :term:`ELCL` language with
    additional meta-syntax.
    While both approaches are viable, the prefix-based solution keeps parser
    implementations simpler, avoids grammar extensions, and reduces overall
    implementation effort.

Rules for Reserved Names
========================

#.  **Prefix Requirement:**
    All reserved names *must* start with the prefix ``vr_``.

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

#.  **All Names with Prefix Are Reserved:**
    Any name that starts with ``vr_`` is considered reserved, regardless of whether
    it has an explicitly defined meaning in this specification.

    Validators *must* reject the use of unknown reserved names.

    .. code-block:: erbsland-conf
        :class: bad-example

        [settings.vr_headset]  # ERROR: unknown reserved name.
        type: "text"

#.  **Escaping Reserved Names:**
    Regular names that would otherwise be interpreted as reserved can be escaped
    by prefixing them with ``vr_vr_``.

    During normalization, the leading escape prefix is removed and the name is
    treated as a regular identifier.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [settings.vr_vr_headset]  # Defines rules for settings.vr_headset
        type: "text"

List of Reserved Names
======================

The following table lists all reserved names defined by this specification.

.. list-table::
    :header-rows: 1
    :class: identifier-table

    *   -   Reserved Name
        -   Description
    *   -   vr_template
        -   Section defined at the document root that provides reusable templates
            for node-rules definitions.
    *   -   vr_any
        -   Matches arbitrary child names under a section.
    *   -   vr_name
        -   Subsection of ``vr_any`` that defines constraints for the names
            themselves.
    *   -   vr_entry
        -   Subsection of a section list, value list, or value matrix definition
            that defines the node-rules for each entry.
    *   -   vr_key
        -   Section list defined at the document root or inside node-rules
            definitions to declare unique keys and create indexes for use with
            ``key`` constraints.
    *   -   vr_dependency
        -   Subsection of a node-rules definition that declares dependencies
            between child nodes.
    *   -   vr_vr_*
        -   Escape prefix used to define regular names that would otherwise be
            interpreted as reserved.
