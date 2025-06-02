..
    Copyright (c) 2024 Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

.. _ref-integer-value:
.. index::
    single: Integer
    single: Integer Value
    single: Byte Count
    single: Decimal Integer
    single: Hexadecimal Integer
    single: Binary Integer

Integer Values
==============

Integer values are a core data type in the language, supporting three commonly used number formats: decimal, hexadecimal, and binary. Additionally, the language includes a byte-count format, where a decimal integer is followed by a suffix indicating a unit of data size (such as ``kb`` for kilobytes).

.. code-block:: bnf

    integer             ::= PLUS_MINUS? ( integer_hex | integer_bin |
                            integer_byte_count | integer_dec )

    integer_hex         ::= "0x" HEX_DIGIT+ ( APOSTROPHE HEX_DIGIT+ )*
    integer_bin         ::= "0b" BIN_DIGIT+ ( APOSTROPHE BIN_DIGIT+ )*
    integer_dec         ::= DIGIT+ ( APOSTROPHE DIGIT+ )*

    integer_byte_count  ::= integer_dec SPACE? byte_count_suffix
    byte_count_suffix   ::= [kmgtpezy] "i"? "b"  /* case-insensitive */

In the following example, you can see valid integer values in each format:

.. code-block:: erbsland-conf
    :class: good-example

    [main]
    Decimal Value     : -123'456
    Hexadecimal Value : 0x34cd'12ef
    Binary Value      : 0b00001111'10101010
    Byte Count Value  : 100 TB


.. index::
    pair: Rules; Integer

Rules for All Integer Values
----------------------------

#.  **Signed 64-bit Support:** Signed 64-bit integer values *must* be supported for all formats (decimal, hexadecimal, and binary).

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        dec minimum: -9223372036854775808  # 64-bit minimum value
        dec maximum:  9223372036854775807  # 64-bit maximum value
        hex minimum: -0x8000000000000000   # 64-bit minimum value in hexadecimal
        hex maximum:  0x7fffffffffffffff   # 64-bit maximum value in hexadecimal
        bin minimum: -0b1000000000000000000000000000000000000000000000000000000000000000   # 64-bit minimum value in binary
        bin maximum:  0b0111111111111111111111111111111111111111111111111111111111111111   # 64-bit maximum value in binary

    .. micro-parser::

        Support for 32-bit signed integers is required.

#.  **Out of Bounds Values:** Any value that exceeds the 64-bit signed integer range must be rejected.

    .. code-block:: erbsland-conf
        :class: bad-example
        :force:

        [main]
        value: 9223372036854775808    # ERROR! Too large for 64-bit.

#.  **Maximum Digit Count:** The number of digits in an integer must not exceed what is required for the largest possible value in its format and storage size. Digit separators (:cp:`'`) are not counted.

    .. code-block:: erbsland-conf
        :class: bad-example
        :force:

        [main]
        value: 1234567890123456789    # ERROR! Too many digits.

    .. note::

        While this may seem redundant for decimal numbers, it's crucial for hexadecimal and binary formats, where values can be padded with leading zeros. Also, this rule allows a parser to immediately flag an error when it encounters too many digits, without needing to process an oversized number.

#.  **Case Insensitive:** Letters in the prefix, such as ``0x`` or ``0b``, or the value itself (:cp:`a-f`), must be interpreted *case-insensitive*.

    .. code-block:: erbsland-conf
        :class: good-example

        [interrupt controller]
        lunch time   : 0xfee00000
        nap time     : 0Xfee00000
        coffee break : 0xFEE00000

#.  **Minus for Negative Numbers:** A minus sign (:cp:`-`) can optionally be used to define a negative integer.

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        value a: -10
        value b: -0x0a
        value c: -0b0110

#.  **Optional Plus Sign:** An integer can optionally be prefixed with a plus sign (:cp:`+`) for positive values.

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        value a: +10
        value b: +0x0a
        value c: +0b0110

#.  **Digit Separators:** Apostrophes (:cp:`'`) can be used as optional digit separators for readability.

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        value a: 100'000
        value b: 0x1000'0000
        value c: 0b10000000'00000000

#.  **No Separator at Start or End:** A number must not start or end with a digit separator.

    .. code-block:: erbsland-conf
        :class: bad-example
        :force:

        [main]
        value a: '100'000    # ERROR! Must not start with a separator.
        value b: 100'000'    # ERROR! Must not end with a separator.

#.  **No Consecutive Separators:** Consecutive digit separators are not allowed.

    .. code-block:: erbsland-conf
        :class: bad-example
        :force:

        [main]
        value a: 100''000    # ERROR! Consecutive separators are not allowed.


.. index::
    single: Digit Count

Digit Counts
~~~~~~~~~~~~

The following table shows the maximum digit counts for each format and storage size:

.. list-table::
    :header-rows: 1
    
    *   -   Format
        -   64-bit
        -   32-bit
    *   -   Decimal
        -   19 digits
        -   10 digits
    *   -   Hexadecimal
        -   16 digits
        -   8 digits
    *   -   Binary
        -   64 digits
        -   32 digits


.. index::
    pair: Rules; Decimal Integer
    pair: Format; Decimal

Rules for Decimal Integers
--------------------------

#.  **Digits:** A decimal integer is composed of a sequence of digits from :cp:`0-9`.

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        value: 1234567890

#.  **No Leading Zeros:** A decimal integer *must not* be padded with leading zeros.

    .. code-block:: erbsland-conf
        :class: bad-example
        :force:

        [main]
        value: 00001    # ERROR! Leading zeros are not allowed.


.. index::
    pair: Rules; Byte Count
    pair: Format; Byte Count

Rules for the Byte Count Format
-------------------------------

#.  **Format:** A byte count consists of a decimal integer (subject to all the rules for decimal integers), optionally followed by a single space (:cp:`20`), and then a valid byte count suffix from :ref:`ref-byte-count-suffix`.

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        value: 100 kb

#.  **Case-Insensitive:** All byte count suffixes are case-insensitive, meaning that both uppercase and lowercase suffixes are treated the same.

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        value a: 100 kib
        value b: 100 KIB
        value c: 100 KiB

#.  **Applying the Factor:** When a byte count suffix is present, the parser must multiply the decimal integer by the appropriate factor corresponding to the suffix. If the result exceeds the valid range of the internal storage format, the value must be rejected.

    .. code-block:: erbsland-conf
        :class: bad-example
        :force:

        [main]
        value: 1 yb     # ERROR! Value exceeds the 64-bit integer limit.


.. _ref-byte-count-suffix:

Byte Count Suffixes
~~~~~~~~~~~~~~~~~~~

The table below lists the valid suffixes for decimal and binary byte counts, along with their corresponding factors.

.. list-table::
    :header-rows: 1

    *   -   Decimal
        -   Factor
        -   Binary
        -   Factor
    *   -   :text-code:`kb`
        -   :math:`1000^1`
        -   :text-code:`kib`
        -   :math:`1024^1`
    *   -   :text-code:`mb`
        -   :math:`1000^2`
        -   :text-code:`mib`
        -   :math:`1024^2`
    *   -   :text-code:`gb`
        -   :math:`1000^3`
        -   :text-code:`gib`
        -   :math:`1024^3`
    *   -   :text-code:`tb`
        -   :math:`1000^4`
        -   :text-code:`tib`
        -   :math:`1024^4`
    *   -   :text-code:`pb`
        -   :math:`1000^5`
        -   :text-code:`pib`
        -   :math:`1024^5`
    *   -   :text-code:`eb`
        -   :math:`1000^6`
        -   :text-code:`eib`
        -   :math:`1024^6`
    *   -   :text-code:`zb`
        -   :math:`1000^7`
        -   :text-code:`zib`
        -   :math:`1024^7`
    *   -   :text-code:`yb`
        -   :math:`1000^8`
        -   :text-code:`yib`
        -   :math:`1024^8`


.. index::
    pair: Rules; Hexadecimal Integer
    pair: Format; Hexadecimal

Rules for Hexadecimal Integers
------------------------------

#.  **Prefix:** A hexadecimal integer must start with the prefix ``0x`` (case-insensitive).

    .. code-block:: erbsland-conf
        :class: good-example

        [vic]
        background: 0xD021

#.  **Digits:** A hexadecimal integer is defined by a sequence of digits from :cp:`0-9` and letters from :cp:`a-f` (case-insensitive).

    .. code-block:: erbsland-conf
        :class: good-example

        [digits]
        value: 0x1a2b'3c4d'5e6f'7890


.. index::
    pair: Rules; Binary Integer
    pair: Format; Binary

Rules for Binary Integers
-------------------------

#.  **Prefix:** A binary integer must start with the prefix ``0b`` (case-insensitive).

    .. code-block:: erbsland-conf
        :class: good-example

        [binary]
        value: 0b00101000

#.  **Digits:** A binary integer consists of a sequence of digits :cp:`0` and :cp:`1`.

    .. code-block:: erbsland-conf
        :class: good-example

        [binary]
        value: 0b00101000'11110010'01110011'11010010

#.  **Sign Bit for Negative Values:** A negative binary integer can be represented by setting the highest bit to 1, indicating a negative number.

    .. code-block:: erbsland-conf
        :class: good-example

        [binary]
        value: 0b11111111'11111111'11111111'11111111'11111111'11111111'11111111'11111110  # => -2


Features
--------

.. list-table::
    :header-rows: 1
    :width: 100%
    :widths: 25, 75

    *   -   Feature
        -   Coverage
    *   -   :text-code:`core`
        -   The integer data type, and the decimal, hexadecimal and binary format are part of the core language.
    *   -   :text-code:`byte-count`
        -   Decimal integers with byte-count suffixes are a standard feature.

Errors
------

.. list-table::
    :header-rows: 1
    :width: 100%
    :widths: 25, 75

    *   -   Error Code
        -   Causes
    *   -   :text-code:`Syntax`
        -   |   Raised if value separators are placed incorrectly.
            |   Raised if a decimal value is padded with zeros.
            |   Raised if an integer exceeds the allowed number or digit limit.
    *   -   :text-code:`LimitExceeded`
        -   Raised if the resulting integer would be too large to be stored correctly.
