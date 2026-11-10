..
    Copyright (c) 2024-2025 Tobias Erbsland - Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

Erbsland Configuration Language
===============================

The Erbsland Configuration Language (:term:`ELCL`) is a human-centric configuration format designed with a focus on clarity and ease of use. :term:`ELCL` simplifies software configuration, making it intuitive for both developers and end-users.

.. figure:: /images/intro-code-example.svg
    :width: 100%

Where to Start?
===============

.. rubric:: Short on time?

.. button-ref:: language-overview
    :ref-type: doc
    :color: success
    :align: center
    :expand:
    :class: sd-fs-5 sd-font-weight-bold sd-p-3

    Check out the Language Overview for a quick introduction →

.. rubric:: Looking for more details?

.. button-ref:: intro/index
    :ref-type: doc
    :color: primary
    :align: center
    :expand:
    :class: sd-fs-5 sd-font-weight-bold sd-p-3

    Read the comprehensive Introduction to get started →

.. rubric:: Implementing a parser?

.. button-ref:: intro/index
    :ref-type: doc
    :color: info
    :align: center
    :expand:
    :class: sd-fs-5 sd-font-weight-bold sd-p-3

    Find all details in the Language Reference chapter →

Design Rationale and Key Features
=================================

:term:`ELCL` balances the flexibility required for human users to freely edit configuration documents and add comments, with the technical needs for strict and straightforward parsing. The language is designed to be familiar and easy to learn, enabling developers to quickly adopt it. Some of the main features include:

.. grid:: 2
    :margin: 4 4 0 0
    :gutter: 1

    .. grid-item-card:: :fas:`lightbulb;sd-text-success` Simplicity
        :link: language-overview
        :link-type: doc

        :term:`ELCL` offers an intuitive syntax with built-in type safety, minimizing common configuration errors.

    .. grid-item-card:: :fas:`shield-alt;sd-text-success` Safety
        :link: intro/index
        :link-type: doc

        The language supports strict and safe parsers, ensuring robust and secure configurations.

    .. grid-item-card:: :fas:`book;sd-text-success` Comprehensive Documentation
        :link: reference/index
        :link-type: doc

        Detailed specifications, along with user and developer guides, make :term:`ELCL` easy to understand and implement.

    .. grid-item-card:: :fas:`code;sd-text-success` Reference Implementations
        :link: parser-implementations
        :link-type: doc

        Available for Python and C++, these implementations help integrate :term:`ELCL` into your application or serve as examples for writing your own parser.

    .. grid-item-card:: :fas:`check-circle;sd-text-success` Compliance Test Suite
        :link: tests/index
        :link-type: doc

        An extensive test suite ensures that parsers conform to the :term:`ELCL` specification, fostering reliable and consistent implementations.

    .. grid-item-card:: :fas:`layer-group;sd-text-success` Implementation Levels
        :link: parser-tiers
        :link-type: doc

        :term:`ELCL` supports various implementation levels, from lightweight micro-parsers for resource-constrained environments to full-featured parsers for complex use cases.

    .. grid-item-card:: :fas:`tags;sd-text-success` Metadata Support
        :link: ref-meta-value
        :link-type: ref

        Metadata statements allow you to specify language versions and required features, ensuring backward compatibility and future-proofing.

    .. grid-item-card:: :fas:`check-square;sd-text-success` Validation Rules
        :link: validation-rules/index
        :link-type: doc

        A standardized mini-language for validating configuration documents, ensuring data integrity and adherence to application-specific constraints.


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
    parser-implementations
    contributing/index
    license
    changelog
    glossary

Dictionaries
============

* :ref:`genindex`
* :ref:`search`