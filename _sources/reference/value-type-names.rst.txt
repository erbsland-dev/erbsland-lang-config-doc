..
    Copyright (c) 2025 Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

.. _ref-value-type-names:
.. index::
    !single: Names for Value Types

*********************
Names for Value Types
*********************

This section is **not** part of the language specification itself. Instead, it provides naming guidelines for developers implementing parsers. These type names are also used in the :ref:`test outcome format<test-outcome-format>`, which is relevant when writing or interpreting test results for configuration parsers.

By standardizing the terminology early, this guide helps parser implementers avoid additional effort with conversion tables when testing or debugging later on.

If you are only interested in how to write configuration files, you can safely skip this chapter.

Containers
==========

A **container** is any value that holds other values, either by index or by name.

.. list-table::
    :header-rows: 1
    :width: 100%

    *   - Name
        - Description
    *   - :text-code:`IntermediateSection`
        - An implicitly created section that fills in missing path elements in a name path.
    *   - :text-code:`SectionWithNames`
        - A section explicitly defined in the configuration file, containing named values or subsections.
    *   - :text-code:`SectionWithTexts`
        - A section that contains text-named values or subsections. This type is created implicitly when a text-named entry is added to an empty :text-code:`SectionWithNames` or :text-code:`IntermediateSection`.
    *   - :text-code:`SectionList`
        - A container that holds a list of sections—either :text-code:`SectionWithNames` or :text-code:`SectionWithTexts`—addressed by index.
    *   - :text-code:`ValueList`
        - A list of leaf values, each addressed by index, or a list of :text-code:`ValueList` values, when nested.
    *   - :text-code:`Document`
        - The document root. Like a :text-code:`SectionWithNames`, but implicitly defined for each document and not convertible into a :text-code:`SectionWithTexts`.

Values
======

A **value** is a leaf node in the value tree. It does not contain any child values.

.. list-table::
    :header-rows: 1
    :width: 100%

    *   - Name
        - Type
        - Description
    *   - :text-code:`Integer`
        - Integer values
        - All integer values, including decimal, hexadecimal, binary, and byte-count values.
    *   - :text-code:`Boolean`
        - Boolean values
        - Boolean literals such as :text-code:`true`, :text-code:`no`, :text-code:`enabled`, etc.
    *   - :text-code:`Float`
        - Floating-point values
        - Floating-point numbers, including special values like :text-code:`NaN` and :text-code:`Inf`.
    *   - :text-code:`Text`
        - Text values
        - All single-line and multiline text values, including code blocks.
    *   - :text-code:`Date`
        - Date values
        - Values that represent calendar dates.
    *   - :text-code:`Time`
        - Time values
        - Values that represent times, with or without timezone offsets.
    *   - :text-code:`DateTime`
        - Date-time values
        - Combined date and time values, with or without timezone offsets.
    *   - :text-code:`Bytes`
        - Byte-data values
        - Binary values, both single-line and multiline.
    *   - :text-code:`TimeDelta`
        - Time-delta values
        - Durations of time, including single values or merged time-delta lists.
    *   - :text-code:`RegEx`
        - Regular expression values
        - Single-line and multiline regular expressions.

