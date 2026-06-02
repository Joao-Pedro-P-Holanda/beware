from contextlib import contextmanager
from typing import Any

from beware._unsafe import unsafe_context


@contextmanager
def sanitize_context(*attrs: Any):
    """Context manager for marking the specified attributes as sanitized after assignment

    Parameters
    ----------
    attrs : tuple[Unsafe, ...]
            arguments that are sanitized after an assignment

    Examples
    --------
    >>> from beware import unsafe
    >>> class MyClass:
    ...     a = unsafe()
    ...
    >>> obj = MyClass()
    >>> with sanitize_context(MyClass.a):
    ...     obj.a = "sanitized"
    >>> obj.a # can be accessed outside an unsafe_context
    'sanitized'
    """

    with unsafe_context(*attrs):
        try:
            for attr in attrs:
                attr._sanitize_on_assignment = True

            yield

        finally:
            for attr in attrs:
                attr._sanitize_on_assignment = False
