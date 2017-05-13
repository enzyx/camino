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
from camino_api import Camino
from PyQt4 import QtGui

class CaminoApiWrapper(Camino):
    def showNotConnectedBox(self):
        msg = QtGui.QMessageBox()
        msg.setIcon(QtGui.QMessageBox.Information)
        msg.setText("Please connect the device!")
        msg.setWindowTitle("Device not connected")
        msg.setStandardButtons(QtGui.QMessageBox.Cancel)
        retval = msg.exec_()

    def programCamino(self):
        if self.serialDevice is not None:
            shipName = self.lineEditShipName.text()
            callSign = self.lineEditCallSign.text()
            mmsi     = self.lineEditMMSI.text()
            shipType = self.comboBoxShipType.getCurrentShipType().getNumber()
            dimA, dimB, dimC, dimD = self.spinBoxDimA.text(),\
                                     self.spinBoxDimB.text(),\
                                     self.spinBoxDimC.text(),\
                                     self.spinBoxDimD.text()
            self.configureAISData(shipName, callSign, [dimA,dimB,dimC,dimD])
            self.configureShipType(shipType)
        else:
            self.showNotConnectedBox()

    def readCamino(self):
        if self.serialDevice is not None:
            self.showStatusBarMessage('Reading Device...')
            self.getDeviceInfo()
        else:
            self.showNotConnectedBox()
