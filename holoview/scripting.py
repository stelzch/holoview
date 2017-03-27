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
import gi
from gi.repository import Gtk
import matplotlib
import logging

matplotlib.use("Gtk3Agg")
gi.require_version('Gtk', '3.0')
logger = logging.getLogger('HoloView')
default_modules = [
    "import numpy as np",
    "import PIL",
    "import matplotlib.pyplot as plt"
]

import matplotlib.pyplot as plt
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas

class Script:
    """Representing a user-written script for image evaluation."""

    def __init__(self, source="", import_lines=default_modules):
        """Create a new Script object."""
        self.source = source
        self.output_vars = {
        "test":"var"
        }
        self.output_figs = dict()
        self.import_lines = import_lines

    def set_source(self, source):
        """Set the scripts source code."""
        self.source = source

    def get_source(self):
        """Get the scripts source code."""
        return self.source

    def get_results(self):
        """Get the results of the script as tuple: (vars, figs)."""
        return self.output_vars, self.output_figs

    def execute(self, image):
        """Execute this script and store its results.

        Beforehand prepend the correct import lines and clean previous results.
        """
        # Prepare import-statements and global vars
        self.image = image
        self.width = image.shape[1]
        self.height = image.shape[0]
        script = self.source
        script_globals = {
            "image": self.image,
            "width": self.width,
            "height": self.height,
            "output_vars": self.output_vars,
            "output_figs": self.output_figs
        }
        for line in self.import_lines:
            script = line + "\n" + script

        # Clearing results
        self.output_vars.clear()
        self.output_figs.clear()
        logger.debug("Running the following script:\n{}".format(script))

        # Here we go
        exec(script, script_globals)
        logger.debug("Script left behind the following results:\n{}\n{}".format(
            self.output_vars,
            self.output_figs
        ))


class ScriptResultViewer:
    """Present the results of a script."""

    def __init__(self):
        """Init."""
        self.box = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 0)

        # Init models
        self.variable_model = Gtk.ListStore(str, str)  # Model for variables

        # Init views
        self.ui = dict()
        self.tabs = dict()
        self.ui["notebook"] = Gtk.Notebook.new()
        self.ui["variable_view"] = Gtk.TreeView(self.variable_model)
        self.ui["renderer1"] = Gtk.CellRendererText()
        self.ui["renderer2"] = Gtk.CellRendererText()

        var_name = Gtk.TreeViewColumn("Variable", self.ui["renderer1"], text=0)
        var_value = Gtk.TreeViewColumn("Value", self.ui["renderer2"], text=1)
        self.ui["variable_view"].append_column(var_name)
        self.ui["variable_view"].append_column(var_value)

        # self.box.pack_start(self.ui["variable_view"], True, True, 0)
        self.box.pack_start(self.ui["notebook"], True, True, 0)

    def get_widget(self):
        """Get the widget."""
        return self.box

    def view_results(self, script):
        """View the results of a given script."""
        # Clear previous results
        self.variable_model.clear()
        while self.ui["notebook"].get_n_pages() is not 0:
            self.ui["notebook"].remove_page(0)

        variables, figs = script.get_results()
        print(figs)

        for key in variables:
            print(key, ":", variables[key])
            self.variable_model.append([str(key), str(variables[key])])
        for key in figs:
            if type(figs[key]) is matplotlib.figure.Figure:
                print(figs)
                logger.info("Processing figure {}".format(key))
                sw = Gtk.ScrolledWindow()
                canvas = FigureCanvas(figs[key])
                sw.add_with_viewport(canvas)

                self.tabs[key] = sw
                self.ui["notebook"].append_page(sw, Gtk.Label.new(key))
                self.ui["notebook"].show_all()
