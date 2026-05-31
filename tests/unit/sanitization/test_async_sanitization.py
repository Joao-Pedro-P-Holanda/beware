import asyncio
import pytest
from beware import unsafe
from beware.exceptions import UnsafeReferenceException
from beware.sanitization import sanitizes


class Example:
    a = unsafe()


@pytest.mark.asyncio
async def test_attribute_sanitized_on_a_coroutine_is_sanitized_on_another_if_sanitization_finishes_first():
    @sanitizes(Example.a)
    async def sanitize_coroutine(instance: Example):
        instance.a = 1

    async def consume_coroutine(instance: Example):
        await asyncio.sleep(2)
        assert instance.a == 1

    instance = Example()

    await asyncio.gather(
        sanitize_coroutine(instance),
        consume_coroutine(instance),
    )


@pytest.mark.asyncio
async def test_attribute_sanitized_on_a_coroutine_raises_unsafe_read_on_another_if_sanitization_finishes_later():
    @sanitizes(Example.a)
    async def sanitize_coroutine(instance: Example):
        await asyncio.sleep(2)
        instance.a = 1

    async def consume_coroutine(instance: Example):
        assert instance.a == 0

    instance = Example()
    instance.a = 0

    with pytest.raises(UnsafeReferenceException):
        await asyncio.gather(
            sanitize_coroutine(instance),
            consume_coroutine(instance),
        )
