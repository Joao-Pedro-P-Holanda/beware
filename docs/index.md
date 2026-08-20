# Beware

`Beware` is a pure python and zero-dependencies project with the goal of providing utility
functions to control the access of unsafe values on your Python code.

This library does not aim to define **how** each value is sanitized, but to *remember*
the developer to sanitize it.

## Instalation
     

You can install the package with `pip install beware` or the equivalent command on your favorite
package manager.

## Features

Beware provides a simple interface to avoid usages of instances attributes without proper sanitization,
allowing both function decorators for functional programming patterns and context managers for imperative patterns.

### Sanitization

The library define two ways of sanitizing instance attributes: decorated functions and context manager blocks. 
Details on how to use both ways are present [here](./sanitization/index.md).

### Unsafe access

There's also the possibility of accessing some unsafe fields without sanitizing them first. 
You can see examples on the docs about [unsafe access](./unsafe_access/index.md).


## Limitations

- `beware` uses descriptors for its internal logic, so It can only be used to enforce
sanitization in instances attributes.

## Alternatives 

- [ItsDangerous](https://itsdangerous.palletsprojects.com/en/stable/): use it if you need to transmit data through an unsafe medium and guarantee that it is not tampered

