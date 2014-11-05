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
from base import constants as c

from lib.network import Client


class NetworkClient(Client):

    def __init__(self):
        super().__init__()
        self.received.connect(self.process)
        self.services = {}
        self.id = -1

    def add_service(self, id, service):
        if id in self.services:
            raise RuntimeError('Already a service with this id registered.')
        self.services[id] = service

    def remove_service(self, id):
        self.services.pop(id)

    def process(self, message):
        # convert signature
        message['id'] = c.MsgIDs(message['id'])
        id = message['id']

        # do we have receivers in this category
        if id not in self.services:
            raise RuntimeError('No suitable service for this id.')

        # execute service with message
        response = self.services[id](self, message)

        # if return value is true, remove service from services list
        if response is True:
            self.services.pop(id)

    def send(self, id, message=None):
        if message is None:
            message = {}
        # need to convert enum to int (cannot be serialized)
        message['id'] = id.value
        super().send(message)
