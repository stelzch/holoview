"""Utilities for image processing."""

import gi
from gi.repository import GdkPixbuf, GLib
from PIL import Image
from io import BytesIO
import numpy as np

gi.require_version('Gtk', '3.0')


def rgbarray2pixbuf(array):
    """Convert an ndarray to a GdkPixbuf."""
    width = array.shape[1]
    height = array.shape[0]
    imgdata = GLib.Bytes.new(array.tostring())
    pixbuf = GdkPixbuf.Pixbuf.new_from_bytes(imgdata,
                                             GdkPixbuf.Colorspace.RGB,
                                             False,
                                             8,
                                             width, height,
                                             width * 3)
    return pixbuf

def rgbarray2bytes(array, iformat='PNG'):
    """Get a RGB array as bytearray encoded in a certain format.

    Keyword arguments:
    array -- a RGB image stored in an ndarray
    format -- string representing the format, e.g. PNG, JPEG, GIF, ...
    """
    tempImage = Image.fromarray(array, 'RGB')
    output = BytesIO()
    tempImage.save(output, format=iformat)
    imgData = output.getvalue()
    output.close()
    return imgData

def bytes2rgbarray(bytes_):
    """Get an RGB array from a bytearray encoded in certain format.

    Keyword arguments:
    bytes -- a bytearray which stores the image
    """
    buffer = BytesIO(bytes_)
    return np.array(Image.open(buffer))
