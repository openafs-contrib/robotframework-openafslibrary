# Copyright (c) 2025, Sine Nomine Associates
# See LICENSE

import pytest
from OpenAFSLibrary.keywords.login import (
    get_principal,
    akimpersonate,
    login_with_password,
    login_with_keytab,
    _LoginKeywords,
)


@pytest.fixture
def keywords():
    return _LoginKeywords()


@pytest.fixture
def tmp_keytab(tmp_path):
    """
    Create an empty file for the keytab since the keywords check for the
    existance of a file.
    """
    keytab = tmp_path / "test.keytab"
    keytab.touch()
    return keytab


#
# Helper function tests.
#


@pytest.mark.parametrize(
    "user,realm,expected",
    [
        ("user", "example.com", "user@example.com"),
        ("user.admin", "example.com", "user/admin@example.com"),
        ("", "example.com", "@example.com"),
        ("user", "", "user@"),
        ("", "", "@"),
    ],
)
def test_get_principal__returns_expected(user, realm, expected):
    got = get_principal(user, realm)
    assert got == expected


def test_akimpersonate___runs_aklog(process):
    proc = process()
    expected = "aklog -d -c example.com -k EXAMPLE.COM -keytab robot.keytab -principal user@EXAMPLE.COM"
    akimpersonate("user")
    assert proc.args == expected


def test_akimpersonate__run_aklog_with_values_when_variable_are_set(process, variables):
    proc = process()
    variables["AKLOG"] = "v1"
    variables["AFS_CELL"] = "v2"
    variables["KRB_REALM"] = "v3"
    variables["KRB_AFS_KEYTAB"] = "v4"
    akimpersonate("user")
    assert proc.args == "v1 -d -c v2 -k v3 -keytab v4 -principal user@v3"


def test_akimpersonate__raises_assertion_error_when_aklog_fails(process):
    process(code=1, stderr=["fail test"])
    with pytest.raises(AssertionError) as e:
        akimpersonate("user")
    assert "aklog failed" in str(e)


def test_login_with_password__runs_klog_krb5(process):
    expected = (
        "klog.krb5 -principal user -password password -cell example.com -k EXAMPLE.COM"
    )
    proc = process()
    login_with_password("user", "password")
    assert proc.args == expected


def test_login_with_password__run_klog_krb5_with_values_when_variables_are_set(
    process, variables
):
    proc = process()
    variables["KLOG_KRB5"] = "v1"
    variables["AFS_CELL"] = "v2"
    variables["KRB_REALM"] = "v3"
    login_with_password("user", "password")
    assert proc.args == "v1 -principal user -password password -cell v2 -k v3"


@pytest.mark.parametrize(
    "user,password",
    [
        (None, None),
        ("", ""),
        (None, "password"),
        ("", "password"),
        ("user", None),
        ("user", ""),
    ],
)
def test_login_with_password__raises_assertion_error_when_arg_is_missing(
    process, user, password
):
    with pytest.raises(AssertionError) as e:
        login_with_password(user, password)
    assert "is required" in str(e.value)


def test_login_with_keytab__runs_kinit_and_aklog(process, tmp_keytab):
    proc_kinit = process()
    proc_aklog = process()
    login_with_keytab("user", str(tmp_keytab))
    assert proc_kinit.args == f"kinit -k -t {tmp_keytab} user@EXAMPLE.COM"
    assert proc_aklog.args == "aklog -d -c example.com -k EXAMPLE.COM"


def test_login_with_keytab__specified_commands_when_variables_are_set(
    process, variables, tmp_keytab
):
    proc_kinit = process()
    proc_aklog = process()
    variables["KINIT"] = "v1"
    variables["AKLOG"] = "v2"
    variables["AFS_CELL"] = "v3"
    variables["KRB_REALM"] = "v4"
    login_with_keytab("user", str(tmp_keytab))
    assert proc_kinit.args == f"v1 -k -t {tmp_keytab} user@v4"
    assert proc_aklog.args == "v2 -d -c v3 -k v4"


#
# Keyword tests.
#


def test_login_with_akimpersonate(keywords, process, variables):
    expected = "aklog -d -c example.com -k EXAMPLE.COM -keytab robot.keytab -principal user@EXAMPLE.COM"
    proc = process(code=0)
    variables["AFS_AKIMPERSONATE"] = True
    keywords.login("user")
    assert proc.args == expected


def test_login_with_password(keywords, process):
    expected = (
        "klog.krb5 -principal user -password password -cell example.com -k EXAMPLE.COM"
    )
    proc = process()
    keywords.login("user", password="password")
    assert proc.args == expected


def test_login_with_keytab(keywords, process, tmp_keytab):
    proc_kinit = process()
    proc_aklog = process()
    keywords.login("user", keytab=str(tmp_keytab))
    assert proc_kinit.args == f"kinit -k -t {tmp_keytab} user@EXAMPLE.COM"
    assert proc_aklog.args == "aklog -d -c example.com -k EXAMPLE.COM"


def test_login__raises_value_error_when_args_are_missing(keywords):

    with pytest.raises(ValueError) as e:
        keywords.login("user")
    assert "password or keytab is required" in str(e)


def test_logout__runs_kdestroy_and_unlog(keywords, process):
    proc_kdestroy = process()
    proc_unlog = process()
    keywords.logout()
    assert proc_kdestroy.args == "KRB5CCNAME=/tmp/afsrobot.krb5cc kdestroy"
    assert proc_unlog.args == "unlog"


def test_logout__runs_commands_when_variables_are_set(keywords, process, variables):
    proc_kdestroy = process()
    proc_unlog = process()
    variables["AFS_AKIMPERSONATE"] = False
    variables["KDESTROY"] = "v1"
    variables["UNLOG"] = "v2"
    keywords.logout()
    assert proc_kdestroy.args == "KRB5CCNAME=/tmp/afsrobot.krb5cc v1"
    assert proc_unlog.args == "v2"


def test_logout__runs_unlog_when_akimperonate_variable_is_true(
    keywords, process, variables
):
    proc_unlog = process()
    variables["AFS_AKIMPERSONATE"] = True
    keywords.logout()
    assert proc_unlog.args == "unlog"
