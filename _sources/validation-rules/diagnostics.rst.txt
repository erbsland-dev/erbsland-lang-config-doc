..
    Copyright (c) 2025 Tobias Erbsland - Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

***********
Diagnostics
***********

.. note::

    This section is **informative**.

    Validators are expected to provide clear and useful diagnostics, but the
    exact format, structure, and delivery mechanism are implementation-specific.

Validation Rules are designed to reduce boilerplate code in applications.
This principle also applies to diagnostics: validators should emit **clear,
actionable error messages by default**, without requiring rule authors to define
custom error texts for every constraint.

While the ``_error`` suffix allows authors to override diagnostics for individual
constraints or node-rules, default messages should be sufficient in most cases.

Scope of Diagnostics
====================

Each diagnostic message should ideally answer the following questions:

* **What** is the problem?
* **Where** did it occur?
* **How** can it be fixed?

Where possible, validators *should* include:

* The :term:`name path` of the offending node.
* A document location (file name, line, column) if such information is available.
* A short hint describing the expected value, structure, or constraint.

Diagnostics should be concise, precise, and focused on helping users correct
their configuration quickly.

Rules for Diagnostics
=====================

#.  **Error Category:**
    All validation failures *must* be reported using the ``Validation`` error
    category.

#.  **Reporting Strategy:**

    * Validators *must* report at least the first validation error encountered.
    * Validators *may* continue validation and report additional errors if doing
      so does not significantly reduce clarity or performance.

    Implementations should balance completeness with usability; overwhelming
    users with cascading errors is discouraged.

Examples
========

Missing Type Match
------------------

The following rules require a text value:

.. code-block:: erbsland-conf
    :class: validation-rules

    [client.identifier]
    type: "text"

The configuration provides an integer instead:

.. code-block:: erbsland-conf
    :class: bad-example

    [client]
    identifier: 1

A validator might produce a diagnostic such as:

.. code-block:: text

    Validation: Expected a Text value, but got Integer.
        name-path: client.identifier
        location: configuration.elcl:2:1

Custom Error Override
---------------------

Here, a custom error message overrides the default diagnostic:

.. code-block:: erbsland-conf
    :class: validation-rules

    [server.port]
    type: "integer"
    minimum: 1024
    minimum_error: "System ports are not allowed"

.. code-block:: erbsland-conf
    :class: bad-example

    [server]
    port: 80

The resulting diagnostic could look like:

.. code-block:: text

    Validation: System ports are not allowed.
        name-path: server.port
        location: configuration.elcl:2:1
