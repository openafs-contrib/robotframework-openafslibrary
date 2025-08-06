# Copyright (c) 2025, Sine Nomine Associates
# See LICENSE

import pytest
from OpenAFSLibrary.keywords.rx import _RxKeywords
from OpenAFSLibrary.command import CommandFailed


@pytest.fixture
def keywords():
    return _RxKeywords()


def test_get_version__success(keywords, process):
    process(
        stdout=[
            "Trying 127.0.0.1 (port 7001):",
            "AFS version: OpenAFS 1.9.2-287-g6f703-dirty 2025-08-01 foo@bar",
        ]
    )
    version = keywords.get_version("localhost", 7001)
    assert version.startswith("OpenAFS 1.9.2")


def test_get_version__fails__when__timeout(keywords, process):
    process(
        code=1,
        stdout=[
            "Trying 127.0.0.1 (port 7001):",
            "get version call failed with code -1, errno 0",
        ],
    )
    with pytest.raises(CommandFailed):
        keywords.get_version("localhost", 7001)


def test_get_version__fails__when__output_is_bad(keywords, process):
    process(
        stdout=[
            "Trying 127.0.0.1 (port 7001):",
            "bogus",
        ]
    )
    with pytest.raises(AssertionError) as e:
        keywords.get_version("localhost", 7001)
    assert "Failed to get version string." in str(e.value)
