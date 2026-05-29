"""Command-line interface for llmbellm."""

from __future__ import annotations

import subprocess
import sys

from .bell import bell


def main(argv: list[str] | None = None) -> int:
    """Run a shell command and ring the bell when it finishes.

    Usage::

        llmbellm <command> [args …]

    Example::

        llmbellm python train.py

    The exit code of <command> is forwarded as the exit code of llmbellm.

    Note: llmbellm intentionally allows executing arbitrary commands supplied
    by the caller, just as you would run them directly in a shell.  The
    command list is passed directly to ``subprocess.run`` without a shell
    interpreter, so shell injection via metacharacters is not possible.
    """
    args = argv if argv is not None else sys.argv[1:]

    if not args or args[0] in ("-h", "--help"):
        print(main.__doc__)
        return 0

    result = subprocess.run(args)  # noqa: S603
    bell(f"Command finished with exit code {result.returncode}")
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
