import pytest
from beware import unsafe
from beware.exceptions import NameAssignmentException


class Example:
    a: str = unsafe()
    b: int = 0


def test_unsafe_descriptor_cant_be_assigned_to_two_attributes():
    with pytest.raises(NameAssignmentException):
        shared_descriptor = unsafe()

        class ReuseDescriptor:
            a = shared_descriptor
            b = shared_descriptor
