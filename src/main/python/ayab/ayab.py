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

from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5.QtCore import Qt, QTranslator, QThread, QLocale, QCoreApplication, QSettings

import simpleaudio as sa
import wave

from . import notify
from .ayab_gui import Ui_MainWindow
from .ayab_fsm import FSM
from .ayab_observer import Observer
from .ayab_menu import Menu
from .ayab_scene import Scene
from .ayab_transforms import Transform
from .firmware_flash import FirmwareFlash
from .ayab_preferences import Preferences, str2bool
from .ayab_progressbar import ProgressBar
from .ayab_about import About
from .ayab_knitprogress import KnitProgress
from .plugins.ayab_plugin import AyabPlugin
from .plugins.ayab_plugin.ayab_options import Alignment
from .plugins.ayab_plugin.machine import Machine

# TODO move to generic configuration

# make AYAB folder in user's home directory
userdata_path = path.expanduser(path.join("~", "AYAB"))
if not path.isdir(userdata_path):
    mkdir(userdata_path)

# configure logger
logfile = path.join(userdata_path, "ayab_log.txt")
logging.basicConfig(
    filename=logfile,
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
    """
    GuiMain is the main object that handles the instance of the Ayab GUI.

    GuiMain inherits from QMainWindow and instantiates a window with
    components from `ayab_gui.ui`
    """
    def __init__(self, app_context):
        super().__init__()
        self.app_context = app_context

        # get preferences
        self.prefs = Preferences(app_context)

        # create UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # add modular components
        self.menu = Menu(self)
        self.about = About(self)
        self.seer = Observer()
        self.scene = Scene(self)
        self.knitprog = KnitProgress(self)
        self.plugin = AyabPlugin(self)
        self.progbar = ProgressBar(self)
        self.flash = FirmwareFlash(self)
        self.gt = GenericThread(self.plugin.knit)

        # set default knitting configuration options
        self.__set_defaults()

        # clear progress bar and notification label
        self.progbar.reset()
        self.update_notification("", False)

        # show UI
        self.showMaximized()

        # Activate signals and UI elements
        self.__activate_ui()
        self.__activate_menu()
        self.seer.activate_signals(self)

        # initialize FSM
        self.fsm = FSM()
        self.fsm.set_transitions(self)
        self.fsm.set_properties(self.ui)
        self.fsm.machine.start()

    def __set_defaults(self):
        """Set default knitting configuration options."""
        defaults = self.prefs.settings
        self.plugin.ui.knitting_mode_box.setCurrentIndex(
            defaults.value("default_knitting_mode"))
        if str2bool(defaults.value("default_infinite_repeat")):
            self.plugin.ui.inf_repeat_checkbox.setCheckState(Qt.Checked)
        else:
            self.plugin.ui.inf_repeat_checkbox.setCheckState(Qt.Unchecked)
        if str2bool(defaults.value("automatic_mirroring")):
            self.plugin.ui.auto_mirror_checkbox.setCheckState(Qt.Checked)
        else:
            self.plugin.ui.auto_mirror_checkbox.setCheckState(Qt.Unchecked)
        self.plugin.ui.alignment_combo_box.setCurrentIndex(
            self.scene.alignment.value)

    def __activate_ui(self):
        self.ui.load_file_button.clicked.connect(
            self.scene.ayabimage.select_file)
        self.ui.filename_lineedit.returnPressed.connect(
            self.scene.ayabimage.select_file)
        self.ui.cancel_button.clicked.connect(self.plugin.cancel)

    def __activate_menu(self):
        self.menu.ui.action_quit.triggered.connect(
            QCoreApplication.instance().quit)
        self.menu.ui.action_load_AYAB_firmware.triggered.connect(
            self.flash.show)
        self.menu.ui.action_set_preferences.triggered.connect(
            self.prefs.open_dialog)
        self.menu.ui.action_about.triggered.connect(self.about.show)
        # get names of image actions from Transform methods
        transforms = filter(lambda x: x[0] != "_", Transform.__dict__.keys())
        for t in transforms:
            action = getattr(self.menu.ui, "action_" + t)
            slot = getattr(self.scene.ayabimage, t)
            action.triggered.connect(slot)

    def start_knitting(self):
        """Start kntting process."""
        # reset knit progress window
        self.knitprog.reset()
        # disable UI elements at start of knitting
        self.menu.depopulate()
        self.ui.filename_lineedit.setEnabled(False)
        self.ui.load_file_button.setEnabled(False)
        # start thread for knit plugin
        self.gt.start()

    def reset_ui_after_knitting(self, audio: bool):
        """(Re-)enable UI elements after knitting finishes."""
        self.menu.repopulate()
        self.ui.filename_lineedit.setEnabled(True)
        self.ui.load_file_button.setEnabled(True)
        if audio:
            self.audio("finish")

    def set_image_dimensions(self):
        """Set dimensions of image"""
        width, height = self.scene.ayabimage.image.size
        self.plugin.set_image_dimensions(width, height)
        self.progbar.row = self.scene.row_progress + 1
        self.progbar.total = height
        self.progbar.refresh()
        self.update_notification(
            QCoreApplication.translate("Scene", "Image dimensions") +
            ": {} x {}".format(width, height), False)
        self.scene.refresh()

    def update_start_row(self, start_row):
        self.progbar.update(start_row)
        self.scene.row_progress = start_row

    def update_notification(self, text, log=True):
        '''Update the notification field'''
        if log:
            logging.info("Notification: " + text)
        self.ui.label_notifications.setText(text)

    def audio(self, sound):
        """Play audio and wait until finished"""
        if str2bool(self.prefs.settings.value("quiet_mode")):
            return
        dirname = self.app_context.get_resource("assets")
        filename = sound + ".wav"
        try:
            wave_read = wave.open(path.join(dirname, filename), 'rb')
        except FileNotFoundError:
            logging.warning("File " + filename + " not found.")
        except OSError:
            logging.warning("Error loading " + filename + ".")
        else:
            wave_obj = sa.WaveObject.from_wave_read(wave_read)
            play_obj = wave_obj.play()
            play_obj.wait_done()

    def wheelEvent(self, event):
        self.scene.zoom = event


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
    except Exception:
        language = None
    try:
        translator.load("ayab_trans." + language, lang_dir)
    except (TypeError, FileNotFoundError):
        logging.warning(
            "Unable to load translation file for preferred language, using default locale"
        )
        try:
            translator.load(QLocale.system(), "ayab_trans", "", lang_dir)
        except Exception:
            logging.warning(
                "Unable to load translation file for default locale, using American English"
            )
            translator.load("ayab_trans.en_US", lang_dir)
    except Exception:
        logging.error("Unable to load translation file")
        raise
    app = QApplication(sys.argv)
    app.installTranslator(translator)

    # execute app
    window = GuiMain(app_context)
    window.show()
    sys.exit(app.exec_())
