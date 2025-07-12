# Copyright (c) 2025, Sine Nomine Associates
# See LICENSE

import pytest
from OpenAFSLibrary.variable import get_var, get_bool, VariableMissing, VariableEmpty


def test_get_var__returns_default_values(variables):
    assert get_var("AFS_AKIMPERSONATE") is False
    assert get_var("AFS_CELL") == "example.com"
    assert get_var("AKLOG") == "aklog"
    assert get_var("BOS") == "bos"
    assert get_var("FS") == "fs"
    assert get_var("KDESTROY") == "kdestroy"
    assert get_var("KINIT") == "kinit"
    assert get_var("KLOG_KRB5") == "klog.krb5"
    assert get_var("KRB_AFS_KEYTAB") == "robot.keytab"
    assert get_var("KRB_REALM") == "EXAMPLE.COM"
    assert get_var("PAG_ONEGROUP") is True
    assert get_var("PAGSH") == "pagsh"
    assert get_var("RXDEBUG") == "rxdebug"
    assert get_var("UNLOG") == "unlog"
    assert get_var("VOS") == "vos"


def test_get_var__returns_custom_value_when_set(variables):
    value = "/my/custom/path/to/vos"
    variables["VOS"] = value
    assert get_var("VOS") == value


def test_get_var__raises_exception_when_variable_name_is_unknown(variables):
    with pytest.raises(VariableMissing):
        get_var("__TEST_NAME__")


def test_get_var__raises_exception_when_variable_value_is_empty(variables):
    variables["__TEST_NAME__"] = ""
    with pytest.raises(VariableEmpty):
        get_var("__TEST_NAME__")


@pytest.mark.parametrize("value", [True, 1, 2, "yes", "y", "true", "t", "1"])
def test_get_bool__returns_true(variables, value):
    variables["__TEST_NAME__"] = value
    assert get_bool("__TEST_NAME__") is True


@pytest.mark.parametrize("value", [False, 0, "no", "false", "other"])
def test_get_bool__returns_false(variables, value):
    variables["__TEST_NAME__"] = value
    assert get_bool("__TEST_NAME__") is False


def test_get_bool__raises_exception_when_variable_is_unknown(variables):
    with pytest.raises(VariableMissing):
        get_bool("__TEST_NAME__")


def test_get_bool__raises_exception_when_variable_value_is_empty(variables):
    variables["__TEST_NAME__"] = ""
    with pytest.raises(VariableEmpty):
        get_bool("__TEST_NAME__")
