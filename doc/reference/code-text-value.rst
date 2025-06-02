..
    Copyright (c) 2025 Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

.. _ref-code-text-value:
.. index::
    single: Multi-line Code Text
    single: Code
    single: Code Text
    single: Code Text Value

Code Text Values
================

Code text values are a special format of :ref:`text values<ref-text-value>` that do not support :term:`escape sequences<escape sequence>`. Code text is enclosed within backticks (:cp:`60`), making it ideal for including short code snippets or text with many backslashes (:cp:`5c`) without the need to escape special characters. It is important to note that code text is not a separate data type; it is simply a formatting style for text values.

.. code-block:: bnf

    code                ::= BACKTICK code_text+ BACKTICK

    code_text           ::= TEXT - BACKTICK

For multi-line code, the format is slightly different, using triple backticks (:cp:`60`) to enclose the text. The content must follow consistent indentation patterns.

.. code-block:: bnf

    multi_line_code      ::= ml_code_start ml_code_line* ml_code_end

    ml_code_start       ::= "```" ( ALPHA FORMAT_DIGIT* )? end_of_line
    ml_code_end         ::= indentation_pattern "```"
    ml_code_line        ::= ( indentation_pattern TEXT+ )? end_of_line

In the following examples, you'll see a single-line code text and a multi-line code text:

.. code-block:: erbsland-conf
    :class: good-example

    [main]
    Python RegEx: `re.compile(r"(-*\*?)(\[)([ \t]*)(\.)?")`
    Python Map:
        ```
        TEXT_ESCAPE_SUBSTITUTIONS = {
            "\\": "\\",
            "n": "\n",
            "r": "\r",
            "t": "\t",
            '"': '"',
            "$": "$",
        }
        ```


.. index::
    pair: Rules; Code Text

Rules for Single Line Code Text
-------------------------------

#.  **Format:** Code text is enclosed between two backtick characters (:cp:`60`).

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        Code Text: `This is code text`

#.  **No Escape Sequences:** Escape sequences are not supported in code text. Any backslashes or other special characters are treated as literal characters.

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        No Escape: `\\\\\\\\\\\`

    .. note::

        There is no way to include the backtick character itself within single-line code text. If needed, consider using multi-line code text, which supports backticks within the content.

#.  **Valid Characters:** Any Unicode character is valid within code text, except control characters (excluding tab (:cp:`09`)) and the closing backtick (:cp:`60`).

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        Code: `re.compile(r"(-*\*?)(\[)([ \t]*)(\.)?")`


.. index::
    pair: Rules; Multi-line Code Text

Rules for Multi-line Code Text
------------------------------

#.  **Beginning the Text:** Multi-line code text begins with a sequence of *three* backtick characters (:cp:`60`). It *can* be followed by an optional language identifier. This sequence (backticks and optional language identifier) *can* also be followed by spaces or comments but *must* be followed by a line break.

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        code 1: ```
            text = "How are you?"
            ```
        code 2:      # Comments after the value separator.
            ```cpp   # Optional language identifier, followed by spacing or comments.
            if (text == "How are you?") {
                out << "I'm fine, thanks, how are you?\n"
            }
            ```

#.  **Language Identifier:** The language identifier must start with a letter (:cp:`a-z`, case-insensitive), and can be followed by a sequence of 0 to 15 letters (:cp:`a-z`, case-insensitive), digits (:cp:`0-9`), the hyphen (:cp:`-`) and underscores (:cp:`_`). The parser must treat the language identifier like a comment and ignore it.

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        code 2:
            ```java
            int sum = 5 + 3;
            System.out.println("Sum: " + sum);
            ```

    .. note::

        The language identifier is for syntax highlighting purposes only and is ignored by the parser.

#.  **Content and Indentation:** The content of the multi-line code text starts after the line break following the opening backticks. Each line *must* be indented by at least one space or tab character. Refer to :ref:`ref-spacing` for details on indentation.

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        code:
            ```
            r"(\n|\r\n)([ \t]+)(```)"
            ```

#.  **Consistent Indentation:** Each continued line of the multi-line code text must follow the exact sequence of spaces and tabs used at the start of the code text. This ensures that code requiring indentation retains its structure. See :ref:`ref-spacing` for more information.

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        code:
            ```cobol
                    IDENTIFICATION DIVISION.
                    PROGRAM-ID. HelloWorld.
                    PROCEDURE DIVISION.
                        DISPLAY 'Hello, World!'.
                        STOP RUN.
            ```

#.  **Ending the Text:** Multi-line code text ends on a new line with the same indentation as the previous lines, followed *immediately* by a sequence of three backtick characters (:cp:`60`).

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        code:
            ```
            // Code can contain backtick (`) characters
            System.out.println("Even multiple ones, like here: ```");
                    ``` // ← This is not the end.
            ``` # ← This is where the code ends.

    .. note::

        Unlike single-line code text, multi-line code text allows backtick characters within its content.

#.  **Allowed Characters:** Any Unicode character can be used in multi-line code text, except for :term:`control characters` (with the exception of the tab character, which is allowed).

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        code: ```rust
            fn main() {
                let greeting = "こんにちは, 世界!";
                println!("{}", greeting);
            }
            ```

#.  **No Escape Sequences:** Escape sequences are not supported in multi-line code text. Any backslashes or other special characters are treated as literal characters.

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        code: ```
            \u{1f604}\n\u2191 is just a random sequence of characters.
            ```

#.  **Line Breaks:** Each line break in multi-line code text is converted into a single newline character (:cp:`0a`), regardless of the original line break style used in the configuration document.

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        code: ```
            print("""
            """)
            ```

    The result will always be: ``print("""↵""")``.

#.  **Trimming Whitespace:** Leading and trailing whitespace around the code text is removed, as described in :ref:`ref-spacing`.

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        code:
            ```
                TEXT
            ```

    The resulting text will be: ``⎵⎵⎵⎵TEXT``.


Features
--------

.. list-table::
    :header-rows: 1
    :width: 100%
    :widths: 25, 75

    *   -   Feature
        -   Coverage
    *   -   :text-code:`code`
        -   Code text values are a standard feature.
    *   -   :text-code:`multi-line`
        -   Multi-line code text values are a standard feature.


Errors
------

.. list-table::
    :header-rows: 1
    :width: 100%
    :widths: 25, 75

    *   -   Error Code
        -   Causes
    *   -   :text-code:`Character`
        -   Raised if any illegal characters are found within the text.
    *   -   :text-code:`Syntax`
        -   Raised if the closing sequence of backtick characters is missing.
    *   -   :text-code:`Indentation`
        -   |   No space or tab character is present before a continued code text.
            |   The indentation pattern does not match the first entry for a continued code text.
    *   -   :text-code:`LimitExceeded`
        -   |   Raised if the code text exceeds the maximum size the parser can handle.
            |   Raised if the language identifier exceeds 16 characters.

