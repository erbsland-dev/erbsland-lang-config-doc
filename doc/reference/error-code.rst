..
    Copyright (c) 2025 Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

.. _ref-error-code:
.. index::
    single: Error
    single: Error Code

Error Names and Codes
=====================

Error names and codes offer a standardized way to classify and report errors that occur while parsing a document. Every parser **must** support the predefined error categories. However, the implementation details—such as the specific names or casing—can be adjusted to align with the conventions of the programming language being used.

Here’s how you might define these error categories in different programming languages:

.. code-block:: cpp

    enum class Error : uint8_t {
        Io = 1,
        Encoding = 2,
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
--------------------------

#. A parser **must** use the predefined error categories.
#. A parser **must** use the name of the error category, adapting it as needed for the target language.
#. A parser **must** provide a method to convert the error category to a case-insensitive string matching the error name.
#. If a parser assigns an integer code to an error category, it **must** use the predefined code from the "code" field.
#. A parser **must** report the line number if the error is related to a specific line in the document.
#. A parser **should** report the column number of the error when possible.
#. A parser **should** include additional context or details about the error whenever feasible.
#. A parser **can** define extra subcategories for each error to offer more specific details.
#. A parser **can** create additional categories starting at code 100. Codes 1–99 are reserved for errors defined by the language specification.


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
    single: Signature
    single: Access
    single: Validation
    single: Internal
    single: Error; IO
    single: Error; Encoding
    single: Error; UnexpectedEnd
    single: Error; Character
    single: Error; Syntax
    single: Error; LimitExceeded
    single: Error; NameConflict
    single: Error; Indentation
    single: Error; Unsupported
    single: Error; Signature
    single: Error; Access
    single: Error; Validation
    single: Error; Internal

List of Error Codes
--------------------

.. list-table::
    :header-rows: 1
    :width: 100%
    :widths: 10, 25, 65

    *   -   Code
        -   Name
        -   Description
    *   -   1
        -   :text-code:`IO`
        -   **Input/Output error:** A problem occurred while reading data from an I/O stream.
    *   -   2
        -   :text-code:`Encoding`
        -   **Invalid encoding:** The document contains a problem with UTF-8 encoding.
    *   -   3
        -   :text-code:`UnexpectedEnd`
        -   **Unexpected end of document:** The document ended unexpectedly.
    *   -   4
        -   :text-code:`Character`
        -   **Disallowed character:** The document contains a control character that is not allowed.
    *   -   5
        -   :text-code:`Syntax`
        -   **Syntax error:** The document has a syntax error.
    *   -   6
        -   :text-code:`LimitExceeded`
        -   **Limit exceeded:** The size of a name, text, or buffer exceeds the permitted limit.
    *   -   7
        -   :text-code:`NameConflict`
        -   **Name conflict:** The same name has already been defined earlier in the document.
    *   -   8
        -   :text-code:`Indentation`
        -   **Indentation mismatch:** The indentation of a continued line does not match the previous line.
    *   -   9
        -   :text-code:`Unsupported`
        -   **Unsupported feature version:** The requested feature/version is not supported by this parser.
    *   -   10
        -   :text-code:`Signature`
        -   **Signature rejected:** The document’s signature was rejected.
    *   -   11
        -   :text-code:`Access`
        -   **Access denied:** The document was rejected due to an access check.
    *   -   12
        -   :text-code:`Validation`
        -   **Validation failure:** The document did not meet one of the validation rules.
    *   -   99
        -   :text-code:`Internal`
        -   **Internal error:** The parser encountered an unexpected internal error.
    *   -   100+
        -   *Implementor Defined*
        -   Implementors can define additional error categories, starting with code 100.

.. note::

    The ``Internal`` error should be reserved as a last-resort indicator for serious issues,
    such as missing runtime data required by the parser.

.. index::
    single: Data; Error Codes

Available Data
--------------

The ``data`` directory contains the ``error-codes.json`` file, which defines all error categories in a machine-readable format.