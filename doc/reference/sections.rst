..
    Copyright (c) 2024 Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

.. _ref-section:
.. index::
    single: Section

Sections
========

In :term:`ELCL`, a section can either define a new map of values or, in the case of a section list, a list of maps. The definition of a section, referred to as ``section_line`` in the following *EBNF* notation, opens the section for value assignments.

.. code-block:: bnf

    section_map_begin   ::= HYPHEN* SQ_BRACKET_OPEN
    section_map_end     ::= SQ_BRACKET_CLOSE HYPHEN*
    section_map         ::= section_map_begin spacing section_name spacing section_map_end

    section_list_begin  ::= HYPHEN* ASTERISK SQ_BRACKET_OPEN
    section_list_end    ::= SQ_BRACKET_CLOSE ASTERISK? HYPHEN*
    section_list        ::= section_list_begin spacing section_name spacing section_list_end

    section             ::= section_list | section_map
    section_line        ::= section end_of_line


.. index::
    pair: Rules; Section

Rules for Regular Sections
--------------------------

#.  **Square Brackets:** Section names must be enclosed in square brackets (:cp:`[` and :cp:`]`).

    .. code-block:: erbsland-conf
        :class: good-example

        [example_section]
        [ Example Section 2 ]
        [Example Section . Sub. Sub]

#.  **Regular Sections:** Regular sections create a new map of named values.

    .. code-block:: erbsland-conf
        :class: good-example

        [section]
        value 1: 123
        value 2: 456

#.  **Hyphens as Visual Separator:** Zero or more hyphen characters (:cp:`-`) may be placed before or after the square brackets as a visual separator.

    .. code-block:: erbsland-conf
        :class: good-example

        --------[ section 1 ]--------
        [section 2]------------------
        ------------------[section 3]

#.  **No Trailing Asterisk:** A trailing asterisk (:cp:`*`) must not be present after the closing square bracket (:cp:`]`).

    .. code-block:: text
        :class: bad-example

        [regular section]*   # ERROR! There must be no trailing asterisk.

#.  **No Leading Spacing:** There must be no spacing before the opening square bracket or hyphen character.

    .. code-block:: text
        :class: bad-example

        # Example Configuration
            [section]  # ERROR! There must be no spacing in front of a section.

#.  **Name Conflicts:** Guidelines for handling name conflicts are explained in detail in :ref:`ref-name-conflict`.


.. index::
    pair: Rules; Section List

Rules for Section Lists
-----------------------

#.  **Square Brackets with Asterisk:** Section names are enclosed in square brackets (:cp:`[` and :cp:`]`), with an asterisk (:cp:`*`) preceding the opening bracket.

    .. code-block:: erbsland-conf
        :class: good-example

        *[section list]
        *[ Section List ]
        *[main . server . connection]

#.  **New Value Map:** Section lists create a new list of value maps or add a new value map to an existing section list.

    .. code-block:: erbsland-conf
        :class: good-example

        *[list]  # Creates a new section list "list" and adds its first entry.
        *[list]  # Adds a second entry to the existing section list "list".

#.  **Optional Trailing Asterisk:** An optional asterisk (:cp:`*`) may be placed after the closing square bracket (:cp:`]`) for visual symmetry.

    .. code-block:: erbsland-conf
        :class: good-example

        *[section list]*
        *[ Section List ]*
        *[main . server . connection]*

#.  **Hyphens as Visual Separator:** Zero or more hyphen characters (:cp:`-`) may precede or follow the asterisk or square brackets as a visual separator.

    .. code-block:: erbsland-conf
        :class: good-example

        -------*[ list ]*-------
        -------*[ list ]--------
        *[list]-----------------
        ----------------*[list]*

#.  **No Leading Spacing:** There must be no spacing before the opening square bracket, asterisk, or hyphen character.

    .. code-block:: text
        :class: bad-example

        # Example Configuration
            *[section]  # ERROR! There must be no spacing in front of a section.

#.  **Name Conflicts:** Guidelines for handling name conflicts are explained in detail in :ref:`ref-name-conflict`.


Implementation
--------------

#.  A regular section defined in a configuration document, even if empty, creates a value of the type ``SectionWithNames``.

    .. literalinclude:: /documents/reference/two-empty-sections.elcl
        :language: erbsland-conf

    .. configuration-tree:: /documents/reference/two-empty-sections.elcl

#.  A section list creates a value of the type ``SectionList``, where each new entry is a ``SectionWithNames``.

    .. literalinclude:: /documents/reference/one-section-list-element.elcl
        :language: erbsland-conf

    .. configuration-tree:: /documents/reference/one-section-list-element.elcl

#.  If a section list with the given name already exists, a new ``SectionWithNames`` entry is added to that list.

    .. literalinclude:: /documents/reference/two-section-list-elements.elcl
        :language: erbsland-conf

    .. configuration-tree:: /documents/reference/two-section-list-elements.elcl

#.  For all missing intermediate elements in the name path, when defining a ``SectionWithNames`` or ``SectionList``, a new value of the type ``IntermediateSection`` is created.

    .. literalinclude:: /documents/reference/two-intermediate-sections.elcl
        :language: erbsland-conf

    .. configuration-tree:: /documents/reference/two-intermediate-sections.elcl

#.  If a section is defined, that exists as ``IntermediateSection``, it is converted into a ``SectionWithNames``.

    .. literalinclude:: /documents/reference/two-intermediate-sections2.elcl
        :language: erbsland-conf
        :emphasize-lines: 2

    .. configuration-tree:: /documents/reference/two-intermediate-sections2.elcl
        :highlight-path: one.two

#.  If a value or section with a text name is added to an empty ``SectionWithNames``, it is converted into a ``SectionWithTexts``.

    Initial definition:

    .. literalinclude:: /documents/reference/regular-to-text-section1.elcl
        :language: erbsland-conf

    .. configuration-tree:: /documents/reference/regular-to-text-section1.elcl

    After adding a value with a text-name:

    .. literalinclude:: /documents/reference/regular-to-text-section2.elcl
        :language: erbsland-conf

    .. configuration-tree:: /documents/reference/regular-to-text-section2.elcl

#.  If a sub section with a text name is added to an empty ``IntermediateSection``, it is converted into a ``SectionWithTexts``.

    Initial definition:

    .. literalinclude:: /documents/reference/regular-to-text-section1.elcl
        :language: erbsland-conf

    .. configuration-tree:: /documents/reference/regular-to-text-section1.elcl

    After adding a sub section with a text-name:

    .. literalinclude:: /documents/reference/regular-to-text-section3.elcl
        :language: erbsland-conf

    .. configuration-tree:: /documents/reference/regular-to-text-section3.elcl


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
    *   -   
        -   |   All errors related to invalid names (see :ref:`ref-name`).
            |   All errors related to invalid text names (see :ref:`ref-text-name`).
            |   All errors related to name conflicts (see :ref:`ref-name-conflict`).
    *   -   :text-code:`Syntax`
        -   If a trailing asterisk follows a regular section.


