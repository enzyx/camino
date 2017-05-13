#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# This file is part of Camino.
# Copyright (C) 2017 Manuel Luitz <manuel.luitz@gmail.com>
#
# Camino is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Camino is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Camino. If not, see <http://www.gnu.org/licenses/>.
#
from PyQt4 import QtGui,QtCore
import settings_window

class Units():
    units = 0
    def setMetric(self):
        self.units = 0
    def setImperial(self):
        self.units = 1
    def isMetric(self):
        return self.units == 0
    def isImperial(self):
        return self.units == 1
    def get(self):
        if self.isMetric():
            return self.metric()
        elif self.isImperial():
            return self.imperial()
    def set(self, text):
        if text == self.metric(): self.setMetric()
        if text == self.imperial(): self.setImperial()
    def metric(self):
        return "Metric"
    def imperial(self):
        return "Imperial"


class Settings(QtGui.QMainWindow, settings_window.Ui_MainWindow):
    serial_port = '/dev/ttyACM0'
    units = Units()
    def __init__(self, parent=None):
        super(Settings, self).__init__(parent)
        self.setupUi(self)
        self.pushButtonApply.clicked.connect(self.applySettings)

    def applySettings(self):
        self.serial_port = self.lineEditSerialDevice.text()
        self.units.set(self.comboBoxUnits.currentText())

    def show(self):
        super(Settings, self).show()
        self.lineEditSerialDevice.setText(self.serial_port)
        index = self.comboBoxUnits.findText(self.units.get(), QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.comboBoxUnits.setCurrentIndex(index)
