import json, zlib

from PySide import QtCore

# TODO compression not working because QDataStream doesn't send bytes

def serialize_compress_and_write_to_socket(socket, value):
    """

    """
    # serialize value to json
    serialized = json.dumps(value, indent=0)

    # encode to utf-8 bytes and compress
    compressed = zlib.compress(serialized.encode())

    # wrap in QByteArray
    bytearray = QtCore.QByteArray(compressed)

    # write using a data stream
    writer = QtCore.QDataStream(socket)
    writer.setVersion(QtCore.QDataStream.Qt_4_8)
    writer << bytearray

def read_from_socket_uncompress_and_deserialize(socket):
    # read a QByteArray using a data stream
    reader = QtCore.QDataStream(socket)
    bytearray = QtCore.QByteArray()
    reader >> bytearray

    # uncompress bytes from bytearray
    uncompressed = zlib.decompress(bytearray.data())

    # decode from utf-8 bytes to unicode and deserialize from json
    deserialized = json.loads(uncompressed.decode())

    return deserialized
