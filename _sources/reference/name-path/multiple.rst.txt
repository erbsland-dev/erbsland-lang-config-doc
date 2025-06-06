..
    Copyright (c) 2025 Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

Name Paths with Multiple Elements
=================================

A name path can also consist of multiple elements, each separated by a period (:cp:`.`). This structure allows you to navigate deeper into the hierarchy. For example, the name path ``server.backend.filter`` points to the last section in the configuration file.

.. literalinclude:: /documents/reference/name-paths.elcl
    :language: erbsland-conf
    :emphasize-lines: 16

.. configuration-tree:: /documents/reference/name-paths.elcl
    :highlight-path: server.backend.filter

Here, the path ``server.backend.filter`` helps identify the specific ``filter`` section nested within the ``server.backend`` structure.

In addition to sections, you can use name paths to target individual values within the configuration. For instance, the name path ``server.startup_delay`` directly references the ``startup_delay`` value within the ``server`` section.

.. configuration-tree:: /documents/reference/name-paths.elcl
    :highlight-path: server.startup_delay

Name paths like this one are crucial when using the parser API to retrieve specific values in a configuration file.
