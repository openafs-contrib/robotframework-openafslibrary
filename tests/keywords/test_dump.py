# Copyright (c) 2025, Sine Nomine Associates
# See LICENSE

import pytest
from OpenAFSLibrary.keywords.dump import (
    VolumeDump,
    _DumpKeywords,
)


@pytest.fixture
def keywords():
    return _DumpKeywords()


#
# VolumeDump helper class tests.
#


class Test_VolumeDump:

    def test_create_dump_file(self, tmp_path):
        filename = tmp_path / "test.dump"
        dump = VolumeDump(filename)
        assert dump.file
        assert filename.exists()


#
# Keyword tests.
#


def test_should_be_a_dump_file__succeeds_when_file_is_a_dump(keywords, tmp_path):
    filename = tmp_path / "test.dump"
    keywords.create_dump(filename, size="small")
    assert filename.exists()
    keywords.should_be_a_dump_file(filename)


def test_create_dump__creates_dump_when_contains_is_bogus_acl(keywords, tmp_path):
    filename = tmp_path / "test.dump"
    keywords.create_dump(filename, size="small", contains="bogus-acl")
    assert filename.exists()


def test_create_dump__creates_empty_dump_when_size_is_empty(keywords, tmp_path):
    filename = tmp_path / "test.dump"
    keywords.create_dump(filename, size="empty")
    assert filename.exists()


def test_create_dump__creates_small_dump_when_size_is_small(keywords, tmp_path):
    filename = tmp_path / "test.dump"
    keywords.create_dump(filename, size="small")
    assert filename.exists()


def test_create_dump__raises_value_error_when_size_is_bogus(keywords, tmp_path):
    filename = tmp_path / "test.dump"
    with pytest.raises(ValueError):
        keywords.create_dump(filename, size="bogus")
    assert not filename.exists()
