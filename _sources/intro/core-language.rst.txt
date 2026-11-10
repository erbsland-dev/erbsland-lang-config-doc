..
    Copyright (c) 2024-2025 Tobias Erbsland - Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

.. _intro-core:
.. index::
    single: Core Language

=============
Core Language
=============

All parsers must support the :term:`core language`, which defines a minimal set of concepts, :term:`features<feature>`, and value types. This chapter introduces these essential elements. Here, you'll learn about fundamental topics such as :ref:`file encoding<intro-file-encoding>`, :ref:`comments<intro-comment>`, :ref:`sections<intro-section>`, :ref:`names<intro-name>`, and :ref:`values<intro-value>` in a concise format.


.. _intro-file-encoding:
.. index::
    single: File Encoding
    single: Line Breaks

File Encoding and Line Breaks
=============================

Let's begin with the basics. All *ELCL* configuration files must be encoded in **UTF-8**. ELCL supports nearly all valid :term:`UTF-8` :term:`Unicode` :term:`characters<character>`, except for certain :term:`control characters`.

ELCL is a **line-based** configuration language, meaning that :term:`line breaks<line break>` are syntactically significant. Line breaks terminate comments, separate statements, and influence overall structure. The following :term:`line-ending<line ending>` styles are supported, and can be mixed within the same document:

* A single newline character (:cp:`0A`).
* A Windows-style carriage return followed by a newline (:cp:`0D&0A`).


.. _intro-document-structure:
.. index::
    single: Document Structure
    single: Structure
    single: Document

Document Structure
==================

Every configuration document in :term:`ELCL` is made up of a sequence of lines, separated by :term:`line breaks<line break>`. Lines that are empty or contain only :ref:`comments<intro-comment>` are ignored by the parser. Configuration data is organized into one or more :ref:`sections<intro-section>`, with each section containing any number of :ref:`name-value pairs<intro-name-value>`. Each pair assigns a value to a given name within its section, effectively configuring the settings for that section.

.. code-block:: erbsland-conf

    # A comment

    [first_section]
    Name1: "A text value"       # Comment
    Name2: 1'000
    last_name: 1                # Another comment.

    [another_section.subsection]  # Comment
    Name: "more keys"

.. figure:: /images/intro_main_structure_simplified.svg
    :width: 100%


.. _intro-comment:
.. index::
    single: Comment

Comments
========

In :term:`ELCL`, a :term:`comment` begins with the :cp:`#` character and continues until the end of the line. Comments are ignored entirely during parsing and can contain any text, except for some :term:`control characters` that are disallowed in ELCL documents.

.. code-block:: erbsland-conf

    # A comment at the start of the line.
        # A comment preceded by some spacing.
    [section]   # A comment after a section.
    Name: "Value"  # A comment after a name-value pair.

Comments can only appear *outside* of a :ref:`value<intro-value>`. For example, a :cp:`#` character within a :term:`text` or :term:`code` value does not initiate a comment.


.. _intro-name:
.. index::
    single: Name
    single: Case-Sensitivity

Names
=====

In :term:`ELCL`, *names* are used to identify both :ref:`sections<intro-section>` and :ref:`name-value pairs<intro-name-value>`. Names are always **case-insensitive**, meaning variations like ``example``, ``EXAMPLE``, and ``eXaMpLe`` are treated as the same name.

Name Rules
----------

Names in ELCL follow specific rules to ensure consistency and readability. They can include :term:`letters<letter>` (:cp:`a-z`), :term:`digits<digit>` (:cp:`0-9`), :term:`underscores<underscore>` (:cp:`_`), and :term:`spaces<space>` (:cp:`20`). However, there are a few important constraints:

1. **Names must start with a letter**: Names cannot begin with a digit or an underscore. For example, ``100days`` or ``_example`` are invalid names.
2. **Spaces and underscores are interchangeable**: Spaces in names are automatically converted to underscores. This means that ``Example Name`` is treated as ``example_name``.
3. **No consecutive underscores**: Names cannot contain consecutive underscores or multiple spaces in a row. This prevents names like ``this__name`` or ``this  name`` from being valid.
4. **No trailing underscores**: Names must not end with an underscore. For instance, ``example_`` is not considered valid.

These rules ensure that names in ELCL are consistent, readable, and unambiguous.

.. code-block:: erbsland-conf

    [ Example Section ]     # Interpreted as: example_section
    DNS Host: "127.0.0.1"   # Interpreted as: dns_host


.. _intro-section:
.. index::
    single: Section

Sections
========

In :term:`ELCL`, a section begins with a :ref:`name<intro-name>` enclosed in square brackets :cp:`[&]`. After the section name, you can define any number of :ref:`name-value pairs<intro-name-value>`. Empty sections—those without any name-value pairs—are also valid.

.. code-block:: erbsland-conf

    [section]
    Name1: "Value"
    Name2: "Value"

    [empty_section]  # Empty sections are allowed.

A section **must** start at the **beginning of a line**, with no :term:`spacing` before the opening square bracket :cp:`[`. However, spacing around the section :ref:`name<intro-name>` inside the brackets is allowed.

Additionally, sections can be visually separated using any number of minus :cp:`-` characters surrounding the section name. These characters are ignored by the parser but can help with visual organization in configuration files.

.. code-block:: erbsland-conf

    [   section1    ]   # Spacing around section names is allowed.
    Name: "Value"

    -----------------[ section2 ]--------------------  # Surrounding minus signs are allowed.
    Name: "Value"

    [ section3 ]-------------------------------------
    Name: "Value"

    -------------------------------------[ section4 ]
    Name: "Value"


.. _intro-subsection:
.. index::
    single: Subsection

Subsections
===========

In :term:`ELCL`, subsections are created by joining two or more :ref:`section names<intro-name>` with a :cp:`.` character, forming a :term:`name path`. This allows you to define nested configurations within a document's structure.

.. code-block:: erbsland-conf

    [section.subsection.one]
    Name: "Value"

    [  section . subsection . another_one ]  # Spacing around the '.' is also allowed.

Absolute and Relative Sections
------------------------------

If a section name begins with a :cp:`.` character, it is considered a **relative section**. Otherwise, it is treated as an **absolute section**.

- An **absolute section** starts from the document root. Each additional name separated by a dot represents a deeper level in the hierarchy.
- A **relative section** refers to a subsection of the **most recently defined absolute section**. Each relative section resets the hierarchy relative to the last absolute section, rather than nesting further under previous subsections. An ELCL document must never begin with a relative section.

.. code-block:: erbsland-conf

    [root]             # => root (absolute)
    [.section1.sub]    # => root.section1.sub (relative to root)
    [.section2]        # => root.section2 (relative to root)
    [.section3.x]      # => root.section3.x (relative to root)
    [another.sub]      # => another.sub (absolute)
    [.section1.sub]    # => another.sub.section1.sub (relative to another.sub)
    [.section2]        # => another.sub.section2 (relative to another.sub)
    [.section3.x]      # => another.sub.section3.x (relative to another.sub)


.. _intro-name-value:
.. index::
    single: Name-Value Pairs
    single: Pair

Name-Value Pairs
================

Name-value pairs in :term:`ELCL` configure individual settings within a :ref:`section<intro-section>`. Each pair must begin with a :ref:`name<intro-name>` at the start of a line, followed by a :term:`value separator`, which can be either a colon (:cp:`:`) or an equal sign (:cp:`=`). After the separator comes the actual :ref:`value<intro-value>`, which is assigned to the name.

.. code-block:: erbsland-conf

    [server]
    dns name: "ecl.example.com"   # Assigns "ecl.example.com" to `server.dns_name`
    port: 9080                    # Assigns 9080 to `server.port`

Spacing and Formatting
----------------------

You are free to add spaces around the value separator for readability:

.. code-block:: erbsland-conf

    [server]
    dns name      :    "ecl.example.com"    # Spacing around the name and value is allowed.
    port          :                         # The value can begin on the next line,
        9080                                # but indentation is required.

If the value starts on the next line, it **must be indented** with at least one :term:`space` or :term:`tab`. Also, there should be no empty line between the name and the start of the value.

.. figure:: /images/intro_section_name_value.svg
    :width: 100%


.. _intro-value:
.. index::
    single: Value

Values
======

A value *must* follow a :ref:`name<intro-name>` and the :term:`value separator`. You can write the value either on the same line or start it on the following line. There are two key rules to remember:

* A value must not start or continue at the beginning of a line.
* There must be no empty line between the name and its value.

The example below shows two valid placements of values. The first value is placed on the same line as the name, while the second value begins on the next line. If you place the value on a new line, you must indent it with at least one :term:`space` (:cp:`20`) or :term:`tab` (:cp:`09`) character.

.. code-block:: erbsland-conf

    [value_placement]
    same_line: 7000
    next_line:
        7000


.. index::
    single: Value Type

Core Value Types
================

The *core language* defines three primary :term:`value types<value type>`, which are fundamental to configuring settings in :term:`ELCL`:

1. **Integer**: Represents whole numbers, such as ``42`` or ``-1000``. Integers are commonly used for numeric settings like port numbers or limits.
2. **Boolean**: Represents logical values. Common literals include ``true`` and ``false``, but ELCL supports multiple synonyms, such as ``yes`` and ``no``, or ``on`` and ``off``. Booleans are ideal for toggling features on or off, such as enabling or disabling a module.
3. **Text**: Represents strings of characters enclosed in quotes, such as ``"example text"``. Text values are used for settings that require descriptive information, like file paths or descriptions.

While these are the core value types, ELCL also supports additional types that extend its capabilities beyond the core language. These extended types will be discussed in detail in later sections.

.. index::
    single: Value Format

Value Formats
-------------

Each value type supports various :term:`formats<value format>`, offering flexibility in how values can be represented in configuration files. For example, an integer can be written as a decimal, hexadecimal, or even using digit grouping, depending on the allowed formats.

These formats provide multiple ways to represent the same value type, making ELCL adaptable to different scenarios and user preferences.


.. _intro-integer:
.. index::
    single: Integer

Integer Values
==============

An integer value in :term:`ELCL` represents a whole positive or negative number. It can be written in decimal, hexadecimal, or binary format. Consider the following examples:

.. code-block:: erbsland-conf

    [integer_values]
    decimal     : -12'000'000
    hexadecimal : 0xAC12'08CD
    binary      : 0b10100100'00010101

Decimal Format
--------------

Numbers without any prefix are interpreted as decimal values. For example, ``120`` is a regular decimal number. Note that ELCL does not support an octal number format, so avoid leading zeros (e.g., ``0120``) to prevent confusion, as they might be misinterpreted as octal in other contexts.

.. code-block:: erbsland-conf

    [decimal_numbers]
    value a: 0                # Zero value
    value b: 12'000           # Positive decimal value with separators
    value c: -987654321       # Negative decimal value

Hexadecimal Format
------------------

Numbers prefixed with `0x` are treated as hexadecimal values. In this format, you can use both lower-case and upper-case letters :cp:`a-f` interchangeably, as ELCL is case-insensitive. Leading zeros are allowed, but the total number of digits must not exceed the parser's limit, typically 16 digits.

.. code-block:: erbsland-conf

    [hexadecimal_numbers]
    value a: 0x0                 # Zero value
    value b: 0x2ee0              # Positive hexadecimal value
    value c: -0x3ADE'68B1        # Negative hexadecimal value with separators

Binary Format
-------------

Numbers prefixed with `0b` are interpreted as binary values, consisting only of the digits :cp:`0` and :cp:`1`. Leading zeros are also permitted. Binary numbers are right-aligned, meaning the last digit always represents the least significant bit.

.. code-block:: erbsland-conf

    [binary_numbers]
    value a: 0b0                   # Zero value
    value b: 0b00101110'11100000   # Positive binary value with separators
    #        ↓ Negative binary value with separators
    value c: -0b111010'11011110'01101000'10110001

Negative and Positive Numbers
-----------------------------

Any of these formats can represent negative numbers by prefixing the value with a minus sign (:cp:`-`). For example, ``-0x1A`` and ``-42`` are valid negative hexadecimal and decimal values, respectively. Note that setting the most significant bit (the leftmost bit) in binary format results in a negative value when interpreted as a signed integer. Also, it is possible to explicitly prefix any number with a plus sign (:cp:`+`).

The four values in the following example represent the same negative integer using different formats:

.. code-block:: erbsland-conf

    [negative_numbers]
    value a: -987'654'321                          # Decimal format
    value b: -0x3ADE68B1                           # Hexadecimal format
    value c: -0b111010'11011110'01101000'10110001  # Binary format
    #        ↓ Long binary format (negative 64-bit value)
    value d: 0b11111111'11111111'11111111'11111111'11000101'00100001'10010111'01001111

Digit Separators
----------------

To enhance readability, you can use a digit separator :cp:`'` between digits in any number format. For instance, ``12'345'678`` or ``0xAC12'08CD`` are valid uses. However, there are some restrictions:

* Separators must be placed between digits only, not at the beginning or end of a number.
* Consecutive separators (e.g., ``12''345``) are not allowed.

By following these rules, you can format numbers in a way that is both flexible and clear, making your configurations easier to read and understand.


.. _intro-boolean:
.. index::
    single: Boolean

Boolean Values
==============

Boolean values represent two possible states, typically ``true`` or ``false``. They are ideal for toggling features, enabling or disabling functionalities, or providing affirmative or negative responses to configuration options. To improve readability, :term:`ELCL` offers several synonyms for "true" and "false" that can be used interchangeably.

ELCL is also :term:`case-insensitive`, meaning there is no difference between ``true``, ``True``, ``TRUE``, or even ``tRuE``—all are interpreted as the same value.

.. code-block:: erbsland-conf

    [boolean_values]
    ecl_is_nice: true        # True using lowercase
    light: Off               # False using a synonym
    motor: ENABLED           # True using uppercase synonym
    stop_now: yes            # True using another synonym

Boolean Synonyms
----------------

The table below lists all the boolean literals recognized by ELCL. You can use any of these for a true or false value, based on your preference.

.. list-table::
    :align: center
    :header-rows: 1
    :widths: 25 25

    *   - :text-code:`True`
        - :text-code:`False`
    *   - :text-code:`Yes`
        - :text-code:`No`
    *   - :text-code:`On`
        - :text-code:`Off`
    *   - :text-code:`Enabled`
        - :text-code:`Disabled`


.. _intro-text:
.. index::
    single: Text

Text Values
===========

The third core value type in :term:`ELCL` is text. Text values are enclosed in double quotes (:cp:`"`). They are used for storing strings of characters, which can include almost any :term:`Unicode` character, making them ideal for representing descriptive or freeform information.

.. code-block:: erbsland-conf

    [text_values]
    value a: ""                        # An empty text
    value b: "Text can be anything"    # A basic text value
    value c: "    Spaces    are    preserved   "  # Text with preserved spaces

The core language supports only single-line text values, as shown above. Multi-line text values are also available in ELCL and will be covered in a later section.

Text Content Restrictions
-------------------------

You can use almost any :term:`Unicode` character in text values, except for the following:

* :term:`Control characters` and :term:`line breaks<line break>` (:cp:`0d` and :cp:`0a`).
* The double quote (:cp:`"`).
* The backslash (:cp:`5c`).

To include these characters in your text values, you must use :term:`escape sequences<escape sequence>`.

Text Escape Sequences
---------------------

Escape sequences allow you to include special characters in text values by using a backslash (:cp:`5c`) followed by a specific sequence of characters. The following table provides an overview of all supported escape sequences in ELCL:

.. list-table::
    :widths: 15, 85
    :header-rows: 1
    :class: wrap-lines

    *   -   Sequence
        -   Description
    *   -   :text-code:`\\\\`
        -   Inserts a backslash (:cp:`5c`)
    *   -   :text-code:`\\"`
        -   Inserts a double quote (:cp:`"`)
    *   -   :text-code:`\\$`
        -   Inserts a dollar sign (:cp:`$`)
    *   -   :text-code:`\\n`
        -   Inserts a newline control code (:cp:`0a`)
    *   -   :text-code:`\\r`
        -   Inserts a carriage-return control code (:cp:`0d`)
    *   -   :text-code:`\\t`
        -   Inserts a tab character (:cp:`09`)
    *   -   :text-code:`\\uXXXX`
        -   Inserts a Unicode character represented by the four-digit hexadecimal code ``XXXX``. The code must be between ``0001`` and ``FFFF``. Surrogate code points between ``D800`` and ``DFFF`` are not allowed.
    *   -   :text-code:`\\u{YYYY}`
        -   Inserts a Unicode character represented by the hexadecimal code ``YYYY``. This form allows for codes with one to eight digits, between ``1`` and ``10FFFF``.

The escape sequence ``\uXXXX`` requires a four-digit hexadecimal code, while ``\u{YYYY}`` provides more flexibility, allowing one to eight digits. This flexibility helps when you need to represent characters beyond the Basic Multilingual Plane or when a fixed digit length is inconvenient.

ELCL intentionally supports only a limited set of escape sequences to keep the language simple and easy to read. For instance, rarely used escape sequences like "form feed" or "vertical tab" are not included.

.. note::

    The escape sequence for the dollar sign (:cp:`$`) is included in the core language to establish a foundation for a unified placeholder system or text interpolation. Although the specification includes a recommended placeholder syntax, support for text replacements during configuration parsing is an optional :term:`feature`. :term:`Full-featured parsers<full-featured parser>` must implement this functionality, allowing dynamic substitution of placeholder values as the configuration is processed.

All three text values in the example below are equivalent, despite being represented with different escape sequences:

.. code-block:: erbsland-conf

    [escape_sequences]
    text a: "ψ\"ありがとう\"😄"  # Direct Unicode characters, except for the double quotes
    text b: "\u{3c8}\u{22}\u3042\u308a\u304c\u3068\u3046\u{22}\u{1f604}"  # Lowercase escape sequences
    text c: "\U{3C8}\U{22}\U3042\U308A\U304C\U3068\U3046\U{22}\U{1F604}"  # Uppercase escape sequences


.. _intro-meta-value:
.. index::
    single: Metadata
    single: Meta Value

Meta Values
===========

*Meta values* are special values that are part of the configuration language itself and its parser, not the actual configuration data. These values have a name that is starting with the "at"-character :cp:`@` and they must always be defined at the beginning of a document, in the document root.

The core language requires all meta values to be placed before the first section in the document, and like :ref:`name-value pairs<intro-name-value>`, each meta value cannot be defined more than once. There are also :term:`meta commands<meta command>`, like ``@include``, which will be discussed later. *Meta commands* can be defined later in the document, between section blocks.

The core language supports the following three meta values:

.. code-block:: erbsland-conf
    :force:

    @signature: "..."
    @version: "1.0"
    @features: "regex, timedelta"

It's important to note that all meta values are completely optional.

The Version Value
-----------------

The *version* meta value specifies the version of :term:`ELCL` for which the configuration was written. This value takes a text with the version number in the format ``<major>.<minor>``. Currently, ELCL is at version ``1.0``, which is the only valid value at this time.

.. code-block:: erbsland-conf

    @version: "1.0"

    [first_section]
    name: "value"

When a parser reads the *version* meta value, it must compare it to its own supported version of the language. For example, if a future version "1.2" of ELCL introduces new features, and a parser that only supports version "1.0" encounters ``@version: "1.2"``, it must stop parsing. This is to prevent the parser from misinterpreting the configuration due to unsupported language features.

This value also helps ensure backward compatibility. If a future version "2.0" introduces breaking changes, a parser reading ``@version: "1.0"`` can switch to a legacy mode to handle the older syntax correctly.

The Features Value
------------------

The *features* meta value specifies a list of features that the document requires. This value takes a space-separated list of feature identifiers as text. If a parser does not support a specified feature, it must stop parsing the configuration.

.. code-block:: erbsland-conf

    @features: "regex timedelta"

    [first_section]
    name: "value"

This meta value ensures that a configuration document is compatible with different parsers. If a parser encounters an unsupported feature, it can provide a clear error message, preventing confusion that may arise from encountering unexpected character sequences in the document.

The Signature Value
-------------------

The *signature* value, if present, must appear in the first line of the document. This value is used to verify the integrity of the document. If a parser or application does not support signature verification, it must stop with an error when it encounters this value.

.. code-block:: erbsland-conf
    :force:

    @signature: "..."

    [first_section]
    name: "value"

This meta value is part of the core language as a security measure. If a document has been signed, the signature must be validated to ensure the document's integrity. If a parser cannot verify the signature, it should not ignore it. Instead, it should require the signature to be manually removed before processing the document. This prevents potentially unauthorized changes to the configuration from going unnoticed.

Parser Meta Values
------------------

Parser implementations are allowed to provide additional meta values, that must start with ``@parser_...``. Like meta values of the :term:`ELCL`, parser meta values must be optional.


.. _intro-name-conflict:
.. index::
    single: Name Conflicts

Name Paths and Name Conflicts
=============================

:term:`ELCL` is designed to keep configurations simple and easy to understand. To maintain this simplicity, each value can be defined only once. Overwriting existing values is not allowed, and :term:`ELCL` does not support "inheritance" or "templates." These features are often sources of unintended complexity and can lead to configuration errors, particularly in large and complex systems.

The rules are intentionally straightforward: every section and value is assigned a unique :term:`name path` starting from the document root. Once a *name path* has been assigned through a written definition in the configuration, it cannot be redefined or overwritten later in the document.

Multiple Values with the Same Name
----------------------------------

In a single configuration, two values cannot share the same name. Attempting to define a value more than once results in an error.

.. code-block:: erbsland-conf
    :class: bad-example
    :force:

    [block.one]      # Creates the value map "block.one"
    name: "value a"  # Assigns the value "value a" to "block.one.name"
    name: "value b"  # Error! "block.one.name" is already defined.

Multiple Sections with the Same Name
------------------------------------

The same rule applies to sections. Two sections in the same configuration cannot share the same name.

.. code-block:: erbsland-conf
    :class: bad-example
    :force:

    [block.one]      # Creates the section "block.one"
    name: "value a"

    [block.one]      # Error! The section "block.one" is already defined.
    name: "value b"

This rule also prevents sections from being "continued" later in the document.

.. code-block:: erbsland-conf
    :class: bad-example
    :force:

    [block one]
    value a: 123
    value b: 123
    value c: 123

    [another block]
    # ... other definitions ...

    [block one]      # Error! The section "block one" was already defined.
    value d: 123
    value e: 123
    value f: 123

Conflicts between Value and Section Names
-----------------------------------------

A section defines a unique instance with its name, behaving similarly to any other value. Consequently, a section cannot share the same :term:`name path` with an existing value.

.. code-block:: erbsland-conf
    :class: bad-example
    :force:

    [block]          # Creates the section "block"
    name: "value a"  # Assigns the value "value a" to "block.name"

    [block.name]     # Error! A value already exists for "block.name".

Likewise, no value can share the same :term:`name path` as a section.

.. code-block:: erbsland-conf
    :class: bad-example
    :force:

    [block.name]     # Creates the section "block.name"

    [block]          
    name: "value b"  # Error! The name path "block.name" is already in use.

The order in which sections or values are defined does not matter—the conflict will occur regardless. The only difference is whether the error is raised for the value or the section, depending on the order of definition.

No Conflicts with Intermediate Sections
---------------------------------------

Intermediate sections are implicitly created when defining a :term:`name path`. These sections are not considered "defined" until explicitly declared, allowing them to be defined later in the same document.

.. code-block:: erbsland-conf

    [one.two.three]  # Creates the intermediate sections "one" and "one.two".
    value: 123

    [one.two]        # This is allowed! Defines the section "one.two".
    value: 123

    [one]            # This is allowed! Defines the section "one".
    value: 123

This exception from the rule is only valid for intermediate sections being defined, the name path for intermediate sections cannot be used by values later in the same document.

.. code-block:: erbsland-conf
    :class: bad-example
    :force:

    [one.two.three] # Creates the intermediate sections "one" and "one.two".

    [one]
    two: 123        # Error! The name "one.two" is already in use. 


Core Language: Key Takeaways and Beyond
=======================================

In this chapter, we explored the essential components of the :term:`ELCL` core language. We discussed how to structure configuration documents using sections, subsections, and name-value pairs, and how to effectively utilize comments for clarity. We also covered the fundamental value types—**integers**, **booleans**, and **text**—along with their formats, rules, and best practices.

Mastering these core concepts is crucial for working with ELCL, as they provide the foundational building blocks for all configurations. Whether you are defining simple settings or creating more complex structures, the core language ensures consistency, readability, and flexibility in your configurations.

While the core language is sufficient for basic configurations and essential for lightweight :term:`micro-parsers<micro-parser>` on microcontrollers, real-world scenarios on desktop applications often require more than just the basics. This is where ELCL's **Standard Features** come into play. These features significantly extend the capabilities of the core language, enabling more sophisticated configurations.

With additional value types like floating-point numbers, dates, times, and byte-data, as well as powerful tools such as multi-line text and code blocks, value and section lists, text names, and the "include" meta command, ELCL provides the flexibility needed for complex and robust configurations.

In the next chapter, we'll explore these standard features in detail, learning how they can help you tackle advanced configuration challenges with ease. Let’s move forward and discover the possibilities that await with ELCL’s extended capabilities.