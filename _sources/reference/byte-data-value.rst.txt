..
    Copyright (c) 2025 Tobias Erbsland - Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

.. _ref-byte-data-value:
.. index::
    single: Multi-line Byte-Data
    single: Byte-Data
    single: Byte-Data Value

Byte-Data Values
================

Byte-data values are a special data type used to store byte sequences. These values are represented as a sequence of hexadecimal digits, enclosed in less-than (:cp:`<`) and greater-than (:cp:`>`) signs. This format is ideal for including short snippets of byte-data, such as data for network protocols or filters.

.. code-block:: bnf

    byte_data             ::= LESS_THAN_SIGN (ALPHA FORMAT_DIGIT* ":")? (spacing byte_data_hex_byte)*
                              spacing GREATER_THAN_SIGN

    byte_data_hex_byte    ::= HEX_DIGIT HEX_DIGIT

For multi-line byte-data, the format is slightly different. Multi-line byte-data is enclosed in triple less-than and greater-than signs (``<<<`` and ``>>>``), with each line containing hexadecimal bytes.

.. code-block:: bnf

    multi_line_byte_data  ::= ml_byte_data_start ml_byte_data_hex_line* ml_byte_data_end

    ml_byte_data_start    ::= "<<<" (ALPHA FORMAT_DIGIT*)? end_of_line
    ml_byte_data_end      ::= indentation_pattern ">>>"
    ml_byte_data_hex_line ::= (indentation_pattern (spacing byte_data_hex_byte)* )? end_of_line

In the following examples, you’ll see both a single-line byte-data value and a multi-line byte-data value:

.. code-block:: erbsland-conf
    :class: good-example

    [main]
    PNG Header: <50 4E47 0D0A 1A0A>        # PNG file header
    EXIF Data:
        <<<                                # - Little endian values
        45786966 0000                      # EXIF identifier + padding (32-bit)
        49492A00                           # TIFF header (32-bit)
        08000000                           # Offset to IFD0 (32-bit)
        0E00                               # Tag count (16-bit)
        0001                               # Tag number (16-bit)
        >>>


.. index::
    pair: Rules; Byte-Data

Rules for Single Line Byte-Data
---------------------------------

#.  **Format:** Single-line byte-data is enclosed between less-than (:cp:`<`) and greater-than (:cp:`>`) signs.

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        Data: <01020304>

#.  **Format Specifier:** Optionally, the opening less-than sign (:cp:`<`) can be followed by a format specifier that is terminated with a colon (:cp:`:`). No spaces are allowed within the format specifier or between the specifier, the colon and the opening less-than sign.

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        Data: <hex: ffe07a09>

    .. code-block:: text
        :class: bad-example

        [main]
        Data 1: <hex ffe07a09>      # ERROR! Missing colon in single-line byte-data.
        Data 2: < hex : ffe07a09>   # ERROR! Spacing around the identifier is not allowed.


#.  **Format Specifier Format:** The format identifier must start with a letter (:cp:`a-z`, case-insensitive), and can be followed by a sequence of 0 to 15 letters (:cp:`a-z`, case-insensitive), digits (:cp:`0-9`), the hyphen (:cp:`-`) and underscores (:cp:`_`). The identifier must be matched case-insensitive.

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        Data: <hex: ffe07a09>

    .. code-block:: text
        :class: bad-example

        [main]
        Data 1: <_fmt: ffe07a09>         # ERROR! Identifier must start with a letter.
        Data 2: <format012345678: 0011>  # ERROR! Identifier must not exceed 16 characters.


.. index::
    pair: Rules; Multi-line Byte-Data

Rules for Multi-line Byte-Data
------------------------------

#.  **Beginning the Byte-Data:** Multi-line byte-data begins with a sequence of *three* less-than signs (``<<<``). It *can* be followed by the optional format specifier ``hex`` (without a colon). This sequence (``<<<`` and optional format specifier) *can* also be followed by spaces or comments, but *must* be followed by a line break.

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        Data 1: <<<
            f0ba1412 0177ec42
            >>>
        Data 2:                # Comment
            <<<hex             # Optional format specifier with comment
            f0ba1412 0177ec42
            >>>

#.  **Content Start and Indentation:** The content of the multi-line byte-data starts after the line break following the opening sequence. Each line *must* be indented by at least one space or tab character. See :ref:`ref-spacing` for details on indentation.

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        Data:
            <<<
            0100
            0200
            0300
            FFFF
            >>>

#.  **Consistent Indentation:** Each continued line of the multi-line byte-data must follow the same indentation pattern as the first line. After the indentation pattern, additional spacing can be used to align content. See :ref:`ref-spacing` for more information.

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        Data:
            <<<
            0100
                ec24
            0100  00
            >>>

#.  **Comments:** Comments, starting with a hash character (:cp:`#`), are allowed inside multi-line byte-data. For more information, see :ref:`ref-comment`.

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        Data:
            <<< #   Tag  Flag Data
                    0100  00          # First tag
                              ec24    # Data block
                    0100  00          # Second tag
                    ffff              # End mark
            >>>

#.  **Ending the Byte-Data:** Multi-line byte-data ends on a new line with the same indentation as the previous lines, followed *immediately* by a sequence of three greater-than signs (``>>>``).

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        Data: <<<
            ffec 0009
            8420 224e
            >>>

    .. code-block:: erbsland-conf
        :class: bad-example
        :force:

        [main]
        Data: <<<
            ffec 0009
            8420 224e
                 >>>   # ERROR! Indentation pattern does not match.

#.  **Line Breaks:** Line breaks have no effect on the byte-data itself and are used only for visual grouping. The content is treated as a continuous sequence of bytes, regardless of line breaks.

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        Data 1: <<<
            ffec 0009
            8420 224e
            >>>
        Data 2: <<<
            ff ec00 09842022 4e
            >>>

    The result for both values is the same byte sequence: ``ff ec 00 09 84 20 22 4e``.

#.  **Format Specifier:** Optionally, the opening less-than signs (``<<<``) can be followed by a format specifier (without terminating colon). No spaces are allowed within the format specifier or before the specifier.

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        Data: <<<hex
            ffe07a09
            >>>

    .. code-block:: text
        :class: bad-example

        [main]
        Data 1: <<<hex:        # ERROR! No colon after the specifier in multi-line values
            ffe07a09
            >>>
        Data 2: <<< hex        # ERROR! Spacing before the identifier is not allowed.
            ffe07a09
            >>>

#.  **Format Specifier Format:** The format identifier must start with a letter (:cp:`a-z`, case-insensitive), and can be followed by a sequence of 0 to 15 letters (:cp:`a-z`, case-insensitive), digits (:cp:`0-9`), the hyphen (:cp:`-`) and underscores (:cp:`_`). The identifier must be matched case-insensitive.

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        Data: <<<hex
            ffe07a09
            >>>

    .. code-block:: text
        :class: bad-example

        [main]
        Data 1: <<<_fmt               # ERROR! Identifier must start with a letter.
            ffe07a09
            >>>
        Data 2: <<<format012345678    # ERROR! Identifier must not exceed 16 characters.
            0011
            >>>


Supported Byte-Data Formats
---------------------------

#.  **Supported Formats:** Only the hexadecimal-format, with the identifier ``hex`` is supported in this version of the language.

    .. list-table::
        :header-rows: 1

        *   -   Identifier
            -   Format
        *   -   ``hex``
            -   Hexadecimal format

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        Data: <hex: 01020304>

    .. code-block:: text
        :class: bad-example

        [main]
        Data: <base64: ffe07a09>   # ERROR! Unsupported format.


Rules for the Hexadecimal Format
--------------------------------

#.  **Hexadecimal Format:** The hexadecimal bytes are represented by two characters, consisting of digits (:cp:`0-9`) and letters (:cp:`a-f`, case-insensitive). The first character specifies the higher-portion of the byte, the second character specifies the lower portion of the byte.

    .. list-table::
        :header-rows: 1

        *   -   Character
            -   Decimal
            -   Hexadecimal
        *   -   :cp:`0`
            -   0
            -   0x0
        *   -   :cp:`1`
            -   1
            -   0x1
        *   -   :cp:`2`
            -   2
            -   0x2
        *   -   :cp:`3`
            -   3
            -   0x3
        *   -   :cp:`4`
            -   4
            -   0x4
        *   -   :cp:`5`
            -   5
            -   0x5
        *   -   :cp:`6`
            -   6
            -   0x6
        *   -   :cp:`7`
            -   7
            -   0x7
        *   -   :cp:`8`
            -   8
            -   0x8
        *   -   :cp:`9`
            -   9
            -   0x9
        *   -   :cp:`a`, :cp:`A`
            -   10
            -   0xA
        *   -   :cp:`b`, :cp:`B`
            -   11
            -   0xB
        *   -   :cp:`c`, :cp:`C`
            -   12
            -   0xC
        *   -   :cp:`d`, :cp:`D`
            -   13
            -   0xD
        *   -   :cp:`e`, :cp:`E`
            -   14
            -   0xE
        *   -   :cp:`f`, :cp:`F`
            -   15
            -   0xF

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        Data: < 01 FF a0 7b >

#.  **Allowed Spacing:** Spaces between the hexadecimal bytes are allowed, but not within a byte.

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        Data: < 01FF     a0   7b    >

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        Data: <<<
            01FF     a0   7b
            >>>

    .. code-block:: erbsland-conf
        :class: bad-example
        :force:

        [main]
        Data: < 0 1 2 3 >  # ERROR! Spacing *within* bytes is not allowed.


Features
--------

.. list-table::
    :header-rows: 1
    :width: 100%
    :widths: 25, 75

    *   -   Feature
        -   Coverage
    *   -   :text-code:`byte-data`
        -   Byte-data values are a standard feature.
    *   -   :text-code:`multi-line`
        -   Multi-line byte-data values are a standard feature.

Errors
------

.. list-table::
    :header-rows: 1
    :width: 100%
    :widths: 25, 75

    *   -   Error Code
        -   Causes
    *   -   :text-code:`Syntax`
        -   |   Raised if the spacing does not align with the bytes.
            |   Raised if non-hexadecimal or illegal characters are present in the content.
            |   Raised if the closing sequence is missing.
            |   Raised if an invalid format identifier is specified.
    *   -   :text-code:`Unsupported`
        -   Raised if an unknown but valid format identifier is specified.
    *   -   :text-code:`Indentation`
        -   |   Raised if no space or tab character is present before a continued byte-data line.
            |   Raised if the indentation pattern does not match the first entry for multi-line byte-data.
    *   -   :text-code:`LimitExceeded`
        -   |   Raised if the byte-data exceeds the maximum size the parser can handle.
            |   Raised if the format identifier exceeds the maximum size.

