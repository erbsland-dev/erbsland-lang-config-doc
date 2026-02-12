..
    Copyright (c) 2025-2026 Tobias Erbsland - Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

****************************
Indexes, Keys and References
****************************

Indexes allow validators to enforce **uniqueness** and to create **references**
between different parts of a configuration document.

Indexes are defined using the reserved section list ``vr_key`` and can appear
either at the document root or inside a *section* definition.
Once defined, the values collected by an index can be referenced using the
``key`` constraint (see :doc:`constraints/key`).

This mechanism enables referential integrity within a configuration, for example
by ensuring that a reference in one section points to an identifier defined
elsewhere.

.. code-block:: erbsland-conf
    :class: validation-rules

    *[vr_key]*
    name: "filter"
    key: "filter.vr_entry.identifier"

    [filter]
    type: "SectionList"

    [filter.vr_entry.identifier]
    type: "text"

    [app.start_filter]
    type: "text"
    key: "filter"

.. code-block:: erbsland-conf
    :class: good-example

    *[filter]*
    identifier: "first"

    *[filter]*
    identifier: "second"

    [app]
    start_filter: "first"

Rules for Indexes
=================

#.  **Index Creation:**
    An index is created by defining a section list named ``vr_key``.

    .. code-block:: erbsland-conf
        :class: validation-rules

        *[vr_key]*
        name: "filter"
        key: "filter.vr_entry.identifier"

#.  **Uniqueness:**
    All key values collected in an index *must* be unique.
    Validators *must* report an error if a duplicate key is encountered.

    .. code-block:: erbsland-conf
        :class: bad-example

        *[filter]*
        identifier: "one"

        *[filter]*
        identifier: "one"  # ERROR: Identifier must be unique

#.  **Placement:**
    A ``vr_key`` section list may appear either:

    * at the document root, or
    * inside a node-rules definition for a section.

    If defined inside a section node-rules definition, the index is scoped
    to each validated instance of that section.

    In the following example, the index is defined inside the
    ``app.server.vr_entry`` definition. As a result, ``id`` must
    be unique *within each individual* ``server`` entry.

    Different ``server`` entries may reuse the same ``id`` values,
    because each ``server`` instance has its own independent index scope.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [app.server]
        type: "SectionList"

        [app.server.vr_entry.connection]
        type: "SectionList"

        [app.server.vr_entry.connection.vr_entry.id]
        type: "text"

        *[app.server.vr_entry.vr_key]*
        name: "connection_id"
        key: "connection.vr_entry.id"

#.  **Scope and Visibility:**
    An index is visible only within the subtree in which it is defined.
    References outside this scope are invalid.

    .. code-block:: erbsland-conf
        :class: bad-validation-rules

        [app.server]
        type: "SectionList"

        [app.server.vr_entry.connection]
        type: "SectionList"

        [app.server.vr_entry.connection.vr_entry.id]
        type: "text"

        *[app.server.vr_entry.vr_key]*
        name: "connection_id"
        key: "connection.vr_entry.id"

        [app.main_connection]
        type: "text"
        key: "connection_id"  # ERROR: No such index in this scope

#.  **Key Field:**
    Each ``vr_key`` entry *must* contain a ``key`` field that specifies one or
    more values to be indexed.

    .. code-block:: erbsland-conf
        :class: validation-rules

        # ...

        *[vr_key]*
        key: "filter.vr_entry.identifier"

#.  **Optional Name:**
    A ``vr_key`` entry *may* define a ``name`` field, which assigns an identifier
    to the index for use in ``key`` constraints.

    .. code-block:: erbsland-conf
        :class: validation-rules

        # ...

        *[vr_key]*
        name: "filter"
        key: "filter.vr_entry.identifier"

#.  **Case-Sensitivity:**
    An optional ``case_sensitive`` field may be defined on a ``vr_key``
    entry to control how indexed values are compared.

    If ``case_sensitive`` is set to ``true``, both uniqueness checks and
    ``key`` constraint comparisons are performed case-sensitively.
    If omitted or set to ``false``, comparisons are case-insensitive.

    The comparison mode defined by the index applies consistently to:

    * detection of duplicate key values, and
    * resolution of references using the ``key`` constraint.

    .. code-block:: erbsland-conf
        :class: validation-rules

        *[vr_key]*
        name: "filter"
        key: "filter.vr_entry.identifier"
        case_sensitive: true


Rules for Keys
==============

#.  **Text Name-Path Required:**
    Each ``key`` value *must* be a text string containing a valid :term:`name path`.

    .. code-block:: erbsland-conf
        :class: validation-rules

        # ...

        *[vr_key]*
        name: "filter"
        key: "filter.vr_entry.identifier"

#.  **Allowed Value Types:**
    A referenced key *must* point to either a text or an integer value.

    .. code-block:: erbsland-conf
        :class: bad-validation-rules

        *[vr_key]*
        key: "blog.vr_entry.created"  # ERROR: Must reference text or integer

        [blog]
        type: "SectionList"

        [blog.vr_entry.created]
        type: "DateTime"

#.  **Section List + Value Requirement:**
    Each name-path *must* resolve to:

    * a section list,
    * its ``vr_entry``, and
    * a value inside each ``vr_entry`` of that section list.

    .. code-block:: erbsland-conf
        :class: validation-rules

        *[vr_key]*
        name: "filter"
        key: "app.filter.vr_entry.meta.id"

        [app.filter]
        type: "SectionList"

        [app.filter.vr_entry.meta.id]
        type: "text"

    In this example:

    * ``app.filter`` identifies the section list
    * ``vr_entry`` identifies the section list's entries
    * ``meta.id`` identifies the value within each entry

#.  **No Nested Section Lists:**
    A ``key`` name-path *must not* reference a section list that is nested
    inside another section list.

    Keys must resolve to values within a single, directly addressed
    section list. Referencing nested section lists would make index
    construction ambiguous and dependent on traversal depth.

    .. code-block:: erbsland-conf
        :class: bad-validation-rules

        [app.filters]
        type: "SectionList"

        [app.filters.vr_entry.rules]
        type: "SectionList"

        [app.filters.vr_entry.rules.vr_entry.id]
        type: "text"

        *[vr_key]*
        key: "app.filters.vr_entry.rules.vr_entry.id"  # ERROR: Cannot reference nested section list

#.  **Alternatives, Optionality and Version Constraints in Key Paths:**
    If a node-rules definition that is part of a ``key`` name-path contains
    version constraints, optionality, or alternatives, index creation becomes
    conditional on the effective structure present in the validated document.

    The following rules apply:

    #. If the referenced section list does not exist in the configuration
       document, the index is created as an empty index.

    #. If a referenced value inside a section list entry does not exist,
       is not active due to version constraints, or resolves to a value
       other than ``text`` or ``integer``, that entry is omitted from the
       index.

       Omitted entries are not validated for uniqueness.

    This behavior ensures that index construction is deterministic and
    tolerant of versioned or alternative schema structures.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [app.filters]
        type: "SectionList"
        minimum_version: 2

        [app.filters.vr_entry.id]
        type: "text"

        *[vr_key]*
        key: "app.filters.vr_entry.id"
        # Index is created only if app.filters is active for the current version

    .. code-block:: erbsland-conf
        :class: validation-rules

        [app.filters]
        type: "SectionList"

        [app.filters.vr_entry.id]
        type: "text"
        minimum_version: 2

        *[vr_key]*
        key: "app.filters.vr_entry.id"
        # For versions < 2, entries without an active 'id' are ignored by the index

Rules for Index Names
=====================

#.  **Optional Name:**
    An index may define a ``name`` entry, which is used by ``key`` constraints to
    reference the index.

#.  **Naming Rules:**
    Index names *must* follow the :ref:`ELCL name rules <ref-name>`.

    .. code-block:: erbsland-conf
        :class: bad-validation-rules

        # ...

        *[vr_key]*
        name: "%my-name%"  # ERROR: Invalid ELCL name
        # ...

#.  **Normalization and Comparison:**
    Index names are normalized and compared according to the
    :doc:`ELCL name rules </reference/names>`.

    Underscores and spaces are equivalent, and comparisons are case-insensitive.

    .. code-block:: erbsland-conf
        :class: validation-rules

        *[vr_key]*
        name: "filter_index"
        key: "filter.vr_entry.identifier"

        [app.start_filter]
        type: "text"
        key: "Filter Index"  # VALID after normalization


Rules for Multi-Key Indexes
===========================

#.  **Combination Must Be Unique:**
    If multiple ``key`` values are specified, the **combination** of their
    resolved values must be unique across all entries of the referenced
    section list.

    Uniqueness is evaluated on the tuple of key values, not on the individual
    components.

    .. code-block:: erbsland-conf
        :class: validation-rules

        *[vr_key]*
        key: "server.vr_entry.service", "server.vr_entry.protocol"

        [server]
        type: "SectionList"

        [server.vr_entry.service]
        type: "text"
        in: "api", "management"

        [server.vr_entry.protocol]
        type: "text"
        in: "https", "json"

#.  **All Keys Must Reference the Same Section List:**
    All name-paths defined in a composite key *must* resolve to values within
    the same section list.

    Mixing keys from different section lists is not permitted.

    .. code-block:: erbsland-conf
        :class: bad-validation-rules

        *[vr_key]*
        key:
            * "server.vr_entry.service"
            * "client.vr_entry.protocol"  # ERROR: Different section lists

        [server]
        type: "SectionList"

        # ...

        [client]
        type: "SectionList"

        # ...

#.  **Composite Key Representation:**
    When a multi-key index is referenced as a whole, its values are combined
    into a single text value separated by commas (:cp:`,`).

    The order of the combined values matches the order in which the
    ``key`` name-paths are defined.

    .. code-block:: erbsland-conf
        :class: validation-rules

        # ...

        *[vr_key]*
        key:
            * "server.vr_entry.service"
            * "server.vr_entry.protocol"

    .. code-block:: erbsland-conf
        :class: good-example

        [server]   # Creates the composite key "api,https"
        service: "api"
        protocol: "https"

    .. design-rationale::

        Although commas could theoretically appear in key values, such cases
        can be avoided by disallowing commas in fields that are used as keys.
        This keeps composite key representation simple, deterministic,
        and efficient.

#.  **Referencing Parts of a Composite Key:**
    A multi-key index may be referenced either as a whole or by addressing
    individual components using the ``key[index]`` syntax.

    The index is zero-based and refers to the position of the corresponding
    name-path in the ``key`` definition.

    .. code-block:: erbsland-conf
        :class: validation-rules

        *[vr_key]*
        name: "server"
        key:
            * "server.vr_entry.service"
            * "server.vr_entry.protocol"

        [server.ports]
        type: "SectionList"

        [server.ports.vr_entry.protocol]
        type: "text"
        key: "server[1]"  # References only the protocol component
        key_error: "No server with this protocol was configured"

Version History
===============

.. version-changed:: 1.3.0

    Introduced the optional ``case_sensitive`` field for ``vr_key`` entries,
    defining explicit case-sensitivity semantics for both uniqueness checks
    and ``key`` constraint comparisons.

.. version-changed:: 1.2.10

    Documented the canonical form of key paths including ``vr_entry`` when
    referencing values inside section lists.

    For compatibility, validators may treat ``list.value`` as shorthand
    for ``list.vr_entry.value`` when ``list`` resolves to a section list.

