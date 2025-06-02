..
    Copyright (c) 2024 Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

.. _ref-feature-identifier:
.. index::
    single: Feature Identifier

Feature Identifiers
===================

Feature identifiers are used by the ``@features`` meta-value (see :ref:`ref-meta-value`) to specify which features are enabled in a document. They can also be used programmatically to customize a parser, for example, to enable or disable specific features.

Feature Groups
--------------

Feature groups allow you to specify a predefined set of features in a compact way. Refer to :ref:`parser-tiers` for more details about the different parser tiers.

.. list-table::
    :header-rows: 1
    :width: 100%
    :widths: 25, 5, 70

    *   -   Identifier
        -   Tier
        -   Description
    *   -   :text-code:`core`
        -   —
        -   **Core Language:** All core language features.
    *   -   :text-code:`minimum`
        -   :text-code:`M`
        -   **Minimum Features:** Includes the minimum required features: float, byte-count.
    *   -   :text-code:`standard`
        -   :text-code:`S`
        -   **Standard Features:** Includes all minimum and standard features: float, byte-count, multi-line, section-list, value-list, text-names, date-time, code, byte-data, include.
    *   -   :text-code:`advanced`
        -   :text-code:`A`
        -   **Advanced Features:** Includes all minimum, standard, and advanced features: float, byte-count, multi-line, section-list, value-list, text-names, date-time, code, byte-data, include, regex, time-delta.
    *   -   :text-code:`all`
        -   —
        -   **All Features:** Includes all features supported by the current language version.


Individual Language Features
----------------------------

The table below lists the individual language features along with their corresponding tier:

.. list-table::
    :header-rows: 1
    :width: 100%
    :widths: 25, 5, 70

    *   -   Identifier
        -   Tier
        -   Description
    *   -   :text-code:`float`
        -   :text-code:`M`
        -   **Floating-Point Numbers:** Support for floating point numbers.
    *   -   :text-code:`byte-count`
        -   :text-code:`M`
        -   **Byte Counts:** Support for byte count suffixes in decimal integers.
    *   -   :text-code:`multi-line`
        -   :text-code:`S`
        -   **Multi-line Values:** Support for multi-line values.
    *   -   :text-code:`section-list`
        -   :text-code:`S`
        -   **Section Lists:** Support for section lists.
    *   -   :text-code:`value-list`
        -   :text-code:`S`
        -   **Value Lists:** Support for value lists.
    *   -   :text-code:`text-names`
        -   :text-code:`S`
        -   **Text Names:** Support for text names.
    *   -   :text-code:`date-time`
        -   :text-code:`S`
        -   **Date-Time Values:** Support for date, time, and date-time values.
    *   -   :text-code:`code`
        -   :text-code:`S`
        -   **Code Values:** Support for code text values.
    *   -   :text-code:`byte-data`
        -   :text-code:`S`
        -   **Byte-Data Values:** Support for hexadecimal-formatted byte-data.
    *   -   :text-code:`include`
        -   :text-code:`S`
        -   **Include Commands:** Support for the include meta command.
    *   -   :text-code:`regex`
        -   :text-code:`A`
        -   **Regular Expression Values:** Support for regular expressions.
    *   -   :text-code:`time-delta`
        -   :text-code:`A`
        -   **Time-Delta Values:** Support for time-delta values.

Parser Features
---------------

Parser features are not meant to be specified in a ``@features`` meta value. They exist to describe advanced capabilities of a parser.

.. list-table::
    :header-rows: 1
    :width: 100%
    :widths: 25, 75

    *   -   Identifier
        -   Description
    *   -   :text-code:`validation`
        -   **Validation Rules Support:** Provides support for validation rules.
    *   -   :text-code:`signature`
        -   **Signature Support:** Provides support for document signatures.


.. index::
    single: Data; Feature Identifier

Available Data
--------------

The ``data`` directory contains the file ``features.json``, which defines all error categories in a machine-readable format.


