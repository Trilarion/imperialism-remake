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
General utility functions (not graphics related) only based on Python or common libraries (not Qt) and not specific
to the project.
"""
import pickle
import zipfile
from enum import Enum


class AutoNumberedEnum(Enum):
    """
    Enum that is automatically numbered with increasing integers. Automatically ensures uniqueness of values.
    """

    def __new__(cls):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj


def read_from_file(file_name):
    """
    Read serialized Python value from file.

    :param file_name: File name
    :return: Python value
    """
    with open(file_name, 'rb') as file:  # open is 'r' by default
        return pickle.load(file)


def write_to_file(file_name, value):
    """
    Writes Python value to a file.

    :param file_name: File name.
    :param value: Python value
    """
    with open(file_name, 'wb') as file:
        pickle.dump(value, file)


class ZipArchiveReader:
    """
    Encapsulates a zip file and reads binary files from it, or even converts from JSON to a Python object.

    See also: https://docs.python.org/3.4/library/zipfile.html
    """

    def __init__(self, file):
        """
        Opens the zip file in read-only mode.

        :param file: File name
        """
        self.zip = zipfile.ZipFile(file)  # mode is 'r' by default

    def read_from_file(self, name):
        """
        Reads the file name from the zip archive

        :param name: File name.
        :return: De-serialized Python value.
        """
        data = self.zip.read(name)
        obj = pickle.loads(data)
        return obj

    def __del__(self):
        """
        Closes the zip upon deletion.
        """
        self.zip.close()


class ZipArchiveWriter:
    """
    Encapsulates a zip file to write files into it or even whole Python objects

    See also: https://docs.python.org/3.4/library/zipfile.html
    """

    def __init__(self, file):
        """
        Open the zip file in write mode with standard zlib compression mode.

        :param file: File name
        """
        self.zip = zipfile.ZipFile(file, mode='w', compression=zipfile.ZIP_DEFLATED)

    def write_to_file(self, name, obj):
        """
        Writes a Python value into a file in the archive.

        :param name: File name
        :param obj: Python value
        """
        data = pickle.dumps(obj)
        self.zip.writestr(name, data)

    def __del__(self):
        """
        Closes the zip upon deletion.
        """
        self.zip.close()


class List2D:
    """
    Implements an 2D array with getter and setter for two indices (x,y). Based on a list but with a mapping of the
    two-dimensional indices into a one-dimensional index.
    """

    def __init__(self, dimension):
        """
        Creates an empty array with a given 2D dimension (tuple - width/height).

        :param dimension: Dimension
        """
        # create empty list
        size = dimension[0] * dimension[1]
        self._array = [0] * size
        # store dimension
        self.dimension = dimension

    def get(self, x, y):
        """
        Returns the element at position (x,y).

        :param x: x position
        :param y: y position
        :return: value
        """
        index = x + self.dimension[0] * y
        return self._array[index]

    def set(self, x, y, v):
        """
        Sets the element at position (x,y).

        :param x: x position
        :param y: y position
        :param v: value
        """
        index = x + self.dimension[0] * y
        self._array[index] = v


def index_of_element(sequence, element):
    """
    Finds the index of a certain element in a list. Returns the index of the first occurrence or ValueError if the
    element is not contained in the list. Raises a ValueError if the element is not contained in the sequence.

    Note: This is a slow operation (O(n)).

    :param sequence: iterable
    :param element: single element
    :return: the index of the element
    """
    for index, e in enumerate(sequence):
        if e == element:
            return index
    raise ValueError('element not contained in sequence')
