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
try:
    from PySide.phonon import Phonon
except ImportError:
    print('Phonon not available')
    # TODO should turn off music and tell the user why

def is_mime_type_ogg_available():
    """
        Checks if the ogg mime type 'audio/ogg' is contained in the list of available mime types
    """
    available_types = Phonon.BackendCapabilities.availableMimeTypes()
    return 'audio/ogg' in available_types

class Player(QtCore.QObject):
    """
        Mostly a wrapper around Phonon.MediaObject this class can play a song or a list of songs while also giving
        some hooks for updating the display or seeking and playing only a part of a file.
    """

    title_changed = QtCore.Signal(str)

    def __init__(self):
        """

        """
        super().__init__()
        self.audio_output = Phonon.AudioOutput(Phonon.MusicCategory, self)
        self.media_object = Phonon.MediaObject(self)
        Phonon.createPath(self.media_object, self.audio_output)

        # some connections
        self.media_object.setTickInterval(500) # every second it updates the time
        self.media_object.tick.connect(self.tick)
        self.media_object.stateChanged.connect(self.stateChanged)

        # connections
        self.media_object.metaDataChanged.connect(self.update_title)

    def tick(self, time):
        """

        """
        pass

    def update_title(self):
        """
            According to the Phonon documentation meta data is only reliably existing after metaDataChanged was emitted.
            Here we extract the title and re-emit a signal containing the title.
        """
        title = self.media_object.metaData('TITLE')
        self.title_changed.emit(title)

    def start(self):
        self.media_object.play()

    def seek(self):
        self.media_object.seek(20000)

    def stateChanged(self, newState, oldState):
        """
            The state (Phonon.State) changed.

            This can mean the state is now playing, paused, stopped.. or an error occurred.
            We only process errors

            See Phonon.MediaObject.stateChanged
        """
        if newState == Phonon.ErrorState:
            print(self.media_object.errorType())
            print(self.media_object.errorString())
            # TODO turn off music and tell the user about the error
