from contextvars import ContextVar

inside_unsafe_context: ContextVar[bool] = ContextVar(
    "inside_unsafe_context", default=False
)
