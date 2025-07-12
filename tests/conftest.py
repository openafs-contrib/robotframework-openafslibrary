# Copyright (c) 2025, Sine Nomine Associates
# See LICENSE

import pytest
import io

from unittest.mock import Mock
import OpenAFSLibrary.command
import OpenAFSLibrary.variable
import OpenAFSLibrary.keywords.acl
import OpenAFSLibrary.keywords.command
import OpenAFSLibrary.keywords.login
import OpenAFSLibrary.keywords.pag
import OpenAFSLibrary.keywords.path
import OpenAFSLibrary.keywords.volume


@pytest.fixture
def logged(monkeypatch):
    captured = Mock()
    captured.debug = []
    captured.info = []

    def sprint(*args):
        with io.StringIO() as out:
            print(*args, file=out, end="")
            return out.getvalue()

    def capture_debug(*args):
        captured.debug.append(sprint(*args))

    def capture_info(*args):
        captured.info.append(sprint(*args))

    for module in [
        OpenAFSLibrary.command,
        OpenAFSLibrary.keywords.acl,
        OpenAFSLibrary.keywords.command,
        OpenAFSLibrary.keywords.login,
        OpenAFSLibrary.keywords.pag,
        OpenAFSLibrary.keywords.path,
        OpenAFSLibrary.keywords.volume,
    ]:
        monkeypatch.setattr(module.logger, "debug", capture_debug)
        monkeypatch.setattr(module.logger, "info", capture_info)

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
