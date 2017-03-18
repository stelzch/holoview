"""Main Window.

 _____     _ _____ _____ _____
|  |  |___| |     |     |   __|
|     | . | | | | |  |  |__   |
|__|__|___|_|_|_|_|_____|_____|
"""

import gi
import os
from gi.repository import Gtk
from holoview.camerasurface import CameraSurface

gi.require_version('Gtk', '3.0')
curdir = os.path.dirname(os.path.abspath(__file__))


class MainWindow:
    """This is the MainWindowController."""

    def __init__(self):
        """Initialize and show the MainWindow."""
        # Initialize UI
        builder = Gtk.Builder()
        builder.add_from_file('%s/ui/mainwindow.glade' % curdir)
        self.ui = dict()
        self.ui["main_window"] = builder.get_object("main_window")
        self.ui["menu_quit"] = builder.get_object("menu_quit")
        self.ui["capture_frame"] = builder.get_object("capture_frame")
        self.ui["brightness_spin"] = builder.get_object("brightness_spin")
        self.ui["contrast_spin"] = builder.get_object("contrast_spin")
        self.ui["saturation_spin"] = builder.get_object("saturation_spin")
        self.ui["capture_surface"] = CameraSurface()
        self.ui["capture_frame"].add(self.ui["capture_surface"])

        # Connect signals
        self.ui["main_window"].connect("delete-event", self.end)
        self.ui["menu_quit"].connect("activate", self.end)
        self.ui["main_window"].show_all()

        self.ui["capture_surface"].start()  # Start displaying camera stream

    def end(self, widget, data):
        """Stop any running capture and end program."""
        self.ui["capture_surface"].stop()
        Gtk.main_quit()

    def __del__(self):
        """Stop any running capture and end program."""
        self.end(None, None)
