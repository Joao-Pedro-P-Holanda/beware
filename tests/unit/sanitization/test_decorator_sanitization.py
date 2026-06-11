from threading import Thread
import threading
import time
from types import LambdaType
from typing import Any, Callable

import pytest
from beware import unsafe, sanitizes
from beware.exceptions import UnsafeReferenceException
from copy import copy, deepcopy
from functools import WRAPPER_ASSIGNMENTS, lru_cache
import sys


class Example:
    a = unsafe()


def test_sanitizes_decorator_accepts_classes():
    @sanitizes(Example.a)
    class SanitizedClass: ...


def test_sanitizes_decorator_accepts_instances_with_dunder_call():
    class CallableInstance:
        def __call__(self):
            return 1

    instance = CallableInstance()

    assert sanitizes(Example.a)(instance)() == 1


def test_sanitizes_decorator_accepts_generators():
    @sanitizes(Example.a)
    def func():
        for i in range(5):
            yield i

    assert list(func()) == list(range(5))


def test_sanitizes_decorator_accepts_classical_coroutines():
    @sanitizes(Example.a)
    def sum_5():
        result = []
        for _ in range(5):
            y = yield
            result.append(y)
        return result

    coroutine = sum_5()

    coroutine.send(None)

    for i in range(4):
        coroutine.send(i)

    try:
        _ = next(coroutine)
    except StopIteration as e:
        assert e.value == list(range(4)) + [None]


@pytest.mark.asyncio
async def test_sanitizes_decorator_accepts_async_functions():
    @sanitizes(Example.a)
    async def func():
        return 1

    assert await func() == 1


@pytest.mark.asyncio
async def test_sanitizes_decorator_accepts_async_generators():
    @sanitizes(Example.a)
    async def func():
        for i in range(5):
            yield i

    result = []
    async for val in func():
        result.append(val)

    assert result == list(range(5))


lambda_calls = [  # type: ignore
    (lambda: 5, tuple(), dict(), 5),
    (lambda x: x, ("test",), dict(), "test"),
    (lambda *x: x, ("test1", "test2"), dict(), ("test1", "test2")),
    (lambda **x: dict(**x), tuple(), {"a": 1, "b": 2}, {"a": 1, "b": 2}),
]


@pytest.mark.parametrize("func,args,kwargs,expected", lambda_calls)
def test_sanitizes_decorator_accepts_lambdas(func: LambdaType, args, kwargs, expected):
    decorator = sanitizes(Example.a)
    assert decorator(func)(*args, **kwargs) == expected


def test_sanitizes_raises_type_error_on_non_callable_argument():
    with pytest.raises(TypeError):
        sanitizes(Example.a)(1)


def test_sanitizes_propagates_exceptions_on_sync_functions():
    @sanitizes(Example.a)
    def func():
        raise RuntimeError("fail")

    with pytest.raises(RuntimeError, match="fail"):
        func()


@pytest.mark.asyncio
async def test_sanitizes_propagates_exceptions_on_async_functions():

    @sanitizes(Example.a)
    async def afunc():
        raise RuntimeError("fail")

    with pytest.raises(RuntimeError, match="fail"):
        await afunc()


def _docstring_and_annotated_function(a: int):
    """
    Function with docstring and arguments with type params
    """


functions_to_wrap: list[Callable[..., Any]] = [_docstring_and_annotated_function]

# tests of type parameter lists wrap are made with eval to avoid invalid syntax on python < 3.12
if sys.version_info[0] >= 3 and sys.version_info[1] >= 12:
    exec(
        "\n".join(
            [
                "def _type_parameter_function[_T]():",
                '\t"""Function with docstring and arguments with type params"""',
                "functions_to_wrap.append(_type_parameter_function)",
            ]
        )
    )


@pytest.mark.parametrize("func", functions_to_wrap)
def test_sanitizes_decorator_wraps_functions_attributes(func):
    sanitized = sanitizes(Example.a)(func)

    for attr in WRAPPER_ASSIGNMENTS:
        assert getattr(sanitized, attr) == getattr(func, attr)


def test_sanitizes_applies_only_to_the_given_attributes_using_decorator():

    class ExampleWithMultipleAttributes:
        a: str = unsafe()
        b: int = unsafe()

    instance = ExampleWithMultipleAttributes()
    instance.b = None

    @sanitizes(ExampleWithMultipleAttributes.a)
    def test(instance: ExampleWithMultipleAttributes):
        with pytest.raises(UnsafeReferenceException):
            assert instance.b is None

    test(instance)


def test_sanitizes_is_not_applied_if_attribute_is_not_modified():

    instance = Example()
    instance.a = "test"

    @sanitizes(Example.a)
    def no_op(instance: Example):
        assert instance

    no_op(instance)

    with pytest.raises(UnsafeReferenceException):
        instance.a


def test_sanitizes_decorator_dont_sanitizes_on_cached_call():

    first_instance = Example()
    first_instance.a = "abc"
    second_instance = Example()
    second_instance.a = "cde"

    calls = 0

    @sanitizes(Example.a)
    @lru_cache
    def function_with_cache_hit(id: int):
        nonlocal calls
        if calls == 0:
            first_instance.a = "1"
        # never called because of cache hit
        elif calls == 1:
            second_instance.a = "2"
        else:
            calls += 1

    function_with_cache_hit(1)
    function_with_cache_hit(1)

    assert first_instance.a == "1"

    with pytest.raises(UnsafeReferenceException):
        second_instance.a


def test_sanitization_persists_on_shallow_copy():

    instance = Example()

    @sanitizes(Example.a)
    def define(instance: Example):
        instance.a = "sanitized"

    define(instance)

    copied = copy(instance)

    assert copied.a == "sanitized"


def test_sanitization_persists_on_deep_copy():

    instance = Example()

    @sanitizes(Example.a)
    def define(instance: Example):
        instance.a = "sanitized"

    define(instance)

    copied = deepcopy(instance)

    assert copied.a == "sanitized"


def test_sanitizes_validate_only_instances_manipulated_on_the_function():
    instance_1 = Example()
    instance_2 = Example()
    instance_2.a = None

    @sanitizes(Example.a)
    def sanitization(instance: Example) -> None:
        instance.a = "a"

    sanitization(instance_1)
    assert instance_1.a == "a"
    with pytest.raises(UnsafeReferenceException):
        assert instance_2.a is None


def test_sanitizes_dont_modifies_a_different_thread():
    instance = Example()

    @sanitizes(Example.a)
    def sanitization(instance: Example):
        instance.a = "a"

    def delayed_access(instance: Example):
        time.sleep(2)
        return instance.a is not None

    t1 = Thread(target=sanitization, args=(instance,))
    # the instance value should not be sanitized on t2, raising an error
    t2 = Thread(target=delayed_access, args=(instance,))

    def check_exception_on_thread(args):
        assert args.thread == t2
        assert args.exc_type == UnsafeReferenceException

    old_excepthook = threading.excepthook
    threading.excepthook = check_exception_on_thread

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    threading.excepthook = old_excepthook
