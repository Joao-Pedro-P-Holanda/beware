import inspect
from functools import wraps
from typing import Callable, ParamSpec, TypeVar, cast

from beware._unsafe import Unsafe
from ._context import sanitize_context

P = ParamSpec("P")
R = TypeVar("R")


def sanitizes(
    *attrs: Unsafe,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Decorator factory that marks all given attrs as safe after the function executes without
    exceptions.

    Parameters
    ----------
    attrs : tuple[Unsafe, ...]
            arguments that are sanitized on attribution,


    Returns
    -------
    A decorated function that will sanitize all given unsafe attributes when modified
    inside the function


    Examples
    --------
    >>> class MyClass:
    ...     a = unsafe()
    ...
    >>> @sanitizes(MyClass.a)
    ... def sanitize_a(instance:MyClass):
    ...     instance.a = "sanitized"
    ...
    >>> obj = MyClass()
    >>> sanitize_a(MyClass.a):
    ...     instance.a = "sanitized"
    ...
    >>> sanitize_a(obj)
    >>> obj.a # can be accessed outside of an unsafe context
    "sanitized"
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:

        # mypy can't resolve the return type correctly when using functool.wraps, thus the casts
        # Full thread: https://stackoverflow.com/questions/78807798/mypy-1-10-reports-error-when-functools-wraps-is-used-on-a-generic-function

        if inspect.iscoroutinefunction(func):

            @wraps(func)
            async def a_inner_function(*args: P.args, **kwargs: P.kwargs):
                try:
                    with sanitize_context(*attrs):
                        result = await func(*args, **kwargs)

                        return result
                except:
                    raise

            return cast(Callable[P, R], a_inner_function)

        elif callable(func):

            @wraps(func)
            def inner_function(*args: P.args, **kwargs: P.kwargs):
                try:
                    with sanitize_context(*attrs):
                        result = func(*args, **kwargs)

                        return result
                except:
                    raise

            return cast(Callable[P, R], inner_function)

        else:
            raise TypeError  # pyright: ignore[reportUnreachable]

    return decorator
