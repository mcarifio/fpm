"""Main module."""

import sys
from . import cli


# PYTHONPATH=${pkgdag_root} python -m pkgdag # treat pkgdag as a module but run at the command line\
# This approach allows for running with pipx or
# python -m pip install -U pip
# python -m pip install -U pkgdag # depends on the location
# python -m pkgdag ${cmd} ${switches} ${args}

if "__main__" == __name__:
    cli.dispatch(sys.argv)
