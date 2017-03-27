"""Utilities for image processing."""

import gi
from gi.repository import GdkPixbuf, GLib

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
