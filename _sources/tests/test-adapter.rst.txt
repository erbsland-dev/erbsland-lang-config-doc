..
    Copyright (c) 2024 Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

.. _test-adapter:
.. index::
    single: Test Adapter

======================
Writing a Test Adapter
======================

To integrate your parser or syntax highlighter with the automated test system, you need to create a simple *test adapter*. A test adapter is a lightweight wrapper that accepts command-line arguments, parses a specified file, and outputs the parsing results. The test system runs this adapter like a standalone program, capturing its output from standard output.

Command Line Arguments
======================

Your test adapter must support the following command-line arguments:

.. code-block:: text

    test_adapter [--version <version>] <test file>

-   ``<test file>``: A required positional argument specifying the path to the test file. The test system provides absolute paths to test files, though it’s recommended that the adapter also accept relative paths based on the current working directory.
-   ``--version <version>``: An optional argument specifying the language version to test, formatted as ``1.0``. Although the test system always includes the language version, it’s advisable to default to the latest version when this argument is omitted.

Return Codes
============

The test adapter must conclude with one of the following return codes:

-   ``0``: Indicates successful parsing of the document.
-   ``1``: Indicates a parsing failure.
-   ``2+``: Used for any internal error within the test adapter.

The test system interprets return codes ``0`` and ``1`` as standard test results. Any other return code will cause the test system to halt immediately, outputting the adapter’s message as an error.

Output
======

Your test adapter must send the parsing results to *standard output* (not standard error). For further details on the output format, refer to :ref:`test-outcome-format`.

