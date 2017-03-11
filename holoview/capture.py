"""Defines classes for image and video capturing.

 _____     _ _____ _____ _____
|  |  |___| |     |     |   __|
|     | . | | | | |  |  |__   |
|__|__|___|_|_|_|_|_____|_____|
"""

import gi
import os
import time
from gi.repository import GObject
from picamera import PiCamera

gi.require_version('Gtk', '3.0')
curdir = os.path.dirname(os.path.abspath(__file__))


class Capture(GObject.GObject):
    """Capture either a video stream or a single image."""

    __gsignals__ = {
        "frame_captured": (GObject.SIGNAL_RUN_FIRST, None,
                           (object,))
    }

    def __init__(self):
        """Initialize Capture Class."""
        GObject.GObject.__init__(self)
        self.cam = PiCamera()
        self.capture_array = bytearray()

    def record(self):
        """Start Video Capturing."""
        self.cam.start_recording(self, 'mjpeg')

    def capture(self):
        """Capture a single image."""
        pass

    def stop(self):
        """Stop current capture."""
        self.cam.stop_recording()

    def write(self, data):
        """Write imagery data."""
        self.capture_array += data

    def flush(self):
        """Emit image data."""
        self.emit("frame_captured", self.capture_array)
        print("frame recv")
        self.capture_array = bytearray()


def write_to_file(self, data, filename):
    """Write data to file."""
    print("Writing to ")
    with open(filename, "wb") as file:
        file.write(data)

if __name__ == "__main__":
    print("Performing simple test:")
    c = Capture()
    c.connect("frame_captured", write_to_file, 'test.file')
    c.record()
    time.sleep(2)
    c.stop()
