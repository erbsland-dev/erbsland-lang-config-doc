..
    Copyright (c) 2025 Tobias Erbsland - Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

************
Introduction
************

Purpose
=======

Validation Rules (:term:`ELCL-VR`) reduce or eliminate the boilerplate code that would otherwise be required to check configuration correctness.
With validation in place, applications can access configuration values directly, confident that the document structure is enforced and the values have the expected type.

Scope
=====

The scope of a validation rules document is limited to a **single configuration document or a subtree of such a document**. ELCL-VR validates:

*   overall structure,
*   data types,
*   allowed value ranges and formats,
*   basic key uniqueness and key references.

Checks beyond these boundaries—such as verifying that a configured file path actually exists—are the responsibility of the application and not part of ELCL-VR.

For the background and rationale behind these rules, see :doc:`design-goals`.

Audience
========

This chapter is intended for both **implementers** and **users** of validation rules.

*   **Implementers** will find the required structure, identifiers, and constraints that a conforming validator must support. Summary tables at the end of this chapter provide a quick reference.
*   **Users** will find a practical introduction to the mini-language, with examples and recipes for creating validation rule documents. Since implementations may vary across parsers, implementers are encouraged to provide documentation of any deviations or extensions relative to this specification.
