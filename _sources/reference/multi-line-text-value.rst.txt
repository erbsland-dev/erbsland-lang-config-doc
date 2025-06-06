..
    Copyright (c) 2024 Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

.. _ref-multi-line-text-value:
.. index::
    single: Multi-line Text
    single: Multi-line Text Value

Multi-line Text Values
======================

Multi-line text allows text values to span multiple lines, providing a convenient way to handle large blocks of text.

.. code-block:: bnf

    multi_line_text      ::= ml_text_start ml_text_line* ml_text_end

    ml_text_start       ::= '"""' end_of_line
    ml_text_end         ::= indentation_pattern '"""'
    ml_text_line        ::= ( indentation_pattern TEXT+ )? end_of_line

Below is an example of valid multi-line text values:

.. code-block:: erbsland-conf
    :class: good-example

    [main]
    text 1: """
        “Hello!” exclaimed the multi-line text,
        As it flowed across the lines;
        It pondered what might happen next,
        And hoped to fit within the rhymes.
        """
    text 2:
        """
            Bracket stands alone
                Indentation now looks fine
                    Code is clean again
        """

.. index::
    pair: Rules; Multi-line Text

Rules for Multi-line Text
-------------------------

#.  **Beginning the Text:** Multi-line text begins with a sequence of three double-quote characters (``"""``). It *can* be followed by spaces or comments but *must* be followed by a line break.

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        text 1: """
            "Kommer du?"
            """
        text 2:         # Spurte hun håpefullt
            """         # Ventende ved døren
            "Ja, jeg skal bare hente jakken min."
            """

#.  **Content and Indentation:** The content of the multi-line text starts after the line break following the opening quotes. Each line *must* be indented by at least one space or tab character. Refer to :ref:`ref-spacing` for details on indentation.

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        text:
            """
            Les vérités invisibles sont les plus profondes.
            """

#.  **Consistent Indentation:** Each line of the multi-line text must follow the exact sequence of spaces and tabs used at the beginning of the text. This ensures consistent indentation. See :ref:`ref-spacing` for more information.

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        text:
            """
            La niebla cubre
            Los caminos sin huellas
            Misterio oculto
            """

#.  **Ending the Text:** Multi-line text ends on a new line with the repeated indentation sequence, followed immediately by a sequence of three double-quote characters (``"""``).

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        text:
            """
            Programmer's note: "Remember to close your loops!"""  ← this isn't the end
                """And don't forget semicolons;" she added.       ← still going
            """ # ← This is where the text ends.

#.  **Allowed Characters:** Any Unicode character can be used in multi-line text, except backslashes (which introduce *escape sequences*) and :term:`control characters`, with the exception of the tab character, which is allowed.

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        text: """
            彼は興奮した様子で言った："ダブルクオート文字はここで使える！"
            どうやら彼は、それが日本語のテキストには不適切な文字だと知らなかったようだ…
            """

    .. note::

        Unlike single-line text values, double quotes are allowed within multi-line text without escaping.

#.  **Escape Sequences:** All escape sequences valid for single-line text are also valid in multi-line text. For detailed information about escape sequences, see :ref:`ref-text-escape-sequence`.

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        text: """
            \u{1f604}\n\u2191 is a grinning face with smiling eyes
            """

#.  **Line Breaks:** Each line break in the multi-line text is converted into a single newline character (:cp:`0a`), regardless of the original line break style used in the configuration document.

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        text: """
            Morning sun rises
            Afternoon clouds drift slowly
            Evening stars twinkle
            """

    This will always result in: ``Morning sun rises↵Afternoon clouds drift slowly↵Evening stars twinkle``.

#.  **Trimming Whitespace:** Leading and trailing whitespace around the text is removed, as described in :ref:`ref-spacing`.

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        text: """
            Simplicity is the ultimate sophistication.
            """

    The resulting text will be: ``Simplicity is the ultimate sophistication.``. The leading and trailing spacing, including the final line break, is removed.

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        text:
            """
                "Simplicity is the ultimate sophistication."
            """

    In this second example, the resulting text will be: ``⎵⎵⎵⎵"Simplicity is the ultimate sophistication."``. While the leading spacing is removed, only the characters after the opening sequence, including the line-break and the indentation pattern count as spacing. Every character afterwards is part of the content. See :ref:`ref-spacing` for details.

Features
--------

.. list-table::
    :header-rows: 1
    :width: 100%
    :widths: 25, 75

    *   -   Feature
        -   Coverage
    *   -   :text-code:`core`
        -   Escape sequences in multi-line text are part of the core language.
    *   -   :text-code:`multi-line`
        -   Multi-line text values are a standard feature.

Errors
------

.. list-table::
    :header-rows: 1
    :width: 100%
    :widths: 25, 75

    *   -   Error Code
        -   Causes
    *   -   :text-code:`Character`
        -   Raised for any illegal character or invalid escape sequence within the text.
    *   -   :text-code:`Syntax`
        -   Raised if the closing sequence of double quotes is missing at the end of the line or document.
    *   -   :text-code:`Indentation`
        -   |   No space or tab character is present before a continued text.
            |   The indentation pattern does not match the first entry for a continued text.
    *   -   :text-code:`LimitExceeded`
        -   Raised if the text exceeds the maximum size the parser can handle.

