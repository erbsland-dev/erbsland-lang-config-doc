..
    Copyright (c) 2025-2026 Tobias Erbsland - Erbsland DEV. https://erbsland.dev
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

        [server.username]
        type: "text"
        is_optional: yes

        [server.password]
        type: "text"
        is_optional: yes
        is_secret: yes

        *[vr_dependency]*
        mode: "if"
        source: "server.hostname"
        target: "server.ip_address"

#.  **Placement and Scope:**
    A ``vr_dependency`` may appear either:

    * at the document root, or
    * inside a node-rules definition for a *section*.

    The dependency applies only within the subtree of the section in which it is defined.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [server]
        type: "section"

        # ...

        *[server.vr_dependency]*
        mode: "xor"
        source: "hostname"
        target: "ip_address"

#.  **Mode Required:**
    Each dependency *must* define a ``mode`` entry with a text value.
    The ``mode`` determines how the configuration state of ``source`` and ``target``
    is interpreted.

    Validators *must* support the following modes:

    *   ``if`` — If the *source* side is configured, the *target* side must also be configured.
        If the source is not configured, the dependency is considered satisfied.
    *   ``if_not`` — If the *source* side is configured, the *target* side must **not** be configured.
    *   ``or`` — At least one side (source or target) must be configured.
        Both sides may be configured.
    *   ``xor`` — Exactly one side must be configured.
        Neither both nor none are allowed.
    *   ``xnor`` — Either both sides must be configured, or neither.
    *   ``and`` — Both source and target must be configured.

    If you are unsure how a specific mode behaves in edge cases,
    refer to :ref:`dependency-modes-logic` below.
    That section defines the exact evaluation matrix and should be treated as normative.

#.  **Source and Target Required:**
    Each dependency *must* define both ``source`` and ``target``.

    * Each entry may be a single text value or a list of text values.
    * Values are :term:`relative name-paths <name path>` resolved within the same section.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [client]
        type: "section"

        [client.username]
        type: "text"
        is_optional: yes

        [client.password]
        type: "text"
        is_optional: yes

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

        # ...

        *[vr_dependency]*
        mode: "if"
        source: "api_key", "token"
        target: "endpoint"

#.  **Custom Error Messages:**
    A dependency *may* define an ``error`` entry to provide a custom validation message.

    .. code-block:: erbsland-conf
        :class: validation-rules

        # ...

        *[vr_dependency]*
        mode: "xor"
        source: "hostname"
        target: "ip_address"
        error: "Configure either 'hostname' or 'ip_address', not both."

#.  **What “Configured” Means:**
    For dependency evaluation, a node on the ``source`` or ``target`` side
    is considered **configured** only if it is explicitly present in the
    configuration document.

    A node is *not* considered configured if it exists solely because a
    ``default`` value was applied during parsing.

    In other words, dependencies operate on what the user actually wrote —
    not on values that were implicitly added by the validator.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [app.a]
        type: "integer"
        default: 1

    .. code-block:: erbsland-conf
        :class: good-example

        [app]
        # "app.a" is NOT configured.
        # The value exists only because of the default.

    .. code-block:: erbsland-conf
        :class: good-example

        [app]
        a: 1
        # "app.a" IS configured.
        # The value is explicitly present in the document,
        # even if it equals the default.

#.  **Valid Source and Target Paths:**
    Each name-path listed in ``source`` and ``target`` *must* resolve to a node
    that has a node-rules definition and whose presence is not already
    unconditionally required.

    In other words, the referenced node must be *conditionally present*.
    A node is considered conditionally present if at least one element in its
    effective path:

    * is marked with ``is_optional: yes``, or
    * defines a ``default`` value.

    A path *must not*:

    * reference nodes inside individual alternatives, or
    * reference elements within a section list (such as ``vr_entry`` values).

    .. code-block:: erbsland-conf
        :class: bad-validation-rules

        [app.username]
        type: "text"

        [app.password]
        type: "text"
        default: ""

        *[vr_dependency]*
        mode: "if"
        source: "app.username"  # ERROR: app.username is not optional
        target: "app.password"

    .. code-block:: erbsland-conf
        :class: bad-validation-rules

        [app.ports]
        type: "SectionList"

        [app.ports.vr_entry.port]
        type: "integer"
        default: 0

        [app.interface]
        type: "text"
        default: ""

        *[app.vr_dependency]*
        mode: "if"
        source: "app.ports.vr_entry.port"  # ERROR: Cannot reference elements of a section list
        target: "app.interface"

    .. code-block:: erbsland-conf
        :class: bad-validation-rules

        *[app.ports]*
        type: "Section"

        [app.ports.start]
        type: "integer"
        default: 0

        [app.ports.end]
        type: "integer"
        default: 65534

        *[app.ports]*
        type: "Integer"
        default: 80

        [app.interface]
        type: "text"
        default: ""

        *[vr_dependency]*
        mode: "if"
        source: "app.ports.start"  # ERROR: app.ports is defined in alternatives
        target: "app.interface"

#.  **Mode Case Insensitivity and Normalization:**
    Mode identifiers are **case-insensitive** and are normalized according to
    the same rules as :term:`names<Name>` in :term:`ELCL`.

    Comparisons are performed on the normalized form of the identifier.
    For example, ``if_not``, ``IF_NOT``, and ``If Not`` all refer to the same mode.

    Validators *must* apply normalization consistently when resolving the
    ``mode`` value.

    .. code-block:: erbsland-conf
        :class: validation-rules

        # ...

        *[vr_dependency]*
        mode: "If Not"
        source: "hostname"
        target: "ip_address"

        *[vr_dependency]*
        mode: "if_not"
        source: "port"
        target: "protocol"

.. |dep-0| raw:: html

    <i class="fa-solid fa-square-dashed sd-text-muted" style="font-size: 24px;"></i>

.. |dep-s| raw:: html

    <i class="fa-solid fa-square-s sd-text-info" style="font-size: 24px;"></i>

.. |dep-t| raw:: html

    <i class="fa-solid fa-square-t sd-text-warning" style="font-size: 24px;"></i>

.. |dep-plus| raw:: html

    <i class="fa-solid fa-dash sd-text-muted" style="font-size: 24px;"></i>

.. |dep-pass| raw:: html

    <i class="fa-solid fa-circle-check sd-text-success" style="font-size: 24px;"></i>

.. |dep-fail| raw:: html

    <i class="fa-solid fa-circle-xmark sd-text-danger" style="font-size: 24px;"></i>

.. _dependency-modes-logic:

Mode Logic Explained
====================

When validating a dependency, the validator performs two steps:

#.  Determine whether the *source* side is configured.
#.  Determine whether the *target* side is configured.

The selected ``mode`` is then applied to these two boolean results.

Importantly, dependencies operate purely on **presence**.
They never inspect or compare actual values.

Testing if Sources and/or Targets are Present
---------------------------------------------

A single name-path in ``source`` or ``target`` is considered configured if:

* the referenced node exists in the original configuration document, and
* its presence is **not** the result of a ``default`` value.

This distinction is essential.

A node that only exists in the parsed configuration tree because a
``default`` value was applied is *not* considered configured for
dependency evaluation.

If multiple name-paths are listed in ``source`` or ``target``,
that side is considered configured if **at least one** of the listed
nodes is configured (logical OR semantics).

Consider this simplified example:

.. code-block:: erbsland-conf
    :class: validation-rules

    *[app.vr_dependency]*
    mode: "if"
    source: "a", "b"
    target: "x", "y"

The following configurations illustrate the four possible situations:

.. code-block:: erbsland-conf
    :class: good-example

    [app]  # Neither source nor target are configured.

.. code-block:: erbsland-conf
    :class: bad-example

    [app]  # Source is configured, but target is not.
    a: 1

.. code-block:: erbsland-conf
    :class: good-example

    [app]  # Target is configured, but source is not.
    x: 1

.. code-block:: erbsland-conf
    :class: good-example

    [app]  # Both source and target are configured.
    b: 1
    y: 1

Four Situations
---------------

When evaluating a dependency, the configuration state of the source
and target side results in exactly one of four possible situations.

These situations form the logical basis for all dependency modes.

.. list-table::
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    *   -   Situation
        -   Description
    *   -   |dep-0| |dep-0|
        -   Neither source nor target values are configured.
    *   -   |dep-s| |dep-0|
        -   One or more source values are configured, and no target values are configured.
    *   -   |dep-0| |dep-t|
        -   No source values are configured, but one or more target values are configured.
    *   -   |dep-s| |dep-t|
        -   One or more source values are configured, and one or more target values are configured.

The Dependency Mode Logic
-------------------------

Each dependency mode defines which of the four situations above
are considered valid.

A green checkmark indicates that the dependency is satisfied.
A red xmark indicates that the dependency is violated and validation fails.

The following table is normative and defines the exact behavior:

.. list-table::
    :width: 100%
    :widths: 20 20 20 20 20
    :header-rows: 1
    :class: dependency-matrix

    *   -   Mode ↓
        -   |dep-0| |dep-0|
        -   |dep-s| |dep-0|
        -   |dep-0| |dep-t|
        -   |dep-s| |dep-t|
    *   -   if
        -   |dep-pass|
        -   |dep-fail|
        -   |dep-pass|
        -   |dep-pass|
    *   -   if_not
        -   |dep-pass|
        -   |dep-pass|
        -   |dep-pass|
        -   |dep-fail|
    *   -   or
        -   |dep-fail|
        -   |dep-pass|
        -   |dep-pass|
        -   |dep-pass|
    *   -   xor
        -   |dep-fail|
        -   |dep-pass|
        -   |dep-pass|
        -   |dep-fail|
    *   -   xnor
        -   |dep-pass|
        -   |dep-fail|
        -   |dep-fail|
        -   |dep-pass|
    *   -   and
        -   |dep-fail|
        -   |dep-fail|
        -   |dep-fail|
        -   |dep-pass|

Unsupported Logic Modes and Why They Are Not Supported
------------------------------------------------------

You may notice that the logical matrix above is not exhaustive.
Several theoretically possible boolean modes are intentionally not supported.

The following modes are omitted by design:

.. list-table::
    :width: 100%
    :widths: 20 20 20 20 20
    :header-rows: 1
    :class: dependency-matrix

    *   -   Mode ↓
        -   |dep-0| |dep-0|
        -   |dep-s| |dep-0|
        -   |dep-0| |dep-t|
        -   |dep-s| |dep-t|
    *   -   none
        -   |dep-pass|
        -   |dep-pass|
        -   |dep-pass|
        -   |dep-pass|
    *   -   nand
        -   |dep-pass|
        -   |dep-pass|
        -   |dep-pass|
        -   |dep-fail|
    *   -   nor
        -   |dep-pass|
        -   |dep-fail|
        -   |dep-fail|
        -   |dep-fail|
    *   -   reverse_if
        -   |dep-pass|
        -   |dep-pass|
        -   |dep-fail|
        -   |dep-pass|

These modes are excluded for the following reasons:

.. list-table::
    :width: 100%
    :widths: 20 80
    :class: identifier-table

    *   -   none
        -   This mode would accept all four situations and therefore impose no constraint.
            It is functionally equivalent to omitting the ``vr_dependency`` entry entirely.
    *   -   nand
        -   While logically valid, it is semantically redundant: the same behavior is already
            provided by ``if_not`` with clearer intent in the context of dependencies.
    *   -   nor
        -   This mode would only allow the situation where neither side is configured.
            In practice, this would prohibit configuring any of the referenced nodes,
            which does not express a dependency but rather a prohibition rule.
    *   -   reverse_if
        -   This would represent the logical inverse direction of ``if``.
            Instead of introducing a separate mode, the same behavior is achieved
            simply by swapping ``source`` and ``target`` in an ``if`` dependency.
            Adding a dedicated mode would therefore increase surface complexity
            without adding expressive power.

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
    key: "api.media_link.vr_entry.id"

    [app.primary_medialink]
    type: "text"
    key: "media_link"
    is_optional: yes

    *[vr_dependency]*
    mode: "if"
    source: "api.media_link"
    target: "app.primary_medialink"
    error: "You must configure 'primary_medialink' when using this feature"

Version History
===============

.. version-changed:: 1.3.1

    * Added the missing ``or`` and ``and`` modes.
    * Clarified that ``mode`` identifiers are case-insensitive and must be
      compared using ELCL normalization rules.
    * Refined the wording of all dependency modes to remove ambiguity.
    * Added a normative section explaining dependency mode logic in detail.
    * Defined stricter requirements for ``source`` and ``target`` name-paths,
      including explicit restrictions on section lists and alternative branches.