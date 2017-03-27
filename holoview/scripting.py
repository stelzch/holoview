"""Scripting utilities.

 _____     _ _____ _____ _____
|  |  |___| |     |     |   __|
|     | . | | | | |  |  |__   |
|__|__|___|_|_|_|_|_____|_____|

In order to provide a flexible and versatile method to analyze images, the
HoloView applications makes use of the python language itself to let the user
choose what happens with the captured images.

This module contains classes and routines for the script execution additional
to the general script documentation.

Reference
=========
All scripts are executed using the current python interpreter (current version
in the raspberry pi: 3.4). The following modules can be used:
  - cv2     - The OpenCV library
  - np      - NumPy
  - plt     - Matplotlibs pyplot module for plotting features similar to matlab
  - PIL     - Pillow Python imaging libraries
  - holoproc- The holoproc module provided with holoview with FRS routines
For security reasons, the script can only use these modules, as access to other
modules like os, sys, etc. could result in high security threats. Users are
still encouraged to look through the script files they use and check for any
malicous content.

Besides the modules, the script can use the following variables:
  - img             - the captured image as np.ndarray (2-dim matrix)
  - width           - the width of the captured image
  - height          - the height         "
  - output_vars     - dict of variables (str/float) to display in HoloView
  - output_figs     - dict of matplotlib figures to display in HoloView
"""
import logging
import cv2
import gi
from gi.repository import Gtk

gi.require_version('Gtk', '3.0')
logger = logging.getLogger('HoloView')


class Script:
    """Representing a user-written script for image evaluation."""

    def __init__(self, source=""):
        """Create a new Script object."""
        self.source = source
        self.figures = dict()
        self.variables = dict()

    def set_source(self, source):
        """Set the scripts source code."""
        self.source = source

    def get_source(self):
        """Get the scripts source code."""
        return self.source

    def execute(self):
        """Execute this script and store its results."""
        pass


class ScriptResultViewer(Gtk.Box):
    """Present the results of a script."""

    def __init__(self):
        """Init."""
        super(ScriptResultViewer, self).__init__()

        # Init models
        self.variable_model = Gtk.ListStore(str, str)  # Model for variables
        self.variable_model.append(["x", "1.0234"])
        self.variable_model.append(["y", "5.2348"])

        # Init views
        self.ui = dict()
        self.ui["notebook"] = Gtk.Notebook.new()
        self.ui["variable_view"] = Gtk.TreeView(self.variable_model)
        self.ui["renderer1"] = Gtk.CellRendererText()
        self.ui["renderer2"] = Gtk.CellRendererText()
        var_name = Gtk.TreeViewColumn("Variable", self.ui["renderer1"], text=0)
        var_value = Gtk.TreeViewColumn("Value", self.ui["renderer2"], text=1)
        self.ui["variable_view"].append_column(var_name)
        self.ui["variable_view"].append_column(var_value)

        self.pack_start(self.ui["variable_view"], True, True, 0)
