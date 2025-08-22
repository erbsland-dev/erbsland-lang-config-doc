..
    Copyright (c) 2024-2025 Tobias Erbsland - Erbsland DEV. https://erbsland.dev
    SPDX-License-Identifier: Apache-2.0

.. _ref-signature-meta-value:
.. index::
    single: @signature
    single: Signature
    single: Meta Value; Signature

Meta Command "Signature"
========================

The ``@signature`` meta command enables secure signing of configuration documents, allowing cryptographic verification of the author and protecting the document against accidental or malicious tampering. The *Erbsland Configuration Language* specifies only the general framework for this meta command, providing guidance on recommended implementation practices without mandating a specific method.

.. code-block:: erbsland-conf
    :class: good-example

    @signature: "..."

    [main configuration]
    value: "text"


.. index::
    pair: Rules; Signature

Rules for the Meta Value
------------------------

#.  **Format:** The ``@signature`` meta value *must* specify a text value that contains the document’s signature.

    .. code-block:: erbsland-conf
        :class: good-example

        @signature: "<signature data>"

#.  **Value Format:** While a parser can interpret the ``@signature`` text value as needed, it is strongly *recommended* to follow the format specified in :ref:`ref-signature-recommendation`.

    .. code-block:: erbsland-conf

        @signature: "name@example.com;2024-12-21T13:42:05;SHA-256;U2lnbmF0dXJlIERhdGEg8J+YiQ=="

#.  **Location:** The ``@signature`` meta value *must* appear on the *first line* of the document.

    .. code-block:: erbsland-conf
        :class: good-example

        @signature: "name@example.com;2024-12-21T13:42:05;SHA-256;U2lnbmF0dXJlIERhdGEg8J+YiQ=="

        [main]
        value: 1


Rules for the Implementation
----------------------------

#.  **Callback for Verification:** A parser that supports signatures *must* provide a callback to allow the application to verify a document's signature. A parser *may* also implement a framework for signature verification.

    .. code-block:: text
        :class: good-example

        Document Verification:
        ┌────────────────────┐                         ┌────────────────────┐
        │ Parser             │ ──────────────────────→ │ Application        │
        │                    │                         │                    │
        │                    │ ←────────────────────── │                    │
        └────────────────────┘                         └────────────────────┘

#.  **Callback for Document Signing:** A parser that supports signatures *must* provide a callback enabling the application to *sign* a document. Additionally, the parser *must* implement a method to sign an existing document using this callback.

    .. code-block:: text
        :class: good-example

        Signing Document:
        ┌────────────────────┐                         ┌────────────────────┐
        │ Parser             │ ──────────────────────→ │ Application        │
        │                    │                         │                    │
        │                    │ ←────────────────────── │                    │
        └────────────────────┘                         └────────────────────┘

#.  **Documents without Signatures:** The verification callback *must* also be called for documents lacking a signature, allowing the application to reject unsigned documents if desired.

    .. code-block:: text
        :class: good-example

        Document Verification:
        ┌────────────────────┐                         ┌────────────────────┐
        │ Parser             │ No signature            │ Application        │
        │                    │ ──────────────────────→ │                    │
        │                    │               Rejected! │                    │
        │                    │ ←────────────────────── │                    │
        └────────────────────┘                         └────────────────────┘

#.  **Verification Callback Interaction:** During a verification callback, the parser *must* send the source identifier (e.g., file path), the signature text, and the hash of the signed content to the application.

    .. code-block:: text
        :class: good-example

        Document Verification:
        ┌────────────────────┐                         ┌────────────────────┐
        │ Parser             │ Source Identifier       │ Application        │
        │                    │ Signature Text          │                    │
        │                    │ Hash Value              │                    │
        │                    │ ━━━━━━━━━━━━━━━━━━━━━━▶ │                    │
        │                    │               Accepted! │                    │
        │                    │ ←────────────────────── │                    │
        └────────────────────┘                         └────────────────────┘

#.  **Verification Callback Response:** The application responds to the verification callback by either accepting or rejecting the signature.

    .. code-block:: text
        :class: good-example

        Document Verification:
        ┌────────────────────┐                         ┌────────────────────┐
        │ Parser             │ Source Identifier       │ Application        │
        │                    │ Signature Text          │                    │
        │                    │ Hash Value              │                    │
        │                    │ ──────────────────────→ │                    │
        │                    │               Accepted! │                    │
        │                    │ ◀━━━━━━━━━━━━━━━━━━━━━━ │                    │
        └────────────────────┘                         └────────────────────┘

#.  **Signing Callback Interaction:** During a signing callback, the parser *must* send the source identifier and the hash of the content to the application.

    .. code-block:: text
        :class: good-example

        Signing Document:
        ┌────────────────────┐                         ┌────────────────────┐
        │ Parser             │ Source Identifier       │ Application        │
        │                    │ Hash Value              │                    │
        │                    │ ━━━━━━━━━━━━━━━━━━━━━━▶ │                    │
        │                    │      "<signature text>" │                    │
        │                    │ ←────────────────────── │                    │
        └────────────────────┘                         └────────────────────┘

#.  **Signing Callback Response:** The application responds to the signing callback by returning the generated signature text.

    .. code-block:: text
        :class: good-example

        Signing Document:
        ┌────────────────────┐                         ┌────────────────────┐
        │ Parser             │ Source Identifier       │ Application        │
        │                    │ Hash Value              │                    │
        │                    │ ──────────────────────→ │                    │
        │                    │      "<signature text>" │                    │
        │                    │ ◀━━━━━━━━━━━━━━━━━━━━━━ │                    │
        └────────────────────┘                         └────────────────────┘

#.  **Signed Content Definition:** Signed content begins on the line following the signature. If no content follows the signature line, the parser must return an error.

    .. code-block:: text
        :class: good-example
        :linenos:

        @signature: "<signature data>"
        Content
        Content
        Content

#.  **Hashing Algorithm:** The parser reads all *byte data* starting from the second line to calculate a strong cryptographic hash (e.g., SHA-256 or SHA-3-512). The parser *may* parse the document and compute the hash simultaneously, performing signature verification after parsing.

    .. code-block:: text
        :class: good-example

        A list of recommended hashing algorithms at the time of writing (2024).

        - SHA-256
        - SHA-384
        - SHA-512
        - SHA-3-256
        - SHA-3-384
        - SHA-3-512
        - BLAKE-256
        - BLAKE-384
        - BLAKE-512

#.  **Unsupported Algorithms:** Non-cryptographic algorithms *must not* be used. Cryptographic algorithms proven unsafe at the time of parser development (e.g., MD5, SHA-1) are also disallowed. Algorithms producing hashes with fewer than 256 bits *must not* be used.

    .. code-block:: text
        :class: bad-example

        DON'T USE: MD5, SHA-1, SHA-2 ...

#.  **Hash Format:** The parser *must* pass the cryptographic hash to the application in the format ``<type> <hash in hex>``, where ``<type>`` is the hashing algorithm (e.g., ``SHA-3-256``) and the hash is a hex-encoded sequence, such as ``a0b1c2d...3e4f5``.


.. _ref-signature-recommendation:

Recommended Signature Implementation
------------------------------------

We recommend using S/MIME certificates for signature verification. S/MIME infrastructure is widely supported, and many organizations already issue these certificates internally from a local certification authority.

By using S/MIME certificates, ownership of an email address can be verified, which is typically sufficient for ensuring that only authorized individuals—such as a specific group of administrators—can modify configurations.

Value Format
~~~~~~~~~~~~

We recommend the following format for signatures:

.. code-block:: text

    <Email address>;<ISO date-time>;<Hash Algorithm>;<Signature data, base64 encoded>

-   *Email address*: The email address associated with the S/MIME certificate’s subject.
-   *ISO date-time*: The date and time when the configuration was signed.
-   *Hash Algorithm*: The hash algorithm used by the parser to create the signature.
-   *Signature data*: The signature, encoded in Base64. For an RSA-4096 certificate, this results in approximately 700 characters, easily fitting within a single line.

Creating a Signature
~~~~~~~~~~~~~~~~~~~~

The following steps outline the process for creating a signature:

#.  The user provides their email address and access to certificate keys (usually managed by the OS).
#.  The application assembles a text string in the following format:

    .. code-block:: text

        <Email address>;<Current ISO date-time>;<Document Hash from Parser>

#.  The assembled text (email address, date-time, and hash) is signed using the private key of the certificate.
#.  A signature text, as shown in the Value Format section, is generated with the Base64-encoded signature.
#.  The parser replaces the unsigned configuration with the newly signed version.

Verifying the Signature
~~~~~~~~~~~~~~~~~~~~~~~

To verify a signature, the application performs the following steps:

#.  It retrieves the relevant certificate associated with the email address stored in the signature.
#.  It verifies that the signing time falls within the certificate’s validity period.
#.  It checks the validity of the certificate signature itself.
#.  It reconstructs the exact text used during the signing process:

    .. code-block:: text

        <Email address from signature>;<ISO date-time from signature>;<Document Hash from Parser>

#.  It verifies whether the signature matches.

Important Considerations
------------------------

-   **Hashing Algorithm Compatibility**: If the parser changes the hashing algorithm, verification of older configurations will fail. To prevent this, design the parser’s API to support previously used hashing algorithms for legacy signatures.
-   **Document Integrity**: While a document signature establishes author identity and prevents tampering, it’s essential to remember the following:

    -   A signed document can still be freely copied. If this poses a risk, consider integrating location information into the signature.
    -   Possession of a valid certificate does not automatically confer trust. The application should maintain a secure, non-locally modifiable list of trusted certificates.


Features
--------

.. list-table::
    :header-rows: 1
    :width: 100%
    :widths: 25, 75

    *   -   Feature
        -   Coverage
    *   -   :text-code:`core`
        -   Meta values and commands are part of the core language.
    *   -   :text-code:`signature`
        -   The ``@signature`` command is an advanced feature.


Errors
------

.. list-table::
    :header-rows: 1
    :width: 100%
    :widths: 25, 75

    *   -   Error Code
        -   Causes
    *   -
        -   All errors related to parsing name and text values.
    *   -   :text-code:`Syntax`
        -   |   Raised if the ``@signature`` meta value is followed by a non-text value.
            |   Raised if the command is not specified on the first line.
    *   -   :text-code:`Signature`
        -   |   Raised if a ``@signature`` meta value is present but the application cannot verify it.
            |   Raised if the application requires a signature but the document lacks one.
            |   Raised if the application rejects the signature.
    *   -   :text-code:`Unsupported`
        -   |   Raised if the parser does not support the ``@signature`` command.
            |   Raised if the application does not support signatures.

