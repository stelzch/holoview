"""Main Module.

 _____     _ _____ _____ _____
|  |  |___| |     |     |   __|
|     | . | | | | |  |  |__   |
|__|__|___|_|_|_|_|_____|_____|
"""
import gi
from gi.repository import Gtk, Gst, GObject
from holoview.mainwindow import MainWindow
from holoview import log

gi.require_version('Gtk', '3.0')


def main():
    logger = log.create_custom_logger('HoloView')
    logger.debug('Starting application')
    GObject.threads_init()
    Gst.init(None)
    mainwindow = MainWindow()
    Gtk.main()