"""Main Module.

 _____     _ _____ _____ _____
|  |  |___| |     |     |   __|
|     | . | | | | |  |  |__   |
|__|__|___|_|_|_|_|_____|_____|
"""
import gi
from gi.repository import Gtk
from holoview.mainwindow import MainWindow

gi.require_version('Gtk', '3.0')


if __name__ == '__main__':
    mainwindow = MainWindow()
    print("Running")
    Gtk.main()
