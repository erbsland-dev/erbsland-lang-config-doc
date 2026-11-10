..
    Copyright (c) 2025 Tobias Erbsland - Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

Addressing Values with an Index
===============================

While **indexes are not part of the ELCL syntax**, they play an essential role in parser APIs, error messages, diagnostics, and tooling. Indexes allow you to unambiguously reference individual elements in a list — whether it's a section list or a value list.

This chapter describes the syntax and meaning of **indexes in name paths** as part of the *parser specification*. Although these paths cannot be written in configuration files, understanding them is crucial for working with value trees and building parser implementations.

.. important::

    **Indexes are not part of the ELCL document syntax.** You cannot manually specify an index in a configuration file. Indexes only exist within the parser environment.

Adding an Index to a Section or Value List
------------------------------------------

An index is added using the syntax ``[<number>]`` — a decimal integer enclosed in square brackets (:cp:`[` and :cp:`]`). The index must appear **immediately after the list name**, with no name separator (:cp:`.`) in between.

This allows a name path to refer to a specific item in a section list or value list.

Example
~~~~~~~

In the following configuration, each ``place`` defines its own list of ``tree`` sections:

.. literalinclude:: /documents/reference/nested-section-lists.elcl
    :language: erbsland-conf

Here is the corresponding value tree with the path ``place[1].tree[0].fruit`` highlighted:

.. configuration-tree:: /documents/reference/nested-section-lists.elcl
    :highlight-path: place[1].tree[0].fruit

This path refers to:

* The **second** element in the ``place`` section list (``place[1]``, zero-based index).
* The **first** ``tree`` section within that place (``tree[0]``).
* The value of ``fruit`` inside that section.

This points to the string ``"apple"`` in the value tree.

.. tip::

    * Indexes **always start at zero**.
    * Indexes are not separated from the list name — write ``place[1]``, **not** ``place.[1]``.

Parser-Specific Behavior
------------------------

The index syntax described in this documentation is a **recommended convention**. Parser authors are encouraged to:

* Use this format when generating name paths for error reporting or diagnostics.
* Accept this format in API methods that resolve paths into specific values.

.. note::

    Always refer to the documentation of the specific parser you are using. Not all implementations may support indexed name paths, or they may use alternative formats or APIs to address list elements.

