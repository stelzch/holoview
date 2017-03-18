"""Display Camera-Live-Stream.

Author: Christoph Stelz
Date: 18 Mar 2017

 _____     _ _____ _____ _____
|  |  |___| |     |     |   __|
|     | . | | | | |  |  |__   |
|__|__|___|_|_|_|_|_____|_____|
"""
import gi
import logging
import os
from gi.repository import Gtk, Gst
from gi.repository import GdkX11, GstVideo
gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')


logger = logging.getLogger('HoloView')


class CameraSurface(Gtk.DrawingArea):
    """Display Camerapreview in Gtk Widget."""

    def __init__(self, *args, **kwargs):
        """Initialize Widget."""
        super(CameraSurface, self).__init__(*args, **kwargs)
        self.set_size_request(600, 400)
        self.uri = "v4l2:///dev/video0"

        if not Gst.is_initialized():
            logger.error("GStreamer Library not initialized")

        if not os.path.exists(self.uri.split("://")[1]):
            logger.error("Capture Device {} does not" +
                         "exist (or access is denied).".format(self.uri))

        # Setup GStreamer Playbin and event handling
        self.player = Gst.ElementFactory.make("playbin", "player")
        print(self.player)
        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.enable_sync_message_emission()
        bus.connect("message", self.on_gst_message)
        bus.connect("sync-message::element", self.on_gst_sync_message)

    def on_gst_message(self, bus, message):
        """Handle a GStreamer Bus Message."""
        t = message.type
        if t == Gst.MessageType.ERROR:
            self.player.set_state(Gst.State.NULL)
            err, debug = message.parse_error()
            logger.error("GStreamer - " + err)
            logger.debug("GStreamer - " + debug)

    def on_gst_sync_message(self, bus, message):
        """Handle a Gstreamer Sync Message."""
        if message.get_structure().get_name() == 'prepare-window-handle':
            imagesink = message.src
            """Force aspect ratio, so images are not distorted."""
            imagesink.set_property("force-aspect-ratio", True)
            """Tell Gstreamer the X11 ID so it can write the images to it."""
            imagesink.set_window_handle(self.get_property('window').get_xid())

    def set_uri(self, uri):
        """Overwrite default media uri."""
        self.uri = uri

    def start(self):
        """Start playing current media uri. Defaults to /dev/video0."""
        self.player.set_property("uri", self.uri)
        self.player.set_state(Gst.State.PLAYING)

    def stop(self):
        """Stop playback."""
        self.player.set_state(Gst.State.NULL)
