# Copyright (c) 2025, Sine Nomine Associates
# See LICENSE

import pytest

from unittest.mock import Mock
import OpenAFSLibrary.logger
import OpenAFSLibrary.command
import OpenAFSLibrary.variable


@pytest.fixture
def logged(monkeypatch):
    captured = Mock()
    captured.trace = []
    captured.debug = []
    captured.info = []
    captured.warn = []
    captured.error = []

    def capture_trace(msg, html=False):
        captured.trace.append(msg)

    def capture_debug(msg, html=False):
        captured.debug.append(msg)

    def capture_info(msg, html=False, also_console=False):
        captured.info.append(msg)

    def capture_warn(msg, html=False):
        captured.warn.append(msg)

    def capture_error(msg, html=False):
        captured.error.append(msg)

    monkeypatch.setattr(OpenAFSLibrary.logger, "trace", capture_trace)
    monkeypatch.setattr(OpenAFSLibrary.logger, "debug", capture_debug)
    monkeypatch.setattr(OpenAFSLibrary.logger, "info", capture_info)
    monkeypatch.setattr(OpenAFSLibrary.logger, "warn", capture_warn)
    monkeypatch.setattr(OpenAFSLibrary.logger, "error", capture_error)
    return captured


@pytest.fixture
def variables(monkeypatch):
    """
    Monkey patch the RF get_variable_value() and env vars so the get_var()
    always returns the default value for a given name.

    Tests can preset variable values by setting keys in the returned dict.
    """
    variables = {}

    # Remove env vars which could interfere with tests.
    for name in OpenAFSLibrary.variable._default_value.keys():
        monkeypatch.delenv(name, raising=False)

    def gvv(name):
        # The name arg is given in the form "${FOO}", where FOO is the key.
        rf_vars = {}
        for key in variables:
            rf_vars["${" + key + "}"] = variables[key]
        return rf_vars.get(name, None)

    monkeypatch.setattr(OpenAFSLibrary.variable._rf, "get_variable_value", gvv)
    return variables


@pytest.fixture
def process(monkeypatch, variables):
    """
    Returns a factory to stage mocked process objects and to monkey patch the
    run_program() function to stub out external programs for testing.

    This fixture manages a queue of mocked processes, since some functions call
    more than one process. The test function should call process() to stage
    each process to be stubbed out. The stubbed out processes return the canned
    results provided in the process() factory call.

    Example usage:

        def test_example(process):
            first_proc = process(code=0, stdout=["hello", "world"])
            second_proc = process(code=1, stderr=["boom"])
            with pytest.raises(CommandFailed):
                example()   # calls run_program() twice
            assert first_proc.args == ["some-program", "-option-given"]
            assert second_proc.args == ["another-program"]
    """
    procs = []  # fifo queue of process mocks.

    def _l2b(lines):
        lines = [] if lines is None else lines
        return bytearray("\n".join(lines), "utf-8")

    def process(expected_args=None, code=0, stdout=None, stderr=None):
        assert isinstance(code, int)
        assert stdout is None or isinstance(stdout, list)
        assert stderr is None or isinstance(stderr, list)
        proc = Mock()
        proc.args = None
        proc.returncode = code
        proc.expected_args = expected_args
        proc.stdout = _l2b(stdout)
        proc.stderr = _l2b(stderr)
        proc.communicate = Mock(return_value=(proc.stdout, proc.stderr))
        procs.append(proc)
        return proc

    def _popen(args, **kwargs):
        assert len(procs) > 0, "process() is missing in test."
        proc = procs.pop(0)
        if proc.expected_args is not None:
            assert args == proc.expected_args
        proc.args = args
        return proc

    monkeypatch.setattr(OpenAFSLibrary.command.subprocess, "Popen", _popen)
    return process
