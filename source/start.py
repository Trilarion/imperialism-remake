# Imperialism remake
# Copyright (C) 2014 Trilarion
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

# test for python version
import sys
if sys.version_info < (3, 3):
    raise RuntimeError('Python version must be 3.3 at least.')

# test for existence of PySide
try:
    from PySide import QtCore
except ImportError:
    raise RuntimeError('PySide must be installed.')

# get constants and log up and running
import tools as t

# test for phonon availability
try:
    from PySide.phonon import Phonon
except ImportError:
    t.log_error('Phonon backend not available, no sound.')
    # TODO set mute in options

# now we can safely assume that the environment is good to us
# and we simply start the client
from client import setup
setup.start()
