..
    Copyright (c) 2024 Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

.. _intro:
.. index::
    single: Introduction

============
Introduction
============

.. centered::
    Too much text? Have a look at the :ref:`language-overview`!

Configuration files play a vital role in setting up applications on servers and devices. With various formats available, each has its own strengths and weaknesses. The *Erbsland Configuration Language* (:term:`ELCL`) seeks to provide a balance between user-friendliness and flexibility. ELCL offers users the freedom to structure, annotate, and format their configurations in an intuitive way, while also maintaining the necessary depth for more advanced use cases.

ELCL is designed not only for everyday users but also with developers and implementors in mind. Its syntax is simple enough to support lightweight implementations, such as basic syntax highlighters or micro-parsers that can run on resource-constrained environments, like microcontrollers, with minimal overhead.

At the other end of the spectrum, ELCL supports more sophisticated implementations, with full-featured parsers capable of handling advanced value types such as regular expressions, code blocks, and time-deltas. It also supports features like nested documents, validation rules, and signatures.

While this introduction is focused on users of the configuration language, this documentation also provides a comprehensive specification for parser implementors. It covers the full range of ELCL features—from micro-parsers to complete parsers—offering detailed information on the validation rules language, API recommendations, and best practices. Additionally, guides and examples are provided to help developers implement parsers and utilize the accompanying test suite to ensure correct behavior.

.. toctree::
    :maxdepth: 2

    core-language
    standard-features
    advanced-features
