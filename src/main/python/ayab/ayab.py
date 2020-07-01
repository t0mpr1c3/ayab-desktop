# -*- coding: utf-8 -*-
# This file is part of AYAB.
#
#    AYAB is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    AYAB is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with AYAB.  If not, see <http://www.gnu.org/licenses/>.
#
#    Copyright 2014 Sebastian Oliva, Christian Obersteiner, Andreas Müller, Christian Gerbrandt
#    https://github.com/AllYarnsAreBeautiful/ayab-desktop

"""Provides an Interface for users to operate AYAB using a GUI."""
from fbs_runtime.application_context.PyQt5 import ApplicationContext

import sys
from os import path, mkdir
import logging
import locale

import numpy as np

from PyQt5.QtWidgets import QMainWindow, QGraphicsView, QApplication, QMessageBox, QFrame, QFileDialog
from PyQt5.QtCore import Qt, QTranslator, QThread, QLocale, QCoreApplication, QSettings, pyqtSignal

from PIL import Image

import simpleaudio as sa
import wave

from .ayab_gui import Ui_MainWindow
from .ayab_about import Ui_AboutForm
from .ayab_fsm import FSM
from .ayab_scene import Scene
from .ayab_preferences import Preferences, str2bool
from .plugins.ayab_plugin import AyabPlugin
from .plugins.ayab_plugin.firmware_flash import FirmwareFlash
from .plugins.ayab_plugin.ayab_progress import KnitProgress
from .plugins.ayab_plugin.ayab_control import Progress
from .plugins.ayab_plugin.ayab_options import Alignment

# Temporal serial imports.
import serial
import serial.tools.list_ports


# TODO move to generic configuration

userdata_path = path.expanduser(path.join("~", "AYAB"))
if not path.isdir(userdata_path):
    mkdir(userdata_path)

logfile = path.join(userdata_path, "ayab_log.txt")
logging.basicConfig(filename=logfile,
                    level=logging.DEBUG,
                    format='%(asctime)s %(name)-8s %(levelname)-8s %(message)s',
                    datefmt='%y-%m-%d %H:%M:%S')
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
console.setFormatter(
    logging.Formatter('%(asctime)s %(name)-8s %(levelname)-8s %(message)s'))
logging.getLogger().addHandler(console)

# Fix PyQt5 for HiDPI screens
if hasattr(Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
# Remove Help Button
if hasattr(Qt, 'AA_DisableWindowContextHelpButton'):
    QApplication.setAttribute(Qt.AA_DisableWindowContextHelpButton, True)

    
class GuiMain(QMainWindow):
    """GuiMain is the main object that handles the instance of AYAB's GUI from ayab_gui.UiForm .

    GuiMain inherits from QMainWindow and instantiates a window with the form components form ayab_gui.UiForm.
    """
    signal_update_progress_bar = pyqtSignal(int, int, int, 'QString')
    signal_update_knit_progress = pyqtSignal(Progress, int)
    signal_update_status = pyqtSignal(int, int, 'QString', int)
    signal_update_notification = pyqtSignal('QString')
    signal_display_popup = pyqtSignal('QString', 'QString')
    signal_display_blocking_popup = pyqtSignal('QString', 'QString')
    signal_playsound = pyqtSignal('QString')
    signal_update_needles = pyqtSignal(int, int)
    signal_update_alignment = pyqtSignal(Alignment)
    signal_image_loaded = pyqtSignal()
    signal_image_transformed = pyqtSignal()
    signal_configure_fail = pyqtSignal()
    signal_configured = pyqtSignal()
    # signal_doneKnitProgress = pyqtSignal()
    signal_done_knitting = pyqtSignal(bool)

    def __init__(self, app_context):
        super(GuiMain, self).__init__(None)
        self.app_context = app_context

        self.image_file_route = None

        # get preferences
        self.prefs = Preferences(app_context)

        # create UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.__setup_menubar()
        self.scene = Scene(self)
        self.kp = KnitProgress(self.ui)
        self.plugin = AyabPlugin()
        self.plugin.setupUi(self)
        self.gt = GenericThread(self.plugin.knit)

        # set initial knitting configuration options
        knitting_mode_box = self.plugin.ui.knitting_mode_box
        knitting_mode_box.setCurrentIndex(self.prefs.settings.value("default_knitting_mode"))
        if str2bool(self.prefs.settings.value("default_infinite_repeat")):
            self.plugin.ui.infRepeat_checkbox.setCheckState(Qt.Checked)
        else:
            self.plugin.ui.infRepeat_checkbox.setCheckState(Qt.Unchecked)
        if str2bool(self.prefs.settings.value("automatic_mirroring")):
            self.plugin.ui.autoMirror_checkbox.setCheckState(Qt.Checked)
        else:
            self.plugin.ui.autoMirror_checkbox.setCheckState(Qt.Unchecked)
        alignment_combo_box = self.plugin.ui.alignment_combo_box
        alignment_combo_box.setCurrentIndex(self.scene.alignment.value)

        # clear progress and status bar
        self.ui.label_notifications.setText("")
        self.reset_progress_bar()

        # show UI
        self.showMaximized()

        # connect signals to slots
        self.__setup_behavior()

        # initialize FSM
        self.fs = FSM(self)
        self.fs.transitions()
        self.fs.properties()
        self.fs.machine.start()
        return

    def reset_progress_bar(self):
        self.ui.label_current_row.setText("")
        self.ui.label_current_color.setText("")

    def update_progress_bar(self, row, total=0, repeats=0, colorSymbol=""):
        '''Updates the color and row in progress bar'''
        if row < 0:
            return

        if colorSymbol == "":
            text = ""
        else:
            text = "Color " + colorSymbol
        self.ui.label_current_color.setText(text)

        # Store to local variable
        self.scene.row_progress = row
        self.scene.refresh()

        # Update label
        if total == 0:
            text = ""
        else:
            text = "Row {0}/{1}".format(row, total)
            if repeats >= 0:
                text += " ({0} repeats completed)".format(repeats)
        self.ui.label_current_row.setText(text)
        self.plugin.ui.label_progress.setText("{0}/{1}".format(row, total))

    def update_status(self, hall_l, hall_r, carriage_type, carriage_position):
        self.plugin.ui.progress_hall_l.setValue(hall_l)
        self.plugin.ui.label_hall_l.setText(str(hall_l))
        self.plugin.ui.progress_hall_r.setValue(hall_r)
        self.plugin.ui.label_hall_r.setText(str(hall_r))
        self.plugin.ui.slider_position.setValue(carriage_position)
        self.plugin.ui.label_carriage.setText(carriage_type)
        
    def update_notification(self, text):
        '''Updates the Notification field'''
        logging.info("Notification: " + text)
        self.ui.label_notifications.setText(text)

    def display_blocking_popup(self, message="", message_type="info"):
        logging.debug("MessageBox {}: '{}'".format(message_type, message))
        box_function = {
            "error": QMessageBox.critical,
            "info": QMessageBox.information,
            "question": QMessageBox.question,
            "warning": QMessageBox.warning
        }
        message_box_function = box_function.get(message_type)

        ret = message_box_function(
            self,
            "AYAB",
            message,
            QMessageBox.Ok,
            QMessageBox.Ok)
        if ret == QMessageBox.Ok:
            return True

    def update_knit_progress(self, progress, row_multiplier):
        self.kp.update(progress, row_multiplier)
        # if progress.current_row > 0 and progress.current_row == progress.total_rows:
        #     self.signal_done_knit_progress.emit()

    def wheelEvent(self, event):
        self.scene.zoom = event

    def __setup_behavior(self):
        # UI actions
        self.ui.load_file_button.clicked.connect(self.open_file_select_dialog)
        self.ui.filename_lineedit.returnPressed.connect(self.open_file_select_dialog)
        self.ui.cancel_button.clicked.connect(self.plugin.cancel)
        self.ui.actionLoad_AYAB_Firmware.triggered.connect(self.generate_firmware_ui)
        self.ui.image_pattern_view.setDragMode(QGraphicsView.ScrollHandDrag)

        # Menu actions
        self.ui.actionSetPreferences.triggered.connect(self.open_preferences_dialog)
        self.ui.actionAbout.triggered.connect(self.open_about_ui)
        self.ui.actionQuit.triggered.connect(QCoreApplication.instance().quit)
        self.ui.actionInvert.triggered.connect(self.scene.invert_image)
        self.ui.actionStretch.triggered.connect(self.scene.stretch_image)
        self.ui.actionRepeat.triggered.connect(self.scene.repeat_image)
        self.ui.actionReflect.triggered.connect(self.scene.reflect_image)
        self.ui.actionHorizontalFlip.triggered.connect(self.scene.hflip_image)
        self.ui.actionVerticalFlip.triggered.connect(self.scene.vflip_image)
        self.ui.actionRotateLeft.triggered.connect(self.scene.rotate_left)
        self.ui.actionRotateRight.triggered.connect(self.scene.rotate_right)

        # Signal actions
        self.signal_update_progress_bar.connect(self.update_progress_bar)
        self.signal_update_status.connect(self.update_status)
        self.signal_update_notification.connect(self.update_notification)
        self.signal_playsound.connect(self.playsound,
                                     type=Qt.BlockingQueuedConnection)
        self.signal_display_blocking_popup.connect(self.display_blocking_popup)
        self.signal_display_popup.connect(self.display_blocking_popup)
        self.signal_update_knit_progress.connect(self.update_knit_progress,
                                              type=Qt.BlockingQueuedConnection)
        self.signal_update_needles.connect(self.scene.update_needles)
        self.signal_update_alignment.connect(self.scene.update_alignment)
        self.signal_done_knitting.connect(self.reset_ui_after_knitting)

    def start_knitting_process(self):
        # reset knit progress window
        self.kp.reset()
        # disable UI elements at start of knitting
        self.__depopulate_menubar()
        self.ui.filename_lineedit.setEnabled(False)        
        self.ui.load_file_button.setEnabled(False)
        # start thread for knit plugin
        self.gt.start()

    def reset_ui_after_knitting(self, audio: bool):
        # (Re-)enable UI elements after knitting finishes
        self.__repopulate_menubar()
        self.ui.filename_lineedit.setEnabled(True)        
        self.ui.load_file_button.setEnabled(True)
        if audio:
            self.__audio("finish")

    def __setup_menubar(self):
        self.__action_image_actions = self.ui.menuImageActions.menuAction()
        self.__action_tools = self.ui.menuTools.menuAction()
        self.__action_preferences = self.ui.menuPreferences.menuAction()
        self.__action_help = self.ui.menuHelp.menuAction()
        self.ui.menubar.addAction(self.__action_tools)
        self.ui.menubar.addAction(self.__action_preferences)
        self.ui.menubar.addAction(self.__action_help)

    def __depopulate_menubar(self):
        try:
            self.ui.menubar.removeAction(self.__action_image_actions)
        except:
            pass
        self.ui.menubar.removeAction(self.__action_tools)

    def __repopulate_menubar(self):
        self.ui.menubar.removeAction(self.__action_preferences)
        self.ui.menubar.removeAction(self.__action_help)
        self.ui.menubar.addAction(self.__action_image_actions)
        self.ui.menubar.addAction(self.__action_tools)
        self.ui.menubar.addAction(self.__action_preferences)
        self.ui.menubar.addAction(self.__action_help)

    def add_image_actions(self):
        # This workaround is necessary because 
        # self.__actionImageActions.setEnabled(True)
        # does not seems to work (at least, not on Ubuntu 16.04)
        # Tom Price June 2020
        self.__depopulate_menubar()
        self.__repopulate_menubar()

    def open_file_select_dialog(self):
        filenameValue = self.ui.filename_lineedit.text()
        if filenameValue == '':
            filePath = self.app_context.get_resource("patterns")
        else:
            filePath = filenameValue
        file_selected_route, _ = QFileDialog.getOpenFileName(
            self, "Open file", filePath, 'Images (*.png *.PNG *.jpg *.JPG *.jpeg *.JPEG *.bmp *.BMP *.gif *.GIF *.tiff *.TIFF *.tif *.TIF *.Pat *.pat *.PAT *.Stp *.stp *.STP)')
        if file_selected_route:
            self.__update_file_selected_text_field(file_selected_route)
            self.__load_image_from_string(str(file_selected_route))

    def __update_file_selected_text_field(self, route):
        '''Sets self.image_file_route and ui.filename_lineedit to route.'''
        self.ui.filename_lineedit.setText(route)
        self.image_file_route = route

    def __load_image_from_string(self, image_str):
        '''Loads an image into self.ui.image_pattern_view using a temporary QGraphicsScene'''
        # TODO Check maximum width of image
        try:
            self.scene.load_image_file(image_str)
        except OSError:
            logging.error("unable to load " + str(image_str))
        except Exception as e:
            logging.error(e)
        else:
            self.scene.refresh()
            self.signal_image_loaded.emit()
            self.statusBar().showMessage(image_str)
            # Tell loaded plugin elements about changed parameters
            width, height = self.scene.image.size
            self.plugin.set_image_dimensions(width, height)

    def generate_firmware_ui(self):
        self.__flash_ui = FirmwareFlash(self)
        self.__flash_ui.show()

    def open_about_ui(self):
        __version__ = "package_version"
        filename_version = self.app_context.get_resource("ayab/package_version")
        with open(filename_version) as version_file:
            __version__ = version_file.read().strip()
        
        self.__AboutForm = QFrame()
        self.__about_ui = Ui_AboutForm()
        self.__about_ui.setupUi(self.__AboutForm)
        self.__about_ui.label_3.setText("Version " + __version__)
        self.__AboutForm.show()

    def open_preferences_dialog(self):
        return self.prefs.setPrefsDialog()

    def getSerialPorts(self):
        """
        Returns a list of all USB Serial Ports
        """
        return list(serial.tools.list_ports.grep("USB"))

    def playsound(self, sound):
        """Blocking -- call from external thread only"""
        self.__audio(sound)

    def __audio(self, sound):
        """Play audio and wait until finished"""
        if str2bool(self.prefs.settings.value("quiet_mode")):
            return 
        dirname = self.app_context.get_resource("assets")
        filename = sound + ".wav"
        try:
            wave_read = wave.open(path.join(dirname, filename), 'rb')
        except:
            logging.warning("File " + filename + " not found.")
        else:
            wave_obj = sa.WaveObject.from_wave_read(wave_read)
            play_obj = wave_obj.play()
            play_obj.wait_done()


class GenericThread(QThread):
    '''A generic thread wrapper for functions on threads.'''

    def __init__(self, function, *args, **kwargs):
        QThread.__init__(self)
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def __del__(self):
        #self.join()
        self.wait()

    def run(self):
        try:
            self.function(*self.args, **self.kwargs)
        except Exception:
            for arg in self.args:
                print(arg)
            for key, value in self.kwargs.items():
                print(key, value)
            raise


def run(app_context):
    # set constants for QSettings
    QCoreApplication.setOrganizationName("AYAB")
    QCoreApplication.setOrganizationDomain("ayab-knitting.com")
    QCoreApplication.setApplicationName("ayab")

    # load translators
    translator = QTranslator()
    lang_dir = app_context.get_resource("ayab/translations")
    try:
        language = QSettings().value("language")
    except:
        language = None
    try:
        translator.load("ayab_trans." + language, lang_dir)
    except (TypeError, FileNotFoundError):
        logging.warning("Unable to load translation file for preferred language, using default locale")
        try:
            translator.load(QLocale.system(), "ayab_trans", "", lang_dir)
        except:
            logging.warning("Unable to load translation file for default locale, using American English")
            translator.load("ayab_trans.en_US", lang_dir)
    except:
        logging.error("Unable to load translation file")
        raise
    app = QApplication(sys.argv)
    app.installTranslator(translator)

    # execute app
    window = GuiMain(app_context)
    window.show()
    sys.exit(app.exec_())
