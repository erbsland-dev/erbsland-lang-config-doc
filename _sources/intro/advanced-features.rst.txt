..
    Copyright (c) 2024-2025 Tobias Erbsland - Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

.. _intro-advanced-features:
.. index::
    single: Advanced Features

=================
Advanced Features
=================

Advanced features in :term:`ELCL` are optional capabilities that standard parsers may or may not support. A parser must implement all advanced features to be considered a full-featured parser. These features extend the functionality beyond the core and standard features, enabling more sophisticated configurations when necessary.

.. design-rationale::

    **Why are advanced features separate?**

    While core and standard features are designed to be easily implemented by any parser across most programming languages and platforms, advanced features rely on more complex components like regular expressions and time-deltas. These components often have varying implementations across different languages and environments. If the underlying system does not natively support these features, it may not be practical or feasible to include them in a parser.

    Additionally, advanced features like validation rules support and digital signatures introduce significant implementation complexity. Schema support requires extensive validation capabilities, adding considerable code and overhead to a parser. Similarly, signature verification demands at least a cryptographic hashing function, such as SHA-256, for even a minimal implementation.

    By separating these advanced features, ELCL allows for a more flexible and modular approach to parser implementation, enabling developers to choose the level of complexity that suits their needs.

.. _intro-regular-expression:
.. index::
    single: Regular Expression
    single: RegEx

Regular Expression Values
=========================

Regular expression values are an advanced feature because their support depends heavily on the platform and programming language used by the parser. They introduce an additional data type that can be returned to the application either as plain text or as a regular expression object, depending on what makes the most sense for the specific platform.

In :term:`ELCL`, a regular expression is enclosed in slashes (:cp:`/`). For multi-line regular expressions, three slashes (``///``) are used.

.. code-block:: erbsland-conf

    [regular_expressions]
    Value A: /(get[A-Z]\w+)\s*\(\s*int\s+(\w+)\s*\)/
    Value B: /^\/data\/folder\/(.+)$/
    Value C: ///
        (get [A-Z] \w+) \s*          # Group 1: getter name
        \( \s* int \s+ (\w+) \s* \)  # Group 2: parameter name
        ///
    Value D: ///
        ^ / data / folder / (.+) $
        ///

Single-Line Regular Expressions
-------------------------------

A single-line regular expression is enclosed between two slashes (:cp:`/`). You can use the backslash character (:cp:`5C`) as usual to escape special characters within the pattern. The sequence ``\\/`` is converted to a single slash, allowing you to include slashes in the expression itself without terminating it prematurely.

Multi-line Regular Expressions
------------------------------

Multi-line regular expressions are enclosed in three slashes (``///``) and work similarly to :ref:`multi-line text<intro-multi-line-text>`. The key differences are:

- The enclosing delimiters are three slashes (``///``) instead of three double quotes.
- Parsers should enable "verbose" or "extended" mode by default, where whitespace, line breaks, and comments within the regular expression are ignored.

This format is useful for complex patterns that require more readability and organization, as it allows you to spread the pattern over multiple lines and add comments for clarity.

Implementation Considerations
-----------------------------

Because regular expression syntax and features can vary between platforms, support for regular expression values in ELCL depends on the capabilities of the parser's underlying language. Some parsers may return regular expression values as text, while others may provide them as specialized regular expression objects. This flexibility allows parsers to integrate more seamlessly with the languages and platforms they support.

.. important::

    Make sure to read the documentation of your parser implementation, to learn if a specific regular expression format is supported and if the regular expression is passed as plain text to the application.


.. _intro-time-delta:
.. index::
    single: Time-Delta

Time-Delta Values
=================

*Time-delta values* are an additional value type in the *Erbsland Configuration Language*, used to represent durations of time. They consist of a whole number followed by a unit. Consider the following examples:

.. code-block:: erbsland-conf

    [time_deltas]
    Value A: 1s            # s = seconds
    Value B: 250 ms        # Space between number and unit is optional.
    Value C: 2'898'283 µs  # Digit separators are allowed.
    Value D: -20 days      # Negative values are also allowed.

The unit must immediately follow the integer value, optionally separated by a single :term:`space` (:cp:`20`). The following units are supported by the language:

.. list-table::
    :width: 100%
    :widths: 20, 40, 40
    :align: center
    :header-rows: 1

    *   -   Short
        -   Long Singular
        -   Long Plural
    *   -   :text-code:`ms`
        -   :text-code:`millisecond`
        -   :text-code:`milliseconds`
    *   -   :text-code:`s`
        -   :text-code:`second`
        -   :text-code:`seconds`
    *   -   :text-code:`m`
        -   :text-code:`minute`
        -   :text-code:`minutes`
    *   -   :text-code:`h`
        -   :text-code:`hour`
        -   :text-code:`hours`
    *   -   :text-code:`d`
        -   :text-code:`day`
        -   :text-code:`days`
    *   -   :text-code:`w`
        -   :text-code:`week`
        -   :text-code:`weeks`

Optional Units
--------------

The following units are optional for parsers to support. Even if a parser does not support these units, it must recognize them and stop with an appropriate error message.

.. list-table::
    :width: 100%
    :widths: 20, 40, 40
    :align: center
    :header-rows: 1

    *   -   Short
        -   Long Singular
        -   Long Plural
    *   -   :text-code:`ns`
        -   :text-code:`nanosecond`
        -   :text-code:`nanoseconds`
    *   -   :text-code:`us`, :text-code:`µs`
        -   :text-code:`microsecond`
        -   :text-code:`microseconds`
    *   -   —
        -   :text-code:`month`
        -   :text-code:`months`
    *   -   —
        -   :text-code:`year`
        -   :text-code:`years`

*   Support for nano- and microseconds is optional because not all platforms provide this level of precision.
*   There are intentionally no short forms for months and years because they are less commonly used, and their abbreviations can be ambiguous.

.. design-rationale::

    **Design Rationale for Optional Units**

    Nanoseconds and microseconds are optional because not all systems provide the necessary precision to handle these values effectively. Months and years, on the other hand, introduce a different complexity level. Units from weeks down to seconds can be converted to a base unit (seconds) relatively easily. However, months and years require more complex date and time calculations, which are not universally supported across platforms.

Combining Time-Deltas
---------------------

Time-deltas can be combined in value lists, as shown in the following examples:

.. code-block:: erbsland-conf

    [complex_time_deltas]
    Value A: 4s, 120ms, 5us
    Value B: -4 days, -20 hours

Parsers are allowed to merge lists that contain only time-delta values into a single cumulative time-delta value. Alternatively, parsers may treat each time-delta as a separate value with its own unit and leave the conversion to the application.

.. important::

    Even if a parser supports time-delta values, and it must recognize all units, there may be significant differences in how they are handled across implementations. As this is not fully specified in the language standard, always refer to the documentation of your specific parser implementation for details.


Validation Rules Support
=========================

Validation rules play a crucial role in defining and verifying the structure of a configuration file. By providing a parser with a set of validation rules before reading the configuration, it can automatically verify both the document's structure and each value, and apply default values where applicable.

Validation rules are essential for anyone using a configuration parser. Without them, configurations must be verified programmatically after parsing, which typically requires considerable effort. As a result, many developers skip this step altogether, which not only leads to a poor user experience but can also pose significant security risks.

In its simplest form, validation rules are expressed as a regular :term:`ELCL` document containing constraints for each :term:`name path`. Parser implementors may also offer programmatic interfaces to define validation rules in code, or provide tools to convert validation rules from an :term:`ELCL` document into a code-based representation.

The *Erbsland Configuration Language* specifies the exact format for validation rules in document form and offers recommendations for designing a programmatic API for validation rules validation. Consistent with the overall design philosophy of ELCL, validation rules are straightforward and user-friendly.


Document Signatures
===================

:term:`ELCL` provides a framework to support embedded digital signatures within configuration files. By embedding a signature, administrators can sign configuration files, ensuring their integrity and authenticity. For any modification of a signed configuration, it has to be signed again or its signature must be removed.

The implementation of signature creation and verification must be handled by the application using the configuration parser. This language specification, however, defines how cryptographic hashes for signatures should be generated and verified and offers best-practice recommendations on signature encoding and implementation.

Signatures enable workflows for change verification and approval in configurations. For example:

#. In a basic setup, an organization may require configuration changes to be digitally signed by an authorized individual, facilitating a simple approval workflow.
#. In more advanced scenarios, an application might enforce a signature validation mechanism, requiring configurations to be signed with an approved certificate from a trusted list before execution. This approach would reject any unsigned or unauthorized configurations.

.. design-rationale::

   While applications could implement configuration signatures using separate "side-car" files, embedding the signature directly in the configuration file simplifies deployment, versioning, and integrity checks. By defining a standard for generating and verifying signatures, along with recommended practices, we aim to encourage consistency and interoperability across implementations.
