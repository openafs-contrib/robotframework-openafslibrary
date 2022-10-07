#!/usr/bin/env python3
import os

def version():
    """Determine the version number from the most recent git tag.

    Convert the version string from git describe into a PEP 440 compliant
    version string by using the '+' separator to append a "local version"
    identifier.

        $ git describe
        v0.7.2-11-gf0c8024
        $ python3 version.py
        VERSION = '0.7.2+11.gf0c8024'
    """
    try:
        with os.popen('git describe') as f:
            version = f.read().strip().lstrip('v').replace('-', '+', 1).replace('-', '.')
    except Exeception:
        version = '0.0.0'
    return version

if __name__ == '__main__':
    print("VERSION = '%s'" % version())
