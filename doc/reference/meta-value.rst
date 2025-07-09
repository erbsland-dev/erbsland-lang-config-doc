..
    Copyright (c) 2024 Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

.. _ref-meta-value:
.. index::
    single: Meta Value
    single: Meta Command

========================
Meta Values and Commands
========================

Meta values and commands are not part of the configuration content, but play a role in the configuration language. The generic EBNF syntax for meta values is defined in chapter :ref:`ref-named-value`. The difference between a meta value and command is that the first defines a value while the second performs an action. The syntax of both is the same. Meta values are part of the core language, meta commands are a standard feature.

.. code-block:: erbsland-conf
    :class: good-example

    @version: "1.0"            # Define a required language version.
    @features: "regex, float"   # Require some features.

    [main]
    Value: 10.9


Basic Rules for Meta Values
===========================

#.  **Name:** The name of a meta value starts with the at-character (:cp:`@`), immediately followed by a regular name as defined in :ref:`ref-name`. All other rules of regular names also apply to the names of meta values.

    .. code-block:: text
        :class: good-example

        @version
        @features
        @parser_strict

#.  **Valid Names in the Core Language:** A parser *must* support the names ``@version``, ``@features``, ``@signature`` and ``@include``, even if it does not support its functionality.

    .. code-block:: text
        :class: good-example

        @signature
        @version
        @features
        @include

#.  **Parser Extensions:** A parser can introduce custom meta values and commands. The names of such meta values and commands must start with ``@parser_``. The name ``@parser_unknown`` is reserved for testing, and must never be used.

    .. code-block:: text
        :class: good-example

        @parser_strict_check
        @parser_debug

#.  **Value After the Name:** The value of meta values and commands must be one of: text, integer or boolean. Other types are not allowed for meta values and commands.

    .. code-block:: erbsland-conf
        :class: good-example

        @parser_strict_checks : "integer32"
        @parser_debug         : Yes

#.  **Location:** Meta value *must* be defined *before* the first section in a document.

    .. code-block:: erbsland-conf
        :class: good-example

        @version: "1.0"
        @features: "regex, float"

        [main]
        Value: 10.9

    .. code-block:: erbsland-conf
        :class: bad-example
        :force:

        [main]
        Value: 10.9

        @version: "1.0"  # ERROR! Must not be defined in or after a section.

#.  **Name Conflicts:** Meta values are local to individual documents, not to a whole configuration that may consists of multiple documents. Each meta value must be defined only once per document.

    .. code-block:: erbsland-conf
        :class: bad-example
        :force:

        @version: "1.0"
        @version: "1.0"  # ERROR! Already defined in this document.

#.  **Behaviour for Unknown Meta Values and Commands:** If a parser reads an unknown meta value or command, it *must* stop with an error.

    .. code-block:: erbsland-conf
        :class: bad-example
        :force:

        @unknown: "text"     # ERROR! The meta value "unknown" is not valid.

.. index::
    single: @version
    single: Version
    single: Meta Value; Version

The Meta Value "Version"
========================

The meta value ``@version`` sets and at the same time requires a given configuration language version. At the moment, there is only version "1.0" of the *Erbsland Configuration Language*, if in the future, new major version of the language introduces incompatible changes - requiring an older version will allow parsers to read a document in a compatibility mode.

Rules
-----

#.  **Value:** The ``@version`` meta value requires a text value, with the language version in the format ``<major>.<minor>`` where major and minor consist of one decimal digit. At the moment, the only valid text is ``1.0``.

    .. code-block:: erbsland-conf
        :class: good-example

        @version: "1.0"

#.  **Behaviour:** If a parser does not support or know the specified version, it must stop parsing with an ``Unsupported`` error.

    .. code-block:: erbsland-conf
        :class: bad-example
        :force:

        @version: "9.7"  # ERROR! Unsupported version.

#.  **Define it once only:** The ``@version`` meta value *must* be defined at most once in a configuration document. Defining it more than once is considered a syntax error.

    .. code-block:: erbsland-conf
        :class: bad-example
        :force:

        @version: "1.0"
        @version: "1.0"  # ERROR! Duplicate @version definition.


.. index::
    single: @features
    single: Features
    single: Meta Value; Features

The Meta Value "Features"
=========================

The meta value ``@features`` requires a given set of features for a document. If a parser does not support one of the specified features, it must stop with an ``Unsupported`` error. By defining this meta value in a document, parsing of a document can be stopped early, with a clear error message when a feature isn't supported on a platform.

.. micro-parser::

    A micro-parser *can* simply accept an empty or ``core`` text and raise an error in every other case. This is perfectly acceptable behaviour.

Rules
-----

#.  **Value:** The ``@features`` meta value requires a text value, with a space separated list of feature identifiers. See :ref:`ref-feature-identifier` for a list of all feature identifiers.

    .. code-block:: erbsland-conf
        :class: good-example

        @features: "value-list multi-line code"

#.  **Behaviour:** A parser must compare each feature identifier, case-insensitive, with its built-in list of supported features. If it reads an unknown or unsupported feature, it must stop with an error.

    .. code-block:: text
        :class: bad-example

        @features: "example"  # ERROR! Unsupported, because unknown feature.

#.  **Define only once:** The ``@features`` meta value *must* be defined at most once in a configuration document. Defining it more than once is considered a syntax error.

    .. code-block:: erbsland-conf
        :class: bad-example
        :force:

        @features: "value-list multi-line code"
        @features: "float"   # ERROR! Duplicate @features definition.


Features
========

.. list-table::
    :header-rows: 1
    :width: 100%
    :widths: 25, 75

    *   -   Feature
        -   Coverage
    *   -   :text-code:`core`
        -   ``@version`` and ``@features`` are part of the core language
    *   -   :text-code:`include`
        -   ``@include`` is a standard feature.
    *   -   :text-code:`signature`
        -   ``@signature`` is an advanced feature.


Errors
======

.. list-table::
    :header-rows: 1
    :width: 100%
    :widths: 25, 75

    *   -   Error Code
        -   Causes
    *   -
        -   All errors from names, text, integer and boolean
    *   -   :text-code:`Syntax`
        -   |   If a meta value or command is at the wrong place.
            |   If a meta value has the wrong type of value.
            |   If ``@version`` or ``@features`` is defined more than once.
    *   -   :text-code:`Unsupported`
        -   Raised if the parser does not support a meta value or command.

