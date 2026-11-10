..
    Copyright (c) 2025 Tobias Erbsland - Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

.. include:: _icons.rst

***********
Constraints
***********

Constraints are the **primary mechanism** used by node-rules definitions to validate
the contents of a parsed configuration document. They express concrete requirements
such as value ranges, allowed formats, uniqueness, or relationships between nodes.

The meaning and applicability of a constraint depend on the declared ``type`` of the
node it constrains. Some constraints—such as ``minimum``—have different semantics
depending on whether they are applied to numbers, text, lists, or other structures.
Other constraints are only valid for specific node types.

This chapter documents all available constraints, explains their semantics, and
describes which node types they apply to. Each constraint page includes examples and
notes to help you choose the correct constraint for your use case.

.. button-ref:: common
    :ref-type: doc
    :color: success
    :align: center
    :expand:
    :class: sd-fs-5 sd-font-weight-bold sd-p-3

    Common Constraint Rules →

.. toctree::

    common
    minimum-maximum
    equals
    in
    multiple
    matches
    starts-ends-contains
    chars
    key
    version
    case-sensitive
