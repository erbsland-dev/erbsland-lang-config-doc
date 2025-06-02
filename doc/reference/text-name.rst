..
    Copyright (c) 2024 Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

.. _ref-text-name:
.. index::
    !single: Text Name

Text Names
==========

In the *Erbsland Configuration Language* (ELCL), *text names* are used for special cases where a single-line text is mapped to a section or a value. A *text name* is essentially a double-quoted string, as defined in the :ref:`ref-text` chapter.

.. code-block:: bnf

    text_name           ::= text

.. code-block:: erbsland-conf
    :class: good-example

    [filter."😀"]         # A section with a text name.
    value: 123

    [Translation.jp]      # A section with values that use text names.
    "Good Morning!"       = "おはようございます！"
    "Have a great day!"   = "良い一日をお過ごしください！"
    "What is your name?"  = "お名前は何ですか？"

The syntax of *text names* follows the same rules as those used for values. However, there are additional restrictions when *text names* are applied in specific contexts, such as :ref:`sections<ref-section-name>` or as a :ref:`name for values<ref-named-value>`.

.. important::

    **A parser is not required to perform Unicode normalization on text names.**

    Text names can be processed internally as UTF-8 encoded byte-data. It is the responsibility of the application to manage Unicode normalization or apply any additional text checks, depending on its use case.


.. index::
    single: Text Name Rules
    pair: Rules; Text Name

Text Name Rules
---------------

The following rules for :term:`text names<text name>` apply not only to :term:`sections<section>`, but also to the names of :term:`values<value>` within a section.

#.  **Do Not Mix Text Names and Regular Names:** Text names and regular names *must not* be mixed within the same section. If a section contains a regular name and the parser encounters a text name, it must raise a ``NameConflict`` error.

    .. code-block:: text
        :class: bad-example

        [text_names_for_values]
        name: 123
        "text": 123     # ERROR! Regular and text names must not be mixed.

    .. code-block:: text
        :class: bad-example

        [section.name]
        name: 123
        [section."text"]   # ERROR! Regular and text names must not be mixed.
        name: 123

#.  **Unique Names:** All names, whether regular or text names, *must* be unique within a section. Refer to :ref:`ref-name-comparison` for detailed information. If the parser encounters a duplicate name, it must raise a ``NameConflict`` error.

    .. code-block:: text
        :class: bad-example

        [unique_names]
        name: 123
        name: 123  # ERROR! Names must be unique.

    .. code-block:: text
        :class: bad-example

        [unique_text_names]
        "text": 123
        "text": 123  # ERROR! Text names must be unique.

#.  **No Subsections in Text-Named Sections:** Sections that use text names *must not* contain subsections. If a subsection is encountered within a text-named section, the parser must raise an error.

    .. code-block:: text
        :class: bad-example

        [text."one"]
        name: 123
        [.subsection]  # ERROR! No subsections allowed in text-named sections.
        [example."text".subsection]  # ERROR! No subsections allowed in text-named sections.

#.  **No Text Names for Section Lists:** Section lists *must not* use text names. Attempting to use a text name in a section list will result in an error.

    .. code-block:: text
        :class: bad-example
    
        *[text."one"]  # ERROR! Section lists must not have text names.
        *[text."one"]


.. _ref-text-name-normalization:
.. index::
    !single: Text Name Normalization
    pair: Normalization; Text Name

Text Name Normalization
-----------------------

Normalization of *text names* is performed according to the following rule:

#.  **Resolve Escape Sequences:** All escape sequences must be fully resolved into their corresponding Unicode characters.

    .. code-block:: text

        "\u{25b6}\u{fe0e}"                 => "▶︎"

#.  **Preserve Double Quotes:** The double quotes around *text names* are considered part of the name itself, which distinguishes a text name from a regular name.

    .. code-block:: text

        "He said \"hello!\""               => "he said "hello!""


.. _ref-text-name-comparison:
.. index::
    !single: Text Name Comparison
    pair: Comparison; Text Name

Text Name Comparison
--------------------

#.  **Code-Point Comparison for Text Names:** Text names are compared based on their Unicode code points, after normalization (see :ref:`ref-text-name-normalization` for details). The comparison is done directly on the *code points* of the text name.

    .. code-block:: text

        "\u{25b6}\u{fe0e}"                 == "▶︎"

    .. important::

        **A parser is not required to perform Unicode normalization for text name comparison.**

        Text names may be processed as UTF-8 encoded byte-data. Applications are responsible for normalization or any additional checks required by their use case.

#.  **Regular Names and Text Names Are Never Equal:** A regular name must never be considered equal to a text name, even if their content appears identical. This is because the double quotes in text names are part of the name.

    .. code-block:: text

        "text" != text


Features
--------

.. list-table::
    :header-rows: 1
    :width: 100%
    :widths: 25, 75

    *   -   Feature
        -   Coverage
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
    *   -   :text-code:`Character`
        -   Raised if a "null" escape sequence is found in a text name.
    *   -   :text-code:`Syntax`
        -   Raised if text names and regular names are mixed.
    *   -   :text-code:`NameConflict`
        -   Raised if an already used text name is reused.
