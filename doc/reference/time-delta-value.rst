..
    Copyright (c) 2024 Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

.. _ref-time-delta-value:
.. index::
    single: Time-Delta
    single: Time-Delta Value

Time-Delta Values
=================

Time delta values represent a duration or difference in time and are considered an advanced feature in :term:`ELCL`. A time delta consists of a positive or negative decimal integer followed by a time unit. This feature is classified as advanced because it adds complexity to the parser, and time delta handling may vary between different programming languages.

.. code-block:: bnf

    time_delta          ::= integer_dec space? time_delta_suffix

    time_delta_suffix   ::= nanoseconds? | ns |
                            microseconds? | us | µs |
                            milliseconds? | ms |
                            seconds? | s |
                            minutes? | m |
                            hours? | h |
                            days? | d |
                            weeks? | w |
                            months? |
                            years?

The following examples demonstrate a few time-delta values in use:

.. code-block:: erbsland-conf
    :class: good-example

    [Time Deltas]
    Value A: +17 days
    Value B: 100ms, 7s, -2m, +4h
    Value C: -1 year
    Value D: 5µs


.. index::
    pair: Rules; Time-Delta

Rules for Time-Delta Values
---------------------------

#.  **Format:** A time delta value consists of a decimal integer (following all the rules for decimal integers), followed by an optional space, and then a time unit.

    .. code-block:: text

        <decimal integer> <optional space> <time unit>

#.  **Time Unit:** The time unit must be one of the valid units listed in :ref:`ref-time-unit`. All time units are case-insensitive, and for microseconds, both ``us`` and ``µs`` must be supported.

    .. code-block:: erbsland-conf
        :class: good-example

        [Time Deltas]
        Value A: 1s
        Value B: 1 S
        Value C: 1 Second
        Value D: 1 SECONDS

#.  **Handling Lists:** A parser *can* convert a list into a single time-delta object if supported by the backend. This allows combined time values like hours, minutes, and seconds to be treated as a single unit.

    .. code-block:: erbsland-conf
        :class: good-example

        [Time Deltas]
        Value: 100ms, 7s, -2m, +4h   # Can be combined into a single value.

#.  **Unit Support:** A parser *must* support the following units: seconds, minutes, hours, days, and weeks. A parser *can* optionally support nanoseconds, microseconds, milliseconds, months, and years. If a parser does not support a specific unit, it must still correctly parse the syntax and return an appropriate error.

    .. code-block:: erbsland-conf
        :class: good-example

        [Time Deltas]
        Value: 100 years    # Support for years is optional.


.. _ref-time-unit:

Time Units
----------

The following table lists the valid time units and their descriptions.

.. list-table::
    :header-rows: 1
    :width: 100%
    :widths: 15, 15, 10, 60

    *   -   Long Plural
        -   Long Singular
        -   Short
        -   Description
    *   -   :text-code:`nanoseconds`
        -   :text-code:`nanosecond`
        -   :text-code:`ns`
        -   Nanoseconds are equal to 0.000000001 seconds.
    *   -   :text-code:`microseconds`
        -   :text-code:`microsecond`
        -   :text-code:`us`, :text-code:`µs`
        -   Microseconds are equal to 0.000001 seconds.
    *   -   :text-code:`milliseconds`
        -   :text-code:`millisecond`
        -   :text-code:`ms`
        -   Milliseconds are equal to 0.001 seconds.
    *   -   :text-code:`seconds`
        -   :text-code:`second`
        -   :text-code:`s`
        -   The base unit of time in the SI system.
    *   -   :text-code:`minutes`
        -   :text-code:`minute`
        -   :text-code:`m`
        -   Minutes are equal to 60 seconds.
    *   -   :text-code:`hours`
        -   :text-code:`hour`
        -   :text-code:`h`
        -   Hours are equal to 60 minutes, or 3600 seconds.
    *   -   :text-code:`days`
        -   :text-code:`day`
        -   :text-code:`d`
        -   Days are equal to 24 hours.
    *   -   :text-code:`weeks`
        -   :text-code:`week`
        -   :text-code:`w`
        -   Weeks are equal to 7 days.
    *   -   :text-code:`months`
        -   :text-code:`month`
        -   (none)
        -   Months cannot be precisely converted to seconds.
    *   -   :text-code:`years`
        -   :text-code:`year`
        -   (none)
        -   Years cannot be precisely converted to seconds.


Features
--------

.. list-table::
    :header-rows: 1
    :width: 100%
    :widths: 25, 75

    *   -   Feature
        -   Coverage
    *   -   :text-code:`time-delta`
        -   Time-delta values are an advanced feature, allowing representation of durations using a variety of time units.

Errors
------

.. list-table::
    :header-rows: 1
    :width: 100%
    :widths: 25, 75

    *   -   Error Code
        -   Causes
    *   -
        -   All errors applicable to decimal integer values.
    *   -   :text-code:`LimitExceeded`
        -   Raised if the resulting time-delta value is too large to be stored or processed correctly.
    *   -   :text-code:`Unsupported`
        -   Raised if a time unit is not supported by the parser.

