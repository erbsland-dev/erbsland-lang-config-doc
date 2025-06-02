..
    Copyright (c) 2024 Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

.. _ref-error-code:
.. index::
    single: Error
    single: Error Code

Error Names and Codes
=====================

Error names and codes provide a standardized way to categorize and report errors encountered during the parsing of a document. A parser *must* support all the predefined error categories, but it has flexibility in how this support is implemented.

The following examples demonstrate how error categories might be defined in different programming languages:

.. code-block:: cpp

    enum class Error : uint8_t {
        Io,
        Encoding,
        // ...
    };

.. code-block:: python

    class Error(enum.StrEnum):
        IO = "io"
        ENCODING = "encoding"
        # ...

.. code-block:: c

    #define ERR_IO 1
    #define ERR_ENCODING 2
    /* ... */


Rules for Error Reporting
-------------------------

#.  A parser *must* use the predefined error categories.
#.  A parser *must* use the name of the error category, it *can* adapt the name to the expected formating for the used language.
#.  A parser *must* provide a method to convert the error category into a text that matches the error name, case-insensitively.
#.  If a parser assigns an integer code to an error category, it *must* use the corresponding integer from the predefined "code" field.
#.  A parser *must* provide the line number where the error occurred.
#.  A parser *should* provide the column number where the error occurred.
#.  A parser *should* provide additional details about the error when possible.
#.  A parser *can* define additional subcategories for each error to offer more specific details.

.. index::
    single: IO
    single: Encoding
    single: UnexpectedEnd
    single: Character
    single: Syntax
    single: LimitExceeded
    single: NameConflict
    single: Indentation
    single: Unsupported
    single: Access
    single: Validation
    single: Signature
    single: Error; IO
    single: Error; Encoding
    single: Error; UnexpectedEnd
    single: Error; Character
    single: Error; Syntax
    single: Error; LimitExceeded
    single: Error; NameConflict
    single: Error; Indentation
    single: Error; Unsupported
    single: Error; Access
    single: Error; Validation
    single: Error; Signature

List of Error Codes
-------------------

.. list-table::
    :header-rows: 1
    :width: 100%
    :widths: 10, 25, 65

    *   -   Code
        -   Name
        -   Description
    *   -   1
        -   :text-code:`IO`
        -   **Input/output error:** There was a problem while reading data from an IO stream.
    *   -   2
        -   :text-code:`Encoding`
        -   **Invalid encoding:** A problem with the UTF-8 encoding of the document.
    *   -   3
        -   :text-code:`UnexpectedEnd`
        -   **Unexpected end of document:** The document ended at an unexpected point.
    *   -   4
        -   :text-code:`Character`
        -   **Character not allowed:** The document contains a control character that is not allowed.
    *   -   5
        -   :text-code:`Syntax`
        -   **Syntax error:** The document contains a syntax error.
    *   -   6
        -   :text-code:`LimitExceeded`
        -   **Limit exceeded error:** The size of a name, text, or buffer exceeds the allowed limit.
    *   -   7
        -   :text-code:`NameConflict`
        -   **Name conflict:** The same name was already defined earlier in the document.
    *   -   8
        -   :text-code:`Indentation`
        -   **Unexpected indentation:** The indentation of a continued line does not match the previous line.
    *   -   9
        -   :text-code:`Unsupported`
        -   **Unsupported version of feature:** The requested feature version is not supported by this parser.
    *   -   10
        -   :text-code:`Signature`
        -   **The signature was rejected:** A document was rejected because of its signature.
    *   -   11
        -   :text-code:`Access`
        -   **No access:** A document was rejected, because of an access check.
    *   -   12
        -   :text-code:`Validation`
        -   **Validation failed:** The document failed one of the validation rules.
    *   -   100+
        -   :text-code:`Internal`
        -   **Internal error:** The parser encountered an internal error.

.. note::

    Internal error is meant as last resort, e.g. when a parser relies a map of predefined values that isn't available at runtime.


.. index::
    single: Data; Error Codes

Available Data
--------------

The ``data`` directory contains the file ``error-codes.json``, which defines all error categories in a machine-readable format.

