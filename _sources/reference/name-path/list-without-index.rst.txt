..
    Copyright (c) 2025 Tobias Erbsland - Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

Addressing Section List Values without an Index
===============================================

This is a special behavior in *ELCL* that applies **only in configuration documents** — not in parser APIs. If a name path refers to a **section list**, and the next segment in the path is a regular name rather than an index, the path automatically points to the **last entry** in the list.

In other words:

* In a configuration file, when no index is given,
* the next name in the path refers to a **child value or section inside the last added entry** of the section list.

Example: Single Section List
----------------------------

The configuration below defines a section list named ``server.connection`` with two entries:

.. literalinclude:: /documents/reference/name-paths.elcl
    :language: erbsland-conf
    :emphasize-lines: 13

The resulting value tree shows how the name path ``server.connection.port`` resolves:

.. configuration-tree:: /documents/reference/name-paths.elcl
    :highlight-path: server.connection.port

Here, the path ``server.connection.port`` points to the ``port`` value of the **last entry** in the ``connection`` list — the one that holds the value ``9000``.

Why This Rule Exists
--------------------

At first glance, this rule may seem unusual — especially when working with a single-level list. However, it becomes intuitive and very useful in **nested list structures**, such as when building hierarchies dynamically.

Example: Nested Section Lists
-----------------------------

Here is a configuration with nested section lists. Each ``place`` may optionally define a list of ``tree`` sections:

.. literalinclude:: /documents/reference/nested-section-lists.elcl
    :language: erbsland-conf

The configuration expands into the following *value tree*:

.. configuration-tree:: /documents/reference/nested-section-lists.elcl

The tree shows how entries are added to the ``place`` list and how ``tree`` sections belong to the **last added** ``place``.

Let’s highlight the relevant part:

.. code-block:: erbsland-conf
    :lineno-start: 13
    :linenos:
    :emphasize-lines: 4

    ---*[place]*---
    name: "example03"

    *[place.tree]
    fruit: "cherry"

Even though ``place`` is a list, we didn’t provide an index in ``place.tree``. Therefore, the configuration implicitly attaches the ``tree`` entry to the **last place** — in this case, the one with name ``example03``.

.. note::

    In this example, the full path ``place.tree`` is used for clarity. In real-world configurations, it's typically better to use relative name paths like ``.tree`` instead.

Clarifying Name Path Semantics
------------------------------

* **In configuration files**, name paths like ``place.tree`` automatically refer to the **last entry** in a list when no index is given.
* **In parser APIs**, this automatic behavior may or may not apply. Instead, you get explicit control over which element in a list you want to access.

