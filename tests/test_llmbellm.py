"""Tests for llmbellm."""

from __future__ import annotations

import io
import sys

import pytest

from llmbellm import bell, wrap
from llmbellm.cli import main


# ---------------------------------------------------------------------------
# bell()
# ---------------------------------------------------------------------------

def test_bell_writes_bell_char(capsys):
    bell()
    captured = capsys.readouterr()
    assert "\a" in captured.err


def test_bell_prints_message(capsys):
    bell("hello world")
    captured = capsys.readouterr()
    assert "hello world" in captured.out
    assert "\a" in captured.err


def test_bell_no_message(capsys):
    bell()
    captured = capsys.readouterr()
    assert captured.out == ""


# ---------------------------------------------------------------------------
# wrap()
# ---------------------------------------------------------------------------

def test_wrap_returns_result(capsys):
    def add(a, b):
        return a + b

    wrapped_add = wrap(add)
    assert wrapped_add(1, 2) == 3


def test_wrap_rings_bell(capsys):
    def noop():
        return "ok"

    wrap(noop)()
    captured = capsys.readouterr()
    assert "\a" in captured.err


def test_wrap_custom_message(capsys):
    def noop():
        pass

    wrap(noop, message="all done")()
    captured = capsys.readouterr()
    assert "all done" in captured.out


def test_wrap_reraises_exception():
    def boom():
        raise ValueError("oops")

    with pytest.raises(ValueError, match="oops"):
        wrap(boom)()


def test_wrap_rings_bell_on_error(capsys):
    def boom():
        raise RuntimeError("fail")

    with pytest.raises(RuntimeError):
        wrap(boom, notify_on_error=True)()
    captured = capsys.readouterr()
    assert "\a" in captured.err


def test_wrap_no_bell_on_error_when_disabled(capsys):
    def boom():
        raise RuntimeError("fail")

    with pytest.raises(RuntimeError):
        wrap(boom, notify_on_error=False)()
    captured = capsys.readouterr()
    assert "\a" not in captured.err


def test_wrap_preserves_name():
    def my_func():
        pass

    assert wrap(my_func).__name__ == "my_func"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def test_cli_help():
    rc = main(["--help"])
    assert rc == 0


def test_cli_no_args():
    rc = main([])
    assert rc == 0


def test_cli_runs_command(capsys):
    rc = main(["echo", "hello"])
    assert rc == 0
    captured = capsys.readouterr()
    assert "\a" in captured.err
    assert "Command finished with exit code 0" in captured.out


def test_cli_forwards_exit_code():
    rc = main(["python", "-c", "import sys; sys.exit(42)"])
    assert rc == 42
