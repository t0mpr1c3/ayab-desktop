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
import os
import logging
from math import ceil
from bitarray import bitarray
import numpy as np

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt, QThread, pyqtSignal

from PIL import Image
from fysom import FysomError

from ayab.ayab_gui import Ui_MainWindow
from ayab.ayab_about import Ui_AboutForm
from .ayab_transforms import Transformable, Mirrors
from ayab.ayab_preferences import Preferences
from ayab.plugins.ayab_plugin import AyabPlugin
from ayab.plugins.ayab_plugin.firmware_flash import FirmwareFlash
from ayab.plugins.ayab_plugin.ayab_progress import Ui_Progress
from ayab.plugins.ayab_plugin.ayab_control import KnittingMode, Progress

from DAKimport import DAKimport

# Temporal serial imports.
import serial
import serial.tools.list_ports

# from playsound import playsound

# TODO move to generic configuration
MACHINE_WIDTH = 200
BAR_HEIGHT = 5.0
LIMIT_BAR_WIDTH = 0.5


logging.basicConfig(filename='ayab_log.txt',
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
    QtWidgets.QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
# Remove Help Button
if hasattr(Qt, 'AA_DisableWindowContextHelpButton'):
    QtWidgets.QApplication.setAttribute(Qt.AA_DisableWindowContextHelpButton, True)

    
class GuiMain(QMainWindow):
    """GuiMain is the main object that handles the instance of AYAB's GUI from ayab_gui.UiForm .

    GuiMain inherits from QMainWindow and instantiates a window with the form components form ayab_gui.UiForm.
    """
    signalNewProgressWindow = pyqtSignal(int, int, int, int)
    signalShowProgressWindow = pyqtSignal()
    signalUpdateProgress = pyqtSignal(int, int, int)
    signalUpdateColorSymbol = pyqtSignal('QString')
    signalUpdateStatus = pyqtSignal(int, int, 'QString', int)
    signalUpdateKnitrow = pyqtSignal(Progress, int)
    signalUpdateNotification = pyqtSignal('QString')
    signalDisplayPopUp = pyqtSignal('QString', 'QString')
    signalUpdateNeedles = pyqtSignal(int, int)
    signalUpdateAlignment = pyqtSignal('QString')
    signalDisplayBlockingPopUp = pyqtSignal('QString', 'QString')
    signalPlaysound = pyqtSignal('QString')
    signalUpdateButtonKnitEnabled = pyqtSignal(bool)
    signalUpdateWidgetKnitcontrolEnabled = pyqtSignal(bool)

    def __init__(self, app_context):
        super(GuiMain, self).__init__(None)

        self.app_context = app_context

        self.image_file_route = None
    
        self.prefs = Preferences()

        self.pil_image = None
        self.start_needle = 80
        self.stop_needle = 119
        self.imageAlignment = self.prefs.settings.value("default_alignment")
        self.var_progress = 0
        self.zoomlevel = 3

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.enabled_plugin = AyabPlugin()
        self.enabled_plugin.setup_ui(self)

        knitting_mode_box = self.enabled_plugin.options_ui.knitting_mode_box
        knitting_mode_box.setCurrentIndex(knitting_mode_box.findText(self.prefs.settings.value("default_knitting_mode")))
        if self.prefs.settings.value("default_infinite_repeat"):
            self.enabled_plugin.options_ui.infRepeat_checkbox.setCheckState(QtCore.Qt.Checked)
        else:
            self.enabled_plugin.options_ui.infRepeat_checkbox.setCheckState(QtCore.Qt.Unchecked)
        if self.prefs.settings.value("automatic_mirroring"):
            self.enabled_plugin.options_ui.autoMirror_checkbox.setCheckState(QtCore.Qt.Checked)
        else:
            self.enabled_plugin.options_ui.autoMirror_checkbox.setCheckState(QtCore.Qt.Unchecked)
        alignment_combo_box = self.enabled_plugin.options_ui.alignment_combo_box
        alignment_combo_box.setCurrentIndex(alignment_combo_box.findText(self.imageAlignment))
        
        self.showMaximized()
        self.setupBehaviour()

        self.ui.label_notifications.setText("")
        self.ui.label_current_row.setText("")
        self.ui.label_current_color.setText("")

    def newProgressWindow(self):
        '''Generates knit progress window.'''
        try:
            self.kp.pd.close()
        except:
            pass
        self.kp = Ui_Progress()
        self.kp.pd.canceled.connect(self.cancel_knitting_process)
        return

    def updateProgress(self, row, total=0, repeats=0):
        '''Updates the Progress Bar.'''
        # Store to local variable
        self.var_progress = row
        self.refresh_scene()

        # Update label
        if total != 0:
            text = "Row {0}/{1}".format(row, total)
            if repeats >= 0:
                text += " ({0} repeats completed)".format(repeats)
        else:
            text = ""
        self.ui.label_current_row.setText(text)
        
        options_ui = self.enabled_plugin.options_ui
        options_ui.label_progress.setText("{0}/{1}".format(row, total))

    def updateColorSymbol(self, colorSymbol):
        '''Updates the current color symbol.'''
        text = ""
        if colorSymbol != "":
            text += "Color "
        self.ui.label_current_color.setText(text + colorSymbol)
            
    def updateStatus(self, hall_l, hall_r, carriage_type, carriage_position):
        options_ui = self.enabled_plugin.options_ui
        options_ui.progress_hall_l.setValue(hall_l)
        options_ui.label_hall_l.setText(str(hall_l))
        options_ui.progress_hall_r.setValue(hall_r)
        options_ui.label_hall_r.setText(str(hall_r))
        options_ui.slider_position.setValue(carriage_position)
        options_ui.label_carriage.setText(carriage_type)

    def updateKnitrow(self, progress, row_multiplier):
        self.kp.update(progress, row_multiplier)
        
    def update_file_selected_text_field(self, route):
        '''Sets self.image_file_route and ui.filename_lineedit to route.'''
        self.ui.filename_lineedit.setText(route)
        self.image_file_route = route

    def slotUpdateNotification(self, text):
        '''Updates the Notification field'''
        logging.info("Notification: " + text)
        self.ui.label_notifications.setText(text)

    def slotUpdateNeedles(self, start_needle, stop_needle):
        '''Updates the position of the start/stop needle visualisation'''
        self.start_needle = start_needle
        self.stop_needle = stop_needle
        self.refresh_scene()

    def slotUpdateAlignment(self, alignment):
        '''Updates the alignment of the image between start/stop needle'''
        self.imageAlignment = alignment
        self.refresh_scene()

    def slotUpdateWidgetKnitcontrolEnabled(self, enabled):
        self.ui.widget_knitcontrol.setEnabled(enabled)        
    
    def slotUpdateButtonKnitEnabled(self, enabled):
        self.ui.knit_button.setEnabled(enabled)

    def wheelEvent(self, event):
        '''Using mouse wheel events to zoom the pattern view'''
        if self.pil_image is not None:
            # angleDelta.y is 120 or -120 when scrolling
            zoom = event.angleDelta().y() / 120

            self.zoomlevel = self.zoomlevel + zoom
            if self.zoomlevel <= 1:
                self.zoomlevel = 1
            elif self.zoomlevel >= 5:
                self.zoomlevel = 5
            self.refresh_scene()

    def start_knitting_process(self):
        # Disable everything which should not be touched
        # during knitting
        self.ui.menuTools.setEnabled(False)
        self.ui.widget_imgload.setEnabled(False)
        self.ui.menuImage_Actions.setEnabled(False)
        self.ui.widget_optionsdock.setEnabled(False)
        self.ui.knit_button.setEnabled(False)
        self.ui.cancel_button.setEnabled(True)
        # start thread for knit plugin
        self.gt = GenericThread(self.enabled_plugin.knit, parent_window=self)
        self.gt.start()

    def cancel_knitting_process(self):
        self.kp.pd.reset()
        self.enabled_plugin.cancel()

    def resetUI(self):
        # (Re-)enable UI elements
        self.ui.menuTools.setEnabled(True)
        self.ui.widget_imgload.setEnabled(True)
        self.ui.menuImage_Actions.setEnabled(True)
        self.ui.widget_optionsdock.setEnabled(True)
        self.ui.knit_button.setEnabled(False)
        self.ui.cancel_button.setEnabled(False)

    def setupBehaviour(self):
        # Connecting UI elements.
        self.ui.load_file_button.clicked.connect(self.file_select_dialog)
        self.ui.knit_button.clicked.connect(self.start_knitting_process)
        self.ui.cancel_button.clicked.connect(self.cancel_knitting_process)
        self.ui.actionLoad_AYAB_Firmware.triggered.connect(self.generate_firmware_ui)
        self.ui.image_pattern_view.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
        # Connecting Signals.
        self.signalNewProgressWindow.connect(self.newProgressWindow)
        self.signalUpdateProgress.connect(self.updateProgress)
        self.signalUpdateColorSymbol.connect(self.updateColorSymbol)
        self.signalUpdateStatus.connect(self.updateStatus)
        self.signalUpdateKnitrow.connect(self.updateKnitrow)
        self.signalUpdateNotification.connect(self.slotUpdateNotification)
        self.signalDisplayPopUp.connect(self.display_blocking_pop_up)
        self.signalUpdateNeedles.connect(self.slotUpdateNeedles)
        self.signalUpdateAlignment.connect(self.slotUpdateAlignment)
        self.signalPlaysound.connect(self.slotPlaysound)
        self.signalUpdateWidgetKnitcontrolEnabled.connect(self.slotUpdateWidgetKnitcontrolEnabled)
        self.signalUpdateButtonKnitEnabled.connect(self.slotUpdateButtonKnitEnabled)

        # This blocks the other thread until signal is done
        self.signalDisplayBlockingPopUp.connect(self.display_blocking_pop_up)

        self.ui.actionQuit.triggered.connect(QtCore.QCoreApplication.instance().quit)
        self.ui.actionAbout.triggered.connect(self.open_about_ui)
        self.ui.actionInvert.triggered.connect(self.invert_image)
        self.ui.actionStretch.triggered.connect(self.stretch_image)
        self.ui.actionRepeat.triggered.connect(self.repeat_image)
        self.ui.actionReflect.triggered.connect(self.reflect_image)
        self.ui.actionHorizontal_Flip.triggered.connect(self.hflip_image)
        self.ui.actionVertical_Flip.triggered.connect(self.vflip_image)
        self.ui.actionRotate_Left.triggered.connect(self.rotate_left)
        self.ui.actionRotate_Right.triggered.connect(self.rotate_right)
        self.ui.actionSetPreferences.triggered.connect(self.set_preferences)

    def load_image_from_string(self, image_str):
        '''Loads an image into self.ui.image_pattern_view using a temporary QGraphicsScene'''

        # TODO Check for maximum width before loading the image

        # check for DAK files
        image_str_suffix = image_str[-4:].lower()
        if (image_str_suffix == ".pat" or image_str_suffix == ".stp"):
            # convert DAK file
            dakfile_processor = DAKimport.Importer()
            if (image_str_suffix == ".pat"):
                self.pil_image = dakfile_processor.pat2im(image_str)
            elif (image_str_suffix == ".stp"):
                self.pil_image = dakfile_processor.stp2im(image_str)
            else:
                logging.error("unrecognized file suffix")
        else:
            self.pil_image = Image.open(image_str)

        self.pil_image = self.pil_image.convert("RGBA")

        self.refresh_scene()
        self.statusBar().showMessage(image_str)
        # Enable plugin elements after first load of image
        self.ui.widget_optionsdock.setEnabled(True)
        self.ui.menuImage_Actions.setEnabled(True)
        # Tell loaded plugin elements about changed parameters
        width, height = self.pil_image.size
        self.enabled_plugin.slotSetImageDimensions(width, height)

    def refresh_scene(self):
        '''Updates the current scene '''
        width, height = self.pil_image.size

        data = self.pil_image.convert("RGBA").tobytes("raw", "RGBA")
        qim = QtGui.QImage(data,
                           self.pil_image.size[0],
                           self.pil_image.size[1],
                           QtGui.QImage.Format_ARGB32)
        pixmap = QtGui.QPixmap.fromImage(qim)

        self.set_dimensions_on_gui(pixmap.width(), pixmap.height())

        qscene = QtWidgets.QGraphicsScene()

        # add pattern and move accordingly to alignment
        pattern = qscene.addPixmap(pixmap)
        if self.imageAlignment == 'left':
            pattern.setPos(
                (self.start_needle - 100),
                0)
        elif self.imageAlignment == 'center':
            pattern.setPos(
                -(pixmap.width() / 2.0) + ((self.start_needle + self.stop_needle) / 2) - 100,
                0)
        elif self.imageAlignment == 'right':
            pattern.setPos(
                (self.stop_needle - 100 - pixmap.width()),
                0)
        else:
            logging.warning("invalid alignment")

        # Draw "machine"
        rect_orange = QtWidgets.QGraphicsRectItem(
            -(MACHINE_WIDTH / 2.0),
            -BAR_HEIGHT,
            (MACHINE_WIDTH / 2.0),
            BAR_HEIGHT)
        rect_orange.setBrush(QtGui.QBrush(QtGui.QColor("orange")))
        rect_green = QtWidgets.QGraphicsRectItem(
            0.0,
            -BAR_HEIGHT,
            (MACHINE_WIDTH / 2.0),
            BAR_HEIGHT)
        rect_green.setBrush(QtGui.QBrush(QtGui.QColor("green")))

        qscene.addItem(rect_orange)
        qscene.addItem(rect_green)

        # Draw limiting lines (start/stop needle)
        qscene.addItem(
            QtWidgets.QGraphicsRectItem(self.start_needle - 101,
                                        -BAR_HEIGHT,
                                        LIMIT_BAR_WIDTH,
                                        pixmap.height() + 2 * BAR_HEIGHT))
        qscene.addItem(
            QtWidgets.QGraphicsRectItem(self.stop_needle - 100,
                                        -BAR_HEIGHT,
                                        LIMIT_BAR_WIDTH,
                                        pixmap.height() + 2 * BAR_HEIGHT))

        # Draw knitting progress
        qscene.addItem(
            QtWidgets.QGraphicsRectItem(-(MACHINE_WIDTH / 2.0),
                                        pixmap.height() - self.var_progress,
                                        MACHINE_WIDTH,
                                        LIMIT_BAR_WIDTH))

        qv = self.ui.image_pattern_view
        qv.resetTransform()
        qv.scale(self.zoomlevel, self.zoomlevel)
        qv.setScene(qscene)

    def set_dimensions_on_gui(self, width, height):
        text = "{} - {}".format(width, height)
        self.ui.label_notifications.setText("Image Dimensions: " + text)

    def display_blocking_pop_up(self, message="", message_type="info"):
        logging.debug("MessageBox {}: '{}'".format(message_type, message))
        box_function = {
            "error": QtWidgets.QMessageBox.critical,
            "info": QtWidgets.QMessageBox.information,
            "question": QtWidgets.QMessageBox.question,
            "warning": QtWidgets.QMessageBox.warning
        }
        message_box_function = box_function.get(message_type)

        ret = message_box_function(
            self,
            "AYAB",
            message,
            QtWidgets.QMessageBox.Ok,
            QtWidgets.QMessageBox.Ok)
        if ret == QtWidgets.QMessageBox.Ok:
            return True

    def conf_button_function(self):
        self.enabled_plugin.configure(self)

    def file_select_dialog(self):
        filenameValue = self.ui.filename_lineedit.text()
        if filenameValue == '':
            filePath = self.app_context.get_resource("patterns")
        else:
            filePath = ''
        file_selected_route, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open file", filePath, 'Images (*.png *.PNG *.jpg *.JPG *.jpeg *.JPEG *.bmp *.BMP *.gif *.GIF *.tiff *.TIFF *.tif *.TIF *.Pat *.pat *.PAT *.Stp *.stp *.STP)')
        if file_selected_route:
            self.update_file_selected_text_field(file_selected_route)
            self.load_image_from_string(str(file_selected_route))

    def generate_firmware_ui(self):
        self.__flash_ui = FirmwareFlash(self)
        self.__flash_ui.show()

    def open_about_ui(self):
        __version__ = "package_version"
        filename_version = self.app_context.get_resource("ayab/package_version")
        with open(filename_version) as version_file:
            __version__ = version_file.read().strip()
        
        self.__AboutForm = QtWidgets.QFrame()
        self.__about_ui = Ui_AboutForm()
        self.__about_ui.setupUi(self.__AboutForm)
        self.__about_ui.label_3.setText("Version " + __version__)
        self.__AboutForm.show()

    def invert_image(self):
        '''Public invert current Image function.'''
        self.apply_image_transform("invert")

    def repeat_image(self):
        '''Public repeat current Image function.'''
        v = QtWidgets.QInputDialog.getInt(
            self,
            "Repeat",
            "Vertical",
            value=1,
            min=1
        )
        h = QtWidgets.QInputDialog.getInt(
            self,
            "Repeat",
            "Horizontal",
            value=1,
            min=1,
            max=ceil(MACHINE_WIDTH / self.pil_image.size[0])
        )
        self.apply_image_transform("repeat", v[0], h[0])

    def stretch_image(self):
        '''Public stretch current Image function.'''
        v = QtWidgets.QInputDialog.getInt(
            self,
            "Stretch",
            "Vertical",
            value=1,
            min=1
        )
        h = QtWidgets.QInputDialog.getInt(
            self,
            "Stretch",
            "Horizontal",
            value=1,
            min=1,
            max=ceil(MACHINE_WIDTH / self.pil_image.size[0])
        )
        self.apply_image_transform("stretch", v[0], h[0])

    def reflect_image(self):
        '''Public reflect current Image function.'''
        m = Mirrors()
        if (m.result == QtWidgets.QDialog.Accepted):
            self.apply_image_transform("reflect", m.mirrors)

    def hflip_image(self):
        '''Public horizontal flip current Image function.'''
        self.apply_image_transform("hflip")

    def vflip_image(self):
        '''Public vertical flip current Image function.'''
        self.apply_image_transform("vflip")

    def rotate_left(self):
        '''Public rotate left current Image function.'''
        self.apply_image_transform("rotate", 90.0)

    def rotate_right(self):
        '''Public rotate right current Image function.'''
        self.apply_image_transform("rotate", -90.0)

    def apply_image_transform(self, method, *args):
        '''Executes an image transform specified by key and args.

        Calls a transform function, forwarding args and the image,
        and replaces the QtImage on scene.
        '''
        transform = getattr(Transformable, method)
        try:
            image = transform(self.pil_image, args)
        except:
            logging.error("Error on executing transform")
        if not image:
            return

        # Update the view
        self.pil_image = image

        # Disable Knit Controls
        self.ui.widget_knitcontrol.setEnabled(False)

        # Update maximum values
        width, height = self.pil_image.size
        self.enabled_plugin.slotSetImageDimensions(width, height)
        # Draw canvas
        self.refresh_scene()

    def set_preferences(self):
        return self.prefs.setPrefsDialog()

    def getSerialPorts(self):
        """
        Returns a list of all USB Serial Ports
        """
        return list(serial.tools.list_ports.grep("USB"))

    def slotPlaysound(self, event):
        return
        # if event == "start":
        #     playsound(self.app_context.get_resource("assets/start.wav"))
        # if event == "nextline":
        #     playsound(self.app_context.get_resource("assets/nextline.wav"))
        # if event == "finished":
        #     playsound(self.app_context.get_resource("assets/finish.wav"))


class GenericThread(QThread):
    '''A generic thread wrapper for functions on threads.'''

    def __init__(self, function, *args, **kwargs):
        QtCore.QThread.__init__(self)
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def __del__(self):
        #self.join()
        self.wait()

    def run(self):
        try:
            self.function(*self.args, **self.kwargs)
        except FysomError as fe:
            logging.error(fe)
        return

def run(app_context):
    translator = QtCore.QTranslator()
    ## Loading ayab_gui main translator.
    translator.load(QtCore.QLocale.system(), "ayab_gui", ".", app_context.get_resource("ayab/translations"), ".qm")
    app = QtWidgets.QApplication(sys.argv)
    app.installTranslator(translator)
    window = GuiMain(app_context)
    window.show()
    sys.exit(app.exec_())
