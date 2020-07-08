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
#    Copyright 2013-2020 Sebastian Oliva, Christian Obersteiner,
#    Andreas Müller, Christian Gerbrandt
#    https://github.com/AllYarnsAreBeautiful/ayab-desktop

import logging
from math import ceil

from PIL import Image
from DAKimport import DAKimport
from PyQt5.QtWidgets import QInputDialog, QDialog, QFileDialog

from . import notify
from .ayab_transforms import Transform, Mirrors
from .plugins.ayab_plugin.ayab_observable import Observable
from .plugins.ayab_plugin.machine import Machine


class AyabImage(Observable):
    """
    Image object with public methods for performing image actions from menu.
    Implemented as PIL.Image with SignalEmitter mixin.

    @author Tom Price
    @date   July 2020
    """
    def __init__(self, parent):
        super().__init__(parent.seer)
        self.image = None
        self.filename = None
        self.filename_input = parent.ui.filename_lineedit
        self.statusbar = parent.statusBar()
        self.app_context = parent.app_context

    def select_file(self):
        filename = self.filename_input.text()
        if filename == '':
            filepath = self.app_context.get_resource("patterns")
        else:
            filepath = filename
        selected_file, _ = QFileDialog.getOpenFileName(
            None, "Open file", filepath,
            'Images (*.png *.PNG *.jpg *.JPG *.jpeg *.JPEG *.bmp *.BMP *.gif *.GIF *.tiff *.TIFF *.tif *.TIF *.Pat *.pat *.PAT *.Stp *.stp *.STP)'
        )
        if selected_file:
            self.filename = selected_file
            self.filename_input.setText(selected_file)
            self.__load(str(selected_file))

    def __load(self, filename):
        '''Load an image into the graphics scene.'''
        # TODO Check maximum width of image
        try:
            self.__open(filename)
        except (OSError, FileNotFoundError):
            notify.display_blocking_popup("Unable to load image file",
                                          "error")  # TODO translate
            logging.error("Unable to load " + str(filename))
        except Exception as e:
            notify.display_blocking_popup("Error loading image file",
                                          "error")  # TODO translate
            logging.error("Error loading image: " + str(e))
            raise
        else:
            self.statusbar.showMessage(filename)

    def __open(self, filename):
        # check for DAK files
        suffix = filename[-4:].lower()
        if (suffix == ".pat" or suffix == ".stp"):
            # convert DAK file
            dakfile_processor = DAKimport.Importer()
            if (suffix == ".pat"):
                self.image = dakfile_processor.pat2im(filename)
            elif (suffix == ".stp"):
                self.image = dakfile_processor.stp2im(filename)
            else:
                raise RuntimeError("Unrecognized file suffix")
        else:
            self.image = open(filename)
        self.image = self.image.convert("RGBA")
        self.emit_got_image_flag()
        self.emit_image_resizer()

    def invert(self):
        self.apply_transform(Transform.invert)

    def repeat(self):
        v = QInputDialog.getInt(None, "Repeat", "Vertical", value=1, min=1)
        h = QInputDialog.getInt(None,
                                "Repeat",
                                "Horizontal",
                                value=1,
                                min=1,
                                max=ceil(Machine.WIDTH / self.image.width))
        self.apply_transform(Transform.repeat, v[0], h[0])

    def stretch(self):
        v = QInputDialog.getInt(None, "Stretch", "Vertical", value=1, min=1)
        h = QInputDialog.getInt(None,
                                "Stretch",
                                "Horizontal",
                                value=1,
                                min=1,
                                max=ceil(Machine.WIDTH / self.image.width))
        self.apply_transform(Transform.stretch, v[0], h[0])

    def reflect(self):
        m = Mirrors()
        if (m.result == QDialog.Accepted):
            self.apply_transform(Transform.reflect, m.mirrors)

    def hflip(self):
        self.apply_transform(Transform.hflip)

    def vflip(self):
        self.apply_transform(Transform.vflip)

    def rotate_left(self):
        self.apply_transform(Transform.rotate_left)

    def rotate_right(self):
        self.apply_transform(Transform.rotate_right)

    def apply_transform(self, transform, *args):
        '''Executes an image transform specified by function and args.

        Calls a transform function, forwarding args and the image,
        and replaces the QtImage on scene.
        '''
        try:
            self.image = transform(self.image, args)
        except:
            logging.error("Error while executing image transform")

        # Update the view
        self.emit_image_resizer()

        # Transition to NOT_CONFIGURED state
        self.emit_new_image_flag()
