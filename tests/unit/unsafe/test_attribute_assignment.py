import pytest
import sys
from beware import unsafe
from beware.exceptions import NameAssignmentException


class Example:
    a: str = unsafe()
    b: int = 0


def test_unsafe_descriptor_cant_be_assigned_to_two_attributes():
    # On python < 3.12 the __set_name__ call wraps exceptions with RuntimeError
    # https://github.com/python/cpython/pull/103402
    exception = NameAssignmentException if sys.version_info > (3, 11) else RuntimeError
    with pytest.raises(exception):
        shared_descriptor = unsafe()

        class ReuseDescriptor:
            a = shared_descriptor
            b = shared_descriptor
