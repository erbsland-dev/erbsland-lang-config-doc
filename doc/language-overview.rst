..
    Copyright (c) 2024-2025 Tobias Erbsland - Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

.. index::
    !single: Overview
    single: Language Overview
.. _language-overview:

=================
Language Overview
=================

This chapter provides a quick overview of the *Erbsland Configuration Language* for those who want to get up to speed quickly. For more detailed information without delving too deeply into technical specifics, refer to the :ref:`intro` chapter.

.. index::
    single: Overview, Core

The Core Language
=================

.. code-block:: erbsland-conf
    :class: good-example

    # ▶︎ Meta Values must be at the top before any sections
    @version: "1.0"                           # Optionally set the version
    @features: "regex"                        # Also optionally, require certain features.

    # ▶︎ Section Definitions
    [Main Settings]                           # Interpreted as: main_settings
    App Name: "ELCL Demo"                     # Name-Value Pair with Text Value
    Version: 1                                # Name-Value Pair with Integer Value

    --[ Numbers ]---------                    # '-' and spacing can be adding to sections
    Decimal Value: 42                         # Integer Values with different formats
    Hex Value: 0x2A
    Binary Value: 0b101010
    Large Number: 1'000'000                   # Digit separators for readability

    [Features]                                # ▶︎ Boolean Values using different synonyms
    Feature Enabled: true
    Debug Mode: On
    Logging    = Enabled                      # '=' is an alternative to ':'
    Maintenance Mode : no                     # spacing around ':' and '=' is allowed

    [Messages]                                # ▶︎ Text Values with escape sequences
    Welcome Message:    "Welcome to \"ELCL Demo\"!"
    Multi Line Support: "First Line\nSecond Line"
    Unicode Example:    "Unicode test: \u{1F600}"  # 😀 Emoji

    [Server]                                  # ▶︎ Subsections and Relative Sections
    Host: "localhost"                         # => 'server.host'
    Port: 8080                                # => 'server.port'
    [.Credentials]                            # ▶︎ Relative subsection of Server
    User: "admin"                             # => 'server.credentials.user'
    Password: "secret"                        # => 'server.credentials.password'

    [Name Rules]                              # ▶︎ Name Rules
    ValidName1:   "Starts with a letter"
    Valid_Name2:  "Uses letters, digits, underscores"
    Valid Name3:  "Spaces are converted to underscores"

.. code-block:: erbsland-conf
    :class: bad-example
    :force:

    # Invalid Names
    1Invalid: "Starts with a digit"           # ERROR! Names must start with a letter
    Invalid__Name: "Consecutive underscores"  # ERROR! No consecutive underscores
    InvalidName_: "Trailing underscore"       # ERROR! No trailing underscores

    [Config]                                  # ▶︎ Name Conflicts
    Setting: "Value1"
    Setting: "Value2"                         # ERROR! 'Setting' is already defined in 'Config'

    [Config]                                  # ERROR! 'Config' section is already defined
    NewSetting: "Value"

    [Wrong Value Placement]
    BadValue:                                 # ERROR! Value must be indented if on a new line
    "This is incorrect"

.. index::
    single: Overview, Standard Features

Standard Features
=================

.. code-block:: erbsland-conf
    :class: good-example
    :force:

    [Floating Point Values]                   # ▶︎ Floating-Point Values:
    Value A: 0.                               # As soon there is a decimal point,
    Value B: .0                               # the value is a floating point value.
    Value C: 12'802.                          # With digit separators
    Value D: 1.293'281                        # Fractional number with digit separators
    Value E: 12e+12                           # Exponent notation
    Value F: 0.45E-7                          # Exponent notation with decimal fraction
    Value G: -Inf                             # Negative infinity
    Value H: NaN                              # Not a number

    [Byte Counts]                             # ▶︎ Integers that are Byte Counts:
    Value A: 1kb                              # Equals 1'000
    Value B: 540 TiB                          # Equals 593'736'278'999'040

    [Multiline Text]                          # ▶︎ Multi-line Text Values:
    Value A: """                              # Must start on the next line ...
        This is the first line of text.
        This is the second line of text.
        """                                   # Must end with """ on its own line.
    Value B:                                  # even better, start the value here
        """                                   # First line sets indent sequence.
        Another multi-line text value.
        It spans multiple lines.
        """               # Indent sequence, space to text and after the text is removed.

    [Value Lists]                             # ▶︎ Value Lists:
    Value A: 100, 200, 300, 400, 500          # Single-line list of integers
    Value B: "text", 5, Yes                   # Mixed type list
    Rainbow Colors:                           # Multi-line value list
        * "Red"
        * "Orange"
        * "Yellow"
        * "Green"
        * "Blue"
                                              # ▶︎ List Sections:
    *[Server.Connection]                      # Asterik marks a list section
    Name: "Web Localhost"
    Port: 8090

    *[Server.Connection]*                     # Second asterix, after section is valid
    Name: "Web Public"
    Port: 80

    ---*[Server.Connection]*----------------  # Can be combined with `-` as well
    Name: "Connector"
    Port: 9010
                                              # ▶︎ Text Names for Sections:
    [Email Filter . "anna@example.com"]       # Text name in section
    Reject: Yes

    [Email Filter . "bert@example.com"]       # Another text-named section
    Reject: No
    Forward To: "caesar@example.com"

    [Translations . jp]                       # ▶︎ Text Names for Values:
    "Good Morning!"      = "おはようございます！"
    "Have a great day!"  = "良い一日をお過ごしください！"
    "What is your name?" = "お名前は何ですか？"

    [Time Values]                             # ▶︎ Time Values:
    Value A: 01:23, 23:59:01, 04:27:09.003    # Hours and minutes [:seconds [.fractions]]
    Value D: 01:23z, 22:45:15z                # UTC time indicated by 'z'
    Value G: 12:01+02, 17:31-03:30            # Time with timezone offset in hours[:minutes]
    Value I: t16:49:03z                       # Optional 't' prefix for ISO compatibility

    [Date Values]                             # ▶︎ Date Values:
    Value A: 2024-12-01                       # Date in YYYY-MM-DD format
    Value B: 2018-01-14                       # Another date

    [DateTime Values]                         # ▶︎ Date-Time Values:
    Value A: 2024-11-19 17:45                 # Date and time with hours and minutes
    Value B: 2024-11-19 23:59:01              # Including seconds
    Value C: 2024-11-19 04:27:09.003          # Including fractions of a second
    Value D: 2024-11-19t01:23z                # Using 't' separator and UTC time
    Value E: 2024-11-19T22:45:15z             # Using 'T' separator and UTC time

    [Code Text]                               # ▶︎ Code Text Values:
    Value A: `return $name + "\r\n";`         # Single-line code text, no escape possible.
    Value B: ```                              # Multi-line code text, must start on new line
        function callback($name) {
            return $name + "\r\n";
        }
        ```                                   # must end on its own line
    Value C:                                  # ... text can have single backticks
        ```js                                 # Language identifier is allowed
        const overlay = document.createElement('div');
        overlay.innerHTML = `
            <div class="content">
                <span>Name: ${name}</span>
            </div>
        `;
        ```

    [Byte Data Values]                        # ▶︎ Byte-Data Values
    Value A: <01b203c405>                     # Single-line byte-data
    Value B: < 01B2 03C4 05 >                 # Spacing between bytes is allowed
    Value C: <hex: 01 b2 03 c4 05>            # Optional 'hex:' prefix
    Value D: <<<                              # Multi-line byte-data
        01b2 03c4 05a6                        # Comments and line breaks are allowed
        0728 390a 1b0c
        >>>
    Value E: <<<hex                           # Format specifier for multi-line byte-data
        01b203c4 05a60728 390a1b0c
        >>>
                                              # ▶︎ Include Meta Command
    @include: "file:configurations/*.ecl"     # Include additional configuration files

.. index::
    single: Overview, Advanced Features

Advanced Features
=================

.. code-block:: erbsland-conf
    :class: good-example
    :force:

    [Regular Expressions]                     # ▶ Regular Expressions
    Value A: /^m(a+)tch!$/                    # Enclosed in `/` characters
    Value B: ///                              # Multi-line is verbose, enclosed in `///`
        ^
        m (a+) tch !
        $
        ///                                   # Must end on its own line.

    [Time Deltas]                             # ▶ Time Deltas
    Value A: 10s                              # Integer with suffix, like `s`, `m`, `h`
    Value B: 59m                              # Single `m` is minutes.
    Value C: 5 minutes                        # Optional single space, long names
    Value D: -4days                           # Positive and negative values.

    # ▶ Validation Rules Support
    # ▶ Document Signatures
    #                        --→ more about these in the documentation.
