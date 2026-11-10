..
    Copyright (c) 2025 Tobias Erbsland - Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

.. include:: _icons.rst

*****
Chars
*****

The ``chars`` constraint restricts **which characters may appear** in a text value.
When negated using ``not_chars``, it instead specifies **forbidden characters**.

This constraint applies **only to text nodes** and evaluates every character in the
value individually.

Type Matrix
===========

The following table summarizes the applicability of the ``chars`` constraint.

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
        -   |   Text
            |   ValueList[Text]
        -   Restricts the set of allowed characters (``chars``) or forbidden
            characters (``not_chars``).
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

Rules for Chars
===============

#.  **Basic Semantics:**
    The ``chars`` constraint defines a *set of allowed characters*.

    Validation succeeds only if **every character** in the text belongs to the
    union of all specified character sets.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [server.name]
        type: "text"
        chars: "(a-z)", "[%]", "digits"

#.  **Multiple Definitions (Union):**
    Multiple values are combined using **OR semantics**.

    A character is valid if it matches *any* of the specified ranges, lists, or
    named sets.

#.  **Supported Forms:**
    Each value assigned to ``chars`` may be one of the following forms:

    * **Character range** — enclosed in round brackets, e.g. ``(a-z)``
    * **Character list** — enclosed in square brackets, e.g. ``[%*,.]``
    * **Named range** — a predefined keyword, e.g. ``digits``

    .. code-block:: erbsland-conf
        :class: validation-rules

        [server.name]
        type: "text"
        chars:
            * "(a-z)"    # Character range
            * "[%*,.]"   # Character list
            * "digits"   # Named range

#.  **Character Ranges:**
    Character ranges are defined as ``(start-end)`` where *start* and *end* are
    single Unicode code points.

    * *start* must have a lower code point than *end*
    * The expression must contain exactly five code points
    * Combining characters are not allowed

    .. code-block:: erbsland-conf
        :class: validation-rules

        [server.name]
        type: "text"
        chars: "(a-z)"  # Allows lowercase ASCII letters

#.  **Character Lists:**
    Character lists are defined as ``[characters]``.

    * Each listed character must be unique
    * The outer square brackets are structural; inner characters are literal
    * No escaping is required inside the list

    .. code-block:: erbsland-conf
        :class: validation-rules

        [server.name]
        type: "text"
        chars: "[0123456789abcdefABCDEF]"  # Hexadecimal digits

#.  **Named Ranges:**
    Values not enclosed in brackets are interpreted as named ranges.

    The following named ranges are defined by ELCL and *must* be supported by all
    implementations:

    .. list-table::
        :header-rows: 1
        :width: 100%
        :class: identifier-table

        *   -   Name
            -   Definition
        *   -   letters
            -   :text-code:`a-z`, :text-code:`A-Z`
        *   -   digits
            -   :text-code:`0-9`
        *   -   control
            -   :text-code:`U+0001`–:text-code:`U+001F`,
                :text-code:`U+007F`–:text-code:`U+00A0`
        *   -   linebreak
            -   :text-code:`U+000D`, :text-code:`U+000A`
        *   -   spacing
            -   :text-code:`U+0009`, :text-code:`U+0020`

    Implementations *may* provide additional named ranges (for example, Unicode
    classes). Such extensions *must not* override built-in names.

    To avoid ambiguity, custom ranges *should* use descriptive prefixes such as
    ``unicode_letters``.

#.  **Case Sensitivity:**
    Character matching is **always case-sensitive**, regardless of the
    :doc:`case-sensitive flag <case-sensitive>`.

    Both uppercase and lowercase characters must be explicitly listed if required.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [server.name]
        type: "text"
        chars: "[a-z]", "[A-Z]"

#.  **Negation with ``not_chars``:**
    When negated as ``not_chars``, the constraint specifies *forbidden characters*.

    Validation fails if **any character** in the text matches one of the forbidden
    sets.

    .. design-rationale::

        Negating the entire constraint naively would allow strings that merely
        *contain* at least one allowed character, which is unintuitive.

        Instead, ``not_chars`` makes every occurrence of the forbidden characters
        invalid.

        Example:
        ``not_chars: "(a-z)"`` rejects ``"123abc"`` because it contains forbidden
        lowercase letters.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [server.name]
        type: "text"
        not_chars: "control"  # Control characters are forbidden
