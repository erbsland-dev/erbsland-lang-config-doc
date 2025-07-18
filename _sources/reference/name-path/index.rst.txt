..
    Copyright (c) 2024-2025 Tobias Erbsland - Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

.. _ref-name-path:
.. index::
    !single: Name Path
    single: Names
    single: Value Tree

Name Paths
==========

In the *Erbsland Configuration Language* (ELCL), a **name path** is a sequence of names that points to a specific value or section in the configuration file. Name paths are essential for two main reasons:

* They are used in ELCL syntax to define sections and values hierarchically.
* They are used in the *value tree* representation of the configuration, which is what a parser constructs and applications consume.

Each name in the path contributes one level to the hierarchy. This design makes it easy to organize and access deeply nested data.

For example, the name path ``server.connection.port`` refers to the value named ``port``, which is part of the section ``connection``, which in turn belongs to the section ``server``.

Name paths are fundamental when navigating the value tree using the parser API. You'll see them throughout this documentation — particularly when addressing sections, values, and lists within the configuration.

.. button-ref:: intro
    :ref-type: doc
    :color: light
    :align: center
    :expand:
    :shadow:

    Visualizing the Value Tree →

.. toctree::

    intro
    single
    multiple
    addressing-list
    list-without-index
    list-with-index
    text-names
    text-names-for-parsers

