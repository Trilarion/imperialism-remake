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
from lib.network import Client


class Channel(QtCore.QObject):
    """
        Just contains a single signal you can connect/disconnect to/from.
    """

    received = QtCore.Signal(object, object)

    def __init__(self):
        super().__init__()
        self.message_counter = 0


class NetworkClient(Client):

    def __init__(self):
        super().__init__()
        self.received.connect(self.process)
        self.channels = {}

    def create_new_channel(self, channel_name):
        if channel_name in self.channels:
            raise RuntimeError('Channel with this name already existing.')
        self.channels[channel_name] = Channel()

    def remove_channel(self, channel_name, ignore_not_existing=False):
        if channel_name in self.channels:
            del self.channels[channel_name]
        elif not ignore_not_existing:
            raise RuntimeError('Channel with this name not existing.')


    def connect_to_channel(self, channel_name, callable):
        if channel_name not in self.channels:
            self.create_new_channel(channel_name)
        self.channels[channel_name].received.connect(callable)

    def disconnect_from_channel(self, channel_name, callable):
        if channel_name not in self.channels:
            raise RuntimeError('Channel with this name not existing.')
        self.channels[channel_name].received.disconnect(callable)

    def process(self, message):
        channel_name = message['channel']

        # do we have receivers in this category
        if channel_name not in self.channels:
            raise RuntimeError('Channel with this name not existing.')

        # send to channel and increase counter
        self.channels[channel_name].message_counter += 1
        self.channels[channel_name].received.emit(self, message['content'])

        # channel_name may now already not be existing anymore

    def send(self, channel_name, message=None):
        # wrap content
        letter = {
            'channel': channel_name,
            'content': message
        }
        # send
        super().send(letter)
