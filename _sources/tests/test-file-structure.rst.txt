..
    Copyright (c) 2025 Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

.. _test-file-structure:
.. index::
    single: Test File Structure

===================
Test File Structure
===================

All test files are organized in a dedicated GitHub repository: ``erbsland-lang-config-tests``. You can easily include this repository as a submodule in your project to integrate the tests.

.. button-link:: https://github.com/erbsland-dev/erbsland-lang-config-tests.git
    :color: primary
    :align: center

    GitHub Repository with the Test Files →

The ``tests`` directory contains file-based tests for the *Erbsland Configuration Language (ELCL)*. These tests ensure that your parser or syntax highlighter correctly implements the language. Each test is designed for readability and easy integration into your unit tests.

You do not need to build an entire testing framework from scratch. Instead, you only need to create a minimal test adapter for your parser. Our test system will execute all tests and verify your parser's output. For more information, see :ref:`test-adapter`.

.. design-rationale::

    The test file structure is deliberately simple and flexible. Test characteristics are embedded directly in filenames and paths, avoiding the need for external test libraries and ensuring broad compatibility. The clear directory and naming conventions also make test data handling straightforward and consistent.

    By using static, file-based tests instead of dynamic test case generators, this system promotes better platform compatibility. These tests can be run across different systems without requiring extensive setup or specialized tools.

Test Naming Convention
----------------------

.. code-block:: text

    0120-FAIL-dec_underscore.elcl

Each test file follows a specific naming convention: ``NNNN-<outcome>-<label>.<suffix>``. The filename is divided into three primary parts, separated by hyphens (:cp:`-`): sequence number, outcome, and label.

Sequence Number
~~~~~~~~~~~~~~~

A unique identifier from 1 to 9999, used exclusively for sorting and organizing tests. This sequence number has no functional impact on test behavior.

Outcome
~~~~~~~

A keyword indicating the expected test result, with the following possible outcomes:

- ``PASS``: The test should parse successfully without errors.
- ``READ``: The test may parse successfully or may trigger an error, depending on the parser's handling of ambiguous cases.
- ``FAIL``: The test should fail with a parsing error.

The ``READ`` outcome applies in cases where the parser may either accept the file or produce an error, allowing both strict and lenient parsing behaviors. These tests ensure that the parser can handle the input without causing unintended side effects or crashes.

For ``FAIL`` tests, the parser is expected to fail with one of the error codes specified in the *outcome file* (see below).

Label
~~~~~

A brief description of the test’s purpose. The label should answer the question, "What does this test check?" For example, "This test checks if the parser succeeds/fails when it encounters...".

Suffix
~~~~~~

Each test comprises two files with the same name but different suffixes:

* An ``*.elcl`` file containing the *ELCL* document to be parsed.
* An ``*.out`` file detailing the expected *test outcome*.

Outcome Files
-------------

Each test includes a corresponding outcome file with the ``out`` suffix. This file is UTF-8 encoded, with each line separated by a newline or carriage return and newline, depending on the system. For failed tests, the outcome file specifies the expected error code(s). For passed tests, it contains the parsed data derived from the test file.

The format for outcome files is detailed in :ref:`test-outcome-format`.

Passed Tests
~~~~~~~~~~~~

For ``PASS`` and ``READ`` tests, the outcome file provides the parsed result of the document in the following format:

.. code-block:: text

    @version = String("1.0")
    main.connection[0].filter = String("test\u{12fe}")
    main.connection[0].flag = Boolean(true)
    main.connection[1].filter = String("test\u{12fe}")
    main.connection[1].flag = Boolean(false)
    main.server = Integer(-473945)
    translation."text" = Float(12.9)

This output format standardizes the parsed data structure, ensuring consistent validation across tests.

Failed Tests
~~~~~~~~~~~~

For ``FAIL`` tests, the outcome file follows this structure:

.. code-block:: text

    FAIL = NameConflict

The identifier ``FAIL`` is followed by zero, one, or more error codes, separated by vertical bars (:cp:`|`). If no specific error code is listed, any error will satisfy the test. If one or more error codes are specified, the parser must fail with one of the listed errors.

Directory Structure
-------------------

.. code-block:: text

    tests/V1_0/core/27_integer/...

The first level of subdirectories corresponds to the language version, using the format ``V1_0`` where the major and minor version numbers are separated by an underscore.

Within each version directory, tests are further organized by language feature, with each feature assigned its own subdirectory. These feature directories are named based on unique feature identifiers, as explained in :ref:`ref-feature-identifier`.

Within each feature directory, additional subdirectories use the format ``NN_<name>`` to group tests. The ``NN`` prefix is a two-digit sequence number that indicates both the order and origin of the tests:

- ``01``–``19``: Generated tests, created from templates and scripts.
- ``20``–``29``: Manually crafted tests, typically a set of passing ones and a list of tests targeting specific scenarios, or testing the logic of the parser.
- ``30``–``39``: Tests derived from documentation examples, in order to make sure the documentation is accurate.

Generated Tests
~~~~~~~~~~~~~~~

Directories with generated tests (``01``–``19``) can be removed and recreated as needed using predefined templates. Since these tests are automatically constructed, manual modifications should be avoided, as they get overwritten.

Human-Crafted Tests
~~~~~~~~~~~~~~~~~~~

Tests in the ``20``–``29`` range are manually written by developers to address specific scenarios or edge cases that generated tests may not cover. These tests provide coverage for real-world parsing situations and are particularly useful for validating language logic, such as handling name conflicts and other nuanced conditions.

These human-created tests are loosely numbered in increments (e.g., by five or ten) to allow additional cases to be added as needed. If parser issues are identified that aren't addressed by existing tests, new tests should be added in this section to cover those cases.

Tests from Documentation Examples
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The test suite also includes tests derived from example listings in the documentation (``30``–``39``), which help verify the accuracy of documented examples. Currently, these tests are curated manually to ensure they reflect valid or invalid cases as described.

In the future, the goal is to annotate example listings within the documentation to allow for automatic extraction into the test suite, further streamlining the process and enhancing the reliability of documentation.

