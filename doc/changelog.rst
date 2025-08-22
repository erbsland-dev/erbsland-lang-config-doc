..
    Copyright (c) 2025 Tobias Erbsland - Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

.. index::
    single: Changelog
    single: Changes

*********
Changelog
*********

Version 1.0.8 - 2025-08-22
==========================

* Added the colon to the list of escaped characters in the "Test Outcome Format" chapter. This character had been accidentally omitted.
* Added a design rationale box to explain the reasoning behind the escaping rules.

Version 1.0.6 - 2025-08-14
==========================

* Added examples of invalid floating-point values for clarity.
* Included `+inf` and `+nan` as recognized values for completeness.
* Clarified that digit separators do not count toward digit limits.
* Broadened the rule to better deny any non-decimal formats for floating-point values.
* Refined explanation of behavior when limits are exceeded, removing potentially misleading rounding example in the context of floating-point numbers.

Version 1.0.4 - 2025-07-10
==========================

- Clarified the relationship between `Syntax` and its specialized subcategories (`Character`, `UnexpectedEnd`, `Indentation`, `LimitExceeded`, `Unsupported`).
- Reworded and expanded descriptions to improve readability and precision for parser implementors.
- Added design rationales to explain the purpose and intent behind each specialized category.
- Explicitly stated that distinguishing specialized errors is optional for parser conformance.

Version 1.0.0 - 2025-07-09
==========================

- Initial release
