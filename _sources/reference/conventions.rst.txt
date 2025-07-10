..
    Copyright (c) 2024-2025 Tobias Erbsland - Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

.. _conventions:
.. index::
    !single: Documentation Conventions
    single: Conventions

Documentation Conventions
=========================

The *language reference* begins by describing the fundamental document structure and progressively introduces more complex elements, ultimately covering the entire language grammar. Most chapters contain one or more grammar sections, presented in *EBNF* (Extended Backus-Naur Form) notation. These syntax definitions are typically followed by a "Rules" section, which provides a more detailed explanation of the syntax. Additionally, many chapters include special "Implementation" and "Error" sections, offering implementation recommendations and specifying the error codes associated with the rules.

Although we've aimed to present the language elements in a logical sequence, certain core concepts needed to be explained before other features could be introduced. As a result, while reading through this reference in the given order, you may encounter references to language features that are described later. Since this is a reference manual, you might need to navigate between chapters to fully understand specific features.


.. index::
    single: EBNF Notation
    single: Notation

The EBNF Notation
-----------------

The *EBNF* notation used in this documentation follows the conventions outlined in the W3C document `Extensible Markup Language <https://www.w3.org/TR/xml/#sec-notation>`_. This notation is designed for human readability and comprehension, rather than for direct use in automated parser generation.

Below is a summary of the grammar conventions described in the W3C document, along with how these conventions are applied in this documentation:

.. list-table::
    :header-rows: 1
    :width: 100%
    :widths: 30 70

    * - Symbol / Expression
      - Description
    * - :text-code:`symbol ::= expression`
      - Each rule in the grammar defines one symbol.
    * - :text-code:`SYMBOL`
      - Uppercase symbols represent characters or character sets.
    * - :text-code:`symbol`
      - Lowercase symbols represent language syntax.
    * - :text-code:`#xN`
      - Represents a character with the Unicode code point N. N is a hexadecimal integer, and zero padding is allowed.
    * - :text-code:`[a-zA-Z], [#xN-#xN]`
      - Matches any character with a value in the specified range(s) (inclusive).
    * - :text-code:`[abc], [#xN#xN#xN]`
      - Matches any character from the listed values. Enumerations and ranges can be mixed within a single set of brackets.
    * - :text-code:`[^a-z], [^#xN-#xN]`
      - Matches any character with a value outside the specified range.
    * - :text-code:`[^abc], [^#xN#xN#xN]`
      - Matches any character not in the specified set. Enumerations and ranges can be mixed within a single set of brackets.
    * - :text-code:`"string"`
      - Matches a literal string enclosed in double quotes.
    * - :text-code:`'string'`
      - Matches a literal string enclosed in single quotes.
    * - :text-code:`(expression)`
      - The expression is treated as a unit.
    * - :text-code:`A?`
      - Matches A or nothing; A is optional.
    * - :text-code:`A B`
      - Matches A followed by B. This has higher precedence than alternation; thus, :text-code:`A B | C D` is equivalent to :text-code:`(A B) | (C D)`.
    * - :text-code:`A | B`
      - Matches A or B.
    * - :text-code:`A - B`
      - Matches any string that matches A but not B.
    * - :text-code:`A+`
      - Matches one or more occurrences of A. Repetition has higher precedence than alternation; thus, :text-code:`A+ | B+` is equivalent to :text-code:`(A+) | (B+)`.
    * - :text-code:`A*`
      - Matches zero or more occurrences of A. Repetition has higher precedence than alternation; thus, :text-code:`A* | B*` is equivalent to :text-code:`(A*) | (B*)`.
    * - :text-code:`/* ... */`
      - Comment notation.


.. index::
    single: Rules

The Rules
---------

The *rules* outlined in each section take **precedence** over the *EBNF* notation. For example, while *EBNF* notation may describe names with no length restrictions, a specific rule limits names to a maximum of 100 characters. Similarly, there is a rule that limits the length of a line to 4000 bytes, which cannot be expressed through *EBNF* syntax alone.

The rules provided in the reference documentation apply universally across the language. We have made every effort to place each rule in the chapter where it is most relevant, minimizing redundancy and avoiding conflicts between rules.


.. index::
    single: Configuration Examples

The Configuration Examples
--------------------------

We have included numerous configuration examples throughout this documentation, recognizing their importance in illustrating key concepts and rules. Valid examples, such as the one below, are presented without additional labeling:

.. code-block:: erbsland-conf

    [main]
    user: "example"
    
    [server]
    threads: 4
    startup delay: 20 s
    
    *[server.connection]
    port: 8080
    interface: "web"

When we showcase invalid syntax, it is always clearly marked with the text ``ERROR`` and often accompanied by a brief explanation. Where applicable, the location of the error is highlighted with a red frame for clarity.

.. code-block:: erbsland-conf
    :class: bad-example
    :force:
    
    [.server]  # ERROR! Configuration must not start with a relative section.
    welcome: "OK"

These examples are typically concise and abstract, allowing you to focus on the specific topic being discussed without unnecessary complexity.


Visualization of Invisible Characters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In instances where we need to visualize invisible characters, we use specific symbols for clarity: ``⎵`` represents a space, ``→`` represents a tab, and ``↵`` indicates a newline character in the results.

.. code-block:: text

    [main]
    text: """
    ⎵⎵⎵⎵One
    ⎵⎵⎵⎵Two
    ⎵⎵⎵⎵"""


.. index::
    single: Value Tree

Visualizations of Value Trees
-----------------------------

To help you understand how configuration files are transformed into their internal representation, the *value tree*, we provide visualizations like the one shown below:

.. configuration-tree:: /documents/reference/name-paths.elcl

The tree structure on the left illustrates the hierarchy of values, showing their names or indexes. Sections and section lists are represented with square brackets and asterisks, matching the original syntax from the configuration files.

On the right, you will see assignment arrows (``<==``), followed by the type and content of each value where applicable. The type is identified by our recommended type names, and the content is enclosed in parentheses. These visualizations are generated dynamically by the documentation system. While the structure of the value tree is accurate, the actual content of the values is for demonstration purposes only and should not be treated as a reference.


Covered Features
----------------

This reference documentation covers all language features, whether they belong to the core language, standard features, or advanced features for full-featured parsers. We chose not to separate these features into different sections to avoid complicating the documentation and to keep it easy to read.

Where appropriate, a section called "Features" details the language features covered in this chapter.

To determine which elements belong to each feature set, refer to the chapters on :ref:`parser-tiers` and also to :ref:`intro-core` for a rough classification. Whenever possible, we have labeled symbols in the EBNF grammar to indicate the feature set they belong to (e.g., ``text-name``).

