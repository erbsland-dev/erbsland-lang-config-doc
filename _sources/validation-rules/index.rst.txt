..
    Copyright (c) 2025 Tobias Erbsland - Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

.. _ref-validation-rules:
.. index::
    single: Validation Rules

****************
Validation Rules
****************

Validation Rules (:term:`ELCL-VR`) are a standardized mini-language, defined as part of
:term:`ELCL`, that allow you to validate the structure and content of configuration
documents. They can be applied to an entire configuration file or to a specific
subtree within it.

A validation rules document is itself written in :term:`ELCL` form, using the same
syntax and naming conventions as regular configuration files. This keeps rules easy
to read, write, and maintain. In addition to file-based rules, some parsers may also
offer a programmatic API for defining and applying validation rules directly in code.

.. rubric:: Single Validation Rule

The following example defines a simple validation rule for a TCP port number:

.. code-block:: erbsland-conf
    :class: validation-rules

    [server.port]
    type: "integer"
    minimum: 1
    maximum: 65535
    default: 8080

.. rubric:: Matching Document

A configuration document that satisfies this rule could look like this:

.. code-block:: erbsland-conf
    :class: good-example

    [server]
    port: 9000

This chapter is intended for **both authors of validation rules and implementers of
validators**.

* As a **rule author**, you will learn how to express structural requirements,
  type constraints, defaults, and dependencies in a concise and declarative way.
* As an **implementer**, you will find precise, normative definitions that describe
  how validation rules must be interpreted and evaluated, along with guidance on
  error handling and diagnostics.

The chapter combines **normative sections**, which define required behavior for
conforming implementations, with **informative sections** that provide background,
design rationale, and practical examples.

.. button-ref:: intro
    :ref-type: doc
    :color: success
    :align: center
    :expand:
    :class: sd-fs-5 sd-font-weight-bold sd-p-3

    Introduction →


.. toctree::
    :caption: Contents of this Chapter
    :maxdepth: 2

    intro
    quickstart
    terms
    model
    evaluation-order
    node-rules
    types
    reserved
    templates
    alternatives
    defaults-and-optionality
    lists
    constraints/index
    variable-names
    keys-and-references
    dependencies
    custom-errors
    diagnostics
    security
    constraint-matrix
    design-goals
