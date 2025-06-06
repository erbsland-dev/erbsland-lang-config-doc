..
    Copyright (c) 2024 Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

.. _ref-name-conflict:
.. index::
    !single: Name Conflict
    single: Conflict

Name Conflicts
==============

In the *Erbsland Configuration Language* (:term:`ELCL`), there is a fundamental rule governing the use of :ref:`names<ref-name>` and :ref:`name paths<ref-name-path>`:

.. centered::
    Each name must be unique and used only once within a configuration.

This simple rule underpins all the other rules related to :ref:`sections<ref-section>` and :ref:`values<ref-named-value>`, ensuring consistency and preventing conflicts in configuration documents.

.. index::
    single: Using a Name

Using a Name
------------

A name is considered *used* when a section or value with that name appears in a configuration document. Once used, that name is reserved and cannot be reused or redefined elsewhere in the configuration.

.. code-block:: erbsland-conf
    :class: good-example

    # This defines a section with the name "server.bindings", which reserves this name
    # for the entire configuration, preventing its redefinition.
    [server.bindings]
    port: 8080           # Defines a value with the name "server.bindings.port"

Straightforward Conflict Scenarios
----------------------------------

.. index::
    pair: Conflict; Section Name

Conflicts with Section Names
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The most straightforward type of name conflict occurs when two sections attempt to use the same name. The example below demonstrates this:

.. code-block:: erbsland-conf
    :class: bad-example
    :force:

    [main]                      # The section name "main" is used here.
    welcome: "Hello!"
    enabled: Yes

    [server]
    port: 8080

    [main]                      # ERROR! The name "main" is already defined.
    working dir: "/tmp"

In :term:`ELCL`, a section must be fully defined in one location within the configuration. Spreading a section’s definition across multiple locations within a file, or even across multiple files, is not possible.

.. index::
    pair: Conflict; Value Name

Conflicts with Value Names
~~~~~~~~~~~~~~~~~~~~~~~~~~

Name conflicts can also arise with values. If a value name is used more than once within the same section, it will result in an error:

.. code-block:: erbsland-conf
    :class: bad-example
    :force:

    [main]
    welcome: "Hello!"           # The value name "main.welcome" is used here.
    port: 8080
    welcome: "Bonjour!"         # ERROR! The value name "main.welcome" is already used.

In :term:`ELCL`, once a value is defined within a section, it cannot be redefined or overwritten at a later point in that same section.


Conflicts with Sections and Values Mixed
----------------------------------------

In *Erbsland Configuration Language* (ELCL), a section is treated like any other value (more details can be found in :ref:`ref-name-path` and :ref:`ref-section`). As a result, sections and values cannot share the same name.

.. code-block:: erbsland-conf
    :class: bad-example
    :force:

    [main]
    server: "host01.example.com"    # The value name "main.server" is defined here.

    [main.server]                   # ERROR! The name "main.server" is already used by a value.
    port: 8080

This rule applies regardless of the order in which the section or value is defined:

.. code-block:: erbsland-conf
    :class: bad-example
    :force:

    [server.binding]                # The section name "server.binding" is defined here.
    protocol: "https"
    port: 8080

    [server]
    binding: "127.0.0.1"            # ERROR! The name "server.binding" is already used by a section.


.. index::
    single: Section List

Why Section Lists Do Not Cause Conflicts
----------------------------------------

When using :ref:`section lists<ref-section>`, the same section name can be repeated without causing conflicts. This is because each section in the list creates a new entry, making the sections distinct.

.. literalinclude:: /documents/reference/section-lists-1.elcl
    :language: erbsland-conf

The configuration above produces the following :term:`value tree`:

.. configuration-tree:: /documents/reference/section-lists-1.elcl

In this case, even though the name `main.server` is repeated, each section list entry creates a new, unique item. Therefore, no conflicts occur. However, using the same name for a regular section or value would cause a conflict:

.. code-block:: erbsland-conf
    :class: bad-example
    :force:

    *[main.server]
    name: "host01"
    port: 8080
    # ...

    [main.server]                # ERROR! The name "main.server" is already used by a section list.

    [main]
    server: "host.example.com"   # ERROR! The name "main.server" is already used by a section list.


.. index::
    single: Intermediate Section

The Special Case of Intermediate Sections
-----------------------------------------

When you create a section with a longer :ref:`name path<ref-name-path>` where the initial names have not been used before, *intermediate sections* are automatically created for these names.

.. literalinclude:: /documents/reference/intermediate-section.elcl
    :language: erbsland-conf

Internally, to place the final element ``port`` at the correct location within the :ref:`value tree<ref-name-path>`, the intermediate sections ``main``, ``main.server``, and ``main.server.binding`` are implicitly created.

.. configuration-tree:: /documents/reference/intermediate-section.elcl


Defining Intermediate Sections Later in the Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Intermediate sections, created implicitly, do not count as *used names*. This means you can define sections with those names later in the configuration without causing conflicts.

.. code-block:: erbsland-conf
    :class: good-example

    [main.server.binding.port]
    filter: "any"

    [main]
    welcome: "Hello!"

    [main.server.binding]
    filter: Enabled

    [main.server]
    port: 8080

This flexibility allows sections to be defined in a less strict hierarchical order, making configurations easier to write and understand without being constrained by the order in which sections appear.


Conflicts When Mixing Intermediate Sections with Values or Lists
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Even though the names of intermediate sections do not count as used, an intermediate section already exists in the value tree if it contains at least one named section. Therefore, it cannot be redefined as a section list or value.

.. code-block:: erbsland-conf
    :class: bad-example
    :force:

    [main.server.binding.port]
    filter: "any"

    *[main.server.binding]  # ERROR! "main.server.binding" cannot be redefined as a section list.
    port: 8000

    [main]
    server: "host01"        # ERROR! "main.server" cannot be redefined as a value.


Features
--------

.. list-table::
    :header-rows: 1
    :width: 100%
    :widths: 25, 75

    *   -   Feature
        -   Coverage
    *   -   :text-code:`core`
        -   Regular names are part of the core language.
    *   -   :text-code:`section-list`
        -   Section lists are a standard feature.
    *   -   :text-code:`text-names`
        -   Text names are a standard feature.

Errors
------

.. list-table::
    :header-rows: 1
    :width: 100%
    :widths: 25, 75

    *   -   Error Code
        -   Causes
    *   -   :text-code:`NameConflict`
        -   |   Raised if a name is defined that was used before.
            |   Raised if text names are mixed with regular names.
            |   Raised if an intermediate section is defined as a section list or value.

