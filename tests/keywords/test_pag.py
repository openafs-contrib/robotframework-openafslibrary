# Copyright (c) 2025, Sine Nomine Associates
# See LICENSE

import pytest
import sys
import OpenAFSLibrary.keywords.pag

from unittest.mock import Mock
from OpenAFSLibrary.keywords.pag import (
    _get_pag_from_one_group,
    _PagKeywords,
)


@pytest.fixture
def keywords():
    return _PagKeywords()


@pytest.mark.parametrize(
    "gids,expected",
    [
        ([4, 24, 27, 30, 46, 120, 131, 139, 1001], None),
        ([4, 24, 27, 30, 46, 120, 131, 139, 1001, 1098354308], 1098354308),
    ],
)
def test__get_pag_from_one_group__succeeds(gids, expected):
    pag = _get_pag_from_one_group(gids)
    assert pag is expected


def test__get_pag_from_one_group__raises_assertion_error_when_too_many_pags():
    gids = [4, 24, 27, 30, 46, 120, 131, 139, 1001, 1098354308, 1098354309]
    with pytest.raises(AssertionError) as e:
        _get_pag_from_one_group(gids)
    assert "More than one PAG group found" in str(e)


@pytest.mark.skip(reason="obsolete")
def test__get_pag_from_two_groups():
    raise NotImplementedError("test not implemented")


@pytest.mark.skipif(
    sys.platform == "win32", reason="This test is not applicable on Windows."
)
@pytest.mark.parametrize(
    "gids,expected",
    [
        # This function returns a string instead of an int !?
        ("4, 24, 27, 30, 46, 120, 131, 139, 1001", "None"),
        ("4, 24, 27, 30, 46, 120, 131, 139, 1001, 1098354308", "1098354308"),
        ("[4, 24, 27, 30, 46, 120, 131, 139, 1001, 1098354308]", "1098354308"),
    ],
)
def test_pag_from_groups__succeeds(keywords, gids, expected):
    got = keywords.pag_from_groups(gids)
    assert got == expected


@pytest.mark.skipif(
    sys.platform == "win32", reason="This test is not applicable on Windows."
)
@pytest.mark.parametrize(
    "gids,expected",
    [
        # This function returns a string instead of an int !?
        ([4, 24, 27, 30, 46, 120, 131, 139, 1001], "None"),
        ([4, 24, 27, 30, 46, 120, 131, 139, 1001, 1098354308], "1098354308"),
    ],
)
def test_pag_from_groups__succeeds_when_getting_current_groups(
    keywords, monkeypatch, gids, expected
):
    mock_getgroups = Mock(return_value=gids)
    monkeypatch.setattr(OpenAFSLibrary.keywords.pag.os, "getgroups", mock_getgroups)
    got = keywords.pag_from_groups(None)
    assert got == expected


@pytest.mark.skipif(
    sys.platform == "win32", reason="This test is not applicable on Windows."
)
def test_pag_should_exist__succeeds_when_pag_is_present(keywords, monkeypatch):
    gids = [4, 131, 139, 1001, 1098354308]
    mock_getgroups = Mock(return_value=gids)
    monkeypatch.setattr(OpenAFSLibrary.keywords.pag.os, "getgroups", mock_getgroups)
    keywords.pag_should_exist()


@pytest.mark.skipif(
    sys.platform == "win32", reason="This test is not applicable on Windows."
)
def test_pag_should_exist__fails_when_pag_is_missing(keywords, monkeypatch):
    gids = [4, 131, 139, 1001]
    mock_getgroups = Mock(return_value=gids)
    monkeypatch.setattr(OpenAFSLibrary.keywords.pag.os, "getgroups", mock_getgroups)
    with pytest.raises(AssertionError) as e:
        keywords.pag_should_exist()
    assert "PAG is not set" in str(e)


@pytest.mark.skipif(
    sys.platform == "win32", reason="This test is not applicable on Windows."
)
def test_pag_should_not_exist__succeeds_when_pag_is_missing(keywords, monkeypatch):
    gids = [4, 131, 139, 1001]
    mock_getgroups = Mock(return_value=gids)
    monkeypatch.setattr(OpenAFSLibrary.keywords.pag.os, "getgroups", mock_getgroups)
    keywords.pag_should_not_exist()


@pytest.mark.skipif(
    sys.platform == "win32", reason="This test is not applicable on Windows."
)
def test_pag_should_not_exist__fails_when_pag_is_present(keywords, monkeypatch):
    gids = [4, 131, 139, 1001, 1098354308]
    mock_getgroups = Mock(return_value=gids)
    monkeypatch.setattr(OpenAFSLibrary.keywords.pag.os, "getgroups", mock_getgroups)
    with pytest.raises(AssertionError) as e:
        keywords.pag_should_not_exist()
    assert "PAG is set" in str(e)


@pytest.mark.parametrize(
    "pag,isvalid",
    # Why does this require a string input !?
    [
        ("-1", False),
        ("0", False),
        ("1090519039", False),
        ("1090519040", True),
        ("1098354308", True),
        ("1107296255", True),
        ("1107296256", False),
    ],
)
def test_pag_should_be_valid(keywords, pag, isvalid):
    if isvalid:
        keywords.pag_should_be_valid(pag)
    else:
        with pytest.raises(AssertionError) as e:
            keywords.pag_should_be_valid(pag)
        assert "PAG is out of range" in str(e)


def test_pag_should_be_valid__none_arg(keywords):
    with pytest.raises(AssertionError) as e:
        keywords.pag_should_be_valid(None)
    assert "PAG is None." in str(e)


def test_pag_should_be_valid__none_str_arg(keywords):
    with pytest.raises(AssertionError) as e:
        keywords.pag_should_be_valid("None")
    assert "PAG is None." in str(e)


def test_pag_should_be_valid__bad_arg(keywords):
    with pytest.raises(ValueError) as e:
        keywords.pag_should_be_valid("bogus")
    assert "invalid literal for int()" in str(e)


@pytest.mark.skip(reason="test not implemented")
def test_pag_shell(keywords):
    raise NotImplementedError("test not implemented")
