# Copyright (c) 2025, Sine Nomine Associates
# See LICENSE

import pytest
import os
import sys

from OpenAFSLibrary.command import (
    run_program,
    rxdebug,
    bos,
    vos,
    fs,
    CommandFailed,
    NoSuchEntryError,
)


@pytest.fixture
def python():
    return sys.executable


def test_run_program__runs_hello_world(python, logged):
    rc, out, err = run_program([python, "-c", "print('hello world')"])
    assert rc == 0
    assert out.strip() == "hello world"
    assert err.strip() == ""
    assert f"running: {python} -c print('hello world')" in logged.info
    assert "code: 0" in logged.debug
    assert "output: hello world\n" in logged.debug
    assert "error: " in logged.debug


def test_run_program__rc_is_1__when__program_exits_with_1(python):
    rc, out, err = run_program([python, "-c", "import sys; sys.exit(1)"])
    assert rc == 1


def test_run_program__raises_file_not_found__when__program_is_missing(tmp_path):
    missing_path = tmp_path / "missing"
    with pytest.raises(FileNotFoundError):
        rc, out, err = run_program([missing_path])


@pytest.mark.skipif(
    sys.platform == "win32", reason="This test is not applicable on Windows."
)
def test_run_program__raises_permission_error__when__file_is_not_executable(
    python, tmp_path
):
    script_path = tmp_path / "no-exec.sh"
    script_path.write_text("#!{python}\nimport sys\nsys.exit(0)\n")
    os.chmod(script_path, 0o644)
    with pytest.raises(PermissionError):
        rc, out, err = run_program([script_path])


def test_run_rxdebug__runs_rxdebug(process):
    usage = "Usage: rxdebug -servers ..."
    proc = process(code=0, stdout=[usage])
    out = rxdebug("-help")
    assert out == usage
    assert proc.args == ["rxdebug", "-help"]


def test_run_vos__runs_vos(process):
    usage = "vos: Commands are: ..."
    proc = process(stdout=[usage])
    out = vos("help")
    assert out == usage
    assert proc.args == ["vos", "help"]


def test_run_vos__raises_command_failed__when__subcommand_is_invalid(process):
    proc = process(code=255, stdout=["vos: Unrecognized operation"])
    with pytest.raises(CommandFailed):
        vos("bogus")
    assert proc.args == ["vos", "bogus"]


def test_run_vos__raises_no_such_entry_error__when__vldb_error_is_seen(process):
    proc = process(code=255, stderr=["error", "VLDB: no such entry"])
    with pytest.raises(NoSuchEntryError):
        vos("examine")
    assert proc.args == ["vos", "examine"]


def test_run_vos__raises_no_such_entry_error__when__does_not_exists_error_seen(process):
    proc = process(code=255, stderr=["error", "does not exist"])
    with pytest.raises(NoSuchEntryError):
        vos("examine")
    assert proc.args == ["vos", "examine"]


def test_run_bos__runs_bos_command(process):
    usage = "bos: Commands are: ..."
    proc = process(stdout=[usage])
    out = bos("help")
    assert out == usage
    assert proc.args == ["bos", "help"]


def test_run_fs__runs_fs_command(process):
    usage = "fs: Commands are: ..."
    proc = process(stdout=[usage])
    out = fs("help")
    assert out == usage
    assert proc.args == ["fs", "help"]


def test_run_fs__runs_command_in_path__when__fs_variable_is_set(process, variables):
    usage = "fs: Commands are: ..."
    proc = process(stdout=[usage])
    variables["FS"] = "/my/custom/path/fs"
    out = fs("help")
    assert out == usage
    assert proc.args == ["/my/custom/path/fs", "help"]
