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

def version():
    """Determine the version number from the most recent git tag."""
    version = os.popen('git describe').read() or '0.0.0'
    version = version.lstrip('v').strip()
    version = version.replace('-', '+', 1)
    version = version.replace('-', '.')
    return version

NAME = name()
VERSION = version()
PYTHON = which('python3')
if PYTHON == 'missing':
    PYTHON = which('python')
PIP = which('pip')
INSTALL = 'pip' if PIP != 'missing' else 'setup'

open('Makefile.config', 'w').write("""\
NAME={NAME}
VERSION={VERSION}
PIP={PIP}
PYTHON={PYTHON}
INSTALL={INSTALL}
""".format(**locals()))
