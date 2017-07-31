# Imperialism remake
# Copyright (C) 2014-16 Trilarion
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
Starts an audio player.
"""

import os, sys

from PyQt5 import QtWidgets

def playlist_index_changed(position):
    print('Next song')
    qt.Notification(window, 'Next song', position_constraint=qt.RelativeLayoutConstraint().center_horizontal().south(20))

if __name__ == '__main__':

    # add source directory to path if needed
    source_directory = os.path.realpath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.path.pardir, os.path.pardir, 'source'))
    if source_directory not in sys.path:
        sys.path.insert(0, source_directory)

    from imperialism_remake.client import audio
    from imperialism_remake.lib import qt

    qt.fix_pyqt5_exception_eating()

    app = QtWidgets.QApplication([])

    window = QtWidgets.QWidget()
    window.show()

    # setup sound system and start playing
    audio.load_soundtrack_playlist()
    print(audio.soundtrack_playlist.mediaCount())
    audio.setup_soundtrack_player()
    audio.soundtrack_playlist.currentIndexChanged.connect(playlist_index_changed)
    audio.soundtrack_player.play()

    app.exec_()
