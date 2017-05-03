"""Main Window.

 _____     _ _____ _____ _____
|  |  |___| |     |     |   __|
|     | . | | | | |  |  |__   |
|__|__|___|_|_|_|_|_____|_____|
"""
import math
import gi
gi.require_version('Gtk', '3.0')
import os
import logging
import cv2
import numpy as np
from gi.repository import Gtk, GtkSource, GObject, GLib
from PIL import Image
from picamera import PiCamera
from holoview.imageutils import rgbarray2pixbuf
from holoview.scripting import ScriptResultViewer, Script
from holoview.project import Project

curdir = os.path.dirname(os.path.abspath(__file__))
docdir = GLib.get_user_special_dir(GLib.USER_DIRECTORY_DOCUMENTS)
logger = logging.getLogger('HoloView')


class MainWindow(GObject.GObject):
    """This is the MainWindowController."""

    def __init__(self):
        """Initialize and show the MainWindow."""
        GObject.GObject.__init__(self)
        # Register new types
        GObject.type_register(GtkSource.View)

        # Initialize UI
        builder = Gtk.Builder()
        builder.add_from_file('%s/ui/mainwindow.glade' % curdir)
        self.ui = dict()
        self.ui['main_window'] = builder.get_object('main_window')
        self.ui['menu_open'] = builder.get_object('menu_open')
        self.ui['menu_save'] = builder.get_object('menu_save')
        self.ui['menu_quit'] = builder.get_object('menu_quit')
        self.ui['menu_info'] = builder.get_object('menu_info')
        # Camera Parameters
        self.ui['brightness_spin'] = builder.get_object('brightness_spin')
        self.ui['contrast_spin'] = builder.get_object('contrast_spin')
        self.ui['saturation_spin'] = builder.get_object('saturation_spin')
        self.ui['resolution_combo'] = builder.get_object('resolution_combo')
        self.ui['brightness_adjus'] = builder.get_object('brightness_adjus')
        self.ui['contrast_adjus'] = builder.get_object('contrast_adjus')
        self.ui['saturation_adjus'] = builder.get_object('saturation_adjus')
        self.ui['awb_mode_combo'] = builder.get_object('awb_mode_combo')
        self.ui['awb_gains_label'] = builder.get_object('awb_gains_label')
        self.ui['awb_red_spin'] = builder.get_object('awb_red_spin')
        self.ui['awb_red_adjus'] = builder.get_object('awb_red_adjus')
        self.ui['awb_blue_adjus'] = builder.get_object('awb_blue_adjus')
        self.ui['awb_blue_spin'] = builder.get_object('awb_blue_spin')
        self.ui['drc_combo'] = builder.get_object('drc_combo')
        self.ui['iso_combo'] = builder.get_object('iso_combo')
        self.ui['shutter_adjus'] = builder.get_object('shutter_adjus')
        self.ui['shutter_spin'] = builder.get_object('shutter_spin')
        self.ui['exposure_combo'] = builder.get_object('exposure_combo')
        self.ui['capture_image'] = builder.get_object('capture_image')
        self.ui['capture_button'] = builder.get_object('capture_button')
        self.ui['tab_widget'] = builder.get_object('tab_widget')
        self.ui['about_dialog'] = builder.get_object('about_dialog')
        self.ui['proc_box'] = builder.get_object('proc_box')
        self.ui['load_script'] = builder.get_object('load_script')
        self.ui['save_script'] = builder.get_object('save_script')
        self.ui['run_script'] = builder.get_object('run_script')
        self.ui['export_figure'] = builder.get_object('export_figure')
        self.ui['python_filter'] = builder.get_object('python_filter')
        self.ui['jpeg_filter'] = builder.get_object('jpeg_filter')
        self.ui['png_filter'] = builder.get_object('png_filter')
        self.ui['svg_filter'] = builder.get_object('svg_filter')
        self.ui['project_filter'] = builder.get_object('project_filter')
        self.ui['postscript_filter'] = builder.get_object('postscript_filter')
        self.ui['script_result'] = ScriptResultViewer()

        # Additional props
        self.ui['awb_red_spin'].set_visible(False)
        self.ui['awb_blue_spin'].set_visible(False)
        self.ui['awb_gains_label'].set_visible(False)

        # Connect signals
        self.ui['main_window'].connect('delete-event', self.end)
        self.ui['main_window'].connect('key_release_event', self.on_key)
        self.ui['menu_open'].connect('activate', self.on_menu)
        self.ui['menu_save'].connect('activate', self.on_menu)
        self.ui['menu_quit'].connect('activate', self.on_menu)
        self.ui['menu_info'].connect('activate', self.on_menu)
        self.ui['capture_button'].connect('clicked', self.start_capture)
        self.ui['brightness_adjus'].connect('value-changed',
                                            self.capture_param_changed)
        self.ui['contrast_adjus'].connect('value-changed',
                                          self.capture_param_changed)
        self.ui['saturation_adjus'].connect('value-changed',
                                            self.capture_param_changed)
        self.ui['resolution_combo'].connect('changed',
                                            self.on_resolution_change)
        self.ui['awb_mode_combo'].connect('changed',
                                          self.capture_param_changed)
        self.ui['awb_red_adjus'].connect('value-changed',
                                         self.capture_param_changed)
        self.ui['awb_blue_adjus'].connect('value-changed',
                                          self.capture_param_changed)
        self.ui['drc_combo'].connect('changed', self.capture_param_changed)
        self.ui['iso_combo'].connect('changed', self.capture_param_changed)
        self.ui['shutter_adjus'].connect('value-changed',
                                        self.capture_param_changed)
        self.ui['exposure_combo'].connect('changed',
                                          self.capture_param_changed)
        self.ui['load_script'].connect('clicked', self.on_toolbar)
        self.ui['save_script'].connect('clicked', self.on_toolbar)
        self.ui['run_script'].connect('clicked', self.on_toolbar)
        self.ui['export_figure'].connect('clicked', self.on_toolbar)
        self.ui['python_filter'].set_name('Python scripts')
        self.ui['jpeg_filter'].set_name('JPEG images')
        self.ui['png_filter'].set_name('PNG images')
        self.ui['svg_filter'].set_name('SVG images')
        self.ui['postscript_filter'].set_name('Postscript documents')
        self.ui['project_filter'].set_name('Project zip files')
        self.ui['script_container'] = builder.get_object(
            'script_editor_container')

        """ This is a textbuffer containing the source typed in the
        sourceview editor."""
        language_manager = GtkSource.LanguageManager.new()
        style_manager = GtkSource.StyleSchemeManager.new()
        logger.info(
            'The following GtkSourceView themes are installed: {}'.format(
                style_manager.get_scheme_ids()
            )
        )
        logger.info(
            'The following GtkSourceView langs are installed: {}'.format(
                language_manager.get_language_ids()
            )
        )
        python_lang = language_manager.get_language('python3')
        self.source = GtkSource.Buffer.new_with_language(python_lang)
        self.source.set_style_scheme(
            style_manager.get_scheme('solarized-dark')
        )
        self.ui['script_editor'] = GtkSource.View.new_with_buffer(self.source)
        self.ui['script_editor'].set_indent_on_tab(True)
        self.ui['script_editor'].set_indent_width(4)
        self.ui['script_editor'].set_insert_spaces_instead_of_tabs(True)
        self.ui['script_editor'].set_show_line_numbers(True)
        self.ui['script_editor'].set_show_right_margin(True)
        self.ui['script_editor'].set_tab_width(4)
        self.ui['script_editor'].set_size_request(400, -1)
        self.ui['script_container'].add(self.ui['script_editor'])
        self.ui['proc_box'].add2(self.ui['script_result'].get_widget())

        # Other flags/variables
        self.previewing = False
        self.script = Script()
        self.project = Project()

        # Initialize camera with overlay
        self.camera = PiCamera()
        self.overlay_image = Image.open('%s/ui/overlay.png' % curdir)
        self.overlay_image = self.overlay_image.tostring()
        self.captured_image = np.zeros((640, 480))

        self.ui['main_window'].show_all()
        self.ui['awb_red_spin'].set_visible(False)
        self.ui['awb_blue_spin'].set_visible(False)
        self.ui['awb_gains_label'].set_visible(False)

    def start_capture(self, widget):
        """Display camera preview."""
        current_tab = self.ui['tab_widget'].get_current_page()
        if current_tab is 0 and not self.previewing:
            self.camera.start_preview()
            self.overlay = self.camera.add_overlay(self.overlay_image,
                                                   size=(1920, 1088),
                                                   format='rgba',
                                                   layer=4)
            logger.info('Viewfinder started')
            self.ui['capture_button'].grab_focus()
            self.previewing = True

    def capture_param_changed(self, widget):
        """Change capture parameter for the camera."""
        if widget is self.ui['brightness_adjus']:
            value = int(widget.get_value())
            self.camera.brightness = value
            logger.info('Setting brightness to {}'.format(value))
        elif widget is self.ui['contrast_adjus']:
            value = int(widget.get_value() * 2 - 100)
            self.camera.contrast = value
            logger.info('Setting contrast to {}'.format(value))
        elif widget is self.ui['saturation_adjus']:
            value = int(widget.get_value() * 2 - 100)
            self.camera.saturation = value
            logger.info('Setting saturation to {}'.format(value))
        elif widget in [self.ui['awb_red_adjus'], self.ui['awb_blue_adjus']]:
            rval = self.ui['awb_red_adjus'].get_value()
            bval = self.ui['awb_blue_adjus'].get_value()
            self.camera.awb_gains = (rval, bval)
            logger.info('Setting awb_gains to ({},{})'.format(rval, bval))
        elif widget is self.ui['awb_mode_combo']:
            value = widget.get_active_text()
            if value not in PiCamera.AWB_MODES:
                logger.error('Invalid awb_mode: {}'.format(value))
            self.camera.awb_mode = value
            logger.info('Setting awb_mode to {}'.format(value))
            if value == 'off':
                self.ui['awb_red_spin'].set_visible(True)
                self.ui['awb_blue_spin'].set_visible(True)
                self.ui['awb_gains_label'].set_visible(True)
            else:
                # Hide the awb gains controls, as they have no effect
                self.ui['awb_red_spin'].set_visible(False)
                self.ui['awb_blue_spin'].set_visible(False)
                self.ui['awb_gains_label'].set_visible(False)
        elif widget is self.ui['drc_combo']:
            val = widget.get_active_id()
            logger.info('Setting drc_strength to {}'.format(val))
            self.camera.drc_strength = val
        elif widget is self.ui['iso_combo']:
            try:
                val = int(widget.get_active_id())
            except ValueError:
                logger.error('Invalid ISO value - not an integer')
                return
            logger.info('Setting iso to {}'.format(val))
            self.camera.iso = val
        elif widget is self.ui['shutter_adjus']:
            val = int(widget.get_value())
            logger.info('Setting shutter_speed to {}'.format(val))
            self.camera.shutter_speed = val
        elif widget is self.ui['exposure_combo']:
            val = widget.get_active_id()
            if val not in PiCamera.EXPOSURE_MODES:
                logger.error('Invalid exposure_mode: {}'.format(val))
            logger.info('Setting exposure_mode to {}'.format(val))
            self.camera.exposure_mode = val

    def on_key(self, widget, event):
        """Handle incoming key events."""
        if self.previewing and event.keyval is ord('c'):
            # trigger capture
            self.camera.stop_preview()

            """Initialize the captured image. However, the picam captures
            raw images with a width of the nearest multiple of 32px from the
            requested width and a height of the nearest multiple of 16px from
            the request height. If we do not allocate the image accordingly
            the capture will result in an error"""
            target_width = self.camera.resolution.width
            target_height = self.camera.resolution.height
            capture_width = math.ceil(self.camera.resolution.width / 32) * 32
            capture_height = math.ceil(self.camera.resolution.height / 16) * 16
            self.captured_image = np.empty(
                (capture_height, capture_width, 3),
                dtype=np.uint8)
            self.camera.capture(self.captured_image, format='rgb')
            """Now reshape that again and remove the unused pixels"""
            self.captured_image = self.captured_image.reshape((
                capture_height, capture_width, 3
            ))
            self.captured_image = self.captured_image[:target_height,
                                                      :target_width,
                                                      :]
            
            """Convert to GdkPixbuf for displaying"""
            pixbuf = rgbarray2pixbuf(self.captured_image)
            self.ui['capture_image'].set_from_pixbuf(pixbuf)
            self.camera.remove_overlay(self.overlay)
            self.previewing = False
            logger.info('Image was captured')
        elif self.previewing and event.keyval is ord('q'):
            self.camera.stop_preview()
            self.camera.remove_overlay(self.overlay)
            self.previewing = False
            logger.info('Viewfinder quit')

    def on_resolution_change(self, widget):
        """Handle change of resolution in capture settings."""
        res = self.ui['resolution_combo'].get_active_text()
        width, height = res.split('x')
        logger.info('Setting resolution to {}x{}'.format(width, height))
        self.camera.resolution = (int(width), int(height))

    def on_toolbar(self, widget):
        """Handle toolbar buttons in the `Processing` tab."""
        if widget is self.ui['save_script']:
            """ This code snippet opens a filechooser in SAVE mode
            so the user can select a destination for the file.
            """
            self.create_dialog('script_saver')  # Recreate the dialog
            res = self.ui['script_saver'].run()
            if res == Gtk.ResponseType.OK:
                filename = self.ui['script_saver'].get_filename()
                logger.info('Saving script to {}'.format(filename))
                with open(filename, 'w') as file:
                    file.write(self.get_sourcecode())
            self.ui['script_saver'].destroy()

        elif widget is self.ui['load_script']:
            """ Here a filechooser is opened to let the user choose a file.
            Its content is then loaded into the GtkSourceView."""
            self.create_dialog('script_chooser')  # Recreate the dialog
            res = self.ui['script_chooser'].run()
            if res == Gtk.ResponseType.OK:
                filename = self.ui['script_chooser'].get_filename()
                logger.info('Loading script from {}'.format(filename))
                with open(filename, 'r') as file:
                    self.source.set_text(file.read())
            self.ui['script_chooser'].destroy()

        elif widget is self.ui['export_figure']:
            if self.ui['script_result'].number_figures() is not 0:
                self.create_dialog('figure_exporter')  # Recreate the dialog
                res = self.ui['figure_exporter'].run()
                if res == Gtk.ResponseType.OK:
                    filename = self.ui['figure_exporter'].get_filename()
                    self.ui['script_result'].export_figure(filename)
                self.ui['figure_exporter'].destroy()
            else:
                # No figure was shown, display error message
                dialog = Gtk.MessageDialog(
                    self.ui['main_window'], None, Gtk.MessageType.ERROR,
                    Gtk.ButtonsType.CANCEL, 'No figure'
                )
                dialog.format_secondary_text(
                    'There was no figure selected when ' +
                    'you hit that export button!'
                )
                dialog.run()
                dialog.destroy()

        elif widget is self.ui['run_script']:
            self.script.set_source(self.get_sourcecode())
            self.script.execute(self.captured_image)
            self.ui['script_result'].view_results(self.script)

    def on_menu(self, widget, *event):
        """Handle menu items."""
        if widget is self.ui['menu_quit']:
            self.end()
        elif widget is self.ui['menu_info']:
            self.ui['about_dialog'].run()
            self.ui['about_dialog'].destroy()
        elif widget is self.ui['menu_open']:
            logger.info('Opening project file')
            self.create_dialog('project_chooser')
            res = self.ui['project_chooser'].run()
            if res == Gtk.ResponseType.OK:
                filename = self.ui['project_chooser'].get_filename()
                self.project.load(filename)
                self.script = self.project.get_script()
                self.source.set_text(self.script.get_source())
                self.captured_image = self.project.get_image()
                pixbuf = rgbarray2pixbuf(self.captured_image)
                self.ui['capture_image'].set_from_pixbuf(pixbuf)
            self.ui['project_chooser'].destroy()
        elif widget is self.ui['menu_save']:
            logger.info('Saving project file')
            self.create_dialog('project_saver')
            res = self.ui['project_saver'].run()
            if res == Gtk.ResponseType.OK:
                self.project.set_image(self.captured_image)
                self.script.set_source(self.get_sourcecode())
                self.project.set_script(self.script)
                filename = self.ui['project_saver'].get_filename()
                self.project.save(filename)
            self.ui['project_saver'].destroy()

    def create_dialog(self, name):
        """Create the dialog with given name."""
        if name is 'script_chooser' or (name is 'all'):
            self.ui['script_chooser'] = Gtk.FileChooserDialog(
                'Choose a script file',
                None, Gtk.FileChooserAction.OPEN,
                (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                 Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
            )
            self.ui['script_chooser'].add_filter(self.ui['python_filter'])
        if name is 'script_saver' or (name is 'all'):
            self.ui['script_saver'] = Gtk.FileChooserDialog(
                'Save to file',
                None, Gtk.FileChooserAction.SAVE,
                (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                 Gtk.STOCK_SAVE, Gtk.ResponseType.OK)
            )
            self.ui['script_saver'].add_filter(self.ui['python_filter'])
            self.ui['script_saver'].set_do_overwrite_confirmation(True)
        if name is 'figure_exporter' or (name is 'all'):
            self.ui['figure_exporter'] = Gtk.FileChooserDialog(
                'Save to file',
                None, Gtk.FileChooserAction.SAVE,
                (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                 Gtk.STOCK_SAVE, Gtk.ResponseType.OK)
            )
            self.ui['figure_exporter'].add_filter(self.ui['jpeg_filter'])
            self.ui['figure_exporter'].add_filter(self.ui['png_filter'])
            self.ui['figure_exporter'].add_filter(self.ui['svg_filter'])
            self.ui['figure_exporter'].add_filter(self.ui['postscript_filter'])
        if name is 'project_chooser' or (name is 'all'):
            self.ui['project_chooser'] = Gtk.FileChooserDialog(
                'Choose project',
                None, Gtk.FileChooserAction.OPEN,
                (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                 Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
            )
            self.ui['project_chooser'].add_filter(self.ui['project_filter'])
        if name is 'project_saver' or (name is 'all'):
            self.ui['project_saver'] = Gtk.FileChooserDialog(
                'Save project',
                None, Gtk.FileChooserAction.SAVE,
                (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                 Gtk.STOCK_SAVE, Gtk.ResponseType.OK)
            )
            self.ui['project_saver'].add_filter(self.ui['project_filter'])

    def get_sourcecode(self):
        """Get the current source code entered in the editor."""
        return self.source.get_text(self.source.get_start_iter(),
                                    self.source.get_end_iter(), True)

    def end(self, *args):
        """Stop any running capture and end program."""
        Gtk.main_quit()

    def __del__(self):
        """Stop any running capture and end program."""
        self.end(None, None)
