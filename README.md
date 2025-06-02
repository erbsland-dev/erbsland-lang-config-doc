# Erbsland Configuration Language

The Erbsland Configuration Language (*ELCL*) is a human-centric configuration format designed with a focus on clarity and ease of use. *ELCL* simplifies software configuration, making it intuitive for both developers and end-users.

## Current Status

*ELCL* is currently in pre-release status. The language specification is complete, reference implementations will be available soon. Minor changes may be made before the first stable release.

## Where to Start?

* **Short on time?** Check out the [Language Overview](https://erbsland-dev.github.io/erbsland-lang-config-doc/language-overview.html) for a quick introduction.
* **Looking for more details?** Read the [comprehensive introduction](https://erbsland-dev.github.io/erbsland-lang-config-doc/intro/index.html) chapter to get started.
* **Implementing a parser?** Find all details the [language reference](https://erbsland-dev.github.io/erbsland-lang-config-doc/reference/index.html) chapter.

## Design Rationale and Key Features

*ELCL* balances the flexibility required for human users to freely edit configuration documents and add comments, with the technical needs for strict and straightforward parsing. The language is designed to be familiar and easy to learn, enabling developers to quickly adopt it. Some of the main features include:

* **Simplicity**: *ELCL* offers an intuitive syntax with built-in type safety, minimizing common configuration errors.
* **Safety**: The language supports strict and safe parsers, ensuring robust and secure configurations.
* **Comprehensive Documentation**: Detailed specifications, along with user and developer guides, make *ELCL* easy to understand and implement.
* **Reference Implementations**: Available for Python and C++, these implementations help integrate *ELCL* into your application or serve as examples for writing your own parser.
* **Compliance Test Suite**: An extensive test suite ensures that parsers conform to the *ELCL* specification, fostering reliable and consistent implementations.
* **Implementation Levels**: *ELCL* supports various implementation levels, from lightweight micro-parsers for resource-constrained environments to full-featured parsers that handle complex configurations seamlessly.
* **Metadata Support**: Metadata statements allow you to specify language versions and required features, ensuring backward compatibility and future-proofing.

## License

Here’s how you can use and share the ELCL specification and reference implementations:

Copyright 2025 Erbsland DEV. https://erbsland.dev

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
