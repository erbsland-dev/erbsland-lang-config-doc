*******************
Keys and References
*******************

Indexes allow validators to enforce **uniqueness** and to create **references**
between different parts of a configuration document.

Indexes are defined using the reserved section list ``vr_key`` and can appear
either at the document root or inside a section definition.
Once defined, the values collected by an index can be referenced using the
``key`` constraint (see :doc:`constraints/key`).

This mechanism enables referential integrity within a configuration, for example
by ensuring that a reference in one section points to an identifier defined
elsewhere.

.. code-block:: erbsland-conf
    :class: validation-rules

    *[vr_key]*
    name: "filter"
    key: "filter.identifier"

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
        key: "filter.identifier"

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

    .. code-block:: erbsland-conf
        :class: validation-rules

        [app.server]
        type: "SectionList"

        *[app.server.vr_entry.vr_key]*
        name: "connection_id"
        key: "connection.id"

#.  **Scope and Visibility:**
    An index is visible only within the subtree in which it is defined.
    References outside this scope are invalid.

    .. code-block:: erbsland-conf
        :class: bad-validation-rules

        *[app.server.vr_entry.vr_key]*
        name: "connection_id"
        key: "connection.id"

        [app.connection]
        type: "text"
        key: "connection_id"  # ERROR: No such index in this scope

#.  **Key Field:**
    Each ``vr_key`` entry *must* contain a ``key`` field that specifies one or
    more values to be indexed.

    .. code-block:: erbsland-conf
        :class: validation-rules

        *[vr_key]*
        key: "filter.identifier"

#.  **Optional Name:**
    A ``vr_key`` entry *may* define a ``name`` field, which assigns an identifier
    to the index for use in ``key`` constraints.

    .. code-block:: erbsland-conf
        :class: validation-rules

        *[vr_key]*
        name: "filter"
        key: "filter.identifier"

.. design-rationale::

    Indexes are intentionally scoped to the subtree in which they are defined.
    This prevents name collisions between unrelated parts of a configuration and
    keeps validation rules modular and predictable.

    A global index space would introduce two problems:

    * **Accidental collisions** between unrelated rules using the same index name.
    * **Unnecessary coupling** between distant parts of the configuration.

    If global or cross-document references are required, they should be modeled
    explicitly at a higher level instead of overloading ``vr_key``.

Rules for Keys
==============

#.  **Text Name-Path Required:**
    Each ``key`` value *must* be a text string containing a valid :term:`name path`.

    .. code-block:: erbsland-conf
        :class: validation-rules

        *[vr_key]*
        name: "filter"
        key: "filter.identifier"

#.  **Allowed Value Types:**
    A referenced key *must* point to either a text or an integer value.

    .. code-block:: erbsland-conf
        :class: bad-validation-rules

        *[vr_key]*
        key: "blog.created"  # ERROR: Must reference text or integer

        [blog]
        type: "SectionList"

        [blog.vr_entry.created]
        type: "DateTime"

#.  **Section List + Value Requirement:**
    Each name-path *must* resolve to:

    * a section list, and
    * a value inside each entry of that section list.

    .. code-block:: erbsland-conf
        :class: validation-rules

        *[vr_key]*
        name: "filter"
        key: "app.filter.meta.id"

        [app.filter]
        type: "SectionList"

        [app.filter.vr_entry.meta.id]
        type: "text"

    In this example:

    * ``app.filter`` identifies the section list
    * ``meta.id`` identifies the value within each entry

#.  **Composite Keys:**
    If multiple keys are specified, their **combination** must be unique across
    all entries.

    .. code-block:: erbsland-conf
        :class: validation-rules

        *[vr_key]*
        key: "server.service", "server.protocol"

        [server]
        type: "SectionList"

        [server.vr_entry.service]
        type: "text"
        in: "api", "management"

        [server.vr_entry.protocol]
        type: "text"
        in: "https", "json"

Rules for Index Names
=====================

#.  **Optional Name:**
    An index may define a ``name`` entry, which is used by ``key`` constraints to
    reference the index.

#.  **Naming Rules:**
    Index names *must* follow the :ref:`ELCL name rules <ref-name>`.

    .. code-block:: erbsland-conf
        :class: bad-validation-rules

        *[vr_key]*
        name: "%my-name%"  # ERROR: Invalid ELCL name

#.  **Normalization and Comparison:**
    Index names are normalized and compared according to the
    :doc:`ELCL name rules </reference/names>`.

    Underscores and spaces are equivalent, and comparisons are case-insensitive.

    .. code-block:: erbsland-conf
        :class: validation-rules

        *[vr_key]*
        name: "filter_index"
        key: "filter.identifier"

        [app.start_filter]
        type: "text"
        key: "Filter Index"  # VALID after normalization

Rules for Multi-Key Indexes
===========================

#.  **Key Combination Representation:**
    Multi-key indexes combine their key values into a single entry, separated by
    commas (:cp:`,`).

    .. code-block:: erbsland-conf
        :class: validation-rules

        *[vr_key]*
        key: "server.service", "server.protocol"

    .. code-block:: erbsland-conf
        :class: good-example

        [server]   # Creates the composite key "api,https"
        service: "api"
        protocol: "https"

    .. design-rationale::

        While commas could theoretically appear in key values, such cases can be
        avoided by disallowing commas in fields used as keys.
        This keeps index representation simple and efficient.

#.  **Referencing Parts of a Multi-Key:**
    A multi-key index can be referenced either as a whole or by individual parts
    using the ``key[index]`` syntax, where the index is zero-based.

    .. code-block:: erbsland-conf
        :class: validation-rules

        *[vr_key]*
        name: "server"
        key: "server.service", "server.protocol"

        [server.ports]
        type: "SectionList"

        [server.ports.vr_entry.protocol]
        type: "text"
        key: "server[1]"  # References only the protocol part
        key_error: "No server with this protocol was configured"
