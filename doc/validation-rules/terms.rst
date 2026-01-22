..
    Copyright (c) 2025 Tobias Erbsland - Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

*****
Terms
*****

This page defines the terminology used throughout the Validation Rules
specification (:term:`ELCL-VR`). The terms introduced here are used consistently
in all following chapters and are essential for understanding both the rules
themselves and the requirements placed on validators.

Vocabulary
==========

Validation Rules use the following core terms:

* :term:`Node` — a single location in the value tree that may be validated.
  A node can represent a value, a section, or a list.
* :term:`Node-Rules` — the complete set of constraints and metadata that apply
  to a specific node.
* :term:`Name Path` — the normalized path that uniquely identifies a node
  within the value tree.
* :term:`Section` — a structured node containing named child entries, usually
  with regular names unless noted otherwise.
* :term:`Section List` — a node containing multiple sections that all share the
  same name.
* :term:`Value List` — a node containing an ordered sequence of scalar values.
* :term:`Reserved Name` — a predefined identifier in a validation rules document
  with special meaning, always starting with the prefix ``vr_``.

Examples
========

Throughout this specification, examples are rendered using visually distinct box
styles. These styles help you immediately understand *what kind of document you
are looking at* and *how it relates to the validation rules*.

The following examples demonstrate all box styles used in this chapter.

Validation Rule Documents
-------------------------

Validation rule documents define constraints and checks that are applied to
configuration files.

.. code-block:: erbsland-conf
    :class: validation-rules

    # This is a valid validation rules document.
    # It follows the rules defined in this specification.

.. code-block:: erbsland-conf
    :class: bad-validation-rules

    # This validation rules document does not conform
    # to the requirements of this specification.

Configuration Examples
----------------------

Configuration examples show how real-world configuration documents behave when
they are validated against a set of rules.

.. code-block:: erbsland-conf
    :class: good-example

    # This configuration document conforms to
    # the associated validation rules.

.. code-block:: erbsland-conf
    :class: bad-example

    # This configuration document violates
    # one or more validation rules.

Identifier Normalization
========================

Identifiers given as text in Validation Rules are **case-insensitive** and follow
the same normalization rules as :term:`names<Name>` in :term:`ELCL`.
For comparison purposes, underscores (``_``) and spaces are treated as equivalent.

For simplicity and consistency, all examples in this specification use normalized
identifiers. In real-world documents, however, it can be helpful to take advantage
of normalization for readability, for example by writing ``VR any`` instead of
``vr_any``.

See :ref:`ref-name-normalization` for a detailed description of name normalization
rules.

Reserved Names
==============

All reserved names begin with the prefix ``vr_``.
They have predefined semantics in Validation Rules and must not be redefined or
used for regular configuration entries.

See :doc:`reserved` for the complete list of reserved names and their meanings.

Conformance Language
====================

This specification uses simple and consistent language to express normative
requirements:

* The word *must* indicates an absolute requirement for conformance.
* The word *should* indicates a recommended feature that is optional but
  strongly encouraged.
* The word *may* indicates an optional feature.

If an element is described as *must* be present or supported, a parser that omits
it does **not** conform to this specification. Elements described with *should*
are optional but recommended, while *may* marks features that can be freely
omitted without breaking conformance.
