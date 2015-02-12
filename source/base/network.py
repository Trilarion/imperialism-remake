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
    Using Signals of Qt, we refine on the network Client class in lib/network.py. Channels are introduced which have
    names and a signal to connect/disconnect to.
"""

from PySide import QtCore

from lib.network import Client


class NetworkClient(Client):
    """
        Extending the Client class (wrapper around QTcpSocket sending and receiving messages) with channels (see Channel
        below) and processing logic, as well as further wrapping the messages (specifying the channel as address).

        The Channel implementation is completely hidden, one just calls the connec/disconnect methods in this class.

        This is kind of a service-subscription pattern and allows for reducing complexity and decoupling of the message
        transport and message processing.
    """

    def __init__(self):
        """
            We start with an empty channels list.
        """
        super().__init__()
        self.received.connect(self.process)
        self.channels = {}

    def create_new_channel(self, channel_name):
        """
            Given a new channel name (cannot already exist, otherwise an error will be thrown) creates a channel of
            this name.
        """
        if channel_name in self.channels:
            raise RuntimeError('Channel with this name already existing.')
        self.channels[channel_name] = Channel()

    def remove_channel(self, channel_name, ignore_not_existing=False):
        """
            Given a channel name, removes this channel if it is existing. Throws an error if not existing and
            ignore_not_existing is not True.
        """
        if channel_name in self.channels:
            del self.channels[channel_name]
        elif not ignore_not_existing:
            raise RuntimeError('Channel with this name not existing.')

    def connect_to_channel(self, channel_name, callable):
        """
            Connect a callable to a channel with a specific name.

            As a convenience shortcut, if a channel of this name is not yet existing, creates a new one before.
        """
        if channel_name not in self.channels:
            self.create_new_channel(channel_name)
        self.channels[channel_name].received.connect(callable)

    def disconnect_from_channel(self, channel_name, callable):
        """
            Given a channel name (which must exist, otherwise an error is raised) disconnects a callable from this
            channel.
        """
        if channel_name not in self.channels:
            raise RuntimeError('Channel with this name not existing.')
        self.channels[channel_name].received.disconnect(callable)

    def process(self, message):
        """
            A message was received from the underlying Client framework. It's a dictionary with keys 'channel' and
            'content'.

            Get the corresponding Channel object and emit its received signal.
        """
        channel_name = message['channel']

        # do we have receivers in this category
        if channel_name not in self.channels:
            raise RuntimeError('Channel with this name not existing.')

        # send to channel and increase counter
        self.channels[channel_name].message_counter += 1
        self.channels[channel_name].received.emit(self, message['content'])

        # note: channel with name channel_name may now already not be existing anymore (may be removed during processing)

    def send(self, channel_name, message=None):
        """
            Given a channel name and a message (optional) wraps them in one dict (a letter) and send it.
        """
        # wrap content
        letter = {
            'channel': channel_name,
            'content': message
        }
        # send
        super().send(letter)


class Channel(QtCore.QObject):
    """
        Just contains a single signal you can connect/disconnect to/from and which sends a client and a dict (the message)
        when emitted. This way many outside parts can subscribe to this channel and using Qt also we can cross Thread
        boundaries easily.
    """

    received = QtCore.Signal(NetworkClient, dict)

    def __init__(self):
        super().__init__()
        self.message_counter = 0