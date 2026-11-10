..
    Copyright (c) 2025 Tobias Erbsland - Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

**********
Quickstart
**********

Before diving into all the details of Validation Rules (:term:`ELCL-VR`), let’s look at a
complete end-to-end example. This quickstart is meant to give you an intuitive feeling
for the overall structure of a validation rules document and the kinds of problems it
can detect early.

At this stage, you do not need to understand every keyword or rule. The goal is simply
to see how validation rules *read*, how they *relate to a configuration document*, and
what kind of guarantees they provide.

Validation Rules
================

The following validation rules describe a simple server configuration:

.. code-block:: erbsland-conf
    :class: validation-rules

    [server.name]
    type: "text"

    [server.bind_to]
    type: "text"
    default: "0.0.0.0"

    [server.port]
    type: "integer"
    minimum: 1
    maximum: 65535
    default: 8080

    [user.vr_any]
    type: "section"
    minimum: 1

    [user.vr_any.vr_name]
    maximum: 30

    [user.vr_any.name]
    type: "text"

    [user.vr_any.home_directory]
    type: "text"
    is_optional: yes

This rules document describes a fictional **server configuration** with two main
sections, ``server`` and ``user``:

*   ``server.name`` is a required text value.
*   ``server.bind_to`` and ``server.port`` are optional values and will use their
    defaults if omitted.
*   ``user`` can contain a variable number of subsections, but **at least one user
    entry must exist**.
*   Each ``user`` subsection must contain a ``name`` value.
*   The ``home_directory`` value is optional for each user.

The special name ``vr_any`` indicates that arbitrary user names are allowed, while
``vr_name`` constrains the *names themselves* (here: to a maximum length).

Valid Example
=============

The following configuration satisfies all validation rules:

.. code-block:: erbsland-conf
    :class: good-example

    [server]
    name: "example01"
    port: 9000

    [user.demo40]
    name: "Demo 40"
    home_directory: "/home/demo40"

Here, all required values are present, types match the rules, defaults are applied
where needed, and no undefined sections or values appear.

Invalid Example
===============

The next configuration violates several validation rules. The comments indicate the
problems that a validator would report:

.. code-block:: erbsland-conf
    :class: bad-example

    [server]
    # ERROR: missing required "name" value
    port: "https"         # ERROR: must be an integer

    [client]              # ERROR: section "client" is not defined
    name: "example"

    # ERROR: the required "user" section is missing

----

This quickstart only scratches the surface, but it already illustrates several key
principles of ELCL-VR:

* configurations are **closed by default**,
* required values are enforced automatically,
* type mismatches are detected early, and
* structural errors are reported precisely.

The following chapters introduce the individual building blocks in detail and explain
how to combine them to express more complex validation logic.
