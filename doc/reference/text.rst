..
    Copyright (c) 2024 Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

.. _ref-text:
.. index::
    !single: Text Definition
    single: Text
    single: Escape Sequence

Text
====

In the *Erbsland Configuration Language* (ELCL), *text*, or more specifically *single-line text*, serves not only as a value but also plays a special role in section and value names. Therefore, it is important to define the syntax of text early, as it will be used throughout this documentation.

.. code-block:: bnf

    text                ::= DOUBLE_QUOTE ( text_character | text_escape )* DOUBLE_QUOTE
    text_character      ::= TEXT - (BACKSLASH | DOUBLE_QUOTE)
    text_escape         ::= BACKSLASH (BACKSLASH | DOUBLE_QUOTE | DOLLAR | [nN] | [rR] | [tT] |
                            [uU] text_unicode )
    text_unicode        ::= ( HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT |
                            CU_BRACKET_OPEN HEX_DIGIT+ CU_BRACKET_CLOSE ) /* 1-8 hex digits */

.. important::

    **A parser is not required to perform Unicode normalization on any parsed text.**

    Unicode text may be internally processed as UTF-8 encoded byte-data. It is the responsibility of the application to handle normalization or perform additional checks on the text, depending on the specific requirements of its use case.

.. index::
    pair: Rules; Text

Basic Rules
-----------

#.  **Format:** Text consists of characters enclosed between two double quote characters (:cp:`"`).

    .. code-block:: text
        :class: good-example

        "This is text"

#.  **Regular Characters:** Any Unicode character can be used in text, except for backslashes (which introduce *escape sequences*), double quotes (which mark the end of the text), and all :term:`control characters` (except the tab character, which is allowed).

    .. code-block:: text
        :class: bad-example
        :force:

        "This
        is
        wrong"              # ERROR! Line breaks and other control characters aren't allowed in text.
        "This "is" wrong"   # ERROR! Double quotes must be escaped in text.
        "This \ wrong"      # ERROR! The backslash introduces escape sequences, so this is invalid.

.. _ref-text-escape-sequence:
.. index::
    pair: Rules; Escape Sequence

Escape Sequence Rules
---------------------

#.  **Escape Sequences:** Each escape sequence inserts exactly one character into the text.
#.  **Format:** An escape sequence begins with a backslash (:cp:`5c`), followed by one or more characters.
#.  **Case-insensitive:** Escape sequences are not case-sensitive.
#.  ``\\``: Inserts a single backslash (:cp:`5c`).
#.  ``\"``: Inserts a double quote (:cp:`"`).
#.  ``\$``: Inserts a dollar sign (:cp:`$`).
#.  ``\n``: Inserts a newline control character (:cp:`0a`).
#.  ``\r``: Inserts a carriage return control character (:cp:`0d`).
#.  ``\t``: Inserts a tab control character (:cp:`09`).
#.  ``\uXXXX``: Inserts a Unicode character, where ``XXXX`` represents exactly four hexadecimal digits that form the character's :term:`code point`.
#.  ``\u{Y}``: Inserts a Unicode character, where ``Y`` can be one to eight hexadecimal digits, forming the character's :term:`code point`. Zero padding is allowed.
#.  **Null is Forbidden:** The "null" character cannot be inserted into text.
#.  **Unknown Sequences Rejected:** Any escape sequences not explicitly listed here must be rejected.


Features
--------

.. list-table::
    :header-rows: 1
    :width: 100%
    :widths: 25, 75

    *   -   Feature
        -   Coverage
    *   -   :text-code:`core`
        -   Text and all escape sequences are part of the core language.


Errors
------

.. list-table::
    :header-rows: 1
    :width: 100%
    :widths: 25, 75

    *   -   Error Code
        -   Causes
    *   -   :text-code:`Character`
        -   This error is raised for any illegal character or invalid escape sequence within the text.
    *   -   :text-code:`Syntax`
        -   Raised if the closing double quote character is missing at the end of the line or document.
    *   -   :text-code:`LimitExceeded`
        -   Raised if the text exceeds the maximum text size the parser can handle.

