..
    Copyright (c) 2025 Tobias Erbsland - Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

********
Security
********

.. note::

    This section is **informative**, except where explicitly stated as normative.

:term:`ELCL` is designed to be a safe and reliable configuration format.
The same principles apply to validation rules and validators: they must avoid
exposing sensitive information, defend against denial-of-service risks, and
enforce reasonable resource limits.

This page describes the ``is_secret`` flag for handling sensitive values and
provides guidance for implementers to avoid common security pitfalls.

Marking Secrets
===============

The ``is_secret`` flag identifies values that must be treated as sensitive.
It applies to all :term:`scalar values <scalar value>`.

Rules for Secrets
-----------------

#.  The ``is_secret`` flag *may* be set in the node-rules definition of any scalar value.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [database.password]
        type: "text"
        is_secret: yes

#.  When set to ``yes``, the parsed value is marked as *secret*.

#.  The *secret* mark *should* be exposed through the validator API so that
    applications can handle such values appropriately (e.g., masking them in
    logs or excluding them from diagnostics).

#.  Validators *must not* include secret values in error messages, warnings,
    or logs. Instead, they must replace the value with a neutral placeholder,
    such as ``***``.

    .. code-block:: none

        Validation: Invalid password format.
            name-path: database.password
            value: ***

.. design-rationale::

    Secrets such as passwords, tokens, or API keys frequently appear in
    configuration files and are often logged during debugging.
    Accidental disclosure through diagnostics is one of the most common sources
    of credential leakage.

    By marking values as secret at the validation level, applications and tools
    can consistently protect sensitive data without relying on ad-hoc safeguards.

ReDoS Considerations
====================

Regular expressions are powerful but potentially dangerous.
Poorly designed patterns may trigger *catastrophic backtracking*, leading to
regular-expression denial-of-service (ReDoS) attacks.

.. rubric:: Guidelines

* Prefer regular-expression engines with linear-time execution guarantees.
* Enforce a maximum input length for values evaluated by regex constraints.
* Apply execution timeouts or step limits when evaluating user-defined patterns.
* Consider using regex libraries with built-in ReDoS protection.

.. design-rationale::

    Validators may operate on untrusted input.
    A single pathological regular expression can block the entire validation
    process and potentially the hosting application.
    Defensive measures against ReDoS are therefore essential.

Resource Limits
===============

:term:`ELCL` is designed as a **human-readable configuration format**, not a
high-volume data exchange format.
Validators are not required to accept arbitrarily large or deeply nested documents.

.. rubric:: Recommendations

* Enforce a maximum document size (for example, a few megabytes).
* Impose limits on nesting depth, recursion, and total node count.
* Reject documents that exceed these limits with a clear validation error.

.. design-rationale::

    Resource limits are a simple and effective security measure.
    Without them, a malicious configuration could exhaust memory or CPU
    resources before meaningful validation begins.

Caveats with ``NotValidated``
=============================

The ``NotValidated`` type provides an escape hatch for values or subtrees that
cannot be expressed using standard validation rules.
While useful, it weakens the guarantees provided by the validation document.

.. rubric:: Guidelines

* Use ``NotValidated`` only as a last resort.
* Prefer explicit types and constraints whenever possible.
* Treat ``NotValidated`` nodes as *untrusted input*.
* Apply additional application-level validation where appropriate.
* Document clearly why ``NotValidated`` is required.

.. design-rationale::

    ELCL validation rules are intentionally strict and predictable.
    ``NotValidated`` exists to handle exceptional cases, but overuse undermines
    the value of validation itself.

    Careful, well-documented use preserves flexibility without sacrificing
    security, correctness, or maintainability.
