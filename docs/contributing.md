---
icon: lucide/heart-handshake
---

# Contributing

First, thanks for wanting to help with beware!

Now, to start contributing we have some guidelines.

## Asking and Solving Issues

If you find any bug or want to request a feature to the package, open an issue on Github on [this link](https://github.com/Joao-Pedro-P-Holanda/beware/issues/new).

For other questions about the project you can create a new discussion [here](https://github.com/Joao-Pedro-P-Holanda/beware/discussions/new/choose). Feel free to help answering other users questions too.

## Development

- Create a fork of the project on Github.
- Setup the project locally using poetry. More about it [here](#setup-local-environment).
- Push your changes, preferentially in a separated branch, on your created fork
- Submit a Pull Request, resolve any requested changes and wait for approval

If you are making code changes, please ensure that you create new tests that fail without your proposed change or change existing tests 
to reflect a new behavior.

### Setup local environment 

This project uses `poetry` as the package manager. You can find instructions to install it on their documentation:
[https://python-poetry.org/docs/#installation](https://python-poetry.org/docs/#installation).

After installing you need to install the development dependencies:

```sh
poetry sync --with=test,lint,docs # you can remove docs if you are not modifying anything on the documentation
```

Now you can proceed to implementation and run the tests with:

```shell
poetry run pytest
```
