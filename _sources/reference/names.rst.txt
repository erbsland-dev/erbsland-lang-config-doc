..
    Copyright (c) 2024-2025 Tobias Erbsland - Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

.. _ref-name:
.. index::
    single: Name
    single: Value Name
    single: Meta Value Name

Names
=====

In the *Erbsland Configuration Language*, names are essential for identifying values, sections, and subsections within a configuration. There are two types of names used:

#.  **Regular names** (or simply *names*): These are primarily used throughout the configuration to define sections and values.
#.  **Text names**: These are reserved for special cases where a portion of text needs to be directly mapped to a configuration section or value.

.. index::
    !single: Name Definition

Name Definition
---------------

Names are defined by a sequence of alphanumeric characters, with optional spaces or underscores to separate words.

.. code-block:: bnf

    name                ::= ALPHA DIGIT_OR_ALPHA* name_part*
    name_part           ::= word_separator DIGIT_OR_ALPHA+
    word_separator      ::= SPACE | UNDERSCORE


.. index::
    pair: Rules; Name

Rules
-----

#.  **Characters:** Names can contain letters (:cp:`a-z`, :cp:`A-Z`), digits (:cp:`0-9`), spaces (:cp:`20`), and underscores (:cp:`_`).

    .. code-block:: text

        Valid names:            Name
                                multiple_words
                                Multiple Words
                                Name123
                                Value 200
                                X_Axis

#.  **Starting Character:** Names must always begin with a letter.

    .. code-block:: text
        :class: bad-example

        100days                 # ERROR! Starts with a digit.
        _example                # ERROR! Starts with an underscore.

#.  **Case-Insensitive:** Names are case-insensitive.

    .. code-block:: text

        Three identical names:  Example_Name
                                example_name
                                EXAMPLE_NAME
                                
#.  **Spaces and Underscores are Interchangeable:** A name can be written with spaces or underscores, and they are treated the same.

    .. code-block:: text

        Three identical names:  one_long_name
                                One Long Name
                                one_long NAME

#.  **No Consecutive Word Separators:** Names cannot contain consecutive underscores or multiple spaces in a row.

    .. code-block:: text
        :class: bad-example

        example__name           # ERROR! Multiple underscores aren't allowed.
        Example  Name           # ERROR! Multiple spaces aren't allowed.
        example _name           # ERROR! Mixing spaces and underscores makes no difference.

#.  **No Trailing Underscores:** Names must not end with an underscore.

    .. code-block:: text
        :class: bad-example

        example_                # ERROR! Must not end with an underscore.

#.  **Maximum Length:** Names must not exceed 100 :term:`characters<character>` in length.

    .. code-block:: text
        :class: bad-example

        abc(+200 chars)xyz      # ERROR! Exceeds the maximum length of 100 characters.

    .. micro-parser::

        The maximum length of a name is 30 characters.

.. _ref-name-normalization:
.. index::
    !single: Name Normalization
    single: Normalization
    pair: Normalization; Name

Name Normalization
------------------

When normalizing a name, the following two rules are applied:

#.  **Convert to Underscores:** Replace all spaces (:cp:`20`) with underscores (:cp:`_`).

    .. code-block:: text

        Name with Spaces                  => name_with_spaces

#.  **Convert to Lowercase:** Convert all uppercase letters (:cp:`A-Z`) to lowercase (:cp:`a-z`).

    .. code-block:: text

        EXAMPLE                           => example
        Multiple_Words                    => multiple_words


.. _ref-name-comparison:
.. index::
    !single: Name Comparison
    pair: Comparison; Name

Name Comparison
---------------

Name comparison is crucial for identifying sections and values using :ref:`name paths<ref-name-path>` and for detecting :ref:`name conflicts<ref-name-conflict>`. The following rules apply when comparing names:

#.  **Normalize Regular Names for Comparison:** Regular names must be compared using their normalized form. For details on normalization, refer to :ref:`ref-name-normalization`.

    .. code-block:: text

        EXAMPLE               == example
        Example               == example
        eXaMpLe               == example
        Name with Words       == name_with_words
        Name_with_Words       == name_with_words

For the comparison of text names, see :ref:`ref-text-name-comparison` in the next chapter.


Features
--------

.. list-table::
    :header-rows: 1
    :width: 100%
    :widths: 25, 75

    *   -   Feature
        -   Coverage
    *   -   :text-code:`core`
        -   Regular names are part of the core language.
    *   -   :text-code:`text-names`
        -   Text names are a standard feature.


Errors
------

.. list-table::
    :header-rows: 1
    :width: 100%
    :widths: 25, 75

    *   -   Error Code
        -   Causes
    *   -   :text-code:`Syntax`
        -   |   Raised if a name starts with an underscore or a digit.
            |   Raised if a name ends with an underscore.
            |   Raised if a name contains consecutive underscores or spaces.
    *   -   :text-code:`NameConflict`
        -   Raised if an already used name is reused.
    *   -   :text-code:`LimitExceeded`
        -   Raised if a name exceeds the 100-character limit.
