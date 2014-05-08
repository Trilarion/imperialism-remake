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

import zipfile, json, sys, datetime
from PySide import QtGui
import constants as c

def load_ui_icon(name):
    """
        Load an icon from a base icon path.
    """
    file_name = c.extend(c.Graphics_UI_Folder, name)
    return QtGui.QIcon(file_name)

def log_info(text, exception=None):
    log_write_entry(sys.stdout, "INFO", text, exception)


def log_error(text, exception=None):
    log_write_entry(sys.stderr, "ERROR", text, exception)


def log_write_entry(writer, type, text, exception):
    now = datetime.datetime.now()
    header = now.isoformat(" ") + '\t' + type + '\t'

    print(header + text, end='\r\n', file=writer)

    if exception != None:
        print(header + exception, end='\r\n', file=writer)

class Options():
    def __init__(self):
        self.options = {}

    def load(self):
        with open(c.Options_File, 'r') as f:
            self.options = json.load(f)

    def save(self, file):
        with open(c.Options_File, 'w') as f:
            json.dump(self.options, f, indent=2, separators=(',', ': '))

    def get(self, key):
        return self.options[key]

    def set(self, key, value):
        self.options[key] = value

# create the single options object, load options and send the first log message
options = Options()
options.load()
log_info('options loaded from user folder ({})'.format(c.User_Folder))

class ZipArchiveReader():
    def __init__(self, file):
        self.zip = zipfile.ZipFile(file, mode='r')

    def read(self, name):
        return self.zip.read(name)

    def read_as_json(self, name):
        bytes = self.read(name)
        obj = json.loads(bytes.decode())
        return obj

    def __del__(self):
        self.zip.close()

class ZipArchiveWriter():
    def __init__(self, file):
        self.zip = zipfile.ZipFile(file, mode='w', compression=zipfile.ZIP_DEFLATED)

    def write(self, name, bytes):
        self.zip.writestr(name, bytes)

    def write_json(self, name, obj):
        bytes = json.dumps(obj).encode()
        self.write(name, bytes)

    def __del__(self):
        self.zip.close()