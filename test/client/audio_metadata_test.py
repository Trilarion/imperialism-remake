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

from PySide import QtCore
from PySide.phonon import Phonon
from client import audio

def state_changed(newState, oldState):
    print('state change {} : {}'.format(oldState, newState))
    if newState == Phonon.ErrorState:
        print('error {} : {}'.format(media_object.errorType(), media_object.errorString()))

def meta_changed():
    meta_data = media_object.metaData()
    print('meta change = {}'.format(meta_data))

if __name__ == '__main__':
    app = QtCore.QCoreApplication([])
    app.setApplicationName('test')

    audio_output = Phonon.AudioOutput(Phonon.MusicCategory)
    media_object = Phonon.MediaObject()
    Phonon.createPath(media_object, audio_output)

    media_object.metaDataChanged.connect(meta_changed)
    media_object.stateChanged.connect(state_changed)

    playlist = audio.load_soundtrack_playlist()
    source = Phonon.MediaSource(playlist[0][0])
    media_object.setCurrentSource(source)
    media_object.play()

    QtCore.QTimer.singleShot(5000, app.quit)
    app.exec_()
