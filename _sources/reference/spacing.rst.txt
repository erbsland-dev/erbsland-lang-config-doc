..
    Copyright (c) 2024-2025 Tobias Erbsland - Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

.. _ref-spacing:
.. index::
    !single: Spacing
    single: Space
    single: Tab

Spacing
=======

In an :term:`ELCL` document, spacing is crucial for indentation and alignment. Proper use of spacing ensures readability and helps the parser correctly interpret the structure of the document.

.. code-block:: bnf

    spacing             ::= (SPACE | TAB)*        /* optional spacing */
    indentation_pattern ::= (SPACE | TAB)+        /* required indentation */

.. note::

    To visualize the spacing in the examples in this chapter, we use the symbols ``⎵`` (for space) and ``→`` (for tab). In the results, ``↵`` is used to represent a newline character.

.. index::
    pair: Rules; Spacing

Rules
-----

#.  **Valid Characters for Spacing:** Spacing can consist of any combination of spaces (:cp:`20`) and tab characters (:cp:`09`). These characters can be used freely within lines to separate elements or align content.

    .. code-block:: text

        [→      ⎵⎵name⎵⎵]→      # Example with space and tab usage

#.  **Consistent Indentation Pattern:** When continuing multi-line text, code, byte-data, or regular expression values, the indentation pattern used on each consecutive line **must** match exactly. This means each line must use the same combination and sequence of spaces and tabs for alignment. Completely empty lines, however, are exempt from this rule.

    .. code-block:: text

        [main]
        text: """
        ⎵⎵⎵⎵⎵⎵⎵⎵First Line
        →          Second Line   # ERROR! Indentation pattern must match.
        ⎵⎵⎵⎵⎵⎵⎵⎵"""

#.  **Spacing at the Beginning:** Spacing at the beginning of multi-line text, code, byte-data, or regular expression values (i.e., between the opening quote and the first line of content) is not part of the value. Only the characters between the opening sequence and the line break are considered for spacing, along with the indentation pattern on the following lines.

    In the example below, the spacing between ``"""`` and ``One`` on the first line is ignored.

    .. code-block:: text

        [main]
        text: """⎵⎵⎵⎵
        ⎵⎵⎵⎵One⎵
        ⎵⎵⎵⎵Two⎵⎵
        ⎵⎵⎵⎵"""

#.  **Spacing at the End:** Spacing at the end of multi-line text, code, byte-data, or regular expression values (i.e., between the last line and the closing quote) is also not part of the value.

    In the example below, the spacing after ``Two`` and before the closing quote ``"""`` is ignored.

    .. code-block:: text

        [main]
        text: """⎵⎵⎵⎵
        ⎵⎵⎵⎵One⎵
        ⎵⎵⎵⎵Two⎵⎵
        ⎵⎵⎵⎵"""

#.  **Spacing at Line Ends:** Any spacing at the end of each line in multi-line text, byte-data, or regular expression values is ignored and not included as part of the value.

    In the example below, the space after ``One`` and the two spaces after ``Two`` are excluded from the final value.

    .. code-block:: text

        [main]
        text: """⎵⎵⎵⎵
        ⎵⎵⎵⎵One⎵
        ⎵⎵⎵⎵Two⎵⎵
        ⎵⎵⎵⎵"""


.. _ref-indentation-pattern:
.. index::
    single: Indentation Pattern

Strict Indentation Patterns Explained
-------------------------------------

:term:`ELCL` enforces strict indentation patterns for multi-line values to prevent misconfigurations. This rule helps avoid issues, such as accidentally mixing tabs and spaces, which can lead to incorrect interpretation of text and code in the configuration. By enforcing a consistent pattern, it also allows parsers to strip unnecessary indentation while preserving the intended format.

The rule for ``indentation_pattern`` in the EBNF syntax indicates where the parser must ensure matching indentation across multi-line values. Each subsequent line in a multi-line value must follow the same pattern as the first line. Any spacing after this pattern is treated as part of the value itself.

This rule applies only to multi-line values such as text, code, byte-data, and regular expressions. Single-line values that continue on the next line after the value separator do not require indentation pattern matching.

Matching Patterns
~~~~~~~~~~~~~~~~~

In the following example, mixed spaces and tabs are used for indentation in a multi-line value:

.. code-block:: erbsland-conf

    [main]
    text: """
          One
          Two
          Three
          """

The ``┊`` character represents the baseline of the indentation pattern. All characters before this baseline are removed from the value.

.. code-block:: text

    [main]
    text: """
    →   ⎵⎵┊One
    →   ⎵⎵┊Two
    →   ⎵⎵┊Three
    →   ⎵⎵┊"""

The resulting value is ``One↵Two↵Three``.

Empty Lines
~~~~~~~~~~~

If a line is completely empty—meaning it contains only spaces, tabs, or no characters at all—the indentation pattern for that line is ignored. Here's an example demonstrating both cases:

.. code-block:: text
    :emphasize-lines: 4, 6

    [main]
    text: """
    →   ⎵⎵┊One

    →   ⎵⎵┊Two
    →→→→⎵⎵
    →   ⎵⎵┊Three
    →   ⎵⎵┊"""

The resulting text is ``One↵↵Two↵↵Three``, where the empty lines are preserved in the final output.

Spacing in the Content
~~~~~~~~~~~~~~~~~~~~~~

The purpose of strict indentation pattern matching is to allow for safe and predictable indentation of multi-line content such as text or code. Here’s an example where spaces are included within the content itself:

.. code-block:: text

    [main]
    text: """
    ⎵⎵⎵⎵┊One
    ⎵⎵⎵⎵┊⎵⎵Two
    ⎵⎵⎵⎵┊⎵⎵⎵⎵Three
    ⎵⎵⎵⎵┊"""

The resulting text will be ``One↵⎵⎵Two↵⎵⎵⎵⎵Three``, with spaces preserved within the content.

Indentation in the First Line
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If a multi-line value begins on the next line after the value separator, the opening indentation pattern will be set by the line with the opening quotes. This allows for the first line to be indented as well.

.. code-block:: text

    [main]
    text:
    ⎵⎵⎵⎵┊"""
    ⎵⎵⎵⎵┊⎵⎵⎵⎵One
    ⎵⎵⎵⎵┊⎵⎵Two
    ⎵⎵⎵⎵┊Three
    ⎵⎵⎵⎵┊"""

The resulting text is ``⎵⎵⎵⎵One↵⎵⎵Two↵Three``, maintaining the initial indentation of the first line.


.. index::
    single: Spacing Removal

Ignored Spacing in Multi-line Text
----------------------------------

:term:`ELCL` automatically removes unwanted spacing from the beginning and end of multi-line text, as well as any trailing spacing at the end of each line. This behavior reflects a common requirement in text processing, where leading and trailing spacing is typically unnecessary. By handling this automatically, *ELCL* simplifies application code and makes configuration files more robust.

Spacing at the Beginning and End
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the following example, all the spacing before the first line and after the last line is removed:

.. code-block:: text

    [main]
    text: """⎵⎵⎵⎵
    ⎵⎵⎵⎵First⎵line⎵
    ⎵⎵⎵⎵Second⎵line⎵⎵⎵
    ⎵⎵⎵⎵"""

This results in the text: ``First⎵line↵Second⎵line``. The spaces at the start, after "Second⎵line", and at the end of each line are ignored.

Adding Empty Lines
~~~~~~~~~~~~~~~~~~

The spacing removal rule applies only to spacing around the content, meaning that empty lines can still be added if needed for specific use cases. You can add empty lines at the beginning or end of the text, or even within the text itself:

.. code-block:: text

    [main]
    text: """

    ⎵⎵⎵⎵Second⎵line

    ⎵⎵⎵⎵Fourth⎵line

    ⎵⎵⎵⎵"""

This results in the text: ``↵Second⎵line↵↵Fourth⎵line↵``, with leading and trailing empty lines retained.

Adding Trailing Spacing
~~~~~~~~~~~~~~~~~~~~~~~

If trailing spaces at the end of a line are required, they can be explicitly added using the escape sequence for the space character ``\u{20}``. This ensures that the spacing is preserved in the final output.

.. code-block:: text

    [main]
    text: """
    ⎵⎵⎵⎵Trailing⎵Space⎵⎵⎵⎵\u{20}
    ⎵⎵⎵⎵"""

This results in the text: ``Trailing⎵Space⎵⎵⎵⎵⎵``, where the trailing spaces are maintained.


Features
--------

.. list-table::
    :header-rows: 1
    :width: 100%
    :widths: 25, 75

    *   -   Feature
        -   Coverage
    *   -   :text-code:`core`
        -   Spacing, comment and indentation pattern matching are part of the core language.
    *   -   :text-code:`multi-line`
        -   Multi-line values are a standard feature.


Errors
------

.. list-table::
    :header-rows: 1
    :width: 100%
    :widths: 25, 75

    *   -   Error Code
        -   Causes
    *   -   :text-code:`Indentation`
        -   |   No space or tab character is present before a continued value.
            |   The indentation pattern does not match the first entry for a continued value.
