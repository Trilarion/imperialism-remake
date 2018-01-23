# Imperialism remake
# Copyright (C) 2016 Trilarion
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

"""
PyQt/Qt versions
"""

from PyQt5.QtCore import QT_VERSION_STR, PYQT_VERSION_STR
from sip import SIP_VERSION_STR

print("QT   version: {}".format(QT_VERSION_STR))
print("PyQt version: {}".format(PYQT_VERSION_STR))
print("SIP  version: {}".format(SIP_VERSION_STR))