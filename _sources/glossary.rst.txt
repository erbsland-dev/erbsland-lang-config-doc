..
    Copyright (c) 2024 Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

.. index::
    single: Glossary

========
Glossary
========

.. glossary::
    :sorted:

    ELCL
        *ELCL* stands for the *Erbsland Configuration Language*, a human-centric configuration format.

        → Read :ref:`intro` for details.

    Document
        :term:`ELCL` configuration *documents* must be encoded in :term:`UTF-8`. A *document* can contain almost all valid :term:`Unicode` :term:`characters<character>`, except :term:`control characters` with a few exceptions.

        A :term:`ELCL` *document* is :term:`line` based, and therefore a document is defined as a sequence of :term:`lines<line>` separated by :term:`line breaks<line break>`.

        → Read :ref:`ref-character` for details about the encoding of documents.

    Document Root
        In the context of :term:`ELCL`, the *document root* is the lowest level where :term:`sections<section>` can be configured. Other than inside of :term:`sections<section>`, the *document root* cannot contain any :term:`name-value pairs<name-value pair>`. As starting from the first :term:`section` line, all :term:`name-value pairs<name-value pair>` are part of one section, the only place for :term:`values<value>` in the document root is at the beginning of a document. All :term:`values<value>` defined in the *document root* must be :term:`meta values<meta value>`.

        .. code-block:: erbsland-conf

            # Here is the document root
            @version: "1.0"   # Only meta values are allowed on the document root

            [section] # After this section, the document root is inaccessible.
            Name: "Value"

        → Read :ref:`ref-name-path` for details.

    Section
        A *section* in :term:`ELCL` starts with a :term:`name`, or a sequence of nested :term:`names<name>`, enclosed in :term:`square-brackets`. *Sections* organize :term:`name-value pairs<name-value pair>` in logical groups.

        .. code-block:: erbsland-conf
            :emphasize-lines: 1, 4, 7, 10

            [section]                  # Regular section with one name.
            Name: "Value"

            [section.subsection]       # Section with one subsection.
            Name: "Value"

            [.another]                 # Relative section => section.subsection.another
            Name: "Value"

            [special."text"]           # Text section
            Name: "Value"

        :term:`Spacing` is allowed inside the enclosing brackets, between the names and separators.

        .. code-block:: erbsland-conf
            :emphasize-lines: 1

            [  section  .  name  ]     # Use spacing around the names if you like.
            Name: "Value"

        If an asterix character :cp:`*` prefixes the starting square bracket :cp:`[`, a :term:`section list` is created. Optionally you can repeat the asterix character after the closing bracket :cp:`]`.

        .. code-block:: erbsland-conf
            :emphasize-lines: 1, 4, 7

            *[section.list_sections]   # The first entry of a section list.
            Name: "Value"

            *[section.list_sections]   # The second entry of a section list.
            Name: "Value"

            *[section.list_sections]*  # You can repeat the `*` after the closing bracket.
            Name: "Value"

        Also, you can surround the enclosing brackets with the minus character :cp:`-` to visually enhance the separation of individual sections.

        .. code-block:: erbsland-conf
            :emphasize-lines: 1, 4

            ------------[ First Section ]-------------   # Use `-` for a visual separation
            Name: "Value"

            ---*[      List Section      ]*---
            Name: "Value"

        → Read :ref:`ref-section` for details.

    Root Section
        A *root section* is a section that is at the :term:`document root`, and is therefore defined with one single name.

        .. code-block:: erbsland-conf

            [root_section]             # A root section.
            [another_root_section]     # Another root section.

        → Read :ref:`ref-name-path` for details.

    Subsection
        The differentiation of a *subsection*, compared to a :term:`root section` is just its :term:`level` in the :term:`section` hierarchy. There is nothing special about *subsections*, except they are not at the :term:`document root`. The distinction between *subsections* and :term:`root sections<root section>` only matters for special features like :term:`text sections<text section>`, which always must be *subsections*.

        .. code-block:: erbsland-conf

            [root_section.sub]                 # A subsection.
            [root_section.sub.sub]             # Another subsection.
            [another_root_section.another]     # Another subsection.

        → Read :ref:`ref-section-name` for details.

    Intermediate Section
        An *intermediate section* is a special type of section that is implicitly created when a configuration uses :term:`name paths<name path>`. Unlike regular sections, *intermediate sections* do not need to be explicitly defined in the configuration. Consider the following example:

        .. literalinclude:: /documents/glossary/intermediate-section.elcl
            :language: erbsland-conf

        This configuration creates one regular section, ``four``, and three *intermediate sections* along the path.

        .. configuration-tree:: /documents/glossary/intermediate-section.elcl

        The key distinction between a regular section and an *intermediate section* becomes important when you create new sections with the same :term:`name path`. Each value or section must be defined only once in a configuration, but *intermediate sections* are an exception to this rule because they are created *implicitly*. In the example above, you can later define sections for ``one``, ``one.two``, and ``one.two.three`` without causing a name conflict.

        .. code-block:: erbsland-conf
            :class: bad-example
            :force:

            [one.two.three.four]
            value: 123

            [one]  # This is allowed.
            value: 456

            [one.two.three]  # This is also allowed.
            value: 789

            [one.two.three.four]  # Error! This name path is already in use.
            another value: "text"

        As shown, redefining the section ``one.two.three.four`` causes an error because it was already explicitly defined earlier in the configuration. However, defining any of the *intermediate sections* created implicitly by the name path is perfectly valid and does not result in a conflict.

        → Read :ref:`ref-section-name` for details.

    Text Section
        *Text sections* are a special form of :term:`subsections<subsection>` where its name is formed with a :term:`text value`. This is an :term:`optional feature` not all :term:`parsers<parser>` must support.

        .. code-block:: erbsland-conf

            [block."A text section"]           # A text section.
            [block."Example"]                  # A text section.

        → Read :ref:`ref-section-name` for details.

    Absolute Section
        An *absolute section* is a :term:`section` that starts with a :term:`name`, rather than with a :term:`name separator` (:cp:`.`). The :term:`name path` of *absolute sections* always start at the :term:`document root`.

        .. code-block:: erbsland-conf

            [section]
            [section.subsection.another]
            [section.special."text"]

        → Read :ref:`ref-section-name` for details.

    Relative Section
        A *relative section* is a :term:`section` that starts with a :term:`name separator` (:cp:`.`). It forms a subsection on the last :term:`absolute section` in the :term:`document`. Multiple *relative subsections* do not accumulate hierarchically but reset with each new *relative section*. Also, an :term:`ELCL` document must not begin with a *relative section*.

        .. code-block:: erbsland-conf
            :emphasize-lines: 2, 3, 5

            [section]
            [.sub]                    # Relative section => section.sub
            [.subsection.another]     # Relative section => section.subsection.another
            [block]
            [."text section"]         # Relative section => block."text section"

        → Read :ref:`ref-section` for details.

    Section List
        A *section list* in :term:`ELCL` allows for repeated :term:`sections<section>` with the same name path, where each instance of the section represents an individual entry in the list. This structure is useful for configurations requiring multiple items under a single logical grouping, such as server connections, filters, or other repeatable elements.

        Section lists are created by prefixing the section :term:`name` with an asterisk (:cp:`*`), allowing multiple entries with the same :term:`name path` without causing a :term:`name conflict`.

        .. code-block:: erbsland-conf

            *[servers]
            name: "web-server-1"
            address: "192.168.1.10"

            *[servers]
            name: "web-server-2"
            address: "192.168.1.11"

            *[servers]
            name: "database-server"
            address: "192.168.1.12"

        In the example above, the ``servers`` section list contains three unique entries, each identified by its own properties while sharing the same logical grouping. The asterisk placement—either at the start, end, or both—does not affect the structure but helps visually distinguish list entries.

        → Read :ref:`ref-section` for details.

    Meta Value
        *Meta values* are :term:`name-value pairs<name-value pair>`, where the :term:`name` is prefixed with an :cp:`@` character. They can have various uses, like define the used :term:`ELCL` :term:`language version`, required :term:`features<feature>`, or :term:`parser` specific :term:`values<value>`.

        *Meta values* must be configured at the very beginning of the document, before the first :term:`section`.

        .. code-block:: erbsland-conf

            @version: "1.0"
            @features: "regex, timedelta"

            [section]
            Name: "Value"

        Version "1.0" of :term:`ELCL`, supports the ``@version``, ``@features``, ``@signature`` and ``@parser_...`` meta values.

    Meta Command
        A *meta command* is a :term:`name-value pairs<name-value pair>`, where the :term:`name` is prefixed with an :cp:`@` character, but compared to :term:`meta values<meta value>`, it can be specified multiple times in the document and also between section blocks. Version "1.0" of :term:`ELCL` only supports the ``@include`` meta command.

        .. code-block:: erbsland-conf

            [first_section]
            Name: "Value"

            @include: "configuration/extension.ecl"

            [another_section]
            Name: "Value"

    Language Version
        The *language version* in *Erbsland Configuration Language* (:term:`ELCL`) specifies the version of the ELCL syntax that a document conforms to. Defining a language version ensures compatibility between configuration documents and parsers by indicating the expected syntax rules and features supported in the document.

        In an ELCL document, the language version is typically defined using a :term:`meta value` at the beginning of the configuration file. This version identifier allows parsers to validate that they support the required language features before processing the document.

        .. code-block:: erbsland-conf

            @version: "1.0"  # Specifies that the document uses ELCL version 1.0

        Specifying a language version is essential for future-proofing configurations, as it allows new features or syntax changes to be introduced in future versions of ELCL without disrupting backward compatibility. If a parser encounters a document with an unsupported language version, it should raise an error or warning.

        → Read :ref:`ref-meta-value` for details.

    Level
        The *level* in the context of :term:`ELCL` means how many :term:`names<name>` build the :term:`name path` up to a :term:`section` or :term:`value`. The :term:`document root` has *level* zero, while all :term:`root sections<root section>` have *level* one. Each :term:`subsection` adds one level to that. Other from counting :term:`names<name>`, the term has no functional meaning.

        .. code-block:: erbsland-conf

            [section]       # This section is at level 1
            Name: "Value"   # "Name" is at level 2: section.Name

            [one.two]       # This section is at level 2
            Three: "Value"  # "Three" is at level 3: one.two.Three

        → Read :ref:`ref-name-path` for details.

    Name
        A *name* can be part of a :term:`section` or define a :term:`value` inside a section. Names must always start with a :term:`letter`, followed by a combination of :term:`letters<letter>`, :term:`digits<digit>`, :term:`underscores<underscore>` or :term:`spaces<space>`. Names are case-insensitive, meaning that ``Example``, ``example``, and ``EXAMPLE`` are considered identical.

        → Read :ref:`ref-name` for details.

    Text Name
        *Text names* are used for special cases where a single-line text is mapped to a section or a value. A *text name* is essentially a double-quoted string, as defined in the :ref:`ref-text` chapter.

        → Read :ref:`ref-text-name` for details.

    Name Path
        In the context of :term:`ELCL`, a *name path* is a sequence of one or more :term:`names<Name>`, separated by a period (:cp:`.`). Name paths are used to define precise locations within :term:`sections<section>` of a configuration document or within the API of a :term:`parser` to retrieve values from the document.
    
        In configuration files, a name path specifies the hierarchy leading to a particular value. In the API, it allows for easy access to values by referencing their location in the configuration.
    
        .. code-block:: erbsland-conf
            :caption: A name path in a configuration document section.
    
            [one.two.three]
            value: 123
    
        .. code-block:: cpp
            :caption: A name path in application code to retrieve a value.
    
            auto value = configuration->getInteger("one.two.three.value");

        → Read :ref:`ref-name-path` for details.

    Name Separator
        The *name separator* is the period (:cp:`.`) character. It separates multiple :term:`names<name>` of a :term:`name path` that is used for a :term:`section`.

        .. code-block:: erbsland-conf

            [ section . subsection ]  # Two names separated with the '.'
            [one.two.three]           # Three names separated with the '.'
            [.four]                   # A relative section, starting with '.'

        → Read :ref:`ref-name-path` for details.

    Name Conflict
        In the *Erbsland Configuration Language* (:term:`ELCL`), a *name conflict* occurs when a section or value attempts to reuse a name or :term:`name path` that has already been defined within the configuration. Since ELCL requires that each name or path be unique within its context, reusing a name results in an error.

        Most common name conflicts are:

        * **Duplicate Sections**: Defining the same section more than once with an identical name path leads to a conflict, as shown below.

            .. code-block:: erbsland-conf
                :class: bad-example
                :force:

                [settings]
                enabled: Yes

                [settings]  # ERROR! The name "settings" is already in use.
                timeout: 30

        * **Duplicate Values**: Attempting to define a value more than once within the same section will result in a conflict.

            .. code-block:: erbsland-conf
                :class: bad-example
                :force:

                [settings]
                enabled: Yes
                enabled: No  # ERROR! The name "enabled" is already in use.

        * **Mixed Sections and Values**: Using the same name for both a section and a value in the same hierarchy causes a conflict.

            .. code-block:: erbsland-conf
                :class: bad-example
                :force:

                [database]
                host: "localhost"

                [database.host]  # ERROR! The name "database.host" is already used as a value.

        → Read :ref:`ref-name-conflict` for details.

    Value
        A *value* follows after a :term:`name` in a :term:`section` after the :term:`value separator`. In can be :term:`text`, a :term:`number` or more specifically an :term:`integer` or :term:`floating-point number`, or one of many other :term:`value types<value type>` and :term:`value formats<value format>`.

        *Values* must never start or being continued at the beginning of a line. There must always be a :term:`value separator` or :term:`spacing` in front of a value.

        .. code-block:: erbsland-conf

            [section]
            Name 01: 8'039                # An integer value
            Name 02: 0x92ac               # An integer value, in hexadecimal format.
            Name 03: 0b10010101           # An integer value, in binary format.
            Name 04: No                   # A boolean value.
            Name 05: 12.9e+7              # A floating point value
            Name 06: "text"               # A text value
            Name 07: 4, 5, 6              # Three values in a list
            Name 08:
                "text"                   # A text value, starting in a new line.
            Name 09: """                  # A multi-line text.
                Multi-line
                Text
                """
            Name 10: 09:30:00Z            # Time value.
            Name 11: 2024-08-31           # Date value.
            Name 12: 2024-08-31 09:40:00  # Date/time value.
            Name 13: <45 72 62 73 6c 61 6e 64>  # A byte-data value

        → Read :ref:`ref-named-value` for details.

    Value Separator
        The *value separator* distinguishes a :term:`name` from its corresponding :term:`value`. In :term:`ELCL`, it can be either be the character :cp:`:` or alternatively :cp:`=`. :term:`Spacing` is allowed before and after the *separator*, also a :term:`line break` is allowed after the *separator*, before the configured :term:`value` starts.

        .. code-block:: erbsland-conf

            [section]
            Name 01: "Value"
            Name 02 = "Value"
            Name 03        : "Value"
            Name 04:
                "Value"

        → Read :ref:`ref-named-value` for details.

    Value Type
        There are several *value type* in :term:`ELCL`. The core value types are: :term:`Integer`, :term:`Text`, and :term:`Boolean`. :term:`Standard parsers<standard parser>` also support :term:`Floating-Point`, :term:`Date`, :term:`Time` and :term:`Date-Time`. :term:`Full-featured parsers<full-featured parser>` also support the following types: :term:`Byte-Data`, :term:`Time Delta`, and :term:`Regular Expression`.

        It is important to note, that the *value type* is not the same as the :term:`value format`. While the *value type* is something a :term:`parser` returns to the application, the same type can often be written in many different :term:`formats<value format>`.

        → Read :ref:`ref-named-value` for details.

    Value Format
        For the same :term:`value type`, there are often several formats in which the same value can be configured. For example the :term:`integer` value has several formats to use:

        .. code-block:: erbsland-conf

            [section]
            Integer 01: 12'293
            Integer 02: 0xab34
            Integer 03: 0b10010010
            Integer 04: 100 kb

        The same is true for the :term:`text` type, that can be written as simple and :term:`multi-line text`, and with :term:`Full-featured parsers<full-featured parser>` also as :term:`code`.

        → Read :ref:`ref-named-value` for details.

    Text
    Text Value
        *Text* can be either a :term:`type of value<value type>`, a special form of a :term:`subsection` or also a special form to name :term:`values<value>` in a section. *Text* is enclosed in two :cp:`"` characters.

        *Text* must not contain :term:`control characters`, but can use :term:`escape sequences<escape sequence>` to add them to the text. Regular *text* must not contain line breaks, these are only allowed in :term:`multi-line text`.

        .. code-block:: erbsland-conf

            [section]
            Name 01: "Simple" # A simple text "Simple"
            Name 02: "→→→😄📝←←←" # Text with Unicode characters.
            Name 03: "\r\n\"\u{20}\u2192\u{1F606}" # Text with escape sequences

        → Read :ref:`ref-text` for details.

    Multi-line Text
    Multi-line Text Value
        *Multi-line text* is a special form of :term:`text` that can span multiple lines. It is enclosed in two sets of three :cp:`"` characters. The text itself must not start directly after the starting ``"""``, there must be an initial :term:`line break`. The same is true for the end of the text, the ending ``"""`` must be placed on its own line.

        Similar to regular :term:`text`, no :term:`control characters`, except :term:`line breaks<line break>` and the :term:`tab` character are allowed, but you can use :term:`escape sequences<escape sequence>` to add them.

        .. code-block:: erbsland-conf

            [section]
            Name 01: """      # A multi-line text.
                A multi_line text
                with a "second" line.
                """
            Name 02: # Another multi-line text, starting after a line break.
                """
                A multi_line text
                starting after a line break.
                """

        :term:`Spacing` and :term:`line breaks<line break>` up to the begin of the text on the second :term:`line` are removed and do not count as part of the text. Also the character sequence you used to indent the first line of your text is removed from any subsequent lines. The :term:`line break` and :term:`spacing` at the end of your text, up to the closing ``"""`` are removed as well. If you require a :term:`line break` at the end of your text, you must insert an empty line at the end.

        → Read :ref:`ref-multi-line-text-value` for details.

    Number
        In the context of :term:`ELCL`, a number can be either an :term:`integer value` or :term:`floating-point value`. This term only plays a role for validating :term:`ELCL` documents, where number adds more flexibility.

        → Read :ref:`ref-integer-value` and :ref:`ref-floating-point-value` for details.

    Integer
    Integer Value
        In the context of :term:`ELCL`, an *integer* is an integral data type that can be positive or negative.  Integral data types may be of different sizes and may or may not be allowed to contain negative values. The supported range is that of a *signed 64-bit value*.  :term:`Micro-parsers<micro-parser>` support *signed 32-bit values*.

        *Integer values* can be written as decimal, hexadecimal and binary numbers. :term:`Full-featured parsers<full-featured parser>` also support byte counts. The :cp:`'` character is supported as separator in all formats.

        .. code-block:: erbsland-conf

            [section]
            Integer 01: 12'293
            Integer 02: -9006
            Integer 03: 0xab34
            Integer 04: 0x1'0000'0000
            Integer 05: 0b10010010
            Integer 06: 100 kb

        → Read :ref:`ref-integer-value` for details .

    Floating-Point
    Floating-Point Value
    Floating-Point Number
        In the context of :term:`ELCL`, *floating-point values* are numbers as specified by the ISO/IEC 60559:2020 standard. The representation of these number shall follow the decimal format described in chapter 5.12 in this document. A parser *should* at least handle the *floating-point values* in the size and with the limitations as specified as ``binary64`` in this standard, the parser *can* support a higher precision.

        .. note::
            Naturally, :term:`parsers<parser>` are written for various programming languages and platforms, each with slightly different internal floating-point value representations. This can and will lead to minimal differences between implementations, which is an issue in the responsibility of the application to address.

        For the representation of *floating-point values* in :term:`ELCL`, the following rules and limitations apply:

        *   A floating point number *must* have exact one decimal point :cp:`.` present.
        *   A maximum of 32 digits *before* the decimal point are allowed.
        *   A maximum of 32 digits *after* the decimal point are allowed.
        *   A maximum of 6 digits for the exponent are allowed.

        .. code-block:: erbsland-conf

            [section]
            Floating Point 01: .0
            Floating Point 02: NaN
            Floating Point 03: INF
            Floating Point 04: 2937.28301
            Floating Point 05: 12e+10
            Floating Point 06: -12.9
            Floating Point 07: -8'283.9e-5

        → Read :ref:`ref-floating-point-value` for details.

    Letter
        In the context of :term:`ELCL`, a *letter* refers to the characters :cp:`a-z` and :cp:`A-Z`. Since :term:`ELCL` :term:`names<name>` are :term:`case-insensitive`, the use of uppercase or lowercase letters does not affect comparison.

        .. code-block:: text
            :caption: All possible letters

            abcdefghijklmnopqrstuvwxyz
            ABCDEFGHIJKLMNOPQRSTUVWXYZ

        → Read :ref:`ref-character` for details.

    Digit
        In the context of :term:`ELCL`, a *digit* refers to the characters :cp:`0-9`.

        .. code-block:: text
            :caption: All possible digits

            0123456789

        → Read :ref:`ref-character` for details.

    Underscore
        In the context of :term:`ELCL`, the *underscore* is character ``_``.

        → Read :ref:`ref-character` for details.

    Line Break
    Line Ending
        A line break in ELCL can be one of the following:

        * A single newline (:cp:`0A`).
        * A Windows-style carriage-return followed by a newline (:cp:`0D` followed by :cp:`0A`).

        → Read :ref:`ref-line-break` for details.

    Spacing
        In the context of :term:`ELCL`, *spacing* (plural) can be any combination of the :term:`space` character (:cp:`20`) and the horizontal :term:`tab` (:cp:`09`). This does not include characters that form a :term:`line break` (:cp:`0D` and :cp:`0A`).

        → Read :ref:`ref-spacing` for details.

    Space
        The *space* character (singular) refers specifically to the following space character :cp:`20`.

        → Read :ref:`ref-character` for details.

    Tab
        The *tab* refers to the horizontal tab character :cp:`09`.

        → Read :ref:`ref-character` for details.

    Square-Brackets
        *Square-brackets* are the characters :cp:`[` and :cp:`]`.

        → Read :ref:`ref-character` for details.

    Unicode
        A computing industry standard for consistent encoding, representation, and handling of text expressed in most of the world’s writing systems. Each character is assigned a unique number called a :term:`code-point`, which identifies it in the *Unicode* standard.

        → Read :ref:`ref-character` for details.

    Code-Point
    Code Point
        A *code-point* is a unique number assigned to each character in a character set, such as :term:`Unicode`. It identifies a character within the standard, enabling consistent representation across different systems.

        → Read :ref:`ref-character` for details.

    Case-Insensitive
        Case-insensitive means that uppercase and lowercase letters are treated as equivalent. For example, the strings ``example`` and ``EXAMPLE`` would be considered the same.

        → Read :ref:`ref-name` for details.

    Case-Sensitive
        Case-sensitive means that uppercase and lowercase letters are treated as distinct. For example, the strings ``example`` and ``EXAMPLE`` would be considered different.

        → Read :ref:`ref-name` for details.

    UTF-8
        *UTF-8* is a variable-width character encoding. It is capable of encoding all possible characters in :term:`Unicode` and is the required encoding format for :term:`ELCL` documents.

        → Read :ref:`ref-character` for details.

    Name-Value Pair
        A *name-value pair* consists of a :term:`name` followed by a :term:`value`, separated by a :term:`value separator`. It represents a single structure within a :term:`section`. A more commonly used term is "key/value pair".

        → Read :ref:`ref-named-value` for details.

    Line
        :term:`ELCL` documents are organized in *lines*. Lines in a document are seperated by :term:`line breaks<line break>`.

        → Read :ref:`ref-line-break` for details.

    Byte
        A *byte* is a unit of digital information that typically consists of eight bits. In the context of :term:`ELCL`, :term:`line` lengths and some other specifications are measured in bytes, not :term:`characters<character>`.

        → Read :ref:`ref-line-break` for details.

    Character
        A *character* is any letter, digit, symbol, or control code that represents text in a computer system. In :term:`ELCL`, characters are encoded according to the *UTF-8 standard*, therefore the number of :term:`bytes<byte>` per character varies.

        → Read :ref:`ref-character` for details.

    Control Characters
        Most :term:`Unicode` *control characters* are not allowed in :term:`ELCL` documents. As *control characters* count all characters in the Unicode Category "Cc" (Control Codes). This are the ranges *U+0000–U+001F* and *U+007F-U+009F*. There are three exceptions: The newline :cp:`0A` and carriage-return character :cp:`0D` for the :term:`line breaks<line break>` and the :term:`tab` character :cp:`09` that counts as :term:`spacing`.

        As :term:`ELCL` documents must have a valid :term:`UTF-8` encoding, which adds more disallowed code points. The following list is a complete list of disallowed code points:

        *   ``U+0000`` – ``U+0008``: Part of the control characters set.
        *   ``U+000B`` – ``U+000C``: Part of the control characters set.
        *   ``U+000E`` – ``U+001F``: Part of the control characters set.
        *   ``U+007F`` – ``U+009F``: Part of the control characters set.
        *   ``U+D800`` – ``U+DFFF``: Low- and high surrogates aren't allowed in :term:`UTF-8` encoding.
        *   ``U+110000`` – ``U+FFFFFFFF``: The valid unicode range ends at ``U+10FFFF``

        → Read :ref:`ref-character` for details.

    Error
        In the context of :term:`ELCL`, an *error* refers to a problem encountered during the parsing process, indicating that the document does not adhere to the expected syntax or rules. Common errors include issues like invalid line breaks, unsupported characters, or violations of length restrictions.
    
        Errors detected during parsing are reported using a predefined set of :term:`error codes<error code>` and accompanied by an :term:`error source<error source>`. The parser also provides detailed information about the error’s location, including the exact line and column number where the issue occurred.

        → Read :ref:`ref-error-code` for details.

    Error Code
        An *error code* is a standardized identifier used to report specific errors encountered during the document parsing process. While a :term:`parser` may offer additional details about the nature of an error, each error is categorized using one of the predefined error codes. This standardization ensures consistent error handling across different parser implementations, making it easier for applications to manage errors in a uniform way, regardless of the parser being used.

        → Read :ref:`ref-error-code` for details.

    Error Source
        The *error source* is a required component of every error report generated by a :term:`parser`. It typically includes the path or identifier of the data source being parsed, along with the exact line and column where the error occurred. This information helps to pinpoint the origin of the issue within the document and aids in troubleshooting.

        → Read :ref:`ref-error-code` for details.

    Parser
        A *parser* is a software library designed to read and interpret configuration files in the *Erbsland Configuration Language* (:term:`ELCL`). Parsers can be developed for any programming language or platform, offering either a document model or an event-based approach to access the configuration values. Each parser can support a variety of features, allowing it to be classified into one of the defined :term:`Parser Tiers<Parser Tier>`.

        → For more details, refer to :ref:`parser-tiers`.

    Parser Tier
        :term:`ELCL` defines four standardized parser tiers to simplify and organize the implementation of parsers. Each tier corresponds to a specific set of features, making it easier to describe and categorize a parser’s functionality.
    
        -   :term:`Micro-Parser`: The smallest parser tier, designed for embedded systems with limited resources.
        -   :term:`Minimal Parser`: Implements the :term:`Core Language` and supports :term:`floating-point values<Floating-Point Value>`.
        -   :term:`Standard Parser`: Implements most features of ELCL, with only a few advanced features omitted.
        -   :term:`Full-featured Parser`: Implements the entire ELCL specification, with all available features.
    
        → For detailed information, see :ref:`parser-tiers`.
    
    Micro-Parser
        In :term:`ELCL`, a *micro-parser* is the most minimal form of a parser, supporting only a basic subset of features. This variant is specifically designed to operate in environments with limited computational resources, such as embedded systems.

        → For more details, refer to :ref:`parser-tiers`.
    
    Minimal Parser
        A *minimal parser* in :term:`ELCL` is required to implement the core elements of the language, including the :term:`Core Language` and support for :term:`floating-point values<Floating-Point Value>`. It provides a foundational level of functionality suitable for lightweight applications, without delving into more complex or advanced features.

        → For more details, refer to :ref:`parser-tiers`.

    Standard Parser
        A *standard parser* provides a more robust implementation of the :term:`ELCL`, supporting most features except for a few advanced options. This tier is ideal for applications that need a comprehensive set of configuration language features without requiring the full extent of the specification.

        → For more details, refer to :ref:`parser-tiers`.

    Full-featured Parser
        A *full-featured parser* implements the complete set of features defined by the :term:`ELCL` specification. This tier supports every aspect of the language, including advanced features, making it suitable for applications that require the highest level of configurability and flexibility.

        → For more details, refer to :ref:`parser-tiers`.

    Feature
        A *feature* in the *Erbsland Configuration Language* (:term:`ELCL`) represents an optional or advanced capability that a parser may support. ELCL includes both core features, which are required for basic functionality, and additional features, which enhance the language’s flexibility and allow for more complex configurations.

        Features in ELCL are grouped into tiers, each tier providing a specific set of capabilities. Depending on the parser's tier—such as *Micro-Parser*, *Minimal Parser*, *Standard Parser*, or *Full-featured Parser*—certain features may or may not be supported. This tiered approach allows implementations to range from lightweight parsers suitable for embedded systems to comprehensive parsers supporting the full ELCL specification.

        → Read :ref:`parser-tiers` for details.

    Escape Sequence
        An *escape sequence* in *Erbsland Configuration Language* (:term:`ELCL`) allows special characters to be included in text values without disrupting the syntax. Escape sequences start with a backslash (:cp:`5c`), followed by a specific character or code that represents the desired special character. They are used to add non-printable characters, symbols, or Unicode characters directly within text values.

        ELCL supports the following escape sequences:

        * ``\\``: Inserts a literal backslash.
        * ``\"``: Inserts a double quote.
        * ``\$``: Inserts a dollar sign.
        * ``\n``: Inserts a newline character.
        * ``\r``: Inserts a carriage return character.
        * ``\t``: Inserts a tab character.
        * ``\uXXXX``: Inserts a Unicode character specified by exactly four hexadecimal digits (``XXXX``).
        * ``\u{Y}``: Inserts a Unicode character specified by one to eight hexadecimal digits (``Y``).

        → Read :ref:`ref-text` for details.

    Code
        A *code* value in ELCL represents a code block, allowing formatted text or instructions to be embedded within configuration files.

        → Read :ref:`ref-code-text-value` for details.

    Boolean
        A *boolean* value represents a logical truth value, typically expressed as :text-code:`Yes`/:text-code:`No` or :text-code:`True`/:text-code:`False` in ELCL.

        → Read :ref:`ref-boolean-value` for details.

    Date
        A *date* value specifies a calendar date in a standard format within ELCL configurations.

        → Read :ref:`ref-date-time-value` for details.

    Time
        A *time* value indicates a time of day, formatted according to ELCL standards.

        → Read :ref:`ref-date-time-value` for details.

    Date-Time
        A *date-time* value combines both date and time, used to specify an exact moment in ELCL.

        → Read :ref:`ref-date-time-value` for details.

    Time Delta
        A *time delta* represents a duration or time interval, allowing relative time specifications in ELCL.

        → Read :ref:`ref-time-delta-value` for details.

    Regular Expression
        A *regular expression* is a pattern used for matching text within ELCL, supporting complex search and validation operations.

        → Read :ref:`ref-regular-expression-value` for details.

    Bytes
    Byte-Data
        A *byte-data* value allows raw byte-data to be represented directly within an ELCL configuration file.

        → Read :ref:`ref-byte-data-value` for details.

    Optional Feature
        An *optional feature* in the *Erbsland Configuration Language* (:term:`ELCL`) is a non-mandatory capability that a parser may implement based on its designated tier. Optional features add flexibility and advanced functionality but are not required for basic ELCL compliance. Examples include support for complex data types like regular expressions and time deltas.

        → Read :ref:`parser-tiers` for details.

    Comment
        In :term:`ELCL`, comments are used to annotate the configuration without affecting the document's structure or content.

        .. code-block:: erbsland-conf

            # A comment in the first line.
            [main]       # A comment after an element.
            value:       # Unicode → but no control characters
                "text"   # Comment

        → Read :ref:`ref-comment` for details.

    Core Language
        The *core language* in *Erbsland Configuration Language* (:term:`ELCL`) encompasses the essential syntax and :term:`features<feature>` required for any compliant :term:`parser`. It includes basic elements like :term:`sections<section>`, :term:`name-value pairs<name>`, and standard :term:`value types<value type>`.

        → Read :ref:`intro-core` for details.

    Value Tree
        The *value tree* is the hierarchical structure representing ELCL configurations, where :term:`sections<section>` and values are organized in a nested, tree-like format based on their :term:`name paths<name path>`.

        → Read :ref:`ref-name-path` for details.

    Value Map
        A *value map* is a collection of :term:`name-value pairs<name>` within an ELCL section, where each key uniquely identifies a value. It serves as a way to group related data.

        → Read :ref:`ref-named-value` for details.

    Value List
        A *value list* in ELCL is an ordered sequence of values, which can be defined on a single line or across multiple lines, allowing multiple values to be grouped under a single name.

        → Read :ref:`ref-single-line-value-list` and :ref:`ref-multi-line-value-list` for details.

