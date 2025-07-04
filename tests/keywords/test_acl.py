# Copyright (c) 2025, Sine Nomine Associates
# See LICENSE

from OpenAFSLibrary.keywords.acl import normalize, AccessControlList

import pprint


def test_normalize():
    cases = [
        ("", ""),
        ("r", "r"),
        ("lr", "rl"),
        ("rlidwka", "rlidwka"),
        ("adiklrw", "rlidwka"),
        ("abcd", None),
    ]
    for x, y in cases:
        try:
            z = "".join(normalize(list(x)))
        except Exception:
            assert y is None, "expected exception: x='%s'" % (x)
        if y:
            assert z == y, "expected='%s', got='%s'" % (y, z)


def test_acl_add():
    cases = [
        "system:administrators rlidwka",
        "system:anyuser rl",
        "user1 rl",
        "user2 rl",
        "user2 rwl",
        "user2 -l",
        "user3 +rlidwk",
        "user4 none",
        "user5 read",
        "user6 write",
        "user7 -write",
    ]
    expected = """\
{'system:administrators': ('rlidwka', ''),
 'system:anyuser': ('rl', ''),
 'user1': ('rl', ''),
 'user2': ('rlw', 'l'),
 'user3': ('rlidwk', ''),
 'user5': ('rl', ''),
 'user6': ('rlidwk', ''),
 'user7': ('', 'rlidwk')}\
"""
    a = AccessControlList()
    for case in cases:
        name, rights = case.split()
        a.add(name, rights)

    got = pprint.pformat(a.acls)
    assert got == expected


def test_acl_from_args():
    t = [
        "system:administrators rlidwka",
        "system:anyuser rl",
        "user1 rl",
        "user2 rl",
        "user2 rwl",
        "user2 -l",
        "user3 +rlidwk",
        "user4 none",
    ]
    expected = """\
{'system:administrators': ('rlidwka', ''),
 'system:anyuser': ('rl', ''),
 'user1': ('rl', ''),
 'user2': ('rlw', 'l'),
 'user3': ('rlidwk', '')}\
"""
    a = AccessControlList.from_args(*t)
    got = pprint.pformat(a.acls)
    assert got == expected


def test_acl_contains():
    t = [
        "system:administrators rlidwka",
        "system:anyuser rl",
        "user1 rl",
        "user2 rl",
        "user2 rwl",
        "user2 -l",
        "user3 +rlidwk",
        "user4 none",
    ]
    a = AccessControlList.from_args(*t)
    assert a.contains("system:administrators", "rlidwka")
    assert a.contains("system:anyuser", "rl")
    assert a.contains("user1", "+rl")
    assert a.contains("user2", "rlw")
    assert a.contains("user2", "-l")
    assert a.contains("user3", "+rlidwk")
    assert not a.contains("user4", "none")
