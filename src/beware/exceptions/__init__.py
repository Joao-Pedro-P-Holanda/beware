class UnsafeReferenceException(Exception):
    """Raised when an attribute is referenced without being sanitized first"""


class NameAssignmentException(AttributeError):
    """Raised when a descriptor instance is assigned to two different attributes on one or more classes"""
