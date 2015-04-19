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

from enum import Enum
import zipfile

import yaml


"""
    General utility functions (not graphics related) only based on Python or common libraries (not Qt) and not specific
    to our project.
"""

# use libyaml if available (see http://pyyaml.org/ticket/34)
if hasattr(yaml, 'CLoader'):
    Loader = yaml.CLoader
else:
    Loader = yaml.Loader
if hasattr(yaml, 'CDumper'):
    Dumper = yaml.CDumper
else:
    Dumper = yaml.Dumper


class AutoNumber(Enum):
    """
        Enum that is automatically numbered with increasing integers.
    """

    def __new__(cls):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj


def read_as_yaml(file_name):
    """
        Read YAML struct from file
    """
    with open(file_name, 'r') as file:
        return yaml.load(file, Loader=Loader)


def write_as_yaml(file_name, value):
    """
        Writes YAML struct to a file.
    """
    with open(file_name, 'w') as file:
        yaml.dump(value, file, allow_unicode=True, Dumper=Dumper)
# TODO are keys of dictionaries in YAML sorted automatically?

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

    def read_as_yaml(self, name):
        """
            First reads the file as byte array, then convert to UTF-8, then convert by YAML to Python object.
        """
        bytes = self.read(name)
        obj = yaml.load(bytes.decode(), Loader=Loader)
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

    def write_as_yaml(self, name, obj):
        """
            Write a Python object via YAML into an entry in the zip file.
        """
        bytes = yaml.dump(obj, allow_unicode=True, Dumper=Dumper).encode()
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


def find_in_list(data, element):
    """
        Finds the index of a certain element in a list. Returns the index of the first occurence or ValueError if the
        element is not contained in the list. This is a slow operation (O(n)).
    """
    for index, e in enumerate(data):
        if e == element:
            return index
    return ValueError