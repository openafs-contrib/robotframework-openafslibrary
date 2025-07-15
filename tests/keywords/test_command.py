# Copyright (c) 2025, Sine Nomine Associates
# See LICENSE

import pytest

from OpenAFSLibrary.keywords.command import _CommandKeywords


@pytest.fixture
def keywords():
    return _CommandKeywords()


def test_command_should_succeed__succeeds_when_exit_code_is_0(
    keywords, process, logged
):
    proc = process(stdout=["success"])
    keywords.command_should_succeed("command flag1 flag2")
    assert proc.args == "command flag1 flag2"
    assert "Output: success" in logged.info


def test_command_should_succeed__raises_assertion_error_when_exit_code_is_1(
    keywords, process, logged
):
    process(code=1, stderr=["failed"])
    with pytest.raises(AssertionError):
        keywords.command_should_succeed("command")
    assert "Error: failed" in logged.info


def test_command_should_fail__raises_assertion_error_when_exit_code_is_0(
    keywords, process, logged
):
    process(code=0, stdout=["success"])
    with pytest.raises(AssertionError) as e:
        keywords.command_should_fail("command")
    assert "Command should have failed" in str(e.value)


def test_command_should_fail__suceeds_when_exit_code_is_1(keywords, process, logged):
    process(code=1, stderr=["failed"])
    keywords.command_should_fail("command")
    assert "Code: 1" in logged.info
