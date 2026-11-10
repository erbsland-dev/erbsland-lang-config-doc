..
    Copyright (c) 2025 Tobias Erbsland - Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0


****************
Evaluation Order
****************

The evaluation order for Validation Rules (:term:`ELCL-VR`) ensures that all parsers
behave consistently and produce identical observable results.
While implementations *may* apply internal optimizations, the outcome of validation
*must* be equivalent to executing the steps in the order described here.

Scope
=====

This specification assumes that a parser first reads the Validation Rules document,
verifies its correctness, and converts it into an internal representation suitable
for validation.

During this preprocessing phase, templates are expanded and identifiers—including
reserved names—are normalized. This phase occurs *before* any configuration document
is validated and is therefore outside the scope of this specification. The internal
order of these preprocessing steps is not relevant.

The evaluation order defined below begins *after* a configuration document has been
successfully parsed into a :term:`Value Tree` and validation is explicitly requested
for the entire document or for a specific subtree.

Rules for the Evaluation Order
==============================

#.  **Validation Stages:**
    Each :term:`Value Tree` *must* be validated in the following stages:

    #.  **First traversal through all node-rules definitions:**

        * Determine the matching alternative for each node.
        * Validate all constraints, except ``key`` and ``vr_dependency`` (see later stages).
        * Assign default values for missing nodes where applicable.
        * Create or update indexes and validate uniqueness constraints.
        * Mark nodes as partially validated or exclude them from validation if
          ``NotValidated`` applies.

        .. important::

            For default values, only the ``type`` constraint is validated.
            No other constraints apply to default values.
            See :doc:`defaults-and-optionality` for details.

    #.  **Traversal of the validated document:**

        * Detect any nodes in the value tree that are not covered by validation rules
          and therefore must not exist.

    #.  **Second traversal through all node-rules definitions:**

        * Validate cross-references using the ``key`` constraint.
        * Validate dependencies declared via ``vr_dependency``.

#.  **Order of Constraints:**
    Constraints within a validation stage *must* be evaluated in the following order:

    #.  The ``type`` constraint is always evaluated first.
    #.  All remaining constraints are evaluated in the *order of definition*.
    #.  During the second traversal, ``key`` constraints are evaluated first.
    #.  Rules declared in ``vr_dependency`` are evaluated last.

    .. design-rationale::

        Validation stops as soon as a constraint fails, so the evaluation order does
        not affect the final validity of the document.
        However, it does influence error reporting.
        By defining constraints in a deliberate order, rule authors can control which
        validation errors are reported first.

#.  **Definition Order of Child Nodes:**
    Child nodes *must* be processed in the order of their definition within the
    configuration document.

    .. code-block:: erbsland-conf

        [server]                # 1.
        z_name: "example"       # 2.
        a_port: 9000            # 3.

        [client]                # 4.
        port: 8080              # 5.

    .. design-rationale::

        Since assignments are captured in definition order during parsing, validating
        them in the same order minimizes implementation complexity and guarantees a
        stable and predictable validation sequence.

#.  **Bottom-Up Structure Traversal:**
    The document structure *must* be traversed bottom up, completing validation of
    each branch before moving on to unrelated branches.

    This ensures that subsections—which may appear later in the document—are fully
    validated before sibling sections that are defined earlier.

    .. code-block:: erbsland-conf

        [server]                # 1.
        name: "example"         # 2.

        [client]                # 5.
        port: 8080              # 6.

        [server.bind]           # 3.
        interface: "0.0.0.0"    # 4.

    .. design-rationale::

        Bottom-up traversal guarantees consistent behavior regardless of declaration
        order and ensures that validation errors are detected as early and reliably
        as possible.

#.  **Order of Alternatives:**
    Alternatives *must* be evaluated in the order of their definition.
    This allows rule authors to deterministically control which alternative applies
    when multiple alternatives could match.

    The following example allows ``server.bind`` to be defined in three different
    ways: as a single text value, as a section with ``address`` and ``port``, or as
    a section list containing multiple entries.

    .. code-block:: erbsland-conf

        *[server.bind]*
        type: "text"
        default: "0.0.0.0:8080"

        *[server.bind]*
        type: "section"

        [.address]
        type: "text"

        [.port]
        type: "integer"
        default: 8080

        *[server.bind]*
        type: "section_list"

        [.vr_entry.address]
        type: "text"

        [.vr_entry.port]
        type: "integer"

    .. code-block:: erbsland-conf
        :class: good-example

        [server]
        bind: "127.0.0.1:9000"

    .. code-block:: erbsland-conf
        :class: good-example

        [server.bind]
        address: "127.0.0.1"
        port: 9000

    .. code-block:: erbsland-conf
        :class: good-example

        *[server.bind]*
        address: "10.50.0.1"
        port: 9000

        *[server.bind]*
        address: "10.62.0.1"
        port: 9000
