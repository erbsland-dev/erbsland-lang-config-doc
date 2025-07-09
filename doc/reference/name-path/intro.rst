..
    Copyright (c) 2025 Tobias Erbsland - Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

Visualizing the Value Tree
==========================

To fully understand how name paths work, it helps to see a real configuration file and its corresponding value tree.

Here is a sample ELCL configuration:

.. literalinclude:: /documents/reference/name-paths.elcl
    :language: erbsland-conf

This configuration is transformed into the following *value tree*:

.. configuration-tree:: /documents/reference/name-paths.elcl

From the example above:

* The configuration defines two :term:`root sections<root section>` named ``main`` and ``server``.
* Under ``server.connection`` there's a :term:`section list`.
* The name path ``server.backend.filter`` introduces a subsection, which implicitly creates the intermediate section ``server.backend``.

On the **left-hand side** of the tree, the hierarchical structure of the configuration is shown. On the **right-hand side**, the actual values appear, annotated with type information in the form ``Type(...)``. These type names are recommended for use by parser implementations.

