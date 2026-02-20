..
    Copyright (c) 2026 Tobias Erbsland - Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

*************
Custom Errors
*************

Validation rules allow you to define custom error messages at either the rule or
constraint level. This is useful when a technical constraint does not provide
meaningful feedback to the user, or when you want to consolidate several
low-level validation errors into a single, clear message.

Custom errors help you keep validation logic declarative while still presenting
user-friendly feedback.

.. code-block:: erbsland-conf
    :class: validation-rules

    [client.port]
    type: "integer"
    minimum: 1
    maximum: 65534
    error: "Please specify a valid port between 1 and 65534."

The basic definition of custom error messages is described in
:doc:`constraints/common` and :doc:`node-rules`. This page focuses on the specific
rules and behaviors that apply to custom errors.

.. design-rationale::

    Custom error messages are a powerful tool for improving user experience and
    simplifying error handling. In many cases, instead of catching and translating
    validation errors in application code, errors can be reported directly to the
    user in a clear and helpful way.

    While the parser tries to provide meaningful default error messages, these are
    not always sufficient. A common example is regular-expression-based constraints:
    they are precise, but difficult to understand for non-programmers and usually
    unsuitable for direct error output.

    In such cases, a well-written custom error message bridges the gap between strict
    validation and a good user experience.

Rules for Custom Error Messages
===============================

#.  **Priority:**
    When multiple custom error messages are defined, the most specific one takes
    precedence.

    This allows you to fine-tune messages for individual constraints while still
    providing a general fallback at the rule level.

    The priority order is:

    * Custom error messages defined at the **constraint level**
    * Custom error messages defined at the **node-rules level**
    * The built-in default error message

    .. code-block:: erbsland-conf
        :class: validation-rules

        [client.port]
        type: "integer"
        minimum: 1024
        maximum: 65534
        not_equal: 80
        not_equal_error: "Port 80 is reserved for internal HTTP traffic"
        error: "Please specify a valid port between 1024 and 65534"

#.  **Overriding Errors:**
    Custom error messages only override default errors that are caused by
    **constraint validation**.

    They do *not* affect validation errors caused by missing values or sections,
    or by invalid or mismatched types. Structural and type-related errors are
    always reported using their default messages.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [main.count]
        type: "integer"
        error: "Custom error message"  # Never used, because no constraints are defined

#.  **No Inheritance or Nesting:**
    Custom error messages apply only to the node in which they are defined.

    They are not inherited by child nodes and do not affect nested rules. This
    keeps validation behavior predictable and avoids unintended side effects in
    complex rule hierarchies.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [client]
        type: "section"
        maximum: 5
        error: "Only up to 5 clients are allowed."

        # This rule is not affected by the custom error message above
        [client.vr_any]
        type: "text"
        minimum: 3

#.  **Empty Messages:**
    Empty custom error messages are allowed, but they are ignored.

    They neither override default messages nor suppress validation errors.

    .. code-block:: erbsland-conf
        :class: validation-rules

        [main.count]
        type: "integer"
        error: ""  # Has no effect
