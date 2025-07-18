..
    Copyright (c) 2024-2025 Tobias Erbsland - Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

.. index::
    single: @include
    single: Include
    single: Meta Value; Include
.. _ref-include:

Meta Command "Include"
======================

The ``@include`` meta command enables the integration of multiple configuration files into a single, unified configuration. The *Erbsland Configuration Language* specifies only the general framework for this command, offering guidance on recommended implementation practices without mandating a specific approach. This flexibility is essential to support various platforms and programming languages, each with unique requirements.

.. code-block:: erbsland-conf
    :class: good-example

    [main configuration]
    value: "text"

    @include: "file:extensions/*.ecl"


.. index::
    pair: Rules; Include

Rules
-----

#.  **Parser Security and Application Consent:** A parser *must* provide a callback or filter mechanism for the application, allowing it to *verify* each included configuration source at a *minimum*. If this callback or filter is not set, the parser *must* reject every included configuration or raise an ``Unsupported`` error.

    .. code-block:: text
        :class: good-example

        ┌────────────────────┐
        │ main.elcl          │                         ┌────────────────────┐
        ├────────────────────┤ Is this include ok?     │ Application        │
        │ [main]             │ ──────────────────────→ │                    │
        │ value: 1           │        yes, this is ok! │                    │
        │ @include "..."     │ ←────────────────────── │                    │
        └────────────────────┘                         │                    │
                                                       └────────────────────┘

#.  **Format:** The ``@include`` meta command *must* specify a text value that indicates the source of one or more configuration files to be included in the main configuration.

    .. code-block:: erbsland-conf
        :class: good-example

        @include: "<source>"

#.  **Value Format:** While a parser can interpret the text value of the ``@include`` command as needed, it is strongly *recommended* to use the format outlined in :ref:`ref-include-format`.

    .. code-block:: erbsland-conf

        @include: "file:sub.elcl"

#.  **Location:** The ``@include`` meta command *can* be specified one or more times, both before and after sections within a configuration.

    .. code-block:: erbsland-conf
        :class: good-example

        @include: "<source>"

        [section 1]
        value: 123

        @include: "<source>"

        [section 2]
        value: 123

        @include: "<source>"

#.  **Impact on the Including Configuration:** Each ``@include`` command *must* close any currently open section and clear the last absolute section name. Therefore, no values or relative sections are permitted following an ``@include`` command.

    .. code-block:: text
        :class: bad-example

        [server]
        value: 123

        @include: "<source>"

        another: 123    # ERROR! There is no open section for this value.

        [.connection]   # ERROR! There is no last absolute section after @include
        value: 123

#.  **Inclusion Order:** Configuration files *must* be included in the order specified by the ``@include`` statements.

    .. code-block:: text
        :class: good-example

        @include: "<source>"   # First
        @include: "<source>"   # Second

#.  **Alphabetical Inclusion of Named Configurations:** If the included configurations contain named files, they *should* be included in alphabetical order, based on Unicode code points.

    .. code-block:: text
        :class: good-example

        0first.elcl
        Second.elcl
        last.elcl

#.  **Hierarchical Inclusion Order:** When configurations are organized in a tree-like structure (e.g., directories), they should be included bottom-up (starting from the deepest files or directories and working upward).

    .. code-block:: text
        :class: good-example

        first.elcl
        sub/second.elcl
        sub/sub/last.elcl

#.  **Shared Value Tree:** The included configuration *must only* share the *value tree* with the main configuration, ensuring a unified data structure across included configurations.

    .. code-block:: text
        :class: good-example

        ┌────────────────────┐
        │ main.elcl          │
        ├────────────────────┤
        │ [main]             │
        │ value: 1           │        ┌────────────────────┐
        │ @include "..."     │  ───→  │ sub.elcl           │
        └────────────────────┘        ├────────────────────┤
                  │                   │ [main.sub]         │
                  │                   │ value: 2           │
                  │                   └────────────────────┘
                  ↓                             ↓
        ┌──────────────────────────────────────────────────┐
        │ Value Tree                                       │
        └──────────────────────────────────────────────────┘

#.  **Name Conflicts:** Any name conflicts *must* be resolved as though all included files form a single, unified configuration. For details, refer to :ref:`ref-name-conflict`.

    .. code-block:: text
        :class: bad-example

        ┌────────────────────┐
        │ main.elcl          │
        ├────────────────────┤
        │ [main]             │
        │ value: 1           │        ┌────────────────────┐
        │ @include "..."     │  ───→  │ sub.elcl           │
        └────────────────────┘        ├────────────────────┤
                                      │ [main] # ERROR!    │
                                      │ value: 2           │
                                      └────────────────────┘

#.  **Section Lists Across Inclusions:** Section lists *must* function seamlessly across multiple included configurations.

    .. code-block:: text
        :class: good-example

        ┌────────────────────┐
        │ main.elcl          │
        ├────────────────────┤
        │ [*list]            │
        │ value: 1           │        ┌────────────────────┐
        │ @include "..."     │  ───→  │ sub.elcl           │
        └────────────────────┘        ├────────────────────┤
                                      │ [*list]            │
                                      │ value: 2           │
                                      └────────────────────┘

#.  **No Access to Outer Context:** The included configuration *must not* have access to any context information from the configuration file that includes it. Only the shared value tree is accessible.

    .. code-block:: text
        :class: good-example

        ┌────────────────────┐
        │ main.elcl          │
        ├────────────────────┤  include   ┌────────────────────┐
        │ [main]             │  ───────→  │ extension.elcl     │
        │ value: 1           │            ├────────────────────┤
        │ @include "..."     │  access    │ [extension]        │
        └────────────────────┘  ←───╳───  │ value: 2           │
                  │ ✓ OK        forbidden └────────────────────┘
                  ↓                             ↓ ✓ OK
            ┌────────────────────────────────────────────┐
            │ Value Tree                                 │
            └────────────────────────────────────────────┘

    Examples of forbidden context access:

    -   The version set in one configuration must not influence an included configuration.
    -   The last absolute section or currently open section must not be available to the included configuration.
    -   The included configuration must not be aware of its inclusion location.
    -   The name or path of the including file must not be known to the included configuration.

#.  **Parsed as Standalone:** The included configuration *must* be parsed as if it were a standalone configuration file.

    .. code-block:: text
        :class: bad-example

        ┌────────────────────┐
        │ main.elcl          │
        ├────────────────────┤
        │ [main]             │
        │ value: 1           │        ┌────────────────────┐
        │ @include "..."     │  ───→  │ sub.elcl           │
        └────────────────────┘        ├────────────────────┤
                                      │ value: 2 # ERROR!  │
                                      │ [.sub]   # ERROR!  │
                                      └────────────────────┘

#.  **Recursion Handling:** A parser *should* detect inclusion loops and *must* limit inclusion to a maximum of *five* nesting levels.

    .. code-block:: text
        :class: good-example

        main.elcl ───→ extension.elcl ───→ extension_detail.elcl

    .. code-block:: text
        :class: bad-example

        main.elcl ───→ sub1.elcl ───→ sub2.elcl ──┐
                                                  │
            ┌─────────────────────────────────────┘
            │
            └──→ sub3.elcl ───→ sub4.elcl ──╳─→ sub5.elcl

        main.elcl ───→ sub.elcl ──┐
        ↑                         │
        └────────────╳────────────┘


.. _ref-include-format:

Recommended Value Format
------------------------

While parsers can freely determine the format used to specify the source for included configuration files, we recommend using the following format for file-based inclusion or a subset/variation of it.

.. code-block:: text

    [ "file:" ] <path>

#.  **Format:** The path may be optionally prefixed with ``file:``, but if the prefix is absent, the entire text is interpreted as a file path.

    .. code-block:: text
        :class: good-example

        @include "file:sub/detail.elcl"
        @include "sub/detail.elcl"

    Allowing a "protocol" prefix like ``file:`` not only enables future parser extensions but also allows applications to implement custom data sources (e.g., using ``internal:`` as a prefix for embedded configuration data).

#.  **File Path:** The file path can be either relative or absolute, pointing to a file and following the path syntax of the underlying operating system. The slash character (:cp:`/`) *must* be supported as a path separator on all operating systems.

    .. code-block:: text
        :class: good-example

        @include "sub/detail.elcl"
        @include "../sub/detail.elcl"
        @include "/users/example/project/configuration.elcl"

#.  **Relative Paths:** Relative paths should always resolve relative to the file that includes them.

    .. code-block:: text
        :class: good-example

        "~/app/main/config.elcl"
        @include "../ext/foo/ext_config.elcl"  =>  "~/app/ext/foo/ext_config.elcl"
        @include "sub/detail.elcl"  =>  "~/app/main/sub/detail.elcl"

#.  **Filename Pattern:** An asterisk (:cp:`*`) in the filename portion of the path includes all matching files from the specified directory.

    .. code-block:: text
        :class: good-example

        @include "extensions/*.elcl"      # Includes all files matching "*.elcl" in "extensions".
        @include "extensions/ext_*.elcl"  # Includes all files matching "ext_*.elcl" in "extensions".
        @include "extensions/*"           # Includes every file in "extensions".

    .. code-block:: text
        :class: bad-example

        @include "ext*/file.elcl"  # ERROR! "*" is allowed only in the filename portion.

#.  **Directory Pattern:** Two consecutive asterisks (``**``) in the path denote a recursive search for matching files across all subdirectories.

    .. code-block:: text
        :class: good-example

        # Includes all "config.elcl" files in "extensions" and its subdirectories.
        @include "extensions/**/config.elcl"
        # Includes all "config.elcl" files in the current directory and its subdirectories.
        @include "**/config.elcl"
        # Includes all "*.elcl" files in any "conf" subdirectory within the current directory and its subdirectories.
        @include "**/conf/*.elcl"

    .. code-block:: text
        :class: bad-example

        @include "ext**/config.elcl"  # ERROR! "**" must be a standalone path element.


Features
--------

.. list-table::
    :header-rows: 1
    :width: 100%
    :widths: 25, 75

    *   -   Feature
        -   Coverage
    *   -   :text-code:`core`
        -   Meta values and commands are part of the core language.
    *   -   :text-code:`include`
        -   ``@include`` is a standard feature.


Errors
------

.. list-table::
    :header-rows: 1
    :width: 100%
    :widths: 25, 75

    *   -   Error Code
        -   Causes
    *   -
        -   All errors related to parsing the name and text values.
    *   -   :text-code:`Syntax`
        -   |   Raised if the ``@include`` meta command is followed by a non-text value.
            |   Raised if the include value syntax is invalid.
            |   Raised if an inclusion loop is detected.
    *   -   :text-code:`LimitExceeded`
        -   Raised if more than five nesting levels are detected.
    *   -   :text-code:`Unsupported`
        -   Raised if the parser does not support the ``@include`` command.

