# Copyright (c) 2025, Sine Nomine Associates
# See LICENSE

import pytest
import errno
import os
import sys

from OpenAFSLibrary.keywords.path import (
    _convert_errno_parm,
    _PathKeywords,
)


@pytest.fixture
def keywords():
    return _PathKeywords()


@pytest.fixture
def tmp_dir(tmp_path):
    dir_ = tmp_path / "tmp_dir"
    dir_.mkdir()
    return dir_


@pytest.fixture
def tmp_file(tmp_path):
    file = tmp_path / "tmp_file"
    file.touch()
    return file


@pytest.fixture
def tmp_symlink(tmp_file):
    symlink = tmp_file.parent / "tmp_symlink"
    symlink.symlink_to(tmp_file)
    return symlink


@pytest.mark.parametrize(
    "value, expected",
    [
        (0, 0),
        (22, 22),
        ("EINVAL", errno.EINVAL),
        ("EPERM", errno.EPERM),
        ("ENODEV", errno.ENODEV),
    ],
)
def test__convert_errno_parm__returns_expected__when__given_valid_arg(value, expected):
    got = _convert_errno_parm(value)
    assert got == expected


def test__convert_errno_parm__raises_exception__when__given_invalid_arg():
    with pytest.raises(AssertionError) as e:
        _convert_errno_parm("bogus")
    assert "'bogus' is not a valid errno name" in str(e)


def test_create_files__creates_a_single_file__when__given_defaults(keywords, tmp_path):
    keywords.create_files(str(tmp_path))
    created_file = tmp_path / "0"
    assert created_file.exists()
    assert created_file.is_file()


def test_directory_entry_should_exist__succeeds__when__dir_is_present(
    keywords,
    tmp_dir,
):
    keywords.directory_entry_should_exist(str(tmp_dir))


def test_directory_entry_should_exist__raises_exception__when__dir_is_missing(
    keywords, tmp_path
):
    missing = tmp_path / "missing"
    with pytest.raises(AssertionError) as e:
        keywords.directory_entry_should_exist(str(missing))
    assert "does not exist" in str(e)


def test_should_be_file__succeeds__when__file_is_present(keywords, tmp_file):
    keywords.should_be_file(str(tmp_file))


def test_should_be_file__raises_exception__when__file_is_missing(keywords, tmp_path):
    missing = tmp_path / "missing"
    with pytest.raises(AssertionError) as e:
        keywords.should_be_file(str(missing))
    assert "is not a file" in str(e)


@pytest.mark.skipif(
    sys.platform == "win32", reason="This test is not applicable on Windows."
)
def test_file_should_be_executable__succeeds__when__file_has_x_mode_bits(
    keywords,
    tmp_file,
):
    tmp_file.chmod(0o755)
    keywords.file_should_be_executable(str(tmp_file))


@pytest.mark.skipif(
    sys.platform == "win32", reason="This test is not applicable on Windows."
)
def test_file_should_be_executable__raises_exception__when__file_has_no_x_mode_bits(
    keywords,
    tmp_file,
):
    tmp_file.chmod(0o644)
    with pytest.raises(AssertionError) as e:
        keywords.file_should_be_executable(str(tmp_file))
    assert "is not executable" in str(e)


def test_should_be_symlink__succeeds__when__symlink_is_present(keywords, tmp_symlink):
    keywords.should_be_symlink(str(tmp_symlink))


def test_should_be_symlink__raises_exception__when__symlink_is_missing(
    keywords, tmp_path
):
    missing = tmp_path / "missing"
    with pytest.raises(AssertionError) as e:
        keywords.should_be_symlink(str(missing))
    assert "is not a symlink" in str(e)


def test_should_not_be_symlink__succeeds__when__file_is_not_a_symlink(
    keywords,
    tmp_file,
):
    keywords.should_not_be_symlink(str(tmp_file))


def test_should_not_be_symlink__succeeds__when__file_is_missing(
    keywords,
    tmp_path,
):
    missing = tmp_path / "missing"
    keywords.should_not_be_symlink(str(missing))


def test_should_not_be_symlink__raise_exception__when__file_is_a_symlink(
    keywords,
    tmp_symlink,
):
    with pytest.raises(AssertionError) as e:
        keywords.should_not_be_symlink(str(tmp_symlink))
    assert "is a symlink" in str(e)


def test_should_be_dir__succeeds__when__dir_is_present(keywords, tmp_dir):
    keywords.should_be_dir(str(tmp_dir))


def test_should_not_be_dir__succeeds__when__dir_is_missing(keywords, tmp_path):
    missing = tmp_path / "missing"
    keywords.should_not_be_dir(str(missing))


def test_should_not_be_dir__succeeds__when__name_is_a_file(keywords, tmp_file):
    keywords.should_not_be_dir(str(tmp_file))


def test_should_not_be_dir__raises_exception__when__name_is_a_dir(keywords, tmp_dir):
    with pytest.raises(AssertionError) as e:
        keywords.should_not_be_dir(str(tmp_dir))
    assert "is a directory" in str(e)


def test_link__creates_hard_link__when__making_new_link(keywords, tmp_file):
    tmp_hardlink = tmp_file.parent / "tmp_hardlink"
    keywords.link(str(tmp_file), str(tmp_hardlink), code_should_be=0)
    assert tmp_hardlink.exists()
    assert tmp_hardlink.is_file()
    assert tmp_hardlink.parent == tmp_file.parent
    assert tmp_hardlink.stat().st_ino == tmp_file.stat().st_ino


def test_link__raises_exception__when__name_is_already_present(keywords, tmp_file):
    bogus = tmp_file.parent / "bogus"
    bogus.touch()
    with pytest.raises(AssertionError) as e:
        keywords.link(str(tmp_file), str(bogus))
    assert "unexpected code" in str(e)


def test_link__code_is_eexist__when__name_is_already_present(keywords, tmp_file):
    bogus = tmp_file.parent / "bogus"
    bogus.touch()
    keywords.link(str(tmp_file), str(bogus), code_should_be=errno.EEXIST)


def test_symlink__creates_symlink_in_same_dir__when__name_is_available(
    keywords, tmp_file
):
    tmp_symlink = tmp_file.parent / "tmp_symlink"
    keywords.symlink(str(tmp_file), str(tmp_symlink), code_should_be=0)
    assert tmp_symlink.exists()
    assert tmp_symlink.is_symlink()


def test_unlink__removes_file__when__file_is_present(keywords, tmp_file):
    keywords.unlink(str(tmp_file))
    assert not tmp_file.exists()


def test_link_count_should_be__returns_2__when__file_has_1_hardlink(keywords, tmp_file):
    keywords.link_count_should_be(str(tmp_file), 1)
    tmp_hardlink = tmp_file.parent / "tmp_hardlink"
    os.link(str(tmp_file), str(tmp_hardlink))
    keywords.link_count_should_be(str(tmp_file), 2)
    keywords.link_count_should_be(str(tmp_hardlink), 2)


def test_inode_should_be_equal__succeeds__when__file_is_linked(keywords, tmp_file):
    tmp_hardlink = tmp_file.parent / "tmp_hardlink"
    os.link(tmp_file, tmp_hardlink)
    keywords.inode_should_be_equal(str(tmp_file), str(tmp_hardlink))


def test_get_inode__returns_file_inode_number__when__file_is_present(
    keywords, tmp_file
):
    ino = keywords.get_inode(tmp_file)
    assert ino != 0
    assert ino == tmp_file.stat().st_ino
