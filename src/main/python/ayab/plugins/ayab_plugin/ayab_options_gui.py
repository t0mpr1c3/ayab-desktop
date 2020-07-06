# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ayab_options_gui.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DockWidget(object):
    def setupUi(self, DockWidget):
        DockWidget.setObjectName("DockWidget")
        DockWidget.resize(240, 581)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            DockWidget.sizePolicy().hasHeightForWidth())
        DockWidget.setSizePolicy(sizePolicy)
        DockWidget.setMinimumSize(QtCore.QSize(240, 581))
        DockWidget.setMaximumSize(QtCore.QSize(240, 581))
        DockWidget.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        DockWidget.setWindowTitle("")
        self.ayab_config = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.ayab_config.sizePolicy().hasHeightForWidth())
        self.ayab_config.setSizePolicy(sizePolicy)
        self.ayab_config.setObjectName("ayab_config")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.ayab_config)
        self.verticalLayout.setContentsMargins(-1, 0, -1, -1)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(self.ayab_config)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QtCore.QSize(220, 0))
        self.groupBox.setMaximumSize(QtCore.QSize(220, 16777215))
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.serial_port_dropdown = QtWidgets.QComboBox(self.groupBox)
        self.serial_port_dropdown.setObjectName("serial_port_dropdown")
        self.horizontalLayout_3.addWidget(self.serial_port_dropdown)
        self.refresh_ports_button = QtWidgets.QPushButton(self.groupBox)
        self.refresh_ports_button.setObjectName("refresh_ports_button")
        self.horizontalLayout_3.addWidget(self.refresh_ports_button)
        self.verticalLayout.addWidget(self.groupBox)
        self.tab_widget = QtWidgets.QTabWidget(self.ayab_config)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.tab_widget.sizePolicy().hasHeightForWidth())
        self.tab_widget.setSizePolicy(sizePolicy)
        self.tab_widget.setMinimumSize(QtCore.QSize(180, 430))
        self.tab_widget.setMaximumSize(QtCore.QSize(1000000, 16777215))
        self.tab_widget.setDocumentMode(False)
        self.tab_widget.setTabBarAutoHide(False)
        self.tab_widget.setObjectName("tab_widget")
        self.tab_knit = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.tab_knit.sizePolicy().hasHeightForWidth())
        self.tab_knit.setSizePolicy(sizePolicy)
        self.tab_knit.setObjectName("tab_knit")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.tab_knit)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(-1, -1, 224, 414))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(
            self.verticalLayoutWidget)
        self.verticalLayout_3.setContentsMargins(6, 13, 12, 6)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_3.addWidget(self.label_4)
        self.knitting_mode_box = QtWidgets.QComboBox(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.knitting_mode_box.sizePolicy().hasHeightForWidth())
        self.knitting_mode_box.setSizePolicy(sizePolicy)
        self.knitting_mode_box.setObjectName("knitting_mode_box")
        self.verticalLayout_3.addWidget(self.knitting_mode_box)
        self.label_6 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_3.addWidget(self.label_6)
        self.color_edit = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.color_edit.sizePolicy().hasHeightForWidth())
        self.color_edit.setSizePolicy(sizePolicy)
        self.color_edit.setMinimum(2)
        self.color_edit.setMaximum(6)
        self.color_edit.setObjectName("color_edit")
        self.verticalLayout_3.addWidget(self.color_edit)
        self.label_5 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_3.addWidget(self.label_5)
        self.start_row_edit = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.start_row_edit.sizePolicy().hasHeightForWidth())
        self.start_row_edit.setSizePolicy(sizePolicy)
        self.start_row_edit.setSuffix("")
        self.start_row_edit.setPrefix("")
        self.start_row_edit.setMinimum(1)
        self.start_row_edit.setMaximum(99999)
        self.start_row_edit.setObjectName("start_row_edit")
        self.verticalLayout_3.addWidget(self.start_row_edit)
        self.inf_repeat_checkbox = QtWidgets.QCheckBox(
            self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.inf_repeat_checkbox.sizePolicy().hasHeightForWidth())
        self.inf_repeat_checkbox.setSizePolicy(sizePolicy)
        self.inf_repeat_checkbox.setObjectName("inf_repeat_checkbox")
        self.verticalLayout_3.addWidget(self.inf_repeat_checkbox)
        self.gbox_startneedle = QtWidgets.QGroupBox(self.verticalLayoutWidget)
        self.gbox_startneedle.setMinimumSize(QtCore.QSize(0, 60))
        self.gbox_startneedle.setFlat(False)
        self.gbox_startneedle.setObjectName("gbox_startneedle")
        self.start_needle_color = QtWidgets.QComboBox(self.gbox_startneedle)
        self.start_needle_color.setGeometry(QtCore.QRect(60, 20, 81, 31))
        self.start_needle_color.setObjectName("start_needle_color")
        self.start_needle_edit = QtWidgets.QSpinBox(self.gbox_startneedle)
        self.start_needle_edit.setGeometry(QtCore.QRect(10, 20, 51, 31))
        self.start_needle_edit.setPrefix("")
        self.start_needle_edit.setMinimum(1)
        self.start_needle_edit.setMaximum(100)
        self.start_needle_edit.setProperty("value", 20)
        self.start_needle_edit.setObjectName("start_needle_edit")
        self.verticalLayout_3.addWidget(self.gbox_startneedle)
        self.gbox_stopneedle = QtWidgets.QGroupBox(self.verticalLayoutWidget)
        self.gbox_stopneedle.setMinimumSize(QtCore.QSize(0, 60))
        self.gbox_stopneedle.setObjectName("gbox_stopneedle")
        self.stop_needle_color = QtWidgets.QComboBox(self.gbox_stopneedle)
        self.stop_needle_color.setGeometry(QtCore.QRect(60, 20, 81, 31))
        self.stop_needle_color.setObjectName("stop_needle_color")
        self.stop_needle_edit = QtWidgets.QSpinBox(self.gbox_stopneedle)
        self.stop_needle_edit.setGeometry(QtCore.QRect(10, 20, 51, 31))
        self.stop_needle_edit.setPrefix("")
        self.stop_needle_edit.setMinimum(1)
        self.stop_needle_edit.setMaximum(100)
        self.stop_needle_edit.setProperty("value", 20)
        self.stop_needle_edit.setObjectName("stop_needle_edit")
        self.verticalLayout_3.addWidget(self.gbox_stopneedle)
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.alignment_combo_box = QtWidgets.QComboBox(
            self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.alignment_combo_box.sizePolicy().hasHeightForWidth())
        self.alignment_combo_box.setSizePolicy(sizePolicy)
        self.alignment_combo_box.setObjectName("alignment_combo_box")
        self.verticalLayout_3.addWidget(self.alignment_combo_box)
        self.auto_mirror_checkbox = QtWidgets.QCheckBox(
            self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.auto_mirror_checkbox.sizePolicy().hasHeightForWidth())
        self.auto_mirror_checkbox.setSizePolicy(sizePolicy)
        self.auto_mirror_checkbox.setObjectName("auto_mirror_checkbox")
        self.verticalLayout_3.addWidget(self.auto_mirror_checkbox)
        self.continuous_reporting_checkbox = QtWidgets.QCheckBox(
            self.verticalLayoutWidget)
        self.continuous_reporting_checkbox.setObjectName(
            "continuous_reporting_checkbox")
        self.verticalLayout_3.addWidget(self.continuous_reporting_checkbox)
        self.tab_widget.addTab(self.tab_knit, "")
        self.tab_status = QtWidgets.QWidget()
        self.tab_status.setObjectName("tab_status")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.tab_status)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(0, -1, 211, 333))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(
            self.verticalLayoutWidget_2)
        self.verticalLayout_4.setContentsMargins(6, 16, 12, 6)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_8 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_4.addWidget(self.label_8, 0,
                                        QtCore.Qt.AlignHCenter)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.progress_hall_l = QtWidgets.QProgressBar(
            self.verticalLayoutWidget_2)
        self.progress_hall_l.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.progress_hall_l.sizePolicy().hasHeightForWidth())
        self.progress_hall_l.setSizePolicy(sizePolicy)
        self.progress_hall_l.setMaximum(1024)
        self.progress_hall_l.setProperty("value", 0)
        self.progress_hall_l.setAlignment(QtCore.Qt.AlignCenter)
        self.progress_hall_l.setOrientation(QtCore.Qt.Vertical)
        self.progress_hall_l.setObjectName("progress_hall_l")
        self.verticalLayout_6.addWidget(self.progress_hall_l, 0,
                                        QtCore.Qt.AlignHCenter)
        self.label_hall_l = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_hall_l.sizePolicy().hasHeightForWidth())
        self.label_hall_l.setSizePolicy(sizePolicy)
        self.label_hall_l.setAlignment(QtCore.Qt.AlignCenter)
        self.label_hall_l.setObjectName("label_hall_l")
        self.verticalLayout_6.addWidget(self.label_hall_l)
        self.horizontalLayout.addLayout(self.verticalLayout_6)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.progress_hall_r = QtWidgets.QProgressBar(
            self.verticalLayoutWidget_2)
        self.progress_hall_r.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.progress_hall_r.sizePolicy().hasHeightForWidth())
        self.progress_hall_r.setSizePolicy(sizePolicy)
        self.progress_hall_r.setMaximum(1024)
        self.progress_hall_r.setProperty("value", 0)
        self.progress_hall_r.setAlignment(QtCore.Qt.AlignCenter)
        self.progress_hall_r.setOrientation(QtCore.Qt.Vertical)
        self.progress_hall_r.setObjectName("progress_hall_r")
        self.verticalLayout_7.addWidget(self.progress_hall_r, 0,
                                        QtCore.Qt.AlignHCenter)
        self.label_hall_r = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_hall_r.sizePolicy().hasHeightForWidth())
        self.label_hall_r.setSizePolicy(sizePolicy)
        self.label_hall_r.setAlignment(QtCore.Qt.AlignCenter)
        self.label_hall_r.setObjectName("label_hall_r")
        self.verticalLayout_7.addWidget(self.label_hall_r)
        self.horizontalLayout.addLayout(self.verticalLayout_7)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.line_2 = QtWidgets.QFrame(self.verticalLayoutWidget_2)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_4.addWidget(self.line_2)
        self.label_7 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_4.addWidget(self.label_7, 0,
                                        QtCore.Qt.AlignHCenter)
        self.label_carriage = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_carriage.sizePolicy().hasHeightForWidth())
        self.label_carriage.setSizePolicy(sizePolicy)
        self.label_carriage.setObjectName("label_carriage")
        self.verticalLayout_4.addWidget(self.label_carriage, 0,
                                        QtCore.Qt.AlignHCenter)
        self.slider_position = QtWidgets.QSlider(self.verticalLayoutWidget_2)
        self.slider_position.setEnabled(False)
        self.slider_position.setMaximum(199)
        self.slider_position.setOrientation(QtCore.Qt.Horizontal)
        self.slider_position.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.slider_position.setObjectName("slider_position")
        self.verticalLayout_4.addWidget(self.slider_position)
        self.label_direction = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_direction.sizePolicy().hasHeightForWidth())
        self.label_direction.setSizePolicy(sizePolicy)
        self.label_direction.setAlignment(QtCore.Qt.AlignCenter)
        self.label_direction.setObjectName("label_direction")
        self.verticalLayout_4.addWidget(self.label_direction, 0,
                                        QtCore.Qt.AlignHCenter)
        self.line_3 = QtWidgets.QFrame(self.verticalLayoutWidget_2)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout_4.addWidget(self.line_3)
        self.label_9 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_4.addWidget(self.label_9, 0,
                                        QtCore.Qt.AlignHCenter)
        self.label_progress = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Sans")
        font.setPointSize(22)
        self.label_progress.setFont(font)
        self.label_progress.setMouseTracking(False)
        self.label_progress.setObjectName("label_progress")
        self.verticalLayout_4.addWidget(self.label_progress, 0,
                                        QtCore.Qt.AlignHCenter)
        self.tab_widget.addTab(self.tab_status, "")
        self.verticalLayout.addWidget(self.tab_widget)
        DockWidget.setWidget(self.ayab_config)

        self.retranslateUi(DockWidget)
        self.tab_widget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(DockWidget)

    def retranslateUi(self, DockWidget):
        _translate = QtCore.QCoreApplication.translate
        self.groupBox.setTitle(_translate("DockWidget", "Port Selection"))
        self.refresh_ports_button.setText(_translate("DockWidget", "Refresh"))
        self.label_4.setText(_translate("DockWidget", "Knitting Mode"))
        self.label_6.setText(_translate("DockWidget", "Colors"))
        self.label_5.setText(_translate("DockWidget", "Start Row"))
        self.inf_repeat_checkbox.setText(
            _translate("DockWidget", "Infinite Repeat"))
        self.gbox_startneedle.setTitle(_translate("DockWidget",
                                                  "Start Needle"))
        self.gbox_stopneedle.setTitle(_translate("DockWidget", "Stop Needle"))
        self.label_3.setText(_translate("DockWidget", "Alignment"))
        self.auto_mirror_checkbox.setText(
            _translate("DockWidget", "Mirror Image"))
        self.continuous_reporting_checkbox.setText(
            _translate("DockWidget", "Continuous Status Reporting"))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_knit),
                                   _translate("DockWidget", "Settings"))
        self.label_8.setText(_translate("DockWidget", "Hall Sensors"))
        self.progress_hall_l.setFormat(_translate("DockWidget", "%p%"))
        self.label_hall_l.setText(_translate("DockWidget", "Hall Left"))
        self.progress_hall_r.setFormat(_translate("DockWidget", "%p%"))
        self.label_hall_r.setText(_translate("DockWidget", "Hall Right"))
        self.label_7.setText(_translate("DockWidget", "Carriage"))
        self.label_carriage.setText(
            _translate("DockWidget", "No carriage detected"))
        self.label_direction.setText(_translate("DockWidget", "direction"))
        self.label_9.setText(_translate("DockWidget", "Progress"))
        self.label_progress.setText(_translate("DockWidget", "progress"))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_status),
                                   _translate("DockWidget", "Status"))
