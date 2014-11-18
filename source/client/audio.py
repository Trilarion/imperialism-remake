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

"""
    Plays soundtrack music.
"""

from PySide import QtCore
from PySide.phonon import Phonon

from base import constants as c
from lib import utils as u


def is_mime_type_ogg_available():
    """
        Checks if the ogg mime type 'audio/ogg' is contained in the list of available mime types
    """
    available_types = Phonon.BackendCapabilities.availableMimeTypes()
    return 'audio/ogg' in available_types


def load_soundtrack_playlist():
    """
        Loads the play list of the soundtracks and replaces the file name with the full path, then returns the list.

        A playlist is a list where each entry is a list of two strings: filepath, title
    """
    playlist = u.read_as_yaml(c.Soundtrack_Playlist)
    # add the soundtrack folder to each file name
    for entry in playlist:
        entry[0] = c.extend(c.Soundtrack_Folder, entry[0])
    return playlist


class Player(QtCore.QObject):
    """
        Mostly a wrapper around Phonon.MediaObject this class can play a song or a list of songs while also giving
        some hooks for updating the display or seeking and playing only a part of a file.

        Public attribute: auto_rewind (True means that after the playlist has finished starts again´)
    """

    next = QtCore.Signal(str)

    def __init__(self, parent=None):
        """
            Setups the sound system.
            Ticks are not implemented because we don't need them but in case we do it is fairly simple.

            TODO what if there are no sound capabilities, is this sure at this point that we have them?
        """
        super().__init__(parent=parent)

        # set up audio output and media object and connect both
        self.audio_output = Phonon.AudioOutput(Phonon.MusicCategory, self)
        self.media_object = Phonon.MediaObject(self)
        Phonon.createPath(self.media_object, self.audio_output)

        # connect signal of media object
        self.media_object.stateChanged.connect(self.state_changed)
        self.media_object.aboutToFinish.connect(self.before_finish)

        # default values
        self.playlist = []
        self.auto_rewind = True

    def set_playlist(self, playlist):
        """
            Sets a new playlist. Stops the playback in any case.
        """
        self.stop()
        self.playlist = playlist
        self.song_index = 0

    def start(self):
        """
            If a playlist has been set, start playing with the next song.
        """
        if self.playlist:
            # schedule next and start playing
            self.schedule_next()
            self.media_object.play()

    def stop(self):
        """
            Stop playing. Should not do anything if we already stopped before.
        """
        self.media_object.stop()

    def schedule_next(self):
        """
            Take the next song from the playlist, send it to the media object, emit the next signal.
        """
        if self.playlist:
            next_source = self.playlist[self.song_index][0]
            self.media_object.enqueue(Phonon.MediaSource(next_source))

            next_title = self.playlist[self.song_index][1]
            self.next.emit(next_title)

    def before_finish(self):
        """
            If we are not yet at the end of the playlist or if auto_rewind is True, schedule the next song.
            Otherwise do nothing.
        """
        if self.auto_rewind:
            self.song_index = (self.song_index + 1) % len(self.playlist)
            self.schedule_next()
        elif self.song_index + 1 < len(self.playlist):
            self.song_index += 1
            self.schedule_next()

    def state_changed(self, new_state, old_state):
        """
            The state (Phonon.State) changed.

            This can mean the state is now playing, paused, stopped.. or an error occurred.
            We only process errors

            See Phonon.MediaObject.stateChanged
        """
        # print('time {} state {} to {}'.format(time.clock(), oldState, newState))
        if new_state == Phonon.ErrorState:
            print(self.media_object.errorType())
            print(self.media_object.errorString())
            # TODO turn off music and tell the user about the error