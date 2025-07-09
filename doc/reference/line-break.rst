..
    Copyright (c) 2024-2025 Tobias Erbsland - Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

.. _ref-line-break:
.. index::
    single: Line Break

Line Break
==========

A line break acts as a separator between lines in an :term:`ELCL` document.

.. code-block:: bnf

    line_break          ::= LF | (CR LF)


.. index::
    pair: Rules; Line Break

Rules
-----

#. **Valid Characters:** A line break can be either a single line-feed character (:cp:`0A`), or a carriage-return followed by a line-feed character (:cp:`0D` + :cp:`0A`).
#. **No Standalone Carriage-Return:** A standalone carriage-return (Macintosh-style) line break is *not allowed*.
#. **Optional Newline At End:** The newline at the end of the file is optional.
#. **Byte Limit:** A single line, including its terminating line break characters, must not exceed 4000 *bytes* in length. The last line can have a maximum of 4000 bytes content when no newline is present.

.. micro-parser::

    The maximum length for a line is 120 bytes.


Implementation Recommendations
------------------------------

#. The tokenizer should read data from a byte-data stream, line by line, into a buffer, scanning for the line-feed (:cp:`0A`) character.
#. Once the buffer is filled, its contents should be decoded and then processed into tokens.


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
    *   -   :text-code:`Character`
        -   Raised if a carriage-return is followed by any character other than a line-feed.
    *   -   :text-code:`UnexpectedEnd`
        -   Raised if the document ends immediately after a carriage-return character.
    *   -   :text-code:`LimitExceeded`
        -   Raised if a line exceeds the allowed maximum size of 4000 bytes.
