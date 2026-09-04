# Changelog

This file describes the relevant changes made on the project for each version.

Changelog entries are generated with [*towncrier*](https://towncrier.readthedocs.io/) and 
defined on the `changelog` folder.

<!-- towncrier release notes start -->

## [0.2.0](https://github.com/Joao-Pedro-P-Holanda/beware/tree/0.2.0) - 2026-09-04

### Security

- Hardened github actions workflows by fixing [zizmor](https://docs.zizmor.sh/) findings

### Added

- Add project documentation describing library usage, caveats and contributing guide with zensical. Deployed on Github Pages at https://joao-pedro-p-holanda.github.io/beware/

### Fixed

- Corrected syntax docstrings examples


## [0.1.0](https://github.com/Joao-Pedro-P-Holanda/beware/tree/0.1.0) - 2026-05-30

### Added

- `Unsafe` descriptor class that raises an UnsafeReadException when used without sanitization
- `sanitize_context` context manager and `sanitizes` decorator to allow defining blocks of code and functions that
  sanitize certain attributes, **ONLY** if they are modified inside the context or decorated function
- `unsafe_context`, a context manager to allow reading certain unsafe attributes without sanitization
