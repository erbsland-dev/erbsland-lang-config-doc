..
    Copyright (c) 2024-2025 Tobias Erbsland - Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

.. _ref-date-time-value:
.. index::
    single: Date
    single: Date-Time
    single: Time
    single: Date Value
    single: Date-Time Value
    single: Time Value

Date, Time, and Date-Time Values
================================

:term:`ELCL` supports date, time, and combined date-time values using a subset of the formats defined in the ISO 8601-1:2019 standard. These formats are based on the Gregorian calendar for dates and the 24-hour clock for times.

.. code-block:: bnf

    date_time           ::= date | [tT]? time time_offset? | date [ tT] time time_offset?

    date                ::= dp_year HYPHEN dp_month HYPHEN dp_day
    time                ::= tp_hour COLON tp_minute ( COLON tp_second ( PERIOD tp_fraction )? )?
    time_offset         ::= [zZ] | ( [-+] tp_hour ( COLON tp_minute )? )

    dp_year             ::= DIGIT DIGIT DIGIT DIGIT /* Valid 0001 - 9999 */
    dp_month            ::= DIGIT DIGIT  /* Valid 01 - 12 */
    dp_day              ::= DIGIT DIGIT  /* Valid 01 - 31 */
    tp_hour             ::= DIGIT DIGIT  /* Valid 00 - 59 */
    tp_minute           ::= DIGIT DIGIT  /* Valid 00 - 59 */
    tp_second           ::= DIGIT DIGIT  /* Valid 00 - 59 */
    tp_fraction         ::= DIGIT+       /* Up to 9 digits */

In the following examples, you can see valid representations of date, time, and date-time values:

.. code-block:: erbsland-conf
    :class: good-example

    [date_values]
    value a: 2024-11-30         # A date in <year>-<month>-<day> format.
    value b: 1412-01-14         # A historical date.

    [time_values]
    value a: 01:23              # A local time in <hour>:<minute> format.
    value b: 23:59:01           # A local time with seconds included.
    value c: 04:27:09.003       # A local time with fractions of seconds.
    value d: 01:23z             # UTC time, indicated by 'z'.
    value e: 22:45:15z          # UTC time with seconds.
    value f: 14:21:59.141Z      # UTC time with fractions of seconds.
    value g: 12:01+02           # Time with a timezone offset in hours.
    value h: 17:31-03:30        # Time with a timezone offset in hours and minutes.
    value i: t16:49:03z         # Optional 't' prefix for ISO compatibility.

    [date_time_values]          # Combined date and time values.
    value a: 2024-12-31 17:45
    value b: 2025-09-19 23:59:01
    value c: 2021-01-01 04:27:09.003
    value d: 2017-01-02t01:23z
    value e: 1912-12-21T22:45:15z


.. index::
    pair: Rules; Date

Date Rules
----------

#.  **Date Format:** A date consists of a sequence of year, month, and day, separated by hyphens (:cp:`-`).

    .. code-block:: erbsland-conf
        :class: good-example

        [schedule]
        publishing date: 1687-07-05

#.  **Year Format and Range:** The year must be a four-digit number within the range ``0001`` to ``9999``. The year zero is not allowed.

    .. code-block:: erbsland-conf
        :class: good-example

        [time machine settings]
        launch_date: 0001-01-01
        calibration_checkpoint: 1582-10-15
        destination_date: 9999-12-31

#.  **Month Format and Range:** The month must be represented as a two-digit number within the range ``01`` to ``12``.

    .. code-block:: erbsland-conf
        :class: good-example

        [start of the month]
        January: 2024-01-01
        February: 2024-02-01
        # ...
        November: 2024-11-01
        December: 2024-12-01

#.  **Day Format and Range:** The day must be represented as a two-digit number within the range ``01`` to ``31``.

    .. code-block:: erbsland-conf
        :class: good-example

        [dna]
        Crick Birthday    : 1916-06-08
        Watson Birthday   : 1928-04-06
        Discovery         : 1953-04-25
        Nobel Prize Award : 1962-12-10

#.  **Valid Dates:** Dates must be validated based on the rules of the Gregorian calendar. Invalid dates must be rejected. For historical dates, the Gregorian rules should be projected backward.

    .. code-block:: text

        Function isLeapYear(year)
            If year is divisible by 400:
                Return true   # Leap year
            Else if year is divisible by 100:
                Return false  # Not a leap year
            Else if year is divisible by 4:
                Return true   # Leap year
            Else:
                Return false  # Not a leap year
        End Function

#.  **Handling Unsupported Date Ranges:** If the system or programming language does not support the full range of dates specified, a custom data format must be used to handle the full range. This allows conversion into a native format while preserving the correct date.

    .. code-block:: cobol

        0      IDENTIFICATION DIVISION.
        1      PROGRAM-ID. DateExample.
        2
        3      DATA DIVISION.
        4      WORKING-STORAGE SECTION.
        5      01 CUSTOM-DATE.
        6          05 YEAR  PIC 9(4).
        7          05 MONTH PIC 99.
        8          05 DAY   PIC 99.


.. index::
    pair: Rules; Time

Time Rules
----------

#.  **Time Format:** A time consists of hours and minutes, optionally followed by seconds. Each component is separated by a colon (:cp:`:`).

    .. code-block:: erbsland-conf
        :class: good-example

        [times]
        breakfast: 07:00
        lunch: 12:31:14
        dinner: 19:42:17
        bed time: 23:17

#.  **Optional Prefix:** A time can be prefixed with the letter :cp:`t` (case-insensitive) for ISO compatibility.

    .. code-block:: erbsland-conf
        :class: good-example

        [iso]
        meeting: t07:00:01

#.  **Fractions of Seconds:** The seconds can optionally be followed by fractions of a second, separated by a period (:cp:`.`).

    .. code-block:: erbsland-conf
        :class: good-example

        [photon race]
        Earth : 13:00:00.000
        Moon  : 13:00:01.282220
        Mars  : 13:12:30.519214283

#.  **Time Offset:** A time (with or without seconds or fractions) can optionally be followed by a time offset.

    .. code-block:: erbsland-conf
        :class: good-example

        [Pauls Lunch Times]
        London       : 12:02z
        Helsinki     : 09:14:13+03:00
        New York     : 15:59:30-04:00
        Kathmandu    : 06:21:07.123+05:45
        Buenos Aires : 15:11-03

#.  **Hour Format and Range:** The hour must be represented by two digits and must be within the range of ``00`` to ``23``.

    .. code-block:: erbsland-conf
        :class: good-example

        [times]
        midnight                 : 00:00:00
        a second before midnight : 23:59:59

#.  **Minute and Second Format and Range:** Minutes and seconds must be represented by two digits each, and their values must be within the range of ``00`` to ``59``.

    .. code-block:: erbsland-conf
        :class: good-example

        [job interview]
        too early                : 13:59:59
        perfect                  : 14:00:00
        too late                 : 14:00:01

#.  **Second Fraction Format and Range:** Fractions of a second must be a sequence of one to nine digits. Trailing zeroes are allowed.

    .. code-block:: erbsland-conf
        :class: good-example

        [precision]
        precise       : 13:21:58.0             # Precise like setting your microwave timer
        more precise  : 13:21:58.004           # Precise like a hummingbird's wingbeat
        super precise : 13:21:58.004289        # Precise like an atomic clock
        ultra precise : 13:21:58.004289192     # Precise like a particle accelerator’s timing

#.  **Time Precision:** Time values must support a precision of nanoseconds.

    .. code-block:: erbsland-conf
        :class: good-example

        [precision]
        time shift : 12:18:00.000000001

#.  **Time Offset Format:** A time offset can be represented by the letter :cp:`z` (indicating UTC) or a plus (:cp:`+`) or minus (:cp:`-`) sign, followed by two digits for the hour. This can optionally be followed by a colon (:cp:`:`) and two digits for the minute offset.

    .. code-block:: erbsland-conf
        :class: good-example

        [time offsets]
        sunrise   : 06:23z
        dawn      : 20:14-06
        sunset    : 12:17+08:00

#.  **Time Offset Range:** A time offset must be within the range of ``-23:59`` to ``+23:59``.

    .. code-block:: erbsland-conf
        :class: good-example

        [time offsets]
        Minimum                   : 12:00-23:59     # Technical minimum
        Baker and Howland Islands : 12:00-12:00     # Largest negative offset at time of writing.
        Line Islands              : 12:00+14:00     # Largest positive offset at time of writing.
        Maximum                   : 12:00+23:59     # Technical maximum

#.  **Handling Unsupported Time Values:** If the underlying system or programming language/library does not support the full range of time values, including offsets and nanoseconds, the time must be handled in a custom data format that supports the full range. A conversion to a native format can then be made.


.. index::
    pair: Rules; Time

Date-Time Rules
---------------

#.  **Format:** A date-time value consists of a date followed by a time, separated by either a space (:cp:`20`) or the letter :cp:`t` (case-insensitive). All rules for dates and times apply.

    .. code-block:: erbsland-conf
        :class: good-example

        [date time values]
        Earliest       : 0001-01-01T00:00:00Z
        Latest         : 9999-12-31 23:59:59.999999999

#.  **Handling Unsupported Date-Times:** If the underlying system or programming language/library does not support the full range of date-time values, the values must be handled in a custom data format. This allows for proper conversion into the system’s native format.


Rules About Handling Times Without Offsets
------------------------------------------

#.  **No Offset Indicates Local Time:** If a time is specified without a UTC specifier (:cp:`z`) or an explicit offset, the parser must assume it represents *local time*.

    .. code-block:: erbsland-conf

        [Times]
        Local Time     : 10:44
        UTC            : 10:44z
        Somewhere Else : 10:44+04

#.  **Local Time Definition:** Local time is the time configured on the system at the moment the parser is reading the configuration.

    .. code-block:: erbsland-conf

        [Times]
        Nighttime      : 03:02

#.  **Systems Without Local Time Settings:** On systems that do not have local time settings (e.g., embedded devices), local time is always assumed to be UTC.

    .. code-block:: erbsland-conf

        [Embedded]
        Unspecified Time : 11:16  # Treated as UTC if local time is unavailable.


About Time Offsets, UTC, Time Zones, and Local Time
---------------------------------------------------

You might wonder why :term:`ELCL` supports local times in its configuration language. While it's true that UTC is the best standard for things like log files and data storage, local time can be useful in configuration files. For example, when defining office hours in a configuration, the times should be interpreted based on the location where the application is running. In cases where local time isn’t desired, and you need a clear, precise time point, the application can easily reject local times and require UTC.

You may also notice that :term:`ELCL` does not support time zones. This decision was made due to the complexity time zones introduce. If you're not familiar with the subject, it's important to understand that time zones and time offsets are not the same. Time offsets are simple—they represent a fixed difference from UTC and can easily be converted to UTC. Time zones, on the other hand, bring a host of complications, including seasonal changes like daylight saving time and historical shifts that vary by region and date.

While time zones are necessary for converting local times into UTC based on the rules of a specific region, we believe they are unsuitable for configuration files. If you need to specify an exact point in time, it's always better to convert the date-time with the time zone into UTC. UTC is stable and will never change, while time zones can shift due to political decisions or other factors. If you want to use local times in your configuration, you can do so safely—local times will automatically adapt to the time zone set on the system running the application.


Features
--------

.. list-table::
    :header-rows: 1
    :width: 100%
    :widths: 25, 75

    *   -   Feature
        -   Coverage
    *   -   :text-code:`date-time`
        -   Date, time and date-time values are a standard feature.


Errors
------

.. list-table::
    :header-rows: 1
    :width: 100%
    :widths: 25, 75

    *   -   Error Code
        -   Causes
    *   -   :text-code:`Syntax`
        -   |   Raised if separators are missing, duplicated or placed incorrectly.
            |   Raised if any date, time or time-offset part, is out of range.
            |   Raised if a date or time is not valid (therefore out of a valid range).

