# Copyright (c) 2025, Sine Nomine Associates
# See LICENSE

import pytest
import os
import sys
from OpenAFSLibrary.command import run_program


@pytest.fixture
def python():
    return sys.executable


def test_run_program__runs_hello_world(python, logged):
    rc, out, err = run_program([python, "-c", "print('hello world')"])
    assert rc == 0
    assert out.strip() == "hello world"
    assert err.strip() == ""
    assert len(logged.info) == 1
    assert logged.info[0] == f"running: {python} -c print('hello world')"


def test_run_program__rc_is_1_when_program_exits_with_1(python, logged):
    rc, out, err = run_program([python, "-c", "import sys; sys.exit(1)"])
    assert rc == 1


def test_run_program__raises_file_not_found_when_program_is_missing(logged, tmp_path):
    missing_path = tmp_path / "missing"
    with pytest.raises(FileNotFoundError):
        rc, out, err = run_program([missing_path])


def test_run_program__raises_permission_error_when_file_is_not_executable(
    python, logged, tmp_path
):
    script_path = tmp_path / "no-exec.sh"
    script_path.write_text("#!{python}\nimport sys\nsys.exit(0)\n")
    os.chmod(script_path, 0o644)
    with pytest.raises(PermissionError):
        rc, out, err = run_program([script_path])
