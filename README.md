# Beware
![PyPI Version](https://img.shields.io/pypi/v/beware)
![PyPI Python Versions](https://img.shields.io/pypi/pyversions/beware)

Beware is a pure python package with zero dependencies that provides functions to track the usage of
unsafe attributes on the code and perform sanitization.

## Features

- Define attributes that need to be sanitized with Python descriptors
- Declare functions or blocks of code to perform sanitization


## Alternatives

- [ItsDangerous](https://itsdangerous.palletsprojects.com/en/stable/): use it if you need to transmit data through an unsafe medium and guarantee that it is not tampered

## Roadmap

- [ ] Publish code documentation
- [ ] Add doctests for docstrings
- [ ] Define a pytest plugin to allow easier checks of unsafe access without modifying the source code

