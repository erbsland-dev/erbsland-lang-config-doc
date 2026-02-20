..
    Copyright (c) 2025 Tobias Erbsland - Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

.. include:: _icons.rst

*******
Matches
*******

The ``matches`` constraint validates that a text value conforms to a specified
**regular expression**.

This constraint is especially useful for enforcing naming conventions,
identifier formats, or complex patterns that cannot be expressed with simpler
constraints such as ``minimum``, ``chars``, or ``in``.

Type Matrix
===========

The following table summarizes which node types support the ``matches`` constraint.

.. list-table::
    :header-rows: 1
    :class: type-matrix

    *   -   Node Type
        -   S
        -   Value Type
        -   Details
    *   -   Integer
        -   |constraint-unsupported|
        -
        -
    *   -   Boolean
        -   |constraint-unsupported|
        -
        -
    *   -   Float
        -   |constraint-unsupported|
        -
        -
    *   -   Text
        -   |constraint-supported|
        -   RegEx
        -   The text value must match the given regular expression.
    *   -   Date
        -   |constraint-unsupported|
        -
        -
    *   -   Time
        -   |constraint-unsupported|
        -
        -
    *   -   DateTime
        -   |constraint-unsupported|
        -
        -
    *   -   Bytes
        -   |constraint-unsupported|
        -
        -
    *   -   TimeDelta
        -   |constraint-unsupported|
        -
        -
    *   -   RegEx
        -   |constraint-unsupported|
        -
        -
    *   -   Value
        -   |constraint-unsupported|
        -
        -
    *   -   ValueList
        -   |constraint-unsupported|
        -
        -
    *   -   ValueMatrix
        -   |constraint-unsupported|
        -
        -
    *   -   Section
        -   |constraint-unsupported|
        -
        -
    *   -   SectionList
        -   |constraint-unsupported|
        -
        -
    *   -   SectionWithTexts
        -   |constraint-unsupported|
        -
        -
    *   -   NotValidated
        -   |constraint-unsupported|
        -
        -

Rules for Matches
=================

#.  **Optional Support:**
    Support for the ``matches`` constraint is optional.

    An implementation *may* omit this constraint entirely if the target platform
    does not provide suitable or safe regular expression support.

#.  **Regex Dialect Must Be Documented:**
    Because regular expression dialects vary between platforms, every
    implementation that supports ``matches`` *must* clearly document the
    supported syntax (for example, PCRE, POSIX, or RE2).

    Rule authors must be able to rely on documented behavior.

#.  **Matching Semantics:**
    By default, the regular expression is applied as a *partial match*.

    To require the entire text to match, validators *must* support the standard
    anchoring tokens:

    * ``^`` — beginning of the string
    * ``$`` — end of the string

#.  **Invalid Regular Expressions:**
    If the provided regular expression is syntactically invalid according to the
    supported dialect, the validator *must* reject the Validation Rules document
    itself.

    This error occurs during rules processing, not during configuration validation.

.. design-rationale::

    Regular expression support is intentionally left flexible.
    This allows implementers to reuse platform-native regex engines instead of
    mandating a specific one.

    At the same time, requiring implementations to document the supported dialect
    ensures that rule authors know exactly which syntax and features they can rely
    on.

Example
=======

The following example enforces a simple username format:

.. code-block:: erbsland-conf
    :class: validation-rules

    [api.user]
    type: "text"
    matches: /(?i)^[a-z][-_0-9a-z]{2,31}$/

.. code-block:: erbsland-conf
    :class: good-example

    [api]
    user: "Example_01"

.. code-block:: erbsland-conf
    :class: bad-example

    [api]
    user: "_bad"   # ERROR: Must start with a letter and be 3–32 characters long.
