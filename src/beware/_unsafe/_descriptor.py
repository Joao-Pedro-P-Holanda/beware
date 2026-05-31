"""
This module contains the Unsafe descriptor class and the factory function for returning
descriptor instances
"""

from typing import Any, overload

from beware._unsafe._context_vars import inside_unsafe_context
from beware.exceptions import NameAssignmentException, UnsafeReferenceException

# sentinel value to check if the default was provided
_MISSING_DEFAULT = object()


class Unsafe:
    """Descriptor class used to control unsafe variables access"""

    __slots__: tuple[str, ...] = (
        "_read_by_context",
        "_default",
        "_sanitize_on_assignment",
        "_sanitize_flag",  # pyright: ignore[reportUninitializedInstanceVariable]
        "_owner",  # pyright: ignore[reportUninitializedInstanceVariable]
        "_private_name",  # pyright: ignore[reportUninitializedInstanceVariable]
        "_public_name",  # pyright: ignore[reportUninitializedInstanceVariable]
    )

    def __init__(self, default: Any | None = _MISSING_DEFAULT) -> None:

        self._read_by_context: bool = False
        """
        Determine if the attribute read should check the inside_unsafe_context ContextVar
        """

        self._sanitize_on_assignment: bool = False
        """
        When it is True, calling __set__ will make the variable sanitized 
        """

        self._default: Any | None = default
        """
        Default values are used when the related object have not modified the 
        corresponding attribute of the descriptor field
        """

    def __set_name__(self, owner: type[object], name: str):
        if getattr(self, "_owner", None):
            raise NameAssignmentException(
                f"Descriptor already binded to '{self._public_name}' attribute in {self._owner}"
            )

        self._owner: type[object] = owner
        self._public_name: str = name
        self._private_name: str = f"_{name}_beware"
        self._sanitize_flag: str = f"{self._private_name}_sanitized"

    @overload
    def __get__(self, obj: None, objtype: None) -> "Unsafe": ...

    @overload
    def __get__(self, obj: object, objtype: type[object]) -> Any: ...

    def __get__(self, obj: Any, objtype: type[object] | None = None) -> "Unsafe|Any":
        if obj is None:
            return self

        read_allowed = inside_unsafe_context.get() if self._read_by_context else False

        # if the descriptor has a default value and it was not overriden, it should be
        # returned.
        # If not, the descriptor field tries to resolve the instance attribute

        # default values don't need sanitization
        val = getattr(obj, self._private_name, self._default)

        if val is _MISSING_DEFAULT:
            raise AttributeError(
                f" '{type(obj).__name__}' object has no attribute {self._public_name}"
            )
        elif self._default == val:
            return self._default
        else:
            if getattr(obj, self._sanitize_flag, False) or read_allowed:
                return val
            else:
                raise UnsafeReferenceException

    def __set__(self, obj: object, value: Any) -> None:
        setattr(obj, self._private_name, value)
        if self._sanitize_on_assignment:
            setattr(obj, self._sanitize_flag, True)

    def __delete__(self, instance: object):
        try:
            delattr(instance, self._private_name)
            delattr(instance, self._sanitize_flag)
        except AttributeError:
            pass


def unsafe(default: Any | None = _MISSING_DEFAULT) -> Any:
    """Factory function for Unsafe descriptors

    Parameters
    -----
    default: Any
        The default value of the field, can be accessed in any context

    Warnings
    -----
        Default values can be accessed normally
    """

    return Unsafe(default=default)
