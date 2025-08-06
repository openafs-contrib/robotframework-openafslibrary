# Copyright (c) 2025, Sine Nomine Associates
# See LICENSE

import pytest

from OpenAFSLibrary.keywords.cache import _CacheKeywords


@pytest.fixture
def keywords():
    return _CacheKeywords()


@pytest.mark.parametrize(
    "using,available,expected",
    [
        (42699, 50000, 50000),
        (9823, 13117814, 13117814),
    ],
)
def test_get_cache_size__parses_fs_getcacheparms_output(
    keywords, process, using, available, expected
):
    process(
        stdout=[
            f"AFS using {using} of the cache's available {available} 1K byte blocks."
        ]
    )
    got = keywords.get_cache_size()
    assert got == expected
