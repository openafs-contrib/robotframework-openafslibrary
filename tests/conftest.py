# Copyright (c) 2025, Sine Nomine Associates
# See LICENSE

import pytest
import io

from unittest.mock import Mock
import OpenAFSLibrary.command
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
