from collections.abc import Generator
from contextlib import contextmanager

from .._unsafe._context_vars import inside_unsafe_context
from .._unsafe._descriptor import Unsafe


@contextmanager
def unsafe_context(*attrs: Unsafe) -> Generator[None, None, None]:
    """Enable the unsafe access of the specified attributes inside the context.

    Parameters
    ----------
    attrs : tuple[Unsafe, ...]
            arguments that can be acessed without raising UnsafeReadException,


    Raises
    ------
    TypeError
        If the given attrs are not Unsafe descriptors


    Examples
    --------
    >>> from beware import unsafe
    >>> class MyClass:
    ...     a = unsafe(default=1)
    ...
    >>> obj = MyClass()
    >>> with unsafe_context(MyClass.a):
    ...     x = obj.a # won't raise an exception, even if it is not sanitized
    ...
    >>> x
    1
    """

    for attr in attrs:
        if not isinstance(attr, Unsafe):
            raise TypeError(
                f"Invalid argument with type {type(attr)} expected Unsafe type"
            )

    token = inside_unsafe_context.set(True)
    try:
        for attr in attrs:
            attr._read_by_context = True

        yield
    finally:
        inside_unsafe_context.reset(token)
        for attr in attrs:
            attr._read_by_context = False
