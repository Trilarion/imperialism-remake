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

import json

from PySide import QtCore
from PySide.phonon import Phonon
import constants as c

def is_mime_type_ogg_available():
    """
        Checks if the ogg mime type 'audio/ogg' is contained in the list of available mime types
    """
    available_types = Phonon.BackendCapabilities.availableMimeTypes()
    return 'audio/ogg' in available_types

def load_soundtrack_playlist():
    """

    """
    file = open(c.Soundtrack_Playlist, 'r')
    playlist = json.load(file)
    # add the soundtrack folder to each file name
    for entry in playlist:
        entry[0] = c.extend(c.Soundtrack_Folder, entry[0])
    return playlist

class Player(QtCore.QObject):
    """
        Mostly a wrapper around Phonon.MediaObject this class can play a song or a list of songs while also giving
        some hooks for updating the display or seeking and playing only a part of a file.
    """

    song_title = QtCore.Signal(str)

    def __init__(self):
        """

            Ticks are not implemented because we don't need them but in case we do it is fairly simple.

        """
        super().__init__()

        # set up audio output and media object and connect both
        self.audio_output = Phonon.AudioOutput(Phonon.MusicCategory, self)
        self.media_object = Phonon.MediaObject(self)
        Phonon.createPath(self.media_object, self.audio_output)

        # connect signal of media object
        self.media_object.stateChanged.connect(self.state_changed)
        self.media_object.aboutToFinish.connect(self.before_finish)

        # default values
        self.playlist = None
        self.auto_rewind = True

    def set_playlist(self, playlist):
        """
            Stops the playback in any case
        """
        self.stop()
        self.playlist = playlist
        self.song_index = 0

    def set_auto_rewind(self, auto_rewind):
        """
         auto_rewind (bool)
        """
        self.auto_rewind = auto_rewind

    def start(self):
        if self.playlist:
            # schedule next
            self.schedule_next()

            # self.media_object.play()
            QtCore.QMetaObject.invokeMethod(self.media_object, 'play')

    def stop(self):
        self.media_object.stop()

    def schedule_next(self):
        """

        """
        next_source = self.playlist[self.song_index][0]
        # print(next_source)
        self.media_object.enqueue(Phonon.MediaSource(next_source))

        next_title = self.playlist[self.song_index][1]
        self.song_title.emit(next_title)

    def before_finish(self):
        if self.auto_rewind:
            self.song_index = (self.song_index + 1) % len(self.playlist)
            self.schedule_next()
        elif self.song_index + 1 < len(self.playlist):
            self.song_index += 1
            self.schedule_next()

    def state_changed(self, newState, oldState):
        """
            The state (Phonon.State) changed.

            This can mean the state is now playing, paused, stopped.. or an error occurred.
            We only process errors

            See Phonon.MediaObject.stateChanged
        """
        # print('time {} state {} to {}'.format(time.clock(), oldState, newState))
        if newState == Phonon.ErrorState:
            print(self.media_object.errorType())
            print(self.media_object.errorString())
            # TODO turn off music and tell the user about the error