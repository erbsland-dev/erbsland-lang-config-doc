..
    Copyright (c) 2025-2026 Tobias Erbsland - Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

.. index::
    single: Changelog
    single: Changes

*********
Changelog
*********

Version 1.3.1 — 2026-02-20
==========================

Significantly expanded and clarified multiple areas of the ELCL-VR specification.

*   Enhanced the documentation of ``vr_dependency``:

    *   Added the previously missing ``or`` and ``and`` modes.
    *   Introduced a formal explanation of dependency evaluation logic, including a normative mode matrix.
    *   Clarified ambiguous and misleading wording to ensure precise, implementation-independent semantics.

*   Clarified the optionality semantics of Section Lists, showing its similarity to value lists to address
    common misunderstandings.

*   Formalized rules for ``type`` identifiers:

    *   Defined case-insensitivity and normalization behavior in the validation rules chapter
        (previously only described informally in the overview).
    *   Added explicit rules regarding type aliases.

*   Extended the documentation of ``vr_key``:

    *   Added rules covering alternatives, optionality, and version constraints in composite key paths.
    *   Removed redundant and overlapping phrasing from existing rules to improve consistency and precision.

Version 1.3.0 — 2026-02-12
==========================

Extended the semantics of ``vr_key`` by introducing the optional
``case_sensitive`` field, allowing indexes to be explicitly marked as
case-sensitive.

The behavior of the ``key`` constraint now depends on the case-sensitivity
of the referenced index. Uniqueness checks and key comparisons follow the
index's defined comparison mode.

.. note::

    The previous specification was ambiguous regarding case-sensitivity in
    ``vr_key`` entries. Although key comparisons were described as
    case-insensitive by default, it was not clearly specified:

    * whether index uniqueness checks were case-sensitive, and
    * whether ``key`` constraint comparisons depended on index behavior.

    This version clarifies and formalizes these rules to ensure
    deterministic and consistent comparison semantics.

Version 1.2.10 — 2026-02-11
===========================

Extended and clarified the validation rules documentation, with a focus on edge cases and key semantics.

*   Significantly expanded the documentation for ``vr_any`` with additional rules, clearer scoping semantics,
    and more comprehensive examples.
*   Expanded and clarified the rules for ``vr_entry``, especially regarding optionality and default values.
*   Refined the documentation for indexes, keys, and references,
    defining precise behavior for edge cases such as versioned schemas, optional nodes, and alternatives in key paths.
*   Corrected key path examples to consistently include ``vr_entry`` where required,
    and explicitly documented that ``vr_entry`` is a mandatory part of section list key paths.

    .. note::

        Key paths are now documented in their canonical form including ``vr_entry``.
        For compatibility, paths that omit ``vr_entry`` may be treated as shorthand.

Version 1.2.4 — 2026-02-05
==========================

Added a “custom errors” chapter and refined validation rules documentation

*   Introduced a new "Custom Errors" chapter detailing the use and rules of defining error messages for user-friendly feedback.
*   Standardized headings and improved consistency in the validation rules documentation.
*   Fixed typos, formatting issues, and refined terminology (e.g., "name-path" to "name path").
*   Updated references to align with the latest structure and naming conventions.

Version 1.2.0 — 2026-01-22
==========================

Added a new chapter :doc:`validation-rules/index` defining **ELCL Validation Rules (ELCL-VR)**:

*   Introduces a standardized mini-language for declarative configuration validation.
*   Covers document structure, node rules, types, constraints, templates, dependencies,
    versioning, diagnostics, and security considerations.
*   Enables portable, implementation-independent validation of ELCL configuration documents.

Version 1.0.10 — 2025-09-01
===========================

* Added a page with a list of all known parser implementations.
* Explained how to add your own parser to the list.
* Improved the contribution guide with buttons to create issues and start discussions.

Version 1.0.8 — 2025-08-22
==========================

* Added the colon to the list of escaped characters in the "Test Outcome Format" chapter. This character had been accidentally omitted.
* Added a design rationale box to explain the reasoning behind the escaping rules.

Version 1.0.6 — 2025-08-14
==========================

* Added examples of invalid floating-point values for clarity.
* Included `+inf` and `+nan` as recognized values for completeness.
* Clarified that digit separators do not count toward digit limits.
* Broadened the rule to better deny any non-decimal formats for floating-point values.
* Refined explanation of behavior when limits are exceeded, removing potentially misleading rounding example in the context of floating-point numbers.

Version 1.0.4 — 2025-07-10
==========================

- Clarified the relationship between `Syntax` and its specialized subcategories (`Character`, `UnexpectedEnd`, `Indentation`, `LimitExceeded`, `Unsupported`).
- Reworded and expanded descriptions to improve readability and precision for parser implementors.
- Added design rationales to explain the purpose and intent behind each specialized category.
- Explicitly stated that distinguishing specialized errors is optional for parser conformance.

Version 1.0.0 — 2025-07-09
==========================

- Initial release
