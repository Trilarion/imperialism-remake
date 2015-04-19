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

from PySide import QtGui

from client import audio
import lib.graphics as g


def show_notification(text):
    text = 'Playing {}'.format(text)
    g.Notification(window, text, positioner=g.Relative_Positioner().center_horizontal().south(20))

app = QtGui.QApplication([])

window = QtGui.QWidget()
window.show()

playlist = audio.load_soundtrack_playlist()

player = audio.Player()
player.next.connect(show_notification)
player.set_playlist(playlist)
player.start()
app.exec_()
