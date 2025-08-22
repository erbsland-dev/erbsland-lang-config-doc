..
    Copyright (c) 2024-2025 Tobias Erbsland - Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

.. _ref-regular-expression-value:
.. index::
    single: Multi-line Regular Expression
    single: Regular Expression
    single: Regular Expression Value

Regular Expression Values
=========================

Regular expression values are a special data type and format designed specifically for including regular expressions in configuration files. These values are enclosed in slash characters (:cp:`/`), similar to many programming languages that support regular expressions.

.. code-block:: bnf

    regex               ::= SLASH ( regex_text | regex_escape )* SLASH

    regex_text          ::= TEXT - SLASH
    regex_escape        ::= BACKSLASH TEXT

For multi-line regular expression values, the format differs slightly. Multi-line regular expressions are enclosed in triple slashes (``///``) and allow regular expressions to span multiple lines.

.. code-block:: bnf

    multi_line_regexp    ::= ml_regex_start ml_regex_line* ml_regex_end

    ml_regex_start      ::= "///" end_of_line
    ml_regex_end        ::= indentation_pattern "///"
    ml_regex_line       ::= ( indentation_pattern ( regex_escape | TEXT )+ )? end_of_line

In the following examples, you’ll see both a single-line regular expression value and a multi-line regular expression value:

.. code-block:: erbsland-conf
    :class: good-example

    [main]
    Meta Name: /(?i)(?=@?[a-z\"])/
    Float:
        ///
        (?i)
        [-+]?                                      # Positive or negative sign.
        (?:
            (?:                                    # [X].Y[E+Z] notation.
                (?: (?: \d+ \u0027 )* \d+ )? \. (?: \d+ \u0027 )* \d+
            |                                      # X.[Y][E+Z] notation.
                (?: \d+ \u0027 )* \d+ \. (?: (?: \d+ \u0027 )* \d+ )?
            )
            (?:
                e[-+]? \d+
            )?
        |                                          # XE+Z notation.
            (?: \d+ \u0027 )* \d+
            e[-+]? \d+
        )
        ///


.. index::
    pair: Rules; Regular Expression

Rules for Regular Expression Values
-----------------------------------

#.  **Format:** Single-line regular expression values are enclosed between slash characters (:cp:`/`).

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        Line Break: /\n|\r\n/

#.  **Valid Characters:** Any Unicode character can be used within regular expression values, except for slashes (which indicate the end of the value), backslashes (which are used for escape sequences), and :term:`control characters` (except the tab character, which is allowed).

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        Text: /[^\x00-\x08\x0A-\x1F\x7F-\x9F]+/

#.  **Escape Sequences:** A backslash (:cp:`5c`) followed by any Unicode character (except control characters) is treated as an escape sequence. If the character following the backslash is a slash, the escape sequence will resolve to a literal slash. For any other character, the escape sequence is passed unchanged into the regular expression.

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        Path: /\/data\/test_\w+\.elcl/

    .. note::

        The main purpose of escape sequences in regular expression values is to allow escaping the closing slash character. Other escape sequences are passed through as part of the regular expression text and do not need to be interpreted by the parser. The parser only needs to properly handle ``\/`` for escaping slashes and ``\\`` for escaping backslashes.


.. index::
    pair: Rules; Multi-line Regular Expression

Rules for Multi-line Regular Expression Values
----------------------------------------------

#.  **Beginning the Regular Expression:** A multi-line regular expression starts with a sequence of *three* slashes (``///``). It *may* be followed by spaces or comments, but it *must* be followed by a line break.

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        Decimal Integer: ///
            (?i)
            [-+]?                               # Positive or negative sign
            0x                                  # Hex prefix
            (?: [a-f0-9]+ \u0027 )* [a-f0-9]+   # Hexadecimal digits with optional '
            ///
        Hexadecimal Integer:        # Comment
            ///                     # Optional comment
            (?i)
            [-+]?                               # Positive or negative sign
            0b                                  # Binary prefix
            (?: [01]+ \u0027 )* [01]+           # Binary digits with optional '
            ///

#.  **Content Start and Indentation:** The content of the multi-line regular expression begins after the line break following the opening sequence. Each line *must* be indented by at least one space or tab character. Refer to :ref:`ref-spacing` for details on indentation.

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        Binary Integer: ///
            (?i)
            [-+]?                                    # Positive or negative sign
            (?: \d+ \u0027 )* \d+                    # Integer digits with optional '
            ///

#.  **Allowed Characters:** Any Unicode character can be used in multi-line regular expression values, except the backslash (which is used for escape sequences) and all :term:`control characters` (except the tab character, which is allowed).

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        Data: ///
            ( /// )
            ( [ \t]* )
            ///

#.  **Escape Sequences:** A backslash (:cp:`5c`) followed by a Unicode character (except control characters) is treated as an escape sequence. If the character after the backslash is a slash, the escape sequence will resolve to a literal slash. For any other character, the escape sequence remains unchanged as part of the regular expression.

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        Path: ///
            ^
            \///: drive \\ ( .* )
            $
            ///

#.  **Consistent Indentation:** Each line of the multi-line regular expression must follow the same indentation pattern as the first line. After the initial indentation, additional spaces can be used to align content. See :ref:`ref-spacing` for more details.

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        Byte Count:
            ///
            (?i)
            (
                [-+]?                    # Positive or negative sign
                (?: \d+ \u0027 )* \d+    # Integer digits with optional '
            )
            ( \x20 )?                    # Optional space between digits and unit
            ( [kmgtpezy] i? b )          # ISO unit up to yottabytes
            ///

#.  **Ending the Regular Expression:** A multi-line regular expression ends on a new line with the same indentation as the previous lines, followed immediately by a sequence of three slashes (``///``).

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        Data: ///
            (?i)
            [-+]?
            (?: inf | nan )
            ///

    .. code-block:: text
        :class: bad-example
        :force:

        [main]
        Data: ///
            (?i)
            [-+]?
            (?: inf | nan )
                ///  # ERROR! Indentation pattern does not match.

#.  **Line Breaks:** Each line break in a multi-line regular expression is converted into a single newline character (:cp:`0a`), regardless of the original line break style used in the configuration document.

#.  **Extended Syntax:** If a parser treats regular expression values as regular expression objects, it *should* automatically enable extended syntax (allowing whitespace and comments) when handling multi-line regular expression values.


Features
--------

.. list-table::
    :header-rows: 1
    :width: 100%
    :widths: 25, 75

    *   -   Feature
        -   Coverage
    *   -   :text-code:`regex`
        -   Regular expression values are an advanced feature.
    *   -   :text-code:`multi-line`
        -   Multi-line regular expression values are a standard feature.

Errors
------

.. list-table::
    :header-rows: 1
    :width: 100%
    :widths: 25, 75

    *   -   Error Code
        -   Causes
    *   -   :text-code:`Syntax`
        -   |   Raised if the closing sequence (``///``) is missing.
            |   *Can* be raised if the regular expression syntax is invalid.
    *   -   :text-code:`Indentation`
        -   |   Raised if no space or tab character is present at the start of a continued line.
            |   Raised if the indentation pattern does not match the first line for multi-line regular expression values.
    *   -   :text-code:`LimitExceeded`
        -   Raised if the regular expression value exceeds the maximum size the parser can handle.
