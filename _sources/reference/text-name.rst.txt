..
    Copyright (c) 2024-2025 Tobias Erbsland - Erbsland DEV. https://erbsland.dev
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

#.  **Maximum Length:**
    A *text name* must not exceed 4000 **bytes** in length, which corresponds to the maximum line length permitted in the configuration document (without the enclosing double quotes).

    .. note::

        Because escape sequences are always fully resolved before a *text name* is stored, it is not possible for a *text name* to exceed this limit during parsing. Parser implementors can therefore choose to enforce this limit only at the API level, depending on their specific application needs.

.. _ref-text-name-normalization:
.. index::
    !single: Text Name Normalization
    pair: Normalization; Text Name

Text Name Normalization
-----------------------

Normalization of *text names* is performed according to these rules:

#.  **Resolve Escape Sequences:**
    All escape sequences in *text names* must be fully resolved into their corresponding Unicode characters.

    .. code-block:: text

        "\u{25b6}\u{fe0e}"  =>  "▶︎"

#.  **Preserve Double Quotes:**
    Double quotes surrounding *text names* are considered an integral part of the name. This distinction ensures that a *text name* cannot be confused with a regular name, even if they share the same character sequence.

    .. code-block:: text

        "He said \"hello!\""  =>  "he said "hello!""

    .. important::

        While double quotes are part of the *text name* for comparison purposes, a parser implementation does not necessarily have to store them. Instead, these quotes establish that a *text name* is always distinct from a regular name.

        For example, the regular name ``example`` will never match the *text name* ``"example"``, because the double quotes are considered part of the *text name*.
        Parser implementations can choose to store an accompanying type identifier—*regular name* or *text name*—alongside the normalized text, ensuring correct comparisons.


.. _ref-text-name-comparison:
.. index::
    !single: Text Name Comparison
    pair: Comparison; Text Name

Text Name Comparison
--------------------

#.  **Code-Point Comparison for Text Names:**
    Text names are compared by evaluating their Unicode code points directly, after all escape sequences have been resolved. For more details on normalization, refer to :ref:`ref-text-name-normalization`.

    .. code-block:: text

        "\u{25b6}\u{fe0e}"  ==  "▶︎"

    .. important::

        **Parsers are not required to perform Unicode normalization during text name comparison.** Text names can be processed directly as UTF-8 encoded byte sequences. It is the responsibility of the application layer to handle any additional normalization or verification as needed for the specific use case.

#.  **Regular Names and Text Names Are Never Equal:**
    Regular names and text names are inherently distinct. Even if their content is identical, they must never be considered equal because the double quotes are part of the *text name*.

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
    *   -   :text-code:`LimitExceeded`
        -   Raised if a text name exceeds the 4000-byte limit.
