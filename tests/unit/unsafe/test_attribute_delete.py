import pytest
from beware import unsafe


def test_delete_unsafe_class_attribute_makes_it_unacessible():
    descriptor = unsafe()

    class Example:
        a = descriptor

    instance = Example()
    instance.a = "a"

    del Example.a

    with pytest.raises(AttributeError):
        getattr(instance, "a")

    with pytest.raises(AttributeError):
        getattr(instance, "a")


def test_delete_unsafe_instance_attribute_remove_flags_on_the_instance():
    descriptor = unsafe()

    class Example:
        a = descriptor

    instance = Example()
    instance.a = "a"

    assert getattr(instance, descriptor._private_name, None) is not None

    del instance.a

    assert getattr(instance, descriptor._private_name, None) is None
