..
    Copyright (c) 2024 Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

.. _ref-section-name:
.. index::
    !single: Section Name

Section Names
=============

Section names in *Erbsland Configuration Language* (ELCL) follow a structured format called *name paths*, as described in :ref:`ref-name-path`. These section names serve to organize the configuration into hierarchical structures.

.. code-block:: bnf

    name_separator      ::= spacing PERIOD spacing

    section_abs_name    ::= name (name_separator name)*
    section_rel_name    ::= name_separator section_abs_name
    section_abs_text    ::= section_abs_name name_separator text_name
    section_rel_text    ::= section_separator (name name_separator)* text_name

    section_name        ::= section_abs_name | section_rel_name |
                            section_abs_text | section_rel_text

This section focuses on the rules for naming sections, while the detailed behavior of sections is covered later in :ref:`ref-section`. The rule ``text_name`` in the syntax above is defined in :ref:`ref-text-name`.

Section Name Rules
------------------

#.  **Name Paths:** Section names consist of one or more names, separated by a period (:cp:`.`). Each name in the path represents a hierarchy level, with the last name referring to the specific section.

    .. code-block:: erbsland-conf
        :class: good-example

        [one.two.three]  # Defines the section "three" within "one.two"

#.  **Absolute Sections:** A section name that starts with a name is considered an :term:`absolute section`. This means the section is defined from the root of the configuration document.

    .. code-block:: erbsland-conf
        :class: good-example

        [one.two.three]  # Absolute section starting at the root

#.  **Relative Sections:** A section name starting with a :term:`name separator` is a :term:`relative section`, indicating that the path is relative to the *last defined* absolute section.

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        [.server.filter]  # Relative section => resolves to "main.server.filter"

#.  **No Relative Section at Start:** A configuration document must *not* start with a relative section. The first section in a document must always be an absolute section.

    .. code-block:: text
        :class: bad-example
        :force:

        [.server.filter]  # ERROR! Cannot start with a relative section

#.  **No Consecutive Name Separators:** A name path must *not* contain multiple consecutive periods (:cp:`.`) as name separators.

    .. code-block:: text
        :class: bad-example
        :force:

        [one..two]  # ERROR! Consecutive periods are not allowed

#.  **No Trailing Name Separator:** A name path must *not* end with a period.

    .. code-block:: text
        :class: bad-example
        :force:

        [one.two.]  # ERROR! The path cannot end with a period

#.  **Name Path Length Limit:** A name path must not exceed 10 names. If a section name has more than 10 names, it will be considered invalid.

    .. code-block:: text
        :class: bad-example
        :force:

        [one.two.three.four.five.six.seven.eight.nine.ten.eleven]  # ERROR! Exceeds the limit of 10 names

    .. micro-parser::

        The name path limit is *five* names.


.. index::
    single: Relative Section

Relative Sections Explained
---------------------------

Relative sections in *Erbsland Configuration Language* (ELCL) start with a :term:`name separator` and must always follow a previously defined :term:`absolute section`. Relative sections extend the path of the most recently defined absolute section, meaning they are not *nested* sections, but rather continue from the last absolute section defined.

The example below illustrates a configuration with a mix of absolute and relative sections. To simplify, the sections are left empty without any values:

.. literalinclude:: /documents/reference/section-names-1.elcl
    :language: erbsland-conf

This configuration is transformed into the following :ref:`value tree<ref-name-path>`:

.. configuration-tree:: /documents/reference/section-names-1.elcl
    :hide-content:

In the example above, each relative section (starting with a period) extends the path of the last absolute section that was defined. For example, ``.sub1`` and ``.sub2`` extend from both ``main.sub.sub_a`` and ``main.sub.sub_b`` depending on their position in the configuration.


.. index::
    single: Intermediate Section Rules
    pair: Rules; Text Name

Intermediate Section Rules
--------------------------

#.  **Create Missing Elements:** If a name in the name path defining a section is unused at the point of its definition, an :term:`intermediate section` must be created implicitly for all these elements.

    .. literalinclude:: /documents/reference/intermediate-section.elcl
        :language: erbsland-conf

    .. configuration-tree:: /documents/reference/intermediate-section.elcl


#.  **Names of Intermediate Sections Stay Unused:** The names for implicitly created intermediate sections do not count used. Therefore a regular section with that name can be defined later in a configuration.

    .. code-block:: erbsland-conf
        :class: good-example

        [main.server]
        port: 8000

        [main]  # That's ok!
        threads: 16

#.  **No Redefinition as Section List or Value:** Intermediate sections *must not* not be (re-)defined as a section list or value later in the configuration.

    .. code-block:: erbsland-conf
        :class: bad-example
        :force:

        [main.server.binding]
        port: 8000

        *[main.server]       # ERROR! You must not redefine "server" as section list.
        name: "example"

        [main]
        server: "host01"     # ERROR! You must not redefine "server" as a value.


.. index::
    single: Section List Rules
    pair: Rules; Section List

Section List Rules for Name Paths
---------------------------------

There is one critical rule regarding the use of *section lists* in a name path:

#.  **Use the Last Element:** If a section list appears in the *middle* of a :ref:`name path<ref-name-path>`, the *last element* in the list is used to continue following the path.

.. important::

    Please note that the *last element* refers to the last element *at the time* the name path is defined in the configuration. With each new section defined for a section list, the last element points to the newly added element.

Implications of This Rule
~~~~~~~~~~~~~~~~~~~~~~~~~

At first glance, repeating the section ``server.filter`` might seem like a potential conflict. However, due to the rule that only the last element of the section list is referenced, each definition of ``server.filter`` points to a unique instance.

.. literalinclude:: /documents/reference/section-list-reference-1.elcl
    :language: erbsland-conf

In the configuration above, two sections of ``server.filter`` are defined under different ``server`` entries. The resulting :ref:`value tree<ref-name-path>` looks like this:

.. configuration-tree:: /documents/reference/section-list-reference-1.elcl

This configuration can also be written using relative *name paths* to achieve the same result.

.. code-block:: erbsland-conf
    :class: good-example

    *[server]
    name: "host01"
    port: 9000

    [.filter]
    reject: "udp"

    *[server]
    name: "host02"
    port: 8000

    [.filter]
    reject: "tcp"

This alternative produces the same value tree.

Nested Section Lists
~~~~~~~~~~~~~~~~~~~~

Section lists can also be nested, and the same simple rule applies: the last element in the list is used to continue the path. Even with nested sections, this rule remains straightforward to follow.

.. literalinclude:: /documents/reference/section-list-reference-2.elcl
    :language: erbsland-conf

In this more complex configuration, multiple ``filter`` sections are nested under different ``server`` entries. The resulting value tree maintains the structure of unique instances:

.. configuration-tree:: /documents/reference/section-list-reference-2.elcl

This configuration demonstrates how nested section lists are managed:

- Each section under ``main.server`` is unique, and the last element in the list is used to build the value tree.
- Nested lists (such as ``filter``) still follow the same rule, therefore ``.filter.log`` is added to the first entry of the new ``filter`` section list.


Features
--------

.. list-table::
    :header-rows: 1
    :width: 100%
    :widths: 25, 75

    *   -   Feature
        -   Coverage
    *   -   :text-code:`core`
        -   Regular names, name paths, absolute and relative regular sections are part of the core language.
    *   -   :text-code:`section-list`
        -   Section lists are a standard feature.
    *   -   :text-code:`text-names`
        -   Text names and sections with text names are a standard feature.


Errors
------

.. list-table::
    :header-rows: 1
    :width: 100%
    :widths: 25, 75

    *   -   Error Code
        -   Causes
    *   -   :text-code:`NameConflict`
        -   Raised for any name conflict as described here and in :ref:`ref-name-conflict`.
    *   -   :text-code:`Syntax`
        -   |   Raised if a document starts with a relative section.
            |   Raised if a name path contains multiple consecutive name separators.
            |   Raised if a name path ends in a name separator.
    *   -   :text-code:`LimitExceeded`
        -   Raised if a name path has more than 10 elements.

