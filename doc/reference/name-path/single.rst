..
    Copyright (c) 2025 Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

Name Paths with One Element
===========================

A *name path* can be as simple as a single :ref:`name<ref-name>`. For instance, the name path ``server`` will either point to or define the ``server`` section in the configuration.

.. literalinclude:: /documents/reference/name-paths.elcl
    :language: erbsland-conf
    :emphasize-lines: 4

.. configuration-tree:: /documents/reference/name-paths.elcl
    :highlight-path: server

In this case, the path ``server`` highlights the section that defines the server-related configurations in the example.
