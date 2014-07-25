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

from PySide import QtGui, QtCore
from client import audio
import lib.graphics as g, tools as t

def show_notification(text):
    t.thread_status('notification')
    text = 'Playing {}'.format(text)
    g.Notification(window, text, positioner=g.Relative_Positioner().centerH().south(20))

t.thread_status('main')

app = QtGui.QApplication([])

window = QtGui.QWidget()
window.show()

playlist = audio.load_soundtrack_playlist()

player = audio.Player()
player.next.connect(show_notification)
player.set_playlist(playlist)
player.start()
QtCore.QTimer.singleShot(0, lambda: t.thread_status('qt'))
app.exec_()
