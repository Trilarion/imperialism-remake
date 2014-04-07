# Omnitux 2 - educational activities based upon multimedia elements
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

import datetime
import os
import sys

def info(text, exception=None):
    log_entry(sys.stdout, "INFO", text, exception)


def error(text, exception=None):
    log_entry(sys.stderr, "ERROR", text, exception)


def log_entry(writer, type, text, exception):
    now = datetime.datetime.now()
    header = now.isoformat(" ") + '\t' + type + '\t'

    print(header + text, end='\r\n', file=writer)

    if exception != None:
        print(header + exception, end='\r\n', file=writer)


def resource(*args):
    # create path
    path = os.path.join('.', 'data', *args)
    # check for existence
    if not os.path.isfile(path):
        error('file {} is not existing'.format(path))
        raise IOError()
    return path