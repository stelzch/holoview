"""Defines classes for image and video capturing.

 _____     _ _____ _____ _____
|  |  |___| |     |     |   __|
|     | . | | | | |  |  |__   |
|__|__|___|_|_|_|_|_____|_____|
"""

import gi
import io
import os
import time
import threading
from gi.repository import GObject, GLib
from picamera import PiCamera

gi.require_version('Gtk', '3.0')
curdir = os.path.dirname(os.path.abspath(__file__))


class Capture(GObject.GObject, threading.Thread):
    """Capture either a video stream or a single image."""

    __gsignals__ = {
        "frame_captured": (GObject.SIGNAL_RUN_FIRST, None,
                           (object,))
    }

    def __init__(self):
        """Initialize Capture Class."""
        GObject.GObject.__init__(self)
        threading.Thread.__init__(self)

        # Initialize Camera
        self.cam = PiCamera()
        self.cam.resolution = (1280, 720)
        self.cam.framerate = 30
        self.shouldStop = False

    def run(self):
        """Start Video Capturing."""
        self.shouldStop = False
        stream = io.BytesIO()
        for image in self.cam.capture_continuous(stream, 'rgb',
                                                 use_video_port=True):
            stream.seek(0)
            image = stream.read()
            self.emit("frame_captured", GLib.Bytes.new(image))
            stream.seek(0)
            stream.truncate()
            if self.shouldStop:
                break
        print("Capture stopped")

    def capture(self):
        """Capture a single image."""
        pass

    def stop(self):
        """Stop current capture."""
        self.shouldStop = True


def write_to_file(self, data, filename):
    """Write data to file."""
    print("Writing to ")
    with open(filename, "wb") as file:
        file.write(data)

if __name__ == "__main__":
    print("Performing simple test:")
    c = Capture()
    c.connect("frame_captured", write_to_file, 'test.file')
    c.start()
    time.sleep(3)
    for i in range(1, 10):
        print("hi")
        time.sleep(2)
    c.stop()
