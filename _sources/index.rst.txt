..
    Copyright (c) 2024 Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

Erbsland Configuration Language
===============================

The Erbsland Configuration Language (:term:`ELCL`) is a human-centric configuration format designed with a focus on clarity and ease of use. :term:`ELCL` simplifies software configuration, making it intuitive for both developers and end-users.

.. figure:: /images/intro-code-example.svg
    :width: 100%

Where to Start?
===============

* **Short on time?** Check out the :ref:`language-overview` for a quick introduction.
* **Looking for more details?** Read the comprehensive :ref:`introduction chapter<intro>` to get started.
* **Implementing a parser?** Find all details :ref:`the language reference chapter<reference>`.

Design Rationale and Key Features
=================================

:term:`ELCL` balances the flexibility required for human users to freely edit configuration documents and add comments, with the technical needs for strict and straightforward parsing. The language is designed to be familiar and easy to learn, enabling developers to quickly adopt it. Some of the main features include:

* **Simplicity**: :term:`ELCL` offers an intuitive syntax with built-in type safety, minimizing common configuration errors.
* **Safety**: The language supports strict and safe parsers, ensuring robust and secure configurations.
* **Comprehensive Documentation**: Detailed specifications, along with user and developer guides, make :term:`ELCL` easy to understand and implement.
* **Reference Implementations**: Available for Python and C++, these implementations help integrate :term:`ELCL` into your application or serve as examples for writing your own parser.
* **Compliance Test Suite**: An extensive test suite ensures that parsers conform to the :term:`ELCL` specification, fostering reliable and consistent implementations.
* **Implementation Levels**: :term:`ELCL` supports various implementation levels, from lightweight micro-parsers for resource-constrained environments to full-featured parsers for complex use cases.
* **Metadata Support**: Metadata statements allow you to specify language versions and required features, ensuring backward compatibility and future-proofing.

Table of Contents
=================

.. toctree::
    :maxdepth: 3

    intro/index
    language-overview
    tests/index
    parser-tiers
    reference/index
    validation-rules/index
    glossary

Dictionaries
============

* :ref:`genindex`
* :ref:`search`