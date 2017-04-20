"""Main Module.

 _____     _ _____ _____ _____
|  |  |___| |     |     |   __|
|     | . | | | | |  |  |__   |
|__|__|___|_|_|_|_|_____|_____|
"""
import gi
import cv2
import logging
import numpy as np
from gi.repository import Gtk, GObject, Gst
from holoview.mainwindow import MainWindow
from holoview import log

gi.require_version('Gtk', '3.0')


def main():
    logger = log.create_custom_logger('HoloView')
    logger.debug('Starting application')
    mainwindow = MainWindow()
    
    Gtk.main()

if __name__ == "__main__":
    main()
