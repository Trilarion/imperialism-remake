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
    Using Signals of Qt, we refine on the network Client class in lib/network.py. Channels are introduced which have
    names and a signal to connect/disconnect to.
"""

import PyQt5.QtCore as QtCore
import PyQt5.QtNetwork as QtNetwork

from base import constants
import lib.network


class NetworkClient(lib.network.ExtendedTcpSocket):
    """
    Extending the Client class (wrapper around QTcpSocket sending and receiving messages) with channels (see Channel)
    and processing logic, as well as further wrapping the messages (specifying the channel as address).

    The Channel implementation is completely hidden, one just calls the connect/disconnect methods in this class.

    This is kind of a service-subscription pattern and allows for reducing complexity and decoupling of the message
    transport and message processing.
    """

    def __init__(self, socket: QtNetwork.QTcpSocket = None):
        """
        We start with an empty channels list.

        :param socket: A socket if there is one existing already.
        """
        super().__init__(socket)
        self.received.connect(self._process)
        self.channels = {}

    def create_new_channel(self, channel: constants.C):
        """
        Given a new channel name (cannot already exist, otherwise an error will be thrown) creates a channel of
        this name.

        :param channel: Name of the channel.
        """
        if channel in self.channels:
            raise RuntimeError('Channel with this name already existing.')
        self.channels[channel] = Channel()

    def remove_channel(self, channel: constants.C, ignore_not_existing=False):
        """
        Given a channel name, removes this channel if it is existing. Raises an error if not existing and
        ignore_not_existing is not True.

        :param channel: Name of the channel
        :param ignore_not_existing: If True does not raise an error if channel with this name is already existing.
        """
        if channel in self.channels:
            del self.channels[channel]
        elif not ignore_not_existing:
            raise RuntimeError('Channel with this name not existing.')

    def connect_to_channel(self, channel: constants.C, callback: callable):
        """
        Connect a callback to a channel with a specific name.

        As a convenience shortcut, if a channel of this name is not yet existing, creates a new one before.

        :param channel: Name of the channel
        :param callback: A callable
        """
        if channel not in self.channels:
            self.create_new_channel(channel)
        self.channels[channel].received.connect(callback)

    def disconnect_from_channel(self, channel: constants.C, callback: callable):
        """
        Given a channel name (which must exist, otherwise an error is raised) disconnects a callback from this
        channel.

        :param channel: Name of the channel
        :param callback: A callable
        """
        if channel not in self.channels:
            raise RuntimeError('Channel with this name not existing.')
        self.channels[channel].received.disconnect(callback)

    def _process(self, letter):
        """
        A letter (a message) was received from the underlying ExtendedTcpSocket framework. Not intended for outside use.
        Here we assume that it's a dictionary with keys 'channel' and 'content' where the value for key 'channel' is
        the name of the channel and the value of the key 'content' is the message.

        We get the corresponding Channel object and emit its received signal.

        :param letter: The letter that was received
        """
        print('network client received letter: {}'.format(letter))
        channel = letter['channel']

        # do we have receivers in this category
        if channel not in self.channels:
            raise RuntimeError('Received message on channel {} which is not existing.'.format(channel))

        # send to channel and increase channel counter
        self.channels[channel].message_counter += 1
        self.channels[channel].received.emit(self, channel, letter['action'], letter['content'])

        # note: channel with name channel_name may now already not be existing anymore (may be removed during processing)

    def send(self, channel: constants.C, action: constants.M, content=None):
        """
        Given a channel and a action id and optionally a message content wraps them in one dict (a letter) and sends it.

        :param channel: Channel id
        :param action: action id
        :param content: Message content
        """
        # wrap content
        letter = {'channel': channel, 'action': action, 'content': content}

        # send
        super().send(letter)


class Channel(QtCore.QObject):
    """
    Just contains a single signal you can connect/disconnect to/from and which sends a client and a value (the message)
    when emitted. This way many outside parts can subscribe to this channel and using Qt also we can cross thread
    boundaries easily.
    """

    #: signal
    received = QtCore.pyqtSignal(NetworkClient, constants.C, constants.M, object)

    def __init__(self):
        super().__init__()
        self.message_counter = 0
