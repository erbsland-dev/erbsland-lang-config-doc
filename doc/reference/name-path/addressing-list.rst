..
    Copyright (c) 2025 Tobias Erbsland - Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

Addressing a Section List
=========================

When a **name path** points to a *section list*, it refers to the list as a whole — not to a specific entry within the list.

This is an important distinction between how name paths behave in a **configuration document** versus how they are used within the **parser API**.

Consider the following example configuration:

.. literalinclude:: /documents/reference/name-paths.elcl
    :language: erbsland-conf
    :emphasize-lines: 8, 12

This results in the following *value tree*:

.. configuration-tree:: /documents/reference/name-paths.elcl
    :highlight-path: server.connection

As shown in the tree:

* The name path ``server.connection`` refers to a section list under the ``server`` section.
* The section list contains two entries: each with its own ``port`` and ``interface`` values.

Usage in Configuration Files
----------------------------

In the configuration file, you can **repeat a section list declaration** by using the same name path, prefixed with an asterisk (:cp:`*`). Each repeated section adds a new entry to the list.

.. code-block:: text

    *[server.connection]
    port: 8080
    interface: "web"

    *[server.connection]
    port: 9000
    interface: "api"

This pattern appends to the list each time the same name path is used with the section list syntax.

Usage in Parser APIs
---------------------

When interacting with a parsed configuration programmatically, the same name path — ``server.connection`` — will return the **entire section list**. You can then iterate over its entries as individual maps of values.

.. code-block:: python

    for conn in config["server.connection"]:
        print(conn["port"], conn["interface"])

This behavior allows you to treat the section list as a collection object, where each item corresponds to one declaration block from the configuration file.

.. important::

    Even though the name path is the same in both cases, the *semantics* differ:

    * In the **configuration language**, repeating the path creates new list entries.
    * In the **API**, it addresses the whole list, enabling you to query, iterate, or inspect its entries programmatically.
