************
Design Goals
************

This page explains the rationale behind Validation Rules (:term:`ELCL-VR`).
It is **informative** and intended to provide context for the intended use cases,
design boundaries, and trade-offs made during development.

Goals
=====

Validation Rules were designed with the following goals in mind:

* **Minimize boilerplate code**
  Cover the most common validation tasks directly, so applications do not need
  to reimplement repetitive checks for structure, types, and basic constraints.

* **Integrate naturally with ELCL**
  Use the same syntax, naming rules, and overall style as :term:`ELCL`,
  so validation rules feel familiar and remain easy to read and write.

* **Enable basic versioning**
  Support forward- and backward-compatible configuration schemas,
  allowing validation rules to evolve alongside applications.

* **Be explicit and predictable**
  Favor explicit declarations over implicit behavior, following ELCL’s design philosophy.
  This makes validator implementations easier to write, test, and reason about.

* **Support composition**
  Allow applications composed of multiple modules to define independent
  validation rules for their own configuration subtrees, without global coupling.

* **Allow selective ignoring**
  Permit parts of a configuration to be excluded from validation
  when checks must be handled manually or by application-specific logic.

Non-Goals
=========

ELCL-VR deliberately does **not** attempt to:

* Embed or execute application logic within validation rules.
* Perform application-level checks, such as verifying that files exist
  or that network resources are reachable.
* Provide application-defined or dynamically extensible constraint languages.

These concerns are intentionally left to the application layer.

Guiding Principles
==================

The design of ELCL-VR follows a small set of guiding principles:

* **Keep validation declarative**
  Rules describe *what* is valid, not *how* validation is performed.

* **Prefer simplicity over completeness**
  Not every conceivable validation feature is included;
  the focus is on common, broadly useful constraints.

* **Support interoperability**
  The same validation rules should behave consistently across different
  parsers and platforms, even if their internal implementations differ.

Together, these principles aim to strike a balance between expressive power,
implementation simplicity, and long-term maintainability.
