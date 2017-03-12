"""Main Window.

 _____     _ _____ _____ _____
|  |  |___| |     |     |   __|
|     | . | | | | |  |  |__   |
|__|__|___|_|_|_|_|_____|_____|
"""

import gi
import os
from gi.repository import Gtk, GdkPixbuf, GObject
from holoview.capture import Capture

gi.require_version('Gtk', '3.0')
curdir = os.path.dirname(os.path.abspath(__file__))


class MainWindow:
    """This is the MainWindowController."""

    def __init__(self):
        """Initialize and show the MainWindow."""
        # Setup camera
        self.capture = Capture()

        # Build UI
        builder = Gtk.Builder()
        builder.add_from_file('%s/ui/mainwindow.glade' % curdir)
        self.ui = dict()
        self.ui["main_window"] = builder.get_object("main_window")
        self.ui["menu_quit"] = builder.get_object("menu_quit")
        self.ui["capture_image"] = builder.get_object("capture_image")
        self.ui["brightness_spin"] = builder.get_object("brightness_spin")
        self.ui["contrast_spin"] = builder.get_object("contrast_spin")
        self.ui["saturation_spin"] = builder.get_object("saturation_spin")

        # Connect signals
        self.ui["main_window"].connect("delete-event", self.end)
        self.ui["menu_quit"].connect("activate", self.end)
        self.ui["main_window"].show_all()
        self.capture.connect("frame_captured", self.show_image, "preview")

        GObject.threads_init()
        self.capture.start()

    def show_image(self, sender, img, type):
        """Show a certain type of image in the main window."""
        if type is "preview":
            image = GdkPixbuf.Pixbuf.new_from_bytes(img,
                                                    GdkPixbuf.Colorspace.RGB,
                                                    False, 8, 1280, 720, 1280*3)
            print("Loaded new image")
            self.ui["capture_image"].set_from_pixbuf(image)

    def end(self, widget, data):
        """Stop any running capture and end program."""
        self.capture.stop()
        Gtk.main_quit()

    def __del__(self):
        """Stop any running capture and end program."""
        self.end(None, None)
