..
    Copyright (c) 2024 Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

.. _ref-comment:
.. index::
    single: Comment

Comments
========

In :term:`ELCL`, comments are used to annotate the configuration without affecting the document's structure or content.

.. code-block:: bnf

    comment             ::= HASH TEXT*
    end_of_line         ::= spacing comment? line_break

.. code-block:: erbsland-conf
    :class: good-example

    # A comment in the first line.
    [main]       # A comment after an element.
    value:       # Unicode → but no control characters
        "text"   # Comment

.. index::
    pair: Rules; Comment

Rules
-----

#.  **Start:** A comment begins with the hash character (:cp:`#`).

    .. code-block:: erbsland-conf
        :class: good-example

        # Comment

#.  **No Control Codes:** A comment may contain any characters, except for control characters, with the exception of the :term:`tab` character (:cp:`09`).

    .. code-block:: erbsland-conf
        :class: good-example

        # → Most Unicode is allowed 👍 ← 

#.  **End:** A line break terminates the comment.

    .. code-block:: erbsland-conf
        :class: good-example

        #           end of comment →
        [no_comment_anymore]


Implementation Recommendations
------------------------------

#. Parsers should completely ignore comments during parsing.
#. Comments must not influence the document’s content or structure in any way.

Features
--------

.. list-table::
    :header-rows: 1
    :width: 100%
    :widths: 25, 75

    *   -   Feature
        -   Coverage
    *   -   :text-code:`core`
        -   The full syntax outlined in this chapter is part of the core language.

Errors
------

.. list-table::
    :header-rows: 1
    :width: 100%
    :widths: 25, 75

    *   -   Error Code
        -   Causes
    *   -   :text-code:`Character`
        -   Raised if a comment contains a control character.
