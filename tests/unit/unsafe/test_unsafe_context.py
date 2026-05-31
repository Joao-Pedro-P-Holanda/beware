import pytest

from beware import unsafe, unsafe_context


class Example:
    a = unsafe()


def test_unsafe_context_fails_when_non_Unsafe_descriptor_is_passed():
    with pytest.raises(
        TypeError, match="Invalid argument with type <class 'str'> expected Unsafe type"
    ):
        with unsafe_context("invalid"):
            pass


def test_unsafe_context_resets_read_by_context_from_descriptor_if_exception_is_raised():
    instance = Example()
    instance.a = 1
    try:
        with unsafe_context(Example.a):
            assert Example.a._read_by_context
            raise Exception
    except:
        assert not Example.a._read_by_context
