..
    Copyright (c) 2025 Tobias Erbsland - Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

Text Names in Name Paths
========================

Text names appear in name paths when a section or value is identified by a double-quoted string — as described in :ref:`ref-text-name`. This feature is typically used in user-facing configuration files to allow full phrases or human-readable keys as section names.

Sections with text names are limited: **they cannot contain subsections**. As a result, *in configuration files*, any section with a text name always forms the **final component** in a name path.

Example
-------

The following configuration defines several ``book`` sections, each identified by its title:

.. literalinclude:: /documents/reference/name-path-section-with-text-name.elcl
    :language: erbsland-conf

This configuration produces the following value tree:

.. configuration-tree:: /documents/reference/name-path-section-with-text-name.elcl

Each ``book`` entry is uniquely keyed by its title. The metadata fields — ``isbn``, ``edition``, and ``pages`` — are stored directly inside each of these leaf sections.

