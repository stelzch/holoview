"""Main Window.

 _____     _ _____ _____ _____
|  |  |___| |     |     |   __|
|     | . | | | | |  |  |__   |
|__|__|___|_|_|_|_|_____|_____|
"""
import gi
import os
import cv2
from gi.repository import Gtk
from PIL import Image
from picamera import PiCamera

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
        self.ui["brightness_spin"] = builder.get_object("brightness_spin")
        self.ui["contrast_spin"] = builder.get_object("contrast_spin")
        self.ui["saturation_spin"] = builder.get_object("saturation_spin")
        self.ui["brightness_adjus"] = builder.get_object("brightness_adjus")
        self.ui["contrast_adjus"] = builder.get_object("contrast_adjus")
        self.ui["saturation_adjus"] = builder.get_object("saturation_adjus")
        self.ui["capture_image"] = builder.get_object("capture_image")
        self.ui["capture_button"] = builder.get_object("capture_button")
        self.ui["tab_widget"] = builder.get_object("tab_widget")

        # Connect signals
        self.ui["main_window"].connect("delete-event", self.end)
        self.ui["main_window"].connect("key_release_event", self.on_key)
        self.ui["menu_quit"].connect("activate", self.end)
        self.ui["capture_button"].connect("clicked", self.start_capture)
        self.ui["brightness_adjus"].connect("value-changed",
                                            self.capture_param_changed)
        self.ui["contrast_adjus"].connect("value-changed",
                                          self.capture_param_changed)
        self.ui["saturation_adjus"].connect("value-changed",
                                            self.capture_param_changed)

        # Other flags
        self.previewing = False

        # Initialize camera with overlay
        self.camera = PiCamera()
        # self.overlay_image = cv2.imread("%s/ui/overlay.png" % curdir)
        # self.overlay_image = cv2.cvtColor(self.overlay_image,
        #                                  cv2.COLOR_BGRA2RGBA)
        self.overlay_image = Image.open('%s/ui/overlay.png' % curdir)
        self.overlay_image = self.overlay_image.tostring()
        """
        overlayBytes = io.BytesIO()
        with open("%s/ui/overlay.ppm" % curdir, "rb") as pixmap:
            pixloader = PixbufLoader.new_with_type("image/x-portable-pixmap")
            pixloader.write(pixmap.read())
            overlay = pixloader.get_pixbuf()
            overlayBytes.write(overlay.get_pixels())
        self.camera.add_overlay(overlayBytes, format='rgba') """

        self.ui["main_window"].show_all()

    def start_capture(self, widget):
        """Display camera preview."""
        current_tab = self.ui["tab_widget"].get_current_page()
        if current_tab is 0 and not self.previewing:
            self.camera.start_preview()
            self.overlay = self.camera.add_overlay(self.overlay_image,
                                                   size=(1920, 1080),
                                                   format='rgba',
                                                   layer=4)
            print("Preview started")
            self.previewing = True

    def capture_param_changed(self, widget):
        """Change capture parameter for the camera."""
        if widget is self.ui["brightness_adjus"]:
            self.camera.brightness = int(widget.get_value())
        elif widget is self.ui["contrast_adjus"]:
            self.camera.contrast = int(widget.get_value() * 2 - 100)
        elif widget is self.ui["saturation_adjus"]:
            self.camera.saturation = int(widget.get_value() * 2 - 100)

    def on_key(self, widget, event):
        """Handle incoming key events."""
        if self.previewing and event.keyval is ord('c'):
            # trigger capture
            self.camera.stop_preview()
            # TODO: Capture to buffer, not to file
            self.camera.capture("/tmp/image.jpg")
            self.ui["capture_image"].set_from_file("/tmp/image.jpg")
            self.camera.remove_overlay(self.overlay)
            self.previewing = False
        elif self.previewing and event.keyval is ord('q'):
            self.camera.stop_preview()
            self.camera.remove_overlay(self.overlay)
            self.previewing = False

    def end(self, widget, *data):
        """Stop any running capture and end program."""
        Gtk.main_quit()

    def __del__(self):
        """Stop any running capture and end program."""
        self.end(None, None)
