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
Plays soundtrack music.

soundtrack_player.play/stop
soundtrack_playlist.next/previous
"""

from PyQt5 import QtMultimedia

from imperialism_remake.base import constants
from imperialism_remake.lib import utils, qt

soundtrack_player = None
soundtrack_playlist = None


def load_soundtrack_playlist():
    """
        Loads the play list of the soundtracks and replaces the file name with the full path.

        A playlist is a list where each entry is a list of two strings: file path, title
    """
    global soundtrack_playlist

    # create playlist
    soundtrack_playlist = QtMultimedia.QMediaPlaylist()
    soundtrack_playlist.setPlaybackMode(QtMultimedia.QMediaPlaylist.Loop)

    # read information file
    data = utils.read_as_yaml(constants.SOUNDTRACK_INFO_FILE)

    # add the soundtrack folder to each file name
    for entry in data:
        file = constants.extend(constants.SOUNDTRACK_FOLDER, entry[0])
        url = qt.local_url(file)
        media = QtMultimedia.QMediaContent(url)
        soundtrack_playlist.addMedia(media)


def setup_soundtrack_player():
    """
        Initializes the singleton soundtrack player.
    """
    global soundtrack_player
    global soundtrack_playlist

    soundtrack_player = QtMultimedia.QMediaPlayer()
    soundtrack_player.setPlaylist(soundtrack_playlist)
