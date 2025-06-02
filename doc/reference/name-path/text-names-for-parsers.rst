..
    Copyright (c) 2024 Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

Parser-Specific Usage of Text Names
===================================

In configuration files, text names always appear as the **final component** in a name path. However, parsers are not bound by this restriction. When traversing or addressing a parsed value tree, a text name may appear in **any position** of a name path — including intermediate positions.

For example, the following name path addresses the ``isbn`` field of a specific book entry:

.. code-block:: text

    book."The Practice of System and Network Administration".isbn

.. note::

    This section documents **parser conventions**, not ELCL language syntax. Although not part of the configuration language itself, these conventions matter for users because name paths often appear in **error messages**, **debug output**, or **API references**.

Escaping Special Characters in Text Names
-----------------------------------------

When parsers handle name paths that include text names, they must apply precise escaping and unescaping rules. These rules follow the same encoding model as single-line string values (see :ref:`ref-text`) and ensure that name paths remain unambiguous across various contexts such as error messages, API calls, or test diagnostics.

Parsing Text Names in Name Paths
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When reading a name path, a parser must resolve all escape sequences into their corresponding Unicode code points. The double quotes surrounding a text name must be preserved during parsing to distinguish it from a regular identifier — for example, ``"text"`` and ``text`` are interpreted as distinct names.

Rendering Text Names in Name Paths
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When rendering name paths for diagnostic or programmatic output, parsers should follow a consistent escaping strategy:

* Escape all control characters and all characters in the multi-byte Unicode range:

  - :text-code:`U+0000` – :text-code:`U+001F`
  - :text-code:`U+007F` – :text-code:`U+1FFFFF`

* Always escape the following characters:

  - Backslash (:cp:`5c`)
  - Double quote (:cp:`"`)
  - Period (:cp:`.`)
  - Colon (:cp:`:`)
  - Equal sign (:cp:`=`)

* Use the ``\u{...}`` format for **all** escape sequences — even for the regular character, new-lines, carriage-returns, and tabs.

The purpose of this strategy is to make name paths easy to parse programmatically. For instance:

* By escaping periods, tools can split name paths on unescaped periods without ambiguity.
* By escaping colons and equals signs, lines like ``main."text\u{3a}": 123`` can be split reliably at separators.

.. design-rationale::

    In contrast to parsing, which affects how users write configuration files, rendering is only used for internal tooling: error messages, logs, diagnostics, or API output. By applying a rigorous escaping scheme, rendered name paths remain predictable and safe for downstream tools.

.. tip::

    If a text name contains several characters that require escaping, the resulting name path can become hard to read. In these cases, consider using the **short-form notation** described in the next section for improved clarity.

Short Form: Index-Based Access to Text Names
--------------------------------------------

Parsers may support a **short-form representation** of text-named entries to simplify name paths in internal contexts such as logs, diagnostics, or programmatic APIs.

Instead of including the full text name, a parser may use a numeric index enclosed in square brackets, prefixed by an empty quoted string (``""``). This index refers to the position of the entry in the corresponding section (order of definition).

For example, both of the following name paths refer to the same value:

.. code-block:: text

    book."The Practice of System and Network Administration".isbn
    book.""[1].isbn

.. configuration-tree:: /documents/reference/name-path-section-with-text-name.elcl
    :highlight-path: book."The Practice of System and Network Administration".isbn

.. note::

    The empty quoted string (``""``) serves as a **placeholder**, indicating that the following index applies to a text-named entry.
    Since empty text names are invalid in ELCL, this notation provides a clean and unambiguous way to separate the short-form from literal text-names.

Implementation Guidance
------------------------

Parsers are encouraged to:

* Use the index form **when it improves readability or reduces complexity**, especially in diagnostics or developer tools.
* Support **both forms** — full-text and index-based — in API calls that resolve or return name paths.

