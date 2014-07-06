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
    Non-specific independent helper functions.
"""

import zipfile, json, sys, datetime
from PySide import QtGui, QtCore
import constants as c

def load_ui_icon(name):
    """
        Load an icon from a base icon path.
    """
    file_name = c.extend(c.Graphics_UI_Folder, name)
    return QtGui.QIcon(file_name)

def read_json(file_name):
    with open(file_name, 'r') as file:
        return json.load(file)

def write_json(file_name, value):
    with open(file_name, 'w') as file:
        json.dump(value, file, indent=2, separators=(',', ': '), sort_keys=True)

def log_info(text):
    log_write_entry(sys.stdout, "INFO", text)

def log_warning(text):
    log_write_entry(sys.stdout, "WARNING", text)

def log_error(text, exception=None):
    log_write_entry(sys.stderr, "ERROR", text, exception)
    # in case we send to somewhere else also send it to the standard error output (console)
    if sys.stderr is not sys.__stderr__:
        log_write_entry(sys.__stderr__, "ERROR", text, exception)

def log_write_entry(writer, type, text, exception=None):
    now = datetime.datetime.now()
    header = now.isoformat(" ") + '\t' + type + '\t'

    print(header + text, end='\r\n', file=writer)

    if exception != None:
        print(header + exception, end='\r\n', file=writer)

options = {}

def load_options(file_name):
    global options
    options = read_json(file_name)

    # main window bounding rectangle from list to QRect
    if c.OG_MW_BOUNDS in options:
        rect = options[c.OG_MW_BOUNDS]
        options[c.OG_MW_BOUNDS] = QtCore.QRect(*rect)

def save_options(file_name):
    data = options.copy()

    # main window bounding rectangle fromn QRect to list
    rect = data[c.OG_MW_BOUNDS]
    data[c.OG_MW_BOUNDS] = [rect.x(), rect.y(), rect.width(), rect.height()]

    write_json(file_name, data)

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
        bytes = json.dumps(obj, indent=2, separators=(',', ': ')).encode()
        self.write(name, bytes)

    def __del__(self):
        self.zip.close()

class List2D():
    def __init__(self, dimension):
        # create empty list
        size = 1
        for v in dimension:
            size *= v
        self.array = [0] * size
        # store dimension
        self.dimension = dimension
        self.nx = dimension[0]

    def get(self, x, y):
        index = x + self.nx * y
        return self.array[index]

    def set(self, x, y, v):
        index = x + self.nx * y
        self.array[index] = v

    def dimension(self):
        return self.dimension

class Worker(QtCore.QObject):
    def __init__(self):
        super().__init__()
        self.thread = QtCore.QThread()
        self.moveToThread(self.thread)
        self.thread.start()

    def check_thread(self):
        current_thread = QtCore.QThread.currentThread()
        if current_thread is not self.thread:
            raise RuntimeError('Not running in internal Thread!')

    def kill(self):
        current_thread = QtCore.QThread.currentThread()
        self.thread.quit()
        while self.thread.isRunning():
            current_thread.msleep(10)