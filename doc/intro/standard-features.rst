..
    Copyright (c) 2024 Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

.. _intro-standard-features:
.. index::
    single: Standard Features

=================
Standard Features
=================

Beyond the core language, :term:`ELCL` offers a set of **standard features** that all parsers—except for lightweight :term:`micro-parsers<micro-parser>` on embedded platforms—must support. These features extend the basic capabilities of the core language, enabling more sophisticated and flexible configurations.

This chapter introduces these standard features, which include advanced data types, enhanced syntax options, and additional configuration tools. Together, they provide the functionality needed for complex and maintainable configurations, making ELCL suitable for a wide range of use cases, from desktop applications to server environments.


.. _intro-floating-point-value:
.. index::
    single: Floating-Point Value

Floating-Point Values
=====================

Floating-point values introduce an additional data type to the language. They are not part of the :ref:`core language<intro-core>` because microcontrollers often lack support for floating-point arithmetic, making it impractical to implement them in :term:`micro-parsers<micro-parser>`.

In :term:`ELCL`, a floating-point number is defined by the presence of a decimal point (:cp:`.`). As soon as a number includes a decimal point, it is interpreted as a floating-point value. Consider the following examples:

.. code-block:: erbsland-conf

    [floating_point]
    value a: 0.
    value b: .0
    value c: 12'802.
    value d: 1.293'281
    value e: 12e+12
    value f: 0.45E-7
    value g: -Inf
    value h: NaN

.. note::

    Well-implemented applications should also accept integer values where a floating-point number is expected. Therefore, while ``0.``, ``.0``, or ``12'802.`` are technically correct floating-point numbers, you should be able to write ``0`` or ``12'802``, which is more readable.

Rules for Floating-Point Values
-------------------------------

When using floating-point numbers in ELCL, keep the following rules in mind:

- **Mandatory Whole or Fraction Part**: A floating-point number must have either a whole number part, a fraction part, or both. A lone decimal point (e.g., ``.``) is not allowed.
- **Decimal Separators**: The whole number and fraction parts can use digit separators (:cp:`'`), following the same rules as for integer numbers: separators cannot be at the beginning or end of the number, and two or more consecutive separators are not allowed.
- **Exponent Notation**: Floating-point numbers may include an exponent, indicated by the letter :cp:`e` or :cp:`E`, followed by an optional sign (:cp:`+` or :cp:`-`) and an integer.
- **Exponent Range**: The exponent can have up to six digits and may be prefixed with zeros. However, since most parsers use the IEEE 754 double-precision floating-point format, practical exponent values typically range from approximately ±308. Values beyond this range will result in ``inf`` (infinity).

Special Floating-Point Values
-----------------------------

ELCL also supports two special floating-point values:

- **Infinity**: Represented as ``Inf`` or ``-Inf``, used to denote a value greater than any finite number.
- **Not-a-Number**: Represented as ``NaN``, used to denote a value that is undefined or unrepresentable, often resulting from an invalid operation.

These special values are case-insensitive and can be written in lowercase or uppercase (e.g., ``inf``, ``NAN``).

Floating-Point Precision
------------------------

ELCL is a practical configuration language, designed with the understanding that floating-point values may be handled differently depending on the programming language or CPU architecture a parser uses. Consequently, the specification clearly states that converting floating-point numbers into the backend's floating-point data type is not strictly defined and should be done "as accurately as possible," allowing for reasonable tolerance during conversion.

Platform-independent applications should be aware of this variability and treat an ELCL document as a configuration file rather than a data format. This means allowing for the same tolerances when interpreting floating-point values, rather than expecting exact numerical precision across different systems.

.. _intro-byte-count:
.. index::
    single: Byte Count

Byte Counts
===========

Byte counts are an additional format for decimal values. A suffix like ``kb`` or ``kib`` can be added to any decimal integer, in order to write larger byte counts in a more readable way. Byte counts are not part of the :ref:`core language<intro-core>` because handling these suffixes correctly adds complexity to the parser for a feature that may not be needed in all use cases.

.. code-block:: erbsland-conf

    [Byte Counts]
    Size A: 10kb
    Size B: 100 MB
    Size D: 56 TiB

While a parser must support all suffixes up to yota-bytes, the actual byte count is limited by the underlying size for integer values. For example, one yota byte does not fit in a 64-bit integer, and must therefore rejected by the parser.

.. _intro-multi-line-text:
.. index::
    single: Multi-line Text

Multi-line Text Values
======================

For configuring larger amounts of text that span multiple lines, :term:`ELCL` supports a special format called **multi-line text**. Unlike single-line text values, which are enclosed in double quotes (:cp:`"`), multi-line text is enclosed in three double quotes (:cp:`"`:cp:`"`:cp:`"`).

.. code-block:: erbsland-conf

    [multi_line_text]
    value a: """
        The first line of text.
        The second line of text.
        """
    value b:   # Multi-line text values can start on the next line,
        """    # following the core language rule for values.
        The first line of text.
        The second line of text.
        """

If you are familiar with languages like Python, Swift, or Kotlin, which also support the ``"""..."""`` syntax, note that ELCL applies stricter rules to avoid common pitfalls associated with multi_line text.

The allowed characters and escape sequences are the same as for single-line text, but there are additional rules specific to the multi_line format:

- **Enclosure**: Multi-line text is enclosed in three double quotes (``"""``), not a single double quote.
- **Start on a New Line**: The text must begin on the line after the opening triple quotes.
- **Consistent Indentation**: All lines must be indented with the same number of :term:`spaces<space>` or :term:`tabs<tab>` as the first line.
- **Closing Line**: The closing triple quotes must appear on their own line, after the last line of text.

.. important::

    Line breaks are normalized to a single newline character (:cp:`0a`), and any trailing :term:`spacing` after the text is ignored.

Ignored Spacing Around Text
---------------------------

The actual content of the multi_line text starts on the line following the opening ``"""``. This means any spacing or comments between the opening ``"""`` and the first line of text are ignored. Similarly, all spaces or comments after the last line of text and before the closing ``"""`` are ignored.

.. figure:: /images/intro-multi-line-1.svg
    :width: 100%

    The opening ``"""`` on the same line as the name, with spacing before the first line of text.

.. figure:: /images/intro-multi-line-2.svg
    :width: 100%

    The opening ``"""`` on the next line, showing the ignored spacing.

To preserve a line break at the end of the text, you must add an explicit newline (`\n`) at the end of the last line, or leave an empty line before the closing ``"""``. Also, if you need trailing spaces in your text, you can use the escape sequence ``\u{20}``.

Strict Indentation Rules
------------------------

The first line's indentation sets the left margin for all subsequent lines. This margin is ignored and does not become part of the actual text content.

ELCL enforces strict indentation rules to prevent common mistakes. While you can use any combination of spaces and tabs for indentation, you must repeat the exact same sequence of characters for each line. If the indentation differs, for example, using four spaces on the first line and a tab on the second, the parser will stop with an error.

An exception of the strict indentation rules are empty lines: They can repeat the indentation pattern, but a line-break with no spacing is allowed too.

Examples
--------

While these rules might seem complex at first, they help avoid ambiguity and ensure consistent formatting. Consider the following examples:

In the example below, the resulting text for ``value_a`` is ``One\n⋅⋅⋅⋅Two\nThree`` (the dots represent spaces).

.. code-block:: erbsland-conf

    [multi_line_text_example]
    value a: """    # Comment
        One
            Two
        Three
        """

If your text requires leading indentation, it’s best to start the multi_line text on the next line, using the opening ``"""`` to set the indentation level. The resulting text for ``value_a`` in the following example is ``⋅⋅⋅⋅"One"\n⋅⋅"Two"\n⋅⋅⋅⋅"Three"`` (the dots represent spaces).

.. code-block:: erbsland-conf

    [multi_line_text_example]
    value a:
        """
            "One"
          "Two"
            "Three"
        """


.. _intro-section-list:
.. index::
    single: Section List

Section Lists
=============

In many configurations, you may need to specify a list of entries rather than a single entry. For these cases, :term:`ELCL` provides **section lists**. A section list behaves like a regular section, but it allows the same section to be repeated multiple times. These repeating sections are then stored as a list in the resulting configuration.

.. code-block:: erbsland-conf

    *[server.connection]
    Name: "Web Localhost"
    Port: 8090
    Address: "127.0.0.1"
    Protocol: "web"
    SSL: Off

    *[server.connection]
    Name: "Web Public"
    Port: 80
    Address: "0.0.0.0"
    Protocol: "web"
    SSL: On

    *[server.connection]
    Name: "Connector"
    Port: 9010
    Address: "0.0.0.0"
    Protocol: "connector"
    SSL: On

The configuration above results in a list of three entries under the ``connection`` section within the ``server`` section, as shown below:

.. code-block:: text

    [server]
    └── [connection]
        ├── [0]
        │   ├── name = "Web Localhost"
        │   ├── port = 8090
        │   └── ...
        ├── [1]
        │   ├── name = "Web Public"
        │   ├── port = 80
        │   └── ...
        └── [2]
            ├── name = "Connector"
            ├── port = 9010
            └── ...

Creating Section Lists
----------------------

To create a section list, simply prefix the opening bracket (:cp:`[`) with an asterisk (:cp:`*`). Optionally, you can add an asterisk after the closing bracket (:cp:`]`) and surround the section name with minus (:cp:`-`) characters for visual separation.

.. code-block:: erbsland-conf

    *[server.connection]*
    Name: "Web"

    ---*[server.connection]*------------------------------------
    Name: "Web"

Rules for Section Lists
-----------------------

The most important rule to keep in mind: you must never mix regular and section lists for the same :term:`name path` in a configuration. If you define a regular section like ``[server.connection]`` and later switch to a section list with ``*[server.connection]*``, the parser will stop with an error. This restriction ensures that a section can only be represented as either a :term:`value map` or a :term:`value list` for the same :term:`name path`, but not both.

.. code-block:: erbsland-conf
    :class: bad-example
    :force:

    *[server.connection]
    Name: "Web"

    [server.connection]   # Error! You must not mix regular with section lists.
    Name: "Web"

The second important rule: When you start a new section, and a *section list* is part of the :term:`name path`, this section always refers to the **last section** in the list that was created in the document.

.. code-block:: erbsland-conf

    *[server.connection]
    Name: "Web"           # "web" => server.connection[0].name

    [.filter]
    Ignore: "value_a"     # "value_a" => server.connection[0].filter.ignore

    *[server.connection]
    Name: "API"           # "API" => server.connection[1].name

    [server.connection.filter]
    Ignore: "value_b"     # "value_b" => server.connection[1].filter.ignore

    *[server.connection]
    Name: "Tunnel"        # "Tunnel" => server.connection[2].name

    [.filter]
    Ignore: "value_c"     # "value_c" => server.connection[2].filter.ignore

The configuration above results in a list of three entries under the ``connection`` section within the ``server`` section, each with a subsection ``filter``, as shown below:

.. code-block:: text

    server
        connection
            [0]
                name = "Web"
                filter
                    ignore = "value_a"
            [1]
                name = "API"
                filter
                    ignore = "value_b"
            [2]
                name = "Tunnel"
                filter
                    ignore = "value_c"


.. _intro-value-list:
.. index::
    single: Value List

Value Lists
===========

In many configuration scenarios, you may need a list of values rather than a single value. :term:`ELCL` supports this by allowing the creation of **value lists**. There are two types of value lists:

1. **Single-line value lists**, where values are separated by a comma (:cp:`,`).
2. **Multi-line value lists**, where each value is placed on a new line, prefixed with an asterisk (:cp:`*`).

Single-Line Value Lists
-----------------------

Single-line value lists are created by separating values with a comma. Here are some examples:

.. code-block:: erbsland-conf

    [value_lists]
    value a: 100, 200, 300, 400, 500   # A list of integers.
    value d: "text", 5, Yes            # A list with mixed value types.

You cannot create empty lists or single-line lists with only one value. These details are handled at the application level. If an application requests a list for a given value and it's defined as a regular value, a list with one element is returned. If the value isn't configured, an empty list is returned.

.. important::

    - Multi-line values are not allowed in single-line lists.
    - Consecutive commas are not allowed in lists.

Multi-line Value Lists
----------------------

Multi-line value lists are useful when you want to list values vertically. Each value must be placed on a new line and must be prefixed with an asterisk (:cp:`*`).

.. code-block:: erbsland-conf

    [value_lists]
    rainbow:
        * "red"
        * "orange"
        * "yellow"
        * "green"
        * "blue"

.. important::

    - Empty lines between values, even lines with only comments, are not allowed.
    - Multi-line values are not allowed in multi_line lists.
    - Each asterisk (:cp:`*`) must be followed by a value.

Combining Single-Line and Multi-line Value Lists
------------------------------------------------

You can combine single-line and multi_line value lists to create a two-dimensional array of values, as shown below:

.. code-block:: erbsland-conf

    [value_lists]
    array:
        *   1,   2,   3,   4
        *  12,  23,  34,  45
        * 123, 234, 345, 456

.. design-rationale::

    Value lists in :term:`ELCL` are designed to handle common configuration needs effectively, while avoiding unnecessary complexity. Key design choices include:

    - **Prohibiting Multi-line Values**: Multi-line values are not allowed in lists to maintain clarity and simplicity in the configuration.
    - **Limited Nesting**: ELCL limits list nesting to two dimensions to keep configurations easy to write and understand. For more complex data structures, formats like JSON or XML are recommended.
    - **No Empty Lists**: There is no way to create an empty list, similar to how there is no "undefined" value in ELCL. Undefined values or empty lists can overcomplicate configurations by being used to represent default values.
    - **No Single-Entry Lists**: There is no distinction between a single regular value and a list with one element. Differentiating between them would create unnecessary confusion for users.

    These constraints ensure that ELCL remains a practical and human-readable configuration language, suited to common use cases without introducing complexity.


.. _intro-text-name:
.. index::
    single: Text Name

Text Names
==========

In some cases, naming values or sections with just :term:`letters<letter>` and :term:`digits<digit>` isn't sufficient. For these situations, :term:`ELCL` provides **text names**, where the name is treated as a text value enclosed in double quotes.

Text Names for Sections
-----------------------

Text names can be used in section definitions to accommodate names that include special characters not allowed in regular names. In the example below, text names are used to configure filter rules for email addresses. Since email addresses often contain characters like :cp:`@` and :cp:`.`, which are not valid in regular names, using text names solves this problem and makes the configuration more readable.

.. code-block:: erbsland-conf

    [Email Filter . "anna@example.com"]
    Reject: Yes

    [Email Filter . "bert@example.com"]
    Reject: No
    Forward To: "caesar@example.com"

Text Names for Values
---------------------

Text names can also be used as value names. This is useful when the value name itself contains special characters or needs to be represented as a string.

.. code-block:: erbsland-conf

    [Translation . jp]
    "Good Morning!"      = "おはようございます！"
    "Have a great day!"  = "良い一日をお過ごしください！"
    "What is your name?" = "お名前は何ですか？"

Rules for Text Names
--------------------

There are a few important rules to follow when using text names in ELCL:

- **Text Format**: Text names for sections and values use the same format, limitations, and escape sequences as single-line text values.
- **Position in Name Path**: In sections, a text name must always be the last element in a :term:`name path` and cannot be the first.
- **No Subsections**: Sections with a text name cannot have subsections. The text name effectively acts as a terminal point in the hierarchy.
- **Mutually Exclusive Naming**: A section can contain either regular named values or text-named values, but not a mix of both.

.. design-rationale::

    The design and limitations of text names in ELCL are intended to prevent misuse and maintain clarity in configurations. This feature allows developers to integrate text mapping into configurations, such as mapping a string to a single value or a set of configuration values. However, it is not meant to enable complex Unicode texts as configuration names or to support native language configuration names. The goal is to provide flexibility without sacrificing the simplicity and readability of the configuration.


.. _intro-time:
.. index::
    single: Date
    single: Time
    single: Date-Time

Date, Time, and Date-Time Values
================================

:term:`ELCL` supports date, time, and combined date-time values using a subset of the formats defined in the ISO 8601-1:2019 standard.

Time Values
-----------

Here are some examples of time values in ELCL:

.. code-block:: erbsland-conf

    [time_values]
    value a: 01:23              # A local time in <hour>:<minute> format.
    value b: 23:59:01           # A local time with seconds.
    value c: 04:27:09.003       # A local time with fractions of seconds.
    value d: 01:23z             # UTC time (indicated by 'z').
    value e: 22:45:15z          # UTC time with seconds.
    value f: 14:21:59.141Z      # UTC time with fractions of seconds.
    value g: 12:01+02           # Time with a timezone offset in hours.
    value h: 17:31-03:30        # Time with a timezone offset in hours and minutes.
    value i: t16:49:03z         # Optional 't' prefix for ISO compatibility.

A time value must contain at least one colon separator (:cp:`:`) and must therefore specify at least hours and minutes. You can optionally include seconds and fractions of seconds. Each element (hours, minutes, and seconds) must consist of two digits. Fractions of a second can be specified with up to nine digits, separated by a decimal point (:cp:`.`).

Each time value can also have an optional timezone offset. This can either be the letter :cp:`z` for UTC, or an offset starting with a plus (:cp:`+`) or minus (:cp:`-`) sign. The offset can be specified with hours and, optionally, minutes.

A parser must always assign a timezone or offset to a time value. For local times without a specified offset, the parser should use the system's local timezone. Unlike data formats where a timezone is crucial, ELCL allows local times since they automatically adapt to the system's timezone.

.. note::

    Geographical time zones are not supported in ELCL because they require a date and are rarely needed in configuration files. If a specific time at a particular geographical location is required, it is best practice to convert it to UTC first.

Date Values
-----------

The following examples demonstrate date values:

.. code-block:: erbsland-conf

    [date_values]
    value a: 2024-12-01
    value b: 2018-01-14

Dates must include a year, month, and day, separated by a minus sign (:cp:`-`). The year requires four digits, while the month and day require two digits each. The year must be in the range of 1 to 9999.

Date-Time Values
----------------

The following examples show combined date-time values:

.. code-block:: erbsland-conf

    [date_time_values]
    value a: 2024-11-19 17:45
    value b: 2024-11-19 23:59:01
    value c: 2024-11-19 04:27:09.003
    value d: 2024-11-19t01:23z
    value e: 2024-11-19T22:45:15z

Date-time values combine a date and a time, separated by either a :term:`space` (:cp:`20`) or the letter :cp:`T`.

ISO Compatibility
-----------------

ELCL supports only a subset of the ISO 8601-1:2019 standard:

- The year zero is not allowed.
- Week and ordinal dates are not supported.
- Times must include at least hours and minutes, and dates require all three components (year, month, and day).
- Separator characters (:cp:`-` and :cp:`:`) are mandatory.
- Hour and minute fractions are not allowed, and the number of fractional digits for seconds is limited to nine.


.. _intro-code:
.. index::
    single: Code

Code Text
=========

*Code* is a special format for text values that does not support escape sequences. It uses backtick (grave accent, :cp:`60`) characters to enclose the text. This format is useful for including short code snippets or text with many backslashes (:cp:`5c`) in the configuration without needing to escape special characters. Code text is not a distinct value type; rather, it is a special :term:`format<value format>` for text values.

Consider the following examples:

.. code-block:: erbsland-conf

    [code_text]
    value a: `return $name + "\r\n";`  # Single-line code text.
    value b:                           # Multi-line code text.
        ```
        function callback($name) {
            return $name + "\r\n";
        }
        ```
    value c:                           # Text with backticks.
        ```
        const overlay = document.createElement('div');
        overlay.innerHTML = `
            <div class="content">
                <span>Name: ${name}</span>
            </div>
        `;
        ```
    value d:
        ```xml    # A language identifier is allowed but ignored by the parser.
        <Document>
        </Document>
        ```

In the examples above, the code format allows JavaScript snippets to be included naturally in the configuration, without escaping double quotes and backslashes, which are common in many programming languages.

Rules for Code Text
-------------------

-   **No Escape Sequences**: Code text does not support escape sequences. This means that it is not possible to use a single backtick in single-line code text or to start a line with three backticks in multi_line code text.
-   **Language Identifier**: For multi_line code text, a language identifier like ``cpp`` or ``xml`` can be added immediately after the opening three backticks. This identifier is ignored by the parser but can be useful for syntax highlighters.
-   **Same Rules as Text Values**: Except for the lack of escape sequences, code text follows the same rules as :ref:`text<intro-text>`:

    -   **No Control Characters**: Control characters are not allowed in code text.
    -   **Line Breaks**: Line breaks are normalized to a single newline character.
    -   **Consistent Indentation**: Continued lines must start with the same sequence of indentation characters.


.. _intro-byte-data:
.. index::
    single: Byte-Data

Byte-Data Values
================

*Byte-data* introduces a new data type to :term:`ELCL`, allowing short sequences of byte-data to be included in configurations. Byte-data is represented using pairs of hexadecimal digits enclosed in angle brackets ``<...>`` for single-line values, or triple angle brackets ``<<<...>>>`` for multi_line values.

Consider the following examples:

.. code-block:: erbsland-conf

    [byte_data_values]
    value a: <01b203c405>           # A single-line value with five bytes.
    value b: < 01B2 03C4 05 >       # Spacing between bytes is allowed.
    value c: <hex: 01 b2 03 c4 05>  # Optional "hex:" prefix is allowed.
    value d: <<<                    # A multi_line byte-data value.
        01b2 03c4 05a6              # Comments and line breaks are allowed
        0728 390a 1b0c              # in multi_line "hex" byte-data.
        >>>
    value e: <<<hex                 # Optional format prefix for multi_line byte-data.
        01b203c4 05a60728 390a1b0c
        >>>



Rules for Byte-Data
---------------------

- **Hexadecimal Pairs**: Byte-data must be specified in pairs of hexadecimal digits, each pair representing a single byte.
- **Allowed Spacing**: Spaces are allowed between byte pairs. In multi_line values, line breaks are also permitted.
- **Format Specifier**: The format of the data can optionally be specified immediately after the opening bracket. Currently, only the ``hex`` format is supported. For single-line values, the format specifier must be followed by a colon (:cp:`:`).

.. design-rationale::

    The purpose of supporting byte-data in ELCL is not to embed large data blobs but to allow for short sequences of byte-data in configurations. This is useful for scenarios such as configuring file headers or protocol-specific data sequences that cannot be easily expressed using text. By providing a dedicated byte-data format, ELCL avoids the uncontrolled growth of various ad-hoc formats embedded in text values, ensuring that configurations remain clear and manageable.

    The optional format specifier (``hex``) is included in this version of the language specification to simplify future extensions. When no format specifier is present, the hexadecimal format is assumed by default.

.. _intro-include:
.. index::
    single: Include

Meta Command "Include"
======================

A standard feature of :term:`ELCL` is the ``@include`` :term:`meta command`. *Meta commands* are similar to :ref:`meta values<intro-meta-value>`, but they can be defined multiple times, and they can be placed between sections or at the end of a document.

The ``@include`` meta command must be followed by a :ref:`text<intro-text>` value containing a URL-like path, either a relative or absolute file-system path, or a file system pattern. This path or pattern specifies one or more configuration files to be read and included at the position of the meta command.

Consider the following example:

.. code-block:: erbsland-conf

    [section]
    name: "value"

    @include: "file:configurations/*.ecl"

Interpretation of the Path
--------------------------

A parser is *not* responsible for interpreting or resolving the path specified in the ``@include`` meta command. In the simplest implementation, the parser can pass this value to the application and expect a list of data streams to parse. However, the ELCL specification recommends that parsers provide a default implementation for resolving paths, allowing the application to validate each path or set limits beforehand.

For security and consistency, applications may want to restrict paths to be within a specific directory, such as the main configuration directory, or require that included files be located in the same directory as the original configuration file. While ELCL defines the mechanism and behavior for including additional configuration files, it leaves the specifics of path resolution and validation to the parser and application.

Order of Included Configuration Values
--------------------------------------

Configuration sections and values from included files are integrated into the main configuration in the order they are encountered.

If multiple files are included using a file pattern, the specification recommends that they be processed in alphabetical order. For recursive patterns, files should be included in alphabetical order within each directory, and subdirectories should be processed in alphabetical order as well. These recommendations are provided to ensure consistency, but they are not strict requirements, as configurations may not always be stored as files with predictable names. Check your parser's documentation for specific details on how it handles file inclusion.

How Configurations are Imported
-------------------------------

Each included file must be a complete and valid ELCL configuration document. This means it can contain meta values, signatures, and must follow all standard ELCL rules. For example:

- An included document must not begin with a relative section or contain values outside of a section.
- :ref:`Name conflicts<intro-name-conflict>` are handled like everything is one single document.

The ``@include`` meta command does not simply copy text from another file into the main configuration. Instead, it incorporates the fully parsed configuration data from the included file into the current document.

Since the ``@include`` meta command is always placed at the :term:`document root`, it closes any previously open section. After an ``@include`` command, you cannot continue configuring values in the previous section or start a new :ref:`relative section<intro-subsection>`.

