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
import gpgsv, gpgga, gpvtg

class InputParser(object):
    def __init__(self, QMainWindow):
        self.QMainWindow = QMainWindow
        self.gpgsvCollector = gpgsv.GPGSVCollector()
        self.gpgsvMessage = gpgsv.GPGSVMessage()
        self.gpggaMessage = gpgga.GPGGAMessage()
        self.gpvtgMessage = gpvtg.GPVTGMessage()

    def update(self, data):
        self.QMainWindow.textEditLog.appendPlainText(data.strip())
        if "(01) MMSI:(" in data:
            self.QMainWindow.lineEditMMSI.setText(data[10:20])
        if "(03) Name:(" in data:
            self.QMainWindow.lineEditShipName.setText(data.strip()[11:-1])
        if "(04) Call Sign:(" in data:
            self.QMainWindow.lineEditCallSign.setText(data.strip()[16:-1])
        if "(05) Ship Cargo Type:(" in data:
            shipType = data.split('(')[2].split(')')[0]
            self.QMainWindow.comboBoxShipType.setShipTypeByNumber(int(shipType))
            self.QMainWindow.spinBoxDimA.setValue(int(data.split('(')[3].split(')')[0]))
            self.QMainWindow.spinBoxDimB.setValue(int(data.split('(')[4].split(')')[0]))
            self.QMainWindow.spinBoxDimC.setValue(int(data.split('(')[5].split(')')[0]))
            self.QMainWindow.spinBoxDimD.setValue(int(data.split('(')[6].split(')')[0]))

        if "$GPGSV," in data:
            self.gpgsvCollector.addMessage(data)
            if self.gpgsvCollector.isComplete():
                self.gpgsvMessage = self.gpgsvCollector.getGPGSVMessage()
                self.QMainWindow.gpsBarPlot.updateData(self.gpgsvMessage)
                self.QMainWindow.gpsSatellitePlot.updateData(self.gpgsvMessage)

        if "$GPGGA," in data:
            self.gpggaMessage.parseGPGGAMessage(data)
            self.QMainWindow.updateGPSData(self.gpggaMessage)
            # print self.gpggaMessage.getPositionString()
            # print self.gpggaMessage.getAltitudeString()

        if "$GPVTG," in data:
            self.gpvtgMessage.parseGPVTGMessage(data)
            self.QMainWindow.updateSpeedOverGround(self.gpvtgMessage)
