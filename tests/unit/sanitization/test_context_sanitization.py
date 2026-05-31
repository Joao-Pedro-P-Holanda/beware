import pytest
from beware import sanitize_context, unsafe
from beware.exceptions import UnsafeReferenceException


class Example:
    a = unsafe()


def test_sanitizes_applies_only_to_the_given_attributes_using_context_manager():
    class ExampleWithMultipleAttributes:
        a = unsafe()
        b = unsafe()

    instance = ExampleWithMultipleAttributes()
    instance.b = None

    with sanitize_context(ExampleWithMultipleAttributes.a):
        with pytest.raises(UnsafeReferenceException):
            assert instance.b is None
