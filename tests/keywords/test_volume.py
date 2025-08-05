# Copyright (c) 2025, Sine Nomine Associates
# See LICENSE

import pytest

from unittest.mock import Mock
from OpenAFSLibrary.keywords.volume import (
    socket,
    examine_path,
    get_volume_entry,
    get_parts,
    release_parent,
    _zap_volume,
    _VolumeKeywords,
)


@pytest.fixture
def keywords():
    return _VolumeKeywords()


def test_examine_path__parses_fs_examine_output(process):
    path = "/afs/example.com/test"
    expected = {
        "path": "/afs/example.com/test",
        "fid": "536871188.1.1",
        "vid": 536871188,
        "name": "test",
        "quota": 0,
        "blocks": 5313118,
        "part": {"free": 861483100, "used": 211730344, "total": 1073213444},
    }
    process(
        expected_args=["fs", "examine", "-path", "/afs/example.com/test"],
        stdout=[
            "File /afs/example.com/test (536871188.1.1) contained in volume 536871188",
            "Volume status for vid = 536871188 named test",
            "Current disk quota is unlimited",
            "Current blocks used are 5313118",
            "The partition has 861483100 blocks available out of 1073213444",
        ],
    )
    info = examine_path(path)
    assert info == expected


def test_get_volume_entry__parses_vos_listvldb_output(process):
    name = "public"
    expected = {
        "locked": False,
        "name": f"{name}",
        "rw": "536871326",
        "ro": "536871327",
        "server": "198.44.193.47",
        "part": "a",
        "rosites": [("198.44.193.51", "b"), ("198.44.193.47", "a")],
    }
    process(
        expected_args=[
            "vos",
            "listvldb",
            "-name",
            name,
            "-quiet",
            "-noresolve",
            "-noauth",
        ],
        stdout=[
            "",
            f"{name}",
            "    RWrite: 536871326     ROnly: 536871327",
            "    number of sites -> 3",
            "       server 198.44.193.47 partition /vicepa RW Site",
            "       server 198.44.193.51 partition /vicepb RO Site",
            "       server 198.44.193.47 partition /vicepa RO Site",
        ],
    )
    info = get_volume_entry(name)
    assert info == expected


def test_get_parts__parses_vos_listpart_output(process):
    server = "fs.example.org"
    process(
        expected_args=["vos", "listpart", server],
        stdout=[
            "The partitions on the server are:",
            "    /vicepa     /vicepb     /vicepc ",
            "Total: 3",
        ],
    )
    parts = get_parts(server)
    assert parts == ["a", "b", "c"]


def test_release_parent__runs_fs_and_vos(process):

    process(
        expected_args=["fs", "examine", "-path", "/afs/example.org"],
        stdout=[
            "File /afs/example.org (536870916.1.1) contained in volume 536870916",
            "Volume status for vid = 536870916 named root.cell.readonly",
            "Current disk quota is 10000",
            "Current blocks used are 14",
            "The partition has 506298812 blocks available out of 1073213444",
        ],
    )
    process(
        expected_args=[
            "vos",
            "listvldb",
            "-name",
            "536870916",
            "-quiet",
            "-noresolve",
            "-noauth",
        ],
        stdout=[
            "",
            "root.cell",
            "    RWrite: 536870915     ROnly: 536870916",
            "    number of sites -> 4",
            "       server 198.44.193.47 partition /vicepa RW Site",
            "       server 198.44.193.51 partition /vicepb RO Site",
            "       server 198.44.193.47 partition /vicepa RO Site",
            "       server 198.44.193.48 partition /vicepa RO Site",
        ],
    )
    process(
        expected_args=["vos", "release", "root.cell", "-verbose"],
        stdout=[
            "",
            "root.cell",
            "    RWrite: 536870915     ROnly: 536870916",
            "    number of sites -> 4",
            "       server afs03.example.org partition /vicepa RW Site",
            "       server afs07.example.org partition /vicepb RO Site",
            "       server afs03.example.org partition /vicepa RO Site",
            "       server afs04.example.org partition /vicepa RO Site",
            "This is a complete release of volume 536870915",
            "Re-cloning permanent RO volume 536870916 ... done",
            "Getting status of parent volume 536870915... done",
            "Starting transaction on RO clone volume 536870916... done",
            "Setting volume flags for volume 536870916... done",
            "Ending transaction on volume 536870916... done",
            "Replacing VLDB entry for root.cell... done",
            "Starting transaction on cloned volume 536870916... done",
            "Updating existing ro volume 536870916 on afs07.example.org ...",
            "Starting ForwardMulti from 536870916 to 536870916 on afs07.example.org (as of Fri May  3 19:45:46 2013).",
            "Updating existing ro volume 536870916 on afs04.example.org ...",
            "Starting ForwardMulti from 536870916 to 536870916 on afs04.example.org (as of Fri May  3 19:45:46 2013).",
            "updating VLDB ... done",
            "Released volume root.cell successfully",
        ],
    )
    process(
        expected_args=["fs", "checkvolumes"],
        stdout=["All volumeID/name mappings checked."],
    )
    release_parent("/afs/example.org/public")


def test__zap_volume__runs_vos_zap(process):
    name = "test"
    server = "fs1.example.org"
    part = "z"
    process(
        expected_args=["vos", "zap", "-id", name, "-server", server, "-part", part],
    )
    _zap_volume(name, server, part)


def test_create_volume__creates_volume_when_default_args_given(
    keywords, process, monkeypatch
):
    name = "test"
    hostname = "fs1.example.org"
    volid = "536882946"
    monkeypatch.setattr(socket, "gethostname", Mock(return_value=hostname))

    process(
        expected_args=[
            "vos",
            "create",
            "-server",
            hostname,
            "-partition",
            "a",
            "-name",
            name,
            "-m",
            "0",
            "-verbose",
        ],
        stdout=[
            f"Volume {name} 536882946 created and brought online",
            f"Created the VLDB entry for the volume {name} 536882946",
            f"Volume {volid} created on partition /vicepa of {hostname}",
        ],
    )
    got = keywords.create_volume(name)
    assert got == volid


def test_remove_volume__deletes_volume_when_present(keywords, process):
    print()
    name = "test"
    server = "fs1.example.org"
    process(
        expected_args=[
            "vos",
            "listvldb",
            "-name",
            name,
            "-quiet",
            "-noresolve",
            "-noauth",
        ],
        stdout=[
            "",
            f"{name} ",
            "    RWrite: 536874630 ",
            "    number of sites -> 1",
            "       server 198.44.193.51 partition /vicepa RW Site ",
        ],
    )
    process(
        expected_args=["vos", "remove", "-id", name],
        stdout=[f"Volume 536874630 on partition /vicepa server {server} deleted"],
    )
    process(
        expected_args=["fs", "checkvolumes"],
        stdout=["All volumeID/name mappings checked."],
    )
    keywords.remove_volume(name)


def test_volume_should_not_exist__succeeds_when_volume_is_not_present(
    keywords, process
):
    name = "test"
    process(
        expected_args=[
            "vos",
            "listvldb",
            "-name",
            name,
            "-quiet",
            "-noresolve",
            "-noauth",
        ],
        code=1,
        stderr=["VLDB: no such entry"],
    )
    keywords.volume_should_not_exist(name)


def test_volume_location_matches__succeeds_when_volume_resides_on_given_site(
    keywords, process, monkeypatch
):
    name = "test"
    address = "198.44.193.47"
    server = "fs3.example.org"
    part = "b"
    volid = "536871188"
    monkeypatch.setattr(socket, "gethostbyname", Mock(return_value=address))

    process(
        expected_args=[
            "vos",
            "listvldb",
            "-name",
            name,
            "-quiet",
            "-noresolve",
            "-noauth",
        ],
        stdout=[
            "",
            f"{name} ",
            f"    RWrite: {volid}     Backup: 536871190 ",
            "    number of sites -> 1",
            f"       server {address} partition /vicepb RW Site ",
        ],
    )
    process(
        expected_args=[
            "vos",
            "listvol",
            "-server",
            "198.44.193.47",
            "-partition",
            "b",
            "-fast",
            "-noauth",
            "-quiet",
        ],
        stdout=[
            "536870942 ",
            "536870996 ",
            "536871020 ",
            f"{volid} ",
            "536871191 ",
            "536871221 ",
            "536871230 ",
        ],
    )

    keywords.volume_location_matches(name, server, part)


def test_volume_should_be_locked__fails_when_volume_is_not_locked(keywords, process):
    name = "test"
    process(
        expected_args=[
            "vos",
            "listvldb",
            "-name",
            name,
            "-quiet",
            "-noresolve",
            "-noauth",
        ],
        stdout=[
            "",
            f"{name} ",
            "    RWrite: 536871188     Backup: 536871190 ",
            "    number of sites -> 1",
            "       server 198.44.193.47 partition /vicepb RW Site ",
        ],
    )
    with pytest.raises(AssertionError) as e:
        keywords.volume_should_be_locked(name)
    assert f"Volume '{name}' is not locked." in str(e)


def test_volume_should_be_unlocked__success_when_volume_is_not_locked(
    keywords, process
):
    name = "test"
    process(
        expected_args=[
            "vos",
            "listvldb",
            "-name",
            name,
            "-quiet",
            "-noresolve",
            "-noauth",
        ],
        stdout=[
            "",
            f"{name} ",
            "    RWrite: 536871188     Backup: 536871190 ",
            "    number of sites -> 1",
            "       server 198.44.193.47 partition /vicepb RW Site ",
        ],
    )
    keywords.volume_should_be_unlocked(name)


def test_get_volume_id__returns_volume_id(keywords, process):
    name = "test"
    volid = "536871188"
    process(
        expected_args=[
            "vos",
            "listvldb",
            "-name",
            name,
            "-quiet",
            "-noresolve",
            "-noauth",
        ],
        stdout=[
            "",
            f"{name} ",
            "    RWrite: 536871188     Backup: 536871190 ",
            "    number of sites -> 1",
            "       server 198.44.193.47 partition /vicepb RW Site ",
            "",
        ],
    )
    got = keywords.get_volume_id(name)
    assert got == volid
