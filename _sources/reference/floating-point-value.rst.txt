..
    Copyright (c) 2024-2025 Tobias Erbsland - Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

.. _ref-floating-point-value:
.. index::
    single: Floating-Point
    single: Floating-Point Value 

Floating-Point Value
====================

*Floating-point values* represent numbers that can include fractional parts and an optional exponent.

.. code-block:: bnf

    float               ::= PLUS_MINUS? ( float_special | float_number )

    float_special       ::= "inf" | "nan"   /* case insensitive */

    float_number        ::= ( integer_dec float_exponent ) |
                            ( integer_dec PERIOD integer_dec? float_exponent? ) |
                            ( integer_dec? PERIOD integer_dec float_exponent? )
                            
    float_exponent      ::= LETTER_E PLUS_MINUS? DIGIT+   /* maximum of 6 digits */

In the example below, you can see various valid floating-point values:

.. code-block:: erbsland-conf
    :class: good-example

    [main]
    value a: .0
    value b: NaN
    value c: INF
    value d: 2937.28301
    value e: 12e+10
    value f: -12.9
    value g: -8'283.9e-5

.. important::

    This specification does not require a specific floating-point storage format for programming language or parser implementations. The reference to ISO/IEC 60559:2020 (or IEEE 754) is only meant to clarify the definition of *floating-point numbers*. What matters most is that parsers follow the floating-point syntax and rules described in the grammar.

    Since different programming languages and platforms may use slightly varied internal representations for floating-point values, small differences between implementations are expected. Handling these differences is the responsibility of the application using the configuration.

    Remember that :term:`ELCL` is a **configuration format**, not a storage format. As such, minor rounding errors in floating-point values should not cause issues in your application.


.. index::
    pair: Rules; Floating-Point

Rules
-----

#.  **Expected Precision:** A parser *should support* floating-point numbers of the size described as ``binary64`` in the ISO/IEC 60559:2020 or IEEE 754 standard. This format uses 64 bits in total, with 11 bits for the exponent and 52 bits for the mantissa.

    .. code-block:: text
        :class: good-example
    
        ┌────────────────────────────────────────────────────────┐
        │ 64 bits                                                │
        ├───┬─────────────────┬──────────────────────────────────┤
        │ 1 │ 11 bits         │ 52 bits                          │
        ├───┼─────────────────┼──────────────────────────────────┤
        │ S │ Exponent        │ Mantissa                         │
        └───┴─────────────────┴──────────────────────────────────┘

#.  **Alternative Precision:** A parser *can support* a different storage format, such as fixed-point, provided it supports a *minimum* precision of 17 decimal places across both the integral and fractional parts.

    .. code-block:: text
        :class: good-example

        ┌────────────────────────────────────────────────────────┐
        │ 128 bits                                               │
        ├───┬────────────────────────┬───────────────────────────┤
        │ 1 │ 63 bits                │ 64 bits                   │
        ├───┼────────────────────────┼───────────────────────────┤
        │ S │ Integral               │ Fraction                  │
        └───┴────────────────────────┴───────────────────────────┘
    
    .. note::

        A parser using an alternative internal storage format must still correctly parse and interpret the full floating-point syntax, including exponents and the special literals ``nan`` and ``inf``.

#.  **Minimum Structure:** A floating-point value *must* include either an integral part, a fractional part, or both.

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        value a: 1293.
        value b: .029
        value c: 1192.0067

#.  **Decimal Point:** The integral part is separated from the fractional part by a decimal point (:cp:`.`).

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        value a: 1293.
        value b: .029
        value c: 11.0067

#.  **Exponent:** A floating-point value with a decimal point *can* have an exponent. A floating-point value without a decimal point *must* include an exponent to be considered a valid floating-point number..

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        value a: 1293.e6
        value b: .029e-4
        value c: 1192e5

#.  **Special Values:** The special literals ``inf`` (infinity) and ``nan`` (not-a-number) are valid floating-point numbers. These literals are case-insensitive.

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        value a: nan
        value b: inf
        value c: -nan   # Though logically unnecessary, this syntax is supported for completeness.
        value d: -inf

#.  **Integral Part:** The integral part of a floating-point number consists of a sequence of digits :cp:`0-9`.

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        value: 1207256.

#.  **No Zero Padding:** The integral part of a floating-point number must not be padded with leading zeros.

    .. code-block:: erbsland-conf
        :class: bad-example
        :force:

        [main]
        value: 005.293    # ERROR! Leading zeros are not allowed.

#.  **Fractional Part:** The fractional part of a floating-point number consists of a sequence of digits :cp:`0-9`. The fractional part may have trailing zeroes.

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        value: .00201982

#.  **Digit Limit:** The total number of digits in both the integral and fractional parts *must not* exceed 20 digits. Trailing zeroes in the fractional part add to the total digit count.

    .. code-block:: erbsland-conf
        :class: bad-example
        :force:

        [main]
        value a: 10000000000.00000000001     # ERROR! Exceeds 20 digits.
        value b: 1.000000000000000000000     # ERROR! Exceeds 20 digits.

#.  **Exponent Part:** An exponent *must* start with the letter :cp:`e` (case-insensitive), followed by an *optional* plus (:cp:`+`) or minus (:cp:`-`) sign, and then one to six digits.

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        value a: 103216.0e-12
        value b: 0.0235e+9

#.  **Exponent Padding:** The exponent *can* be padded with leading zeros.

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        value: 103216.0e-000012

#.  **Zero:** All possible variants of zero, ``0.0``, ``.0`` and ``0.`` with plus or minus sign are valid floating-point numbers.

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        value a: 0.0
        value b: 0.
        value c: .0
        value d: -0.0
        value e: -.0
        value f: +0.

#.  **Digit Separators:** Apostrophes (:cp:`'`) can be used as optional digit separators in the integral and fractional parts, but not in the exponent, to improve readability.

    .. code-block:: erbsland-conf
        :class: good-example

        [main]
        value: 100'000.000'001

#.  **No Separator at Start or End:** A number must not begin or end with a digit separator.

    .. code-block:: erbsland-conf
        :class: bad-example
        :force:

        [main]
        value a: '100'000.    # ERROR! Must not start with a separator.
        value b: 100'000'.    # ERROR! Must not end with a separator.

#.  **No Consecutive Separators:** Consecutive digit separators are not allowed.

    .. code-block:: erbsland-conf
        :class: bad-example
        :force:

        [main]
        value: 100''000    # ERROR! Consecutive separators are not allowed.

#.  **No Hexadecimal and Binary Forms:** Hexadecimal or octal formats of floating-point numbers are not allowed

    .. code-block:: erbsland-conf
        :class: bad-example
        :force:

        [main]
        value: 0x1.921fb54442d18p+1  # ERROR! Hexadecimal or binary formats are not allowed.

#.  **Conversion Method:** Floating-point conversions *should* follow the guidelines outlined in the ISO/IEC 60559:2020 standard (section 5.12) or IEEE 754.

    .. important::

        :term:`ELCL` is a **configuration format**, not a storage format. Therefore, small rounding errors, especially after 15 significant digits, are perfectly acceptable.

#.  **Behavior When Limits Are Exceeded:** If a floating-point value exceeds the internal storage range (crossing the minimum or maximum value), the stored value should be rounded down to zero or rounded up to represent infinity, as appropriate.

    .. important::

        :term:`ELCL` is a **configuration format**, not a storage format. Therefore, small rounding errors, particularly after 15 significant digits, are expected and acceptable.


Features
--------

.. list-table::
    :header-rows: 1
    :width: 100%
    :widths: 25, 75

    *   -   Feature
        -   Coverage
    *   -   :text-code:`float`
        -   Floating-point numbers are a standard feature.


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
            |   Raised if there are multiple decimal points.
            |   Raised if the integral part is padded with zeros.
            |   Raised if the value exceeds the allowed number of digits.
