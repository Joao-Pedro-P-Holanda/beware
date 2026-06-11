from typing import Any
import pytest
from beware import unsafe, unsafe_context
from beware.exceptions import UnsafeReferenceException


class Example:
    a: str = unsafe()
    b: int = 0


class ExampleWithGetAttribute(Example):
    def __init__(self) -> None:
        super().__init__()

    def __getattribute__(self, name: str, /) -> Any:
        return super().__getattribute__(name)


class ExampleWithGetAttr(Example):
    def __getattr__(self, name: str):
        return name


def test_unsafe_reference_raises_attribute_error_on_not_set_attribute():

    instance = Example()

    with unsafe_context(Example.a):
        with pytest.raises(AttributeError):
            print(instance.a)


def test_unsafe_reference_dont_applies_on_overriden_attribute():
    class OverridenExample(Example):
        a = "overriden"

    instance = OverridenExample()

    instance.a = "value"

    assert instance.a == "value"


def test_dont_applies_on_dunder_get_attr():
    instance = ExampleWithGetAttr()

    instance.a = "value"

    assert instance.__getattr__("a") != "value"


def test_unsafe_internal_attributes_dont_appear_on_instance_dict(): ...


def test_unsafe_access_dont_triggers_on_attribution():
    instance = Example()

    instance.a = "a"


def test_unsafe_access_triggers_when_calling_dunder_get_attribute_outside_unsafe_context():
    instance = ExampleWithGetAttribute()

    instance.a = "a"

    with pytest.raises(UnsafeReferenceException):
        instance.__getattribute__("a")


def test_unsafe_access_dont_trigger_when_attribute_is_referenced_on_unsafe_context():
    instance = Example()
    instance.a = "a"
    with unsafe_context(Example.a):
        assert instance.a == "a"


def test_unsafe_access_when_a_different_attribute_is_declared_on_unsafe_context():
    class TwoUnsafeExample:
        a: str = unsafe()
        b: str = unsafe()

    instance = TwoUnsafeExample()
    instance.b = "b"
    with unsafe_context(TwoUnsafeExample.a):
        with pytest.raises(UnsafeReferenceException):
            assert instance.b == "b"


def test_unsafe_attribute_triggers_on_subclass():
    class SubExample(Example):
        def __init__(self, c) -> None:
            self.c = c
            super().__init__()

    instance = SubExample(1)
    instance.a = "a"

    with pytest.raises(UnsafeReferenceException):
        assert instance.a == "a"


def test_unsafe_uses_default_when_attribute_is_not_set():
    class ExampleWithDefault:
        a = unsafe(1)

    instance = ExampleWithDefault()

    with unsafe_context(ExampleWithDefault.a):
        assert instance.a == 1


def test_unsafe_accepts_None_as_default():
    class ExampleWithDefault:
        a = unsafe(None)

    instance = ExampleWithDefault()

    with unsafe_context(ExampleWithDefault.a):
        assert instance.a == None


def test_unsafe_ignores_default_when_attribute_is_set():
    class ExampleWithDefault:
        a = unsafe(1)

    instance = ExampleWithDefault()
    instance.a = 2

    with unsafe_context(ExampleWithDefault.a):
        assert instance.a == 2


def test_attribute_with_unsafe_default_does_not_raise_exception():
    class ExampleWithDefault:
        a = unsafe(1)

    assert ExampleWithDefault().a == 1


def test_unsafe_uses_default_on_deleted_attrs():
    """
    Maintained for compatibility with the dataclass API
    """

    class ExampleWithDefault:
        a = unsafe(1)

    instance = ExampleWithDefault()
    del instance.a

    assert instance.a == 1


def test_unsafe_raises_attribute_error_when_deleted_unsafe_dont_have_default():
    class ExampleWithoutDefault:
        a = unsafe()

    instance = ExampleWithoutDefault()

    with pytest.raises(AttributeError):
        with unsafe_context(ExampleWithoutDefault.a):
            instance.a
