..
    Copyright (c) 2024 Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

.. _parser-tiers:
.. index::
    !single: Parser Tiers
    single: Feature
    single: Parser; Tiers
    single: Parser; Micro
    single: Parser; Minimal
    single: Parser; Standard
    single: Parser; Full-featured
    single: Micro Parser
    single: Standard Parser
    single: Full-featured Parser

============
Parser Tiers
============

For the :term:`ELCL`, an implementor of a Parser can categorize it in one of four tiers. Depending on the chosen category, they have to implement a number of requirements and features. All parser tiers must implement the :ref:`core language<tiers-core-language>`.

At the moment there are the following parser tiers:

*   Micro Parser
*   Minimal Parser
*   Standard Parser
*   Full-featured Parser

.. index::
    single: Requirements
    single: Parser; Requirements

Requirements
============

The following table shows the three tiers with all encoding and size requirements for the different parsers.

.. list-table::
    :width: 100%
    :widths: 60, 20, 20
    :header-rows: 1

    *   -   Requirement
        -   Micro
        -   Minimal – Full
    *   -   Supported Encoding
        -   7-bit ASCII
        -   UTF-8
    *   -   Maximum Line Length (Bytes) [1]_
        -   120
        -   4000
    *   -   Maximum Name Length (Chars)
        -   30
        -   100
    *   -   Maximum Name Path Length [2]_
        -   5
        -   10
    *   -   Minimum Text Length (KB) [3]_
        -   1
        -   100
    *   -   Integer Size (Bit) [4]_
        -   32
        -   64
    *   -   FP-Number Size (Bit) [5]_
        -   —
        -   64
    *   -   Event Driven Parser Implementation
        -   ✅
        -   ✅
    *   -   Model Parser Implementation
        -   —
        -   ✅

.. [1] This includes the characters for the line-break.
.. [2] A parser must reject any name path that exceeds this number of names.
.. [3] A parser can reject text that exceeds this limit, but it can also implement additional limits and reject a document because of its total size.
.. [4] The parser must support signed integers with a *minimum* of this size.
.. [5] The parser must support floating-point number, with a *minimum* of this size. Handling imprecision from text conversion is in the responsibility of the application.

.. _tiers-core-language:
.. index::
    single: Core Language

Core Language
=============

All parsers must implement the minimalistic :term:`core language`. The following list is a summary of all elements that are part of the core language. The :ref:`reference documentation<reference>` explains in more details, which parts of the language are part of the core language, and which parts are features.

*   Strict Parsing with all Error Codes
*   Comments
*   Case-Insensitive: Names, Escape Sequences and Keywords
*   Sections: Absolute and Relative
*   Values: Decimal Integer, Hexadecimal Integer, Binary Integer, Boolean, Single Line Text
*   Meta Values: ``@version``, ``@signature`` [6]_, ``@features``

.. [6] Only the meta keyword must be supported. If the parser does not support signatures, parsing must fail if this keyword is encountered.

.. micro-parser::

    Can ignore the ``@features`` meta-value and just stop parsing when it is encountered.


.. index::
    single: Features
    single: Parser; Features

Features
========

.. list-table::
    :width: 100%
    :widths: 80, 5, 5, 5, 5
    :header-rows: 1

    *   -   Requirement
        -   Micro
        -   Minimal
        -   Standard
        -   Full
    *   -   Floating-Point Values
        -   —
        -   ✅
        -   ✅
        -   ✅
    *   -   Byte Counts
        -   —
        -   ✅
        -   ✅
        -   ✅
    *   -   Multi-line Text
        -   —
        -   —
        -   ✅
        -   ✅
    *   -   Text Names (for Values and Sections)
        -   —
        -   —
        -   ✅
        -   ✅
    *   -   List Sections
        -   —
        -   —
        -   ✅
        -   ✅
    *   -   Value Lists (Single- / Multi-line)
        -   —
        -   —
        -   ✅
        -   ✅
    *   -   Date, Time and Date/Time Values
        -   —
        -   —
        -   ✅
        -   ✅
    *   -   Code Text (Single- / Multi-line) [8]_
        -   —
        -   —
        -   ✅
        -   ✅
    *   -   Byte-Data Value (Single- / Multi-line)
        -   —
        -   —
        -   ✅
        -   ✅
    *   -   Meta Command ``@include``
        -   —
        -   —
        -   ✅
        -   ✅
    *   -   Regular Expression (Single- / Multi-line) [9]_
        -   —
        -   —
        -   —
        -   ✅
    *   -   Time-Delta Values
        -   —
        -   —
        -   —
        -   ✅
    *   -   Validation Rules Support
        -   —
        -   —
        -   —
        -   ✅
    *   -   Document Signatures [10]_
        -   —
        -   —
        -   —
        -   ✅

.. [8] A parser is not required to distinguish between text and code and can handle both as regular text.
.. [9] The parser passes regular expressions to the application as text.
.. [10] The parser just provides the callback-interface for signing documents and verifying a document signature. The parser is not required to implement the required cryptological algorithms.


Recommended Parser Naming
=========================

If you publish a parser, we recommend the following naming scheme:

.. centered::
    <Tier> ( ELCL | Erbsland Configuration ) Parser for <Language>

After this title, list any extra features your parser is supporting and passes all tests. We do not recommend that you list features that do not pass 100% of all tests, as this could confuse users of your parser when they expect a certain functionality that does not work as expected.

Here are a few example how to describe an ELCL parser:

*   Standard ELCL Parser for Rust
*   Full-featured ELCL Parser for C++
*   Standard Erbsland Configuration Parser for Java, with Validation Rules support.

