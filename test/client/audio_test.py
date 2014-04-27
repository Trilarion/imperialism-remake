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

from PySide import QtCore, QtGui
from client import audio

if __name__ == '__main__':
    app = QtGui.QApplication([])

    window = QtGui.QWidget()
    window.show()

    playlist = audio.load_soundtrack_playlist()

    player = audio.Player()
    player.song_title.connect(print)
    player.set_playlist(playlist)
    player.start()

    app.exec_()
