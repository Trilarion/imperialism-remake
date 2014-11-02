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

from lib.network import Client
import constants as c

class NetworkClient(Client):

    def __init__(self):
        super().__init__()
        self.received.connect(self.process)
        self.receivers = {}
        self.id = -1

    def register_receiver(self, category, listener):
        if category not in self.receivers:
            self.receivers[category] = []
        self.receivers[category].append(listener)

    def unregister_receiver(self, category, listener):
        if listener in self.receivers[category]:
            self.receivers[category].remove(listener)
        else:
            raise RuntimeError('Receiver unknown.')

    def process(self, message):
        # convert signature
        message['signature'] = [c.MsgID(x) for x in message['signature']]

        # get category
        category = message['signature'][0]

        # call all receivers until one returns True or there are None left
        if category in self.receivers:
            for receiver in self.receivers[category]:
                if receiver(self, message) is True:
                    return
        # either there was no listener in this category or no listener returned true


    def send(self, signature, message=None):
        if message is None:
            message = {}
        message['signature'] = [x.value for x in signature]
        super().send(message)
