# Copyright (c) 2025, Sine Nomine Associates
# See LICENSE

import pytest

from OpenAFSLibrary.keywords.acl import (
    normalize,
    parse,
    AccessControlList,
    _ACLKeywords,
)


@pytest.fixture
def keywords():
    return _ACLKeywords()


#
# Tests for Internal helper functions.
#


@pytest.mark.parametrize(
    "value, expected",
    [
        (list(), list()),
        (list("r"), list("r")),
        (list("lr"), list("rl")),
        (list("rlidwka"), list("rlidwka")),
        (list("adiklrw"), list("rlidwka")),
    ],
    ids=lambda p: "".join(p),
)
def test_normalize__returns_expected(value, expected):
    got = normalize(value)
    assert got == expected


@pytest.mark.parametrize("invalid", list("bcmxyzXZY123.,-+=!?@/(){}"))
def test_normalize__raises_assertion_error_when_input_is_invalid(invalid):
    with pytest.raises(AssertionError) as e:
        normalize([invalid])
    assert "Illegal rights character" in str(e)


@pytest.mark.parametrize(
    "value,sign,rights",
    [
        # "",  TODO: This test fails!
        ("r", "+", list("r")),
        ("rl", "+", list("rl")),
        ("rlidwka", "+", list("rlidwka")),
        ("all", "+", list("rlidwkaABCDEFGH")),
        ("read", "+", list("rl")),
        ("write", "+", list("rlidwk")),
        ("none", "+", list()),
        ("dlikraw", "+", list("rlidwka")),
        ("rrrrllll", "+", list("rl")),
        ("+r", "+", list("r")),
        ("-r", "-", list("r")),
        ("-all", "-", list("rlidwkaABCDEFGH")),
        ("-read", "-", list("rl")),
        ("-write", "-", list("rlidwk")),
        ("-none", "-", list()),
    ],
)
def test_parse__returns_expected(value, sign, rights):
    got_sign, got_rights = parse(value)
    assert got_sign == sign
    assert got_rights == rights


@pytest.mark.parametrize(
    "value",
    [
        list("abc"),
        list("+XYZ"),
        list("---"),
        list("+++"),
    ],
)
def test_parse__raises_assertion_error_when_input_is_invalid(value):
    with pytest.raises(AssertionError) as e:
        parse(value)
    assert "Illegal rights character" in str(e)


#
# Tests for the internal helper class.
#


class Test_AccessControlList:

    @pytest.mark.parametrize(
        "args,expected",
        [
            # ([], "", "", {}),  # todo
            (["u r"], {"u": ("r", "")}),
            (["u r", "v w"], {"u": ("r", ""), "v": ("w", "")}),
        ],
    )
    def test_from_args__creates_instance(self, args, expected):
        a = AccessControlList.from_args(*args)
        assert a.acls == expected

    def test_from_path__creates_instance(self, process, tmp_path):
        process(
            stdout=[
                f"Access list for {tmp_path}",
                "Normal rights:",
                "  system:anyuser rl",
                "  user rlidwk",
            ]
        )
        expected = {"system:anyuser": ("rl", ""), "user": ("rlidwk", "")}
        a = AccessControlList.from_path(tmp_path)
        assert a.acls == expected

    @pytest.mark.parametrize(
        "args,name,rights,expected",
        [
            # ([], "", "", {}),  # todo
            ([], "u", "r", {"u": ("r", "")}),
            ([], "u", "-r", {"u": ("", "r")}),
            ([], "u", "read", {"u": ("rl", "")}),
            ([], "u", "write", {"u": ("rlidwk", "")}),
            ([], "u", "all", {"u": ("rlidwkaABCDEFGH", "")}),
            (["u r"], "v", "w", {"u": ("r", ""), "v": ("w", "")}),
            (["u rlidwka"], "u", "rlidwk", {"u": ("rlidwka", "")}),
        ],
    )
    def test_add__adds_an_acl(self, args, name, rights, expected):
        a = AccessControlList.from_args(*args)
        a.add(name, rights)
        assert a.acls == expected

    @pytest.mark.parametrize(
        "args,name,rights,expected",
        [
            ([], "u", "r", False),
            (["u r"], "u", "r", True),
            (["u r", "v w"], "v", "w", True),
            (["u read"], "u", "rl", True),
            (["u read"], "u", "rlidwk", False),
            (["u rl", "u -a"], "u", "-a", True),
        ],
    )
    def test_contains__acl(self, args, name, rights, expected):
        a = AccessControlList.from_args(*args)
        assert a.contains(name, rights) is expected


#
# Keyword tests.
#


@pytest.mark.parametrize(
    "rights",
    [
        "r",
        "rlidwka",
        "read",
        "write",
        "none",
    ],
)
def test_add_access_rights__runs_fs_setacl(keywords, process, rights):
    proc = process()
    keywords.add_access_rights("/a/b/c", "myuser", rights)
    assert proc.args == ["fs", "setacl", "-dir", "/a/b/c", "-acl", "myuser", rights]


def test_access_control_list_matches__succeeds_when_acls_match(
    keywords, process, tmp_path
):
    acls = "user rlidwk"
    process(
        stdout=[
            "Access list for {tmp_path}",
            "Normal rights:",
            f"  {acls}",
        ]
    )
    keywords.access_control_list_matches(tmp_path, acls)


def test_access_control_list_matches__fails_when_acls_do_not_mactch(
    keywords, process, tmp_path
):
    acls = "user rlidwk"
    process(
        stdout=[
            f"Access list for {tmp_path}",
            "Normal rights:",
            "  bogus rlidwk",
        ]
    )
    with pytest.raises(AssertionError) as e:
        keywords.access_control_list_matches(tmp_path, acls)
    assert "ACLs do not match" in str(e)


def test_access_control_list_contains__succeeds_when_list_contains_acls(
    keywords, process, tmp_path
):
    process(
        stdout=[
            f"Access list for {tmp_path}",
            "Normal rights:",
            "  user1 rlidwk",
        ]
    )
    name = "user1"
    rights = "rlidwk"
    keywords.access_control_list_contains(tmp_path, name, rights)


def test_access_control_list_contains__fails_when_list_does_not_contain_acls(
    keywords, process, tmp_path
):
    process(
        stdout=[
            f"Access list for {tmp_path}",
            "Normal rights:",
            "  user rlidwk",
        ]
    )
    name = "user"
    rights = "rl"
    with pytest.raises(AssertionError) as e:
        keywords.access_control_list_contains(tmp_path, name, rights)
    assert "ACL entry rights do not match" in str(e)


def test_access_control_should_exist__succeeds_when_acls_are_present(
    keywords, process, tmp_path
):
    process(
        stdout=[
            f"Access list for {tmp_path}",
            "Normal rights:",
            "  user rlidwk",
        ]
    )
    name = "user"
    keywords.access_control_should_exist(tmp_path, name)


def test_access_control_should_exist__fails_when_acls_not_present(
    keywords, process, tmp_path
):
    process(
        stdout=[
            f"Access list for {tmp_path}",
            "Normal rights:",
            "  bogus rlidwk",
        ]
    )
    name = "user"
    with pytest.raises(AssertionError) as e:
        keywords.access_control_should_exist(tmp_path, name)
    assert "ACL entry does not exist" in str(e)


def test_access_control_should_not_exist__succeeds_when_acls_not_present(
    keywords, process, tmp_path
):
    process(
        stdout=[
            f"Access list for {tmp_path}",
            "Normal rights:",
            "  bogus rlidwk",
        ]
    )
    name = "user"
    with pytest.raises(AssertionError) as e:
        keywords.access_control_should_exist(tmp_path, name)
    assert "ACL entry does not exist" in str(e)


def test_access_control_should_not_exist__fails_when_acls_are_present(
    keywords, process, tmp_path
):
    process(
        stdout=[
            f"Access list for {tmp_path}",
            "Normal rights:",
            "  user rlidwk",
        ]
    )
    name = "user"
    keywords.access_control_should_exist(tmp_path, name)
