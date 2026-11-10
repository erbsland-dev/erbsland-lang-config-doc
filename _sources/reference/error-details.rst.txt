..
    Copyright (c) 2025 Tobias Erbsland - Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

.. _ref-error-details:
.. index::
    single: Error
    single: Error Details

Error Category Details
======================

This section provides a deeper look into the predefined error categories of the *Erbsland Configuration Language* (:term:`ELCL`). Each category groups together similar types of parsing issues, making it easier to understand, classify, and respond to errors in a structured and meaningful way.

.. figure:: /images/error-categories.svg
    :width: 100%

Relaxed Handling of Specialized Syntax Errors
---------------------------------------------

Some error types in the *Erbsland Configuration Language* (ELCL) are easy to classify—for example, issues related to ``IO``, ``Encoding``, or ``NameConflict`` are clearly defined and straightforward to detect. However, other categories such as ``Character``, ``UnexpectedEnd``, ``Indentation``, ``LimitExceeded``, and ``Unsupported`` are significantly harder to implement with precise reporting. These are specialized subtypes of general ``Syntax`` errors.

To simplify implementation, any parser that conforms to the ELCL specification is allowed to report such cases using the generic ``Syntax`` error code, even if a more specific category would technically be more accurate.

This means that while specialized categories are available for better diagnostics, parser implementations are not required to distinguish them. This show allow smaller implementations—especially useful for micro-parsers or resource-constrained environments.

.. list-table::
    :header-rows: 1
    :width: 100%
    :widths: 50, 50

    * - Distinct Error Categories
      - Specialized Syntax Categories
    * - | :text-code:`IO`
        | :text-code:`Encoding`
        | :text-code:`NameConflict`
        | :text-code:`Signature`
        | :text-code:`Access`
        | :text-code:`Validation`
        | :text-code:`Internal`
      - | :text-code:`Syntax`
        | ▲
        | :text-code:`UnexpectedEnd`
        | :text-code:`Character`
        | :text-code:`LimitExceeded`
        | :text-code:`Indentation`
        | :text-code:`Unsupported`

.. note::

   The ▲ symbol indicates that all specialized syntax categories conceptually derive from ``Syntax``. Parsers may always choose to report these cases using the more general ``Syntax`` code without violating the specification.


.. index::
    single: IO

Error ``IO``
------------

The ``IO`` category covers all errors related to input/output operations, typically originating from the underlying operating system or file system.

These errors are considered external to the document's syntax and structure and should be reported as early as possible. Since they are not tied to a specific part of the parsed content, it's more important to return them immediately rather than attempt precise location tracking.

The error message should include:

* A short identifier to indicate the affected source (e.g., filename or stream name).
* The exact error returned by the OS or runtime.


.. index::
    single: Encoding

Error ``Encoding``
------------------

The ``Encoding`` category is used exclusively for UTF-8 decoding errors. It only applies to:

* Invalid UTF-8 byte sequences.
* Valid UTF-8 sequences that represent disallowed Unicode code points (such as surrogate pairs or out-of-range characters).

It does **not** apply to legal characters that are disallowed by ELCL’s rules—that is covered by the ``Character`` category.

Refer to :ref:`ref-character` for full details on encoding rules and a list of illegal UTF-8 sequences that must be rejected.

When reporting an encoding error:

* Always treat it as a **high-priority** issue.
* Do not mask it with later-stage ``Syntax`` errors.
* Ensure that valid text preceding the error is still processed correctly.


.. index::
    single: UnexpectedEnd

Error ``UnexpectedEnd``
-----------------------

The ``UnexpectedEnd`` category is a specialized subtype of the general ``Syntax`` error. It is reserved for cases where the **document ends prematurely**, leaving a construct incomplete. This error can only occur at the very end of the document. If an invalid or partial construct appears earlier in the file, it must be reported as a ``Syntax`` error instead.

Typical examples of ``UnexpectedEnd`` include:

* An unterminated text block.
* A value name followed by a separator but no value.
* A carriage return at the end of the document with no following line-feed.

.. design-rationale::

    The purpose of the ``UnexpectedEnd`` category is to help applications detect situations where the document may not have been fully read—for example, when data is received from an unreliable source such as a network stream or incomplete file transfer. A parser returning this error allows the application to retry or request retransmission.

    While the line-based structure of ELCL makes it difficult to perfectly distinguish between syntax errors and premature ends, this category serves as a useful signal in practical scenarios. It can reveal edge cases that general ``Syntax`` errors would otherwise obscure.


.. index::
    single: Character

Error ``Character``
-------------------

The ``Character`` error category is a specialized subtype of the general ``Syntax`` error. It is triggered when a character is **valid UTF-8**, but explicitly disallowed by the *ELCL* specification.

This error is not an encoding issue—UTF-8 decoding has already succeeded. Instead, ``Character`` errors arise when a disallowed Unicode code point appears in the document. Common examples include:

* Control characters such as ``U+0000``.
* Other restricted Unicode ranges as defined in :ref:`ref-character`.

.. note::

    This category does **not** apply to valid characters that are disallowed only in certain syntactic contexts. For example, if a ``+`` character appears in a regular name (which is structurally invalid), the error should be reported as ``Syntax``, not ``Character``.

For a complete list of prohibited characters and ranges, see :ref:`ref-character`.

.. design-rationale::

    The ``Character`` category serves a similar purpose to ``Encoding``: it helps detect malformed or corrupted documents early in the parsing process. While technically well-formed in terms of encoding, documents containing forbidden characters are considered invalid by ELCL rules.

    By distinguishing encoding-level issues from specification-level character constraints, parser implementations can produce clearer diagnostics. This separation also enables applications to handle user errors differently from technical decoding failures.


.. index::
    single: Syntax

Error ``Syntax``
----------------

The ``Syntax`` category is the default for any violation of the *ELCL* grammar or structure, when no more specific category applies.

It serves as a general-purpose error type for malformed constructs, missing separators, misaligned indentation, unmatched quotes, and similar issues.

Use ``Syntax`` if:

* The document fails to follow the expected grammar.
* No other category—such as ``UnexpectedEnd``, ``Character``, ``LimitExceeded`` or ``Indentation``—clearly matches the problem.

This category ensures that all structurally invalid configurations are properly reported, even if they don’t fit neatly into other predefined categories.


.. index::
    single: LimitExceeded

Error ``LimitExceeded``
-----------------------

The ``LimitExceeded`` error category is a specialized subtype of the general ``Syntax`` error. It is used when a configuration document exceeds a defined numeric or structural boundary, such as size or depth limits.

Typical causes for this error include:

* A line exceeds the maximum allowed length of 4000 bytes.
* A regular name exceeds the maximum length of 100 characters.
* A name path contains more than 10 elements.
* A text, code block, regular expression, or binary data value exceeds the parser’s configured size limit.
* A byte-data format identifier exceeds the allowed length.
* The nesting depth of included documents exceeds five levels.

.. note::

    While these limits are enforced by all full-featured parsers, micro-parsers may impose stricter constraints. Refer to the relevant chapters for the exact limits applied by your target parser.


.. index::
    single: NameConflict

Error ``NameConflict``
----------------------

The ``NameConflict`` error category is used when a name is reused or conflicts with a previously defined value or section.

In *ELCL*, each name must be unique within its scope. This includes:

* Defining the same section or value name more than once.
* Defining a section and a value with the same name path.
* Mixing regular names and text names within the same section.

All possible causes and edge cases for name conflicts are described in detail in :ref:`ref-name-conflict`.


.. index::
    single: Indentation

Error ``Indentation``
---------------------

The ``Indentation`` error category is a specialized subtype of the general ``Syntax`` error. It is raised when spacing or indentation does not match the expected pattern.

This applies specifically to:

* Multiline values with inconsistent indentation.
* List entries or text blocks that are not properly indented.
* Any content that violates the required spacing before continuation lines.

This category does **not** apply if a value list or block ends unexpectedly or is malformed—such cases fall under ``Syntax``.

For a complete overview of indentation rules, see :ref:`ref-spacing`.


.. index::
    single: Unsupported

Error ``Unsupported``
---------------------

The ``Unsupported`` error category is a specialized subtype of the general ``Syntax`` error. It indicates that the document uses a feature not supported by the parser.

There are three primary cases where this error can occur:

* The document declares a ``@version`` meta value, with a language version that is not supported by the parser.
* The document declares its required features using the ``@features`` meta value, and one or more are not supported.
* The parser encounters a construct or value type it does not support, even if the ``@features`` meta value is not present.

In parsers that do not implement feature tracking, unsupported features may also be reported as ``Syntax`` errors instead. However, when feature-awareness is enabled, ``Unsupported`` should be used to clearly distinguish between unsupported constructs and general syntax errors.

See also: :ref:`ref-feature-identifier`


.. index::
    single: Access

Error ``Access``
----------------

The ``Access`` error category is used when access to a document source is explicitly denied by user code or a custom access policy.

This commonly applies to documents referenced via the ``@include`` meta command. For example, a callback may be used to restrict access to certain files, directories, or external sources.

See :ref:`ref-include` for details on how the ``@include`` mechanism works and how access control can be implemented.


.. index::
    single: Validation

Error ``Validation``
--------------------

The ``Validation`` error category is used when a document fails to meet semantic validation rules—beyond syntax and structure.

This includes:

* Invalid values according to schema rules.
* Missing required keys or sections.
* Constraint violations such as disallowed combinations.

Refer to :ref:`ref-validation-rules` for an overview of how validation rules can be defined and evaluated.


.. index::
    single: Signature

Error ``Signature``
-------------------

The ``Signature`` error category is used when a document contains a digital signature that is either invalid or cannot be verified.

This error may be triggered in the following situations:

* The signature does not match the document contents.
* The verification key or algorithm is unsupported or missing.
* The signature format is malformed.

See :ref:`ref-signature-meta-value` for implementation guidelines on how digital signatures can be added to documents and verified during parsing.


.. index::
    single: Internal

Error ``Internal``
------------------

The ``Internal`` error category is reserved for fatal errors that originate within the parser itself—typically due to unexpected conditions, logic bugs, or implementation faults.

Such errors indicate that the parser has entered an invalid or unrecoverable state. While rare, they serve as a safeguard for parser integrations, allowing the host application to detect and handle critical failures gracefully.

This error should be reserved for true internal inconsistencies or unexpected exceptions—not for user mistakes or invalid input.

.. note::

    Use of the ``Internal`` error category is **optional**. If the implementation language provides a more appropriate mechanism—such as exceptions or assertions—for reporting unexpected internal conditions, that approach may be preferred. The ``Internal`` error is available when no better alternative exists or as a deliberate design choice within the parser interface.