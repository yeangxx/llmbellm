"""Core bell functionality for llmbellm."""

from __future__ import annotations

import functools
import sys
import time
from typing import Any, Callable, TypeVar

F = TypeVar("F", bound=Callable[..., Any])

_BELL = "\a"


def bell(message: str = "") -> None:
    """Write a terminal bell character to stderr and optionally print *message*."""
    sys.stderr.write(_BELL)
    sys.stderr.flush()
    if message:
        print(message)


def wrap(fn: F, *, message: str = "", notify_on_error: bool = True) -> F:
    """Return a wrapper around *fn* that rings the bell after *fn* returns.

    Args:
        fn: The callable to wrap (e.g. an OpenAI chat-completions call).
        message: Optional message to print after the bell.
        notify_on_error: If ``True`` (default), also ring the bell when *fn*
            raises an exception.

    Returns:
        A callable with the same signature as *fn*.

    Example::

        import openai
        from llmbellm import wrap

        client = openai.OpenAI()
        create = wrap(client.chat.completions.create, message="Done!")
        response = create(model="gpt-4o", messages=[{"role": "user", "content": "hi"}])
    """

    @functools.wraps(fn)
    def _wrapped(*args: Any, **kwargs: Any) -> Any:
        start = time.monotonic()
        try:
            result = fn(*args, **kwargs)
            elapsed = time.monotonic() - start
            _msg = message or f"{fn.__qualname__} finished in {elapsed:.1f}s"
            bell(_msg)
            return result
        except Exception:
            if notify_on_error:
                bell(f"{fn.__qualname__} raised an exception")
            raise

    return _wrapped  # type: ignore[return-value]
