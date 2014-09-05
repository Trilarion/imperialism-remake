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
    Non-specific independent helper functions. Do not depend on any other part of the project except on the constants.
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
    """
        Read JSON struct from file
    """
    with open(file_name, 'r') as file:
        return json.load(file)

def write_json(file_name, value):
    """
        Writes JSON struct with a bit custom formatting to a file.
    """
    with open(file_name, 'w') as file:
        json.dump(value, file, indent=2, separators=(',', ': '), sort_keys=True)

def log_info(text):
    """
        Prints a INFO message to stdout.
    """
    log_write_entry(sys.stdout, "INFO", text)

def log_warning(text):
    """
        Prints a WARNING message to stdout.
    """
    log_write_entry(sys.stdout, "WARNING", text)


def log_error(text, exception=None):
    """
        Prints a ERROR message and exception to stderr.
    """
    log_write_entry(sys.stderr, "ERROR", text, exception)
    # in case we send to somewhere else also send it to the standard error output (console)
    if sys.stderr is not sys.__stderr__:
        log_write_entry(sys.__stderr__, "ERROR", text, exception)


def log_write_entry(writer, prefix, text, exception=None):
    """
        Prints a message of format: date, time, prefix, text, exception to a writer.
    """
    now = datetime.datetime.now()
    header = now.isoformat(" ") + '\t' + prefix + '\t'

    print(header + text, end='\r\n', file=writer)

    if exception is not None:
        print(header + exception, end='\r\n', file=writer)

# singleton options dictionary (we only need one throughout the application)
options = {}

def load_options(file_name):
    """
        Load options from a JSON file and apply some conversions like changing the main window bounding rectangle
        from list to QtCore.QRect.
    """
    global options
    options = read_json(file_name)

    # main window bounding rectangle from list to QRect
    if c.OG_MW_BOUNDS in options:
        rect = options[c.OG_MW_BOUNDS]
        options[c.OG_MW_BOUNDS] = QtCore.QRect(*rect)

def save_options(file_name):
    """
        Saves the options into a JSON file after performing some conversions from types like QtCore.QRect to types
        supported by JSON.
    """
    data = options.copy()

    # main window bounding rectangle fromn QRect to list
    rect = data[c.OG_MW_BOUNDS]
    data[c.OG_MW_BOUNDS] = [rect.x(), rect.y(), rect.width(), rect.height()]

    # write to file
    write_json(file_name, data)


class ZipArchiveReader():
    """
        Encapsulates a zip file and reads binary files from it, or even converts from JSON to a Python object.

        See also: https://docs.python.org/3.4/library/zipfile.html
    """
    def __init__(self, file):
        """
            Open the zip file in read-only mode.
        """
        self.zip = zipfile.ZipFile(file, mode='r')

    def read(self, name):
        """
            Just reads a file as byte array.
        """
        return self.zip.read(name)

    def read_as_json(self, name):
        """
            First reads the file as byte array, then convert to UTF-8, then convert by JSON to Python object.
        """
        bytes = self.read(name)
        obj = json.loads(bytes.decode())
        return obj

    def __del__(self):
        """
            Close the zip upon deletion.
        """
        self.zip.close()


class ZipArchiveWriter():
    """
        Ecapsulates a zip file to write files into it or even whole Python objects via JSON.
    """
    def __init__(self, file):
        """
            Open the zip file in write mode with standard zlib compression mode.
        """
        self.zip = zipfile.ZipFile(file, mode='w', compression=zipfile.ZIP_DEFLATED)

    def write(self, name, bytes):
        """
            Writes a byte array to an entry in the zip file.
        """
        self.zip.writestr(name, bytes)

    def write_json(self, name, obj):
        """
            Write a Python object via JSON into an entry in the zip file.
        """
        bytes = json.dumps(obj, indent=2, separators=(',', ': '), sort_keys=True).encode()
        self.write(name, bytes)

    def __del__(self):
        """
            Close the zip upon deletion.
        """
        self.zip.close()


class List2D():
    """
        Implements an 2D array with getter and setter for two indices (x,y). Based on list.
    """
    def __init__(self, dimension):
        """
            Creates an empty array with a given dimensions (tuple).
        """
        # create empty list
        size = dimension[0] * dimension[1]
        self._array = [0] * size
        # store dimension
        self.dimension = dimension

    def get(self, x, y):
        """
            Returns the element at position (x,y).
        """
        index = x + self.dimension[0] * y
        return self._array[index]

    def set(self, x, y, v):
        """
            Sets the element at position (x,y).
        """
        index = x + self.dimension[0] * y
        self._array[index] = v


class Worker(QtCore.QObject):
    """
        Not yet in workable state. Skeleton of a worker doing jobs on a specific thread.
    """
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