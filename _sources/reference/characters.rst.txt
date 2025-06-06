..
    Copyright (c) 2025 Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

.. _ref-character:
.. index::
    single: Character

Characters
==========

The *Erbsland Configuration Language* (:term:`ELCL`) supports all valid :term:`Unicode` characters, except for most control codes. In this section, we define characters, character groups, and ranges that carry specific meanings in the language.


.. index::
    single: Encoding

Encoding
--------

#. An :term:`ELCL` document **must** be encoded in :term:`UTF-8`.
#. A parser **must** support an optional UTF-8 *BOM* (Byte Order Mark).
#. A parser **must** raise an ``Encoding`` error if it encounters an illegal byte sequence in the UTF-8 encoded data.
#. A parser **must** raise an ``Encoding`` error if it encounters a valid UTF-8 sequence that represents an illegal Unicode code point.

.. micro-parser::

    Parsers **must** support at least 7-bit ASCII, but may support additional UTF-8 encoded data.


.. index::
    single: UTF-8
    single: Invalid UTF-8

Illegal UTF-8 Sequences
-----------------------

An :term:`ELCL` parser must reject any illegal UTF-8 sequences and terminate with an error. Since not all programming languages or libraries fully implement UTF-8 decoding, the following list outlines illegal UTF-8 sequences that a parser must reject. These sequences are representative examples, not exhaustive lists.

.. list-table::
    :header-rows: 1
    :widths: 25, 75
    :width: 100%

    *   -   Sequence
        -   Description
    *   -   | :text-code:`ED A0 80` ...
            | :text-code:`ED BF BF`
        -   Low- and high-surrogates are special 16-bit code points used in UTF-16 to encode 32-bit values. They represent the code point range from :text-code:`U+D800` to :text-code:`U+DFFF`, which are illegal in UTF-8 and must be rejected.
    *   -   | :text-code:`F4 90 80 80` ...
            | :text-code:`F5 ...`
            | :text-code:`F6 ...`
            | ...
            | :text-code:`FD ...`
        -   The :term:`Unicode` standard limits the highest valid code point to :text-code:`U+10FFFF`. Any UTF-8 sequence that generates a code point above this range, such as :text-code:`U+110000` and higher, must be rejected.
    *   -   | :text-code:`C0 80`
            | :text-code:`C1 80`
        -   While UTF-8 multi-byte sequences can encode 7-bit values, only the shortest possible encoding is allowed. Therefore, sequences beginning with :text-code:`C0` or :text-code:`C1` are illegal and must be rejected.
    *   -   | :text-code:`C2` + 7-bit
            | :text-code:`EO 80` + 7-bit
            | :text-code:`FO 80 80` + 7-bit
        -   If a start byte is not followed by the required number of continuation bytes, the sequence is illegal. This can occur if a 7-bit character follows an incomplete sequence, or if the document ends mid-sequence.
    *   -   :text-code:`80` — :text-code:`BF`
        -   A continuation byte must only appear after a valid start byte. If encountered elsewhere, it is illegal and must be rejected.
    *   -   :text-code:`FE`, :text-code:`FF`
        -   These are invalid start bytes and must be rejected.

.. design-rationale::

    Enforcing strict UTF-8 handling ensures predictable behavior, as opposed to lenient alternatives like skipping, ignoring, or replacing invalid encodings with the *replacement character*. If encoding issues are not handled upfront, they will surface in the application layer, potentially causing problems or requiring additional error-handling logic. Strict encoding rules ensure that users of an :term:`ELCL` parser can reliably process text from configuration files.


Implementation Examples
~~~~~~~~~~~~~~~~~~~~~~~

A safe and complete UTF-8 decoding process, including the rejection of all illegal characters, can be implemented with minimal code if you use bit-tests in your decoder.

.. code-block:: cpp
    :caption: Pseudo C++ code for proper UTF-8 decoding 

    if (at_end()) return Char(); // EOF
    byte c = get_next_byte();
    if (c < 0x80) return Char(c); // 7-bit ASCII
    uint8_t cSize = 0;
    uint32_t unicodeValue;
    if ((c & 0b11100000u) == 0b11000000u && c >= 0b11000010u) {
        cSize = 2; // 2-byte sequence
        unicodeValue = (c & 0b00011111u);
    } else if ((c & 0b11110000u) == 0b11100000u) {
        cSize = 3; // 3-byte sequence
        unicodeValue = (c & 0b00001111u);
    } else if ((c & 0b11111000u) == 0b11110000u && c < 0b11110101u) {
        cSize = 4; // 4-byte sequence
        unicodeValue = (c & 0b00000111u);
    }
    if (cSize < 2) throw EncodingError(); // Invalid start byte sequence
    UnsafeConstBytePtr lastIt = it;
    for (uint8_t i = 1; i < cSize; ++i) {
        if (at_end()) throw EncodingError();
        c = get_next_char();
        if ((c & 0b11000000u) != 0b10000000u) throw EncodingError(); // Invalid continuation byte
        unicodeValue <<= 6;
        unicodeValue |= (c & 0b00111111u);
    }
    const auto result = Char(unicodeValue);
    // Validate against invalid Unicode ranges (surrogates, code points > 0x10FFFF)
    if (!result.isValidUnicode()) throw EncodingError();
    return result;

.. code-block:: python
    :caption: Pseudo Python code for proper UTF-8 decoding

    def parse_utf8_char() -> str:
        if at_end():
            return None  # EOF
        c = get_next_byte()
        if c < 0x80:
            return chr(c)  # 7-bit ASCII
        c_size = 0
        unicode_value = 0
        if (c & 0b11100000) == 0b11000000 and c >= 0b11000010:
            c_size = 2  # 2-byte sequence
            unicode_value = c & 0b00011111
        elif (c & 0b11110000) == 0b11100000:
            c_size = 3  # 3-byte sequence
            unicode_value = c & 0b00001111
        elif (c & 0b11111000) == 0b11110000 and c < 0b11110101:
            c_size = 4  # 4-byte sequence
            unicode_value = c & 0b00000111
        else:
            raise EncodingError("Invalid start byte sequence")
        for _ in range(1, c_size):
            if at_end():
                raise EncodingError("Unexpected end of data")
            c = get_next_byte()
            if (c & 0b11000000) != 0b10000000:
                raise EncodingError("Invalid continuation byte")
            unicode_value = (unicode_value << 6) | (c & 0b00111111)
        if not is_valid_unicode(unicode_value):
            raise EncodingError("Invalid Unicode code point")
        return chr(unicode_value)


.. index::
    single: Control
    single: Control Code
    single: Illegal Control Codes

Illegal Control Codes
---------------------

Most control codes are prohibited in an :term:`ELCL` document. The following table lists all illegal control codes.

.. list-table::
    :header-rows: 1
    :widths: 25, 75
    :width: 100%

    *   -   Code/Range
        -   Description
    *   -   :text-code:`U+0000`
        -   The "null" control character is disallowed in any part of a document, including text. The escape sequence ``\u0000`` is not permitted in text.
    *   -   | :text-code:`U+0001` — :text-code:`U+0008`
            | :text-code:`U+000B` — :text-code:`U+000C`
            | :text-code:`U+000E` — :text-code:`U+001F`
            | :text-code:`U+007F` — :text-code:`U+00A0`
        -   These control codes are disallowed in documents. However, they may appear in text blocks as escape sequences.

The only **valid control codes** in *ELCL* documents are the tab (:cp:`09`), new-line (:cp:`0a`), and carriage-return (:cp:`0d`).

.. design-rationale::

    Historically, control codes had specific uses, but today, most of them introduce errors or even security vulnerabilities. For this reason, control codes are disallowed in *ELCL* documents, particularly in text. If a control code is needed in text, it can be inserted using the appropriate Unicode escape sequence.

    The "null" control character is forbidden in text because it frequently causes issues when passing text through API boundaries. Like other control codes, it serves no meaningful purpose in text contexts. If byte-data is needed, *ELCL* provides support for such structures, and if values need to be separated, lists can be used.

    Prohibiting control codes simplifies text processing, although more complex Unicode behaviors—such as combining characters or directionality markers—remain possible within text blocks. However, the responsibility for handling these complexities can safely be delegated to the application code.


.. index::
    single: Character
    single: Named Characters

Named Characters in EBNF
------------------------

Characters in the shown EBNF syntax are named according to their Unicode or common names, rather than their function within the language.

.. code-block:: bnf

    TAB                 ::= #x0009    /* Tab character               */
    LF                  ::= #x000A    /* Line feed                   */
    CR                  ::= #x000D    /* Carriage return             */
    SPACE               ::= #x0020    /* Space character             */
    DOUBLE_QUOTE        ::= #x0022    /* Double Quote (")            */
    HASH                ::= #x0023    /* Hash symbol (#)             */
    DOLLAR              ::= #x0024    /* Dollar sign ($)             */
    APOSTROPHE          ::= #x0027    /* Apostrophe (')              */
    ASTERISK            ::= #x002A    /* Asterisk (*)                */
    PLUS                ::= #x002B    /* The plus sign (+)           */
    COMMA               ::= #x002C    /* Comma (,)                   */
    HYPHEN              ::= #x002D    /* Hyphen (-)                  */
    PERIOD              ::= #x002E    /* Period (.)                  */
    SLASH               ::= #x002F    /* Slash (/)                   */
    COLON               ::= #x003A    /* Colon (:)                   */
    LESS_THAN_SIGN      ::= #x003C    /* Less-Than Sign (<)          */
    EQUAL               ::= #x003D    /* Equals sign (=)             */
    GREATER_THAN_SIGN   ::= #x003E    /* Greater-Than Sign (>)       */
    AT_SIGN             ::= #x0040    /* At sign (@)                 */
    SQ_BRACKET_OPEN     ::= #x005B    /* Opening square bracket ([)  */
    BACKSLASH           ::= #x005C    /* Backslash (\)               */
    SQ_BRACKET_CLOSE    ::= #x005D    /* Closing square bracket (])  */
    UNDERSCORE          ::= #x005F    /* Underscore (_)              */
    BACKTICK            ::= #x0060    /* Backtick (`)                */
    CU_BRACKET_OPEN     ::= #x007B    /* Opening curly bracket ({)   */
    CU_BRACKET_CLOSE    ::= #x007D    /* Closing curly bracket ({)   */

.. index::
    single: Character Groups

Character Groups in EBNF
------------------------

In ELCL, certain character groups have predefined ranges or sets. Below is a list of important character groups used in the EBNF syntax:

.. code-block:: bnf

    DIGIT               ::= [#x0030-#x0039]               /* Decimal digits 0-9              */
    HEX_DIGIT           ::= [#x0030-#x0039#x0041-#x0046#x0061-#x0066]  /* Hexadecimal digits 0-9, A-F, a-f */
    BIN_DIGIT           ::= [#x0030#x0031]                /* Binary digits 0, 1              */
    ALPHA               ::= [#x0041-#x005A#x0061-#x007A]  /* Alphabetic characters A-Z, a-z  */
    TEXT                ::= [#x0009#x0020-#x007E#x00A0-#x10FFFF]  /* Any printable character (excluding control codes) */
    DIGIT_OR_ALPHA      ::= DIGIT | ALPHA                 /* Digits or alphabetic characters */
    FORMAT_DIGIT        ::= ALPHA | DIGIT | HYPHEN | UNDERSCORE  /* One element of a format specifier */
    PLUS_MINUS          ::= PLUS | HYPHEN                 /* Plus or minus                   */
    LETTER_E            ::= [eE]                          /* The letter E                    */

.. note::

    The ``TEXT`` character group must exclude low and high surrogates, as well as any characters that are invalid in a UTF-8 encoded document.


Features
--------

.. list-table::
    :header-rows: 1
    :width: 100%
    :widths: 25, 75

    *   -   Feature
        -   Coverage
    *   -   :text-code:`core`
        -   The full syntax outlined in this chapter is part of the core language.

Errors
------

.. list-table::
    :header-rows: 1
    :width: 100%
    :widths: 25, 75

    *   -   Error Code
        -   Causes
    *   -   :text-code:`Encoding`
        -   Raised if the parser detects invalid UTF-8 sequences.
    *   -   :text-code:`Character`
        -   Raised if an illegal control character is read in the configuration document.
