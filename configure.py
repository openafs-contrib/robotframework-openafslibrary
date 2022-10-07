#!/usr/bin/env python3

import os
import re

def which(program):
    """Find a program in the PATH or return 'missing'."""
    for path in os.environ['PATH'].split(os.pathsep):
        path = os.path.join(path.strip('"'), program)
        if os.access(path, os.X_OK):
            if ' ' in path:
                path = '"{0}"'.format(path)
            return path
    return 'missing'

def name():
    """Extract our name from the setup.py."""
    setup = open('setup.py').read()
    match = re.search(r'NAME\s*=\s*[\'\"](.*)[\'\"]', setup)
    if match:
        return match.group(1)
    raise ValueError('NAME not found in setup.py.')

NAME = name()
PYTHON = which('python3')
if PYTHON == 'missing':
    PYTHON = which('python')
PIP = which('pip')
INSTALL = 'pip' if PIP != 'missing' else 'setup'

open('Makefile.config', 'w').write("""\
NAME={NAME}
PIP={PIP}
PYTHON={PYTHON}
INSTALL={INSTALL}
""".format(**locals()))
