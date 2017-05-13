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
from PyQt4 import QtGui, QtCore

class ShipType():
    def __init__(self, desc, number):
        self.description = desc
        self.number = number
    def getDescription(self):
        return self.description
    def getNumber(self):
        return self.number

class QComboBoxShipType(QtGui.QComboBox):
    shipTypes = [ShipType("WIG", 20),
                 ShipType("Vessel-Fishing", 30),
                 ShipType("Vessel-Towing", 31),
                 ShipType("Vessel-Tow, L>200m, W>25m", 32),
                 ShipType("Vessel-Dredge, Underwater OP", 33),
                 ShipType("Vessel-Diving OP", 34),
                 ShipType("Vessel-Military OP", 35),
                 ShipType("Vessel-Sailing", 36),
                 ShipType("Vessel-Pleasure Craft", 37),
                 ShipType("HSC", 40),
                 ShipType("Pilot Vessel", 50),
                 ShipType("Search And Rescue Vessel", 51),
                 ShipType("Tug", 52),
                 ShipType("Port tender", 53),
                 ShipType("Anti-Pollution Vessel", 54),
                 ShipType("Law Enforcement Vessel", 55),
                 ShipType("Medical Transport", 58),
                 ShipType("Resolution 18(Mob-83)", 59),
                 ShipType("Passenger Ship", 60),
                 ShipType("Cargo Ship", 70),
                 ShipType("Tanker", 80)]

    def __init__(self, parent=None):
        super(QComboBoxShipType, self).__init__(parent)
        for shipType in self.shipTypes:
            self.addItem("{} = {}".format(shipType.getNumber(),
                                          shipType.getDescription()))
        # Default value is Vessel-Sailing
        self.setShipTypeByNumber(36)

    def setShipTypeByNumber(self, shipNumber):
        for index, shipType in enumerate(self.shipTypes):
            if shipType.getNumber() == shipNumber:
                self.setCurrentIndex(index)
                self.setItemData(index, QtGui.QColor("#FFFF3D"), QtCore.Qt.BackgroundRole)
            else:
                self.setItemData(index, QtGui.QColor("#FFFFFF"), QtCore.Qt.BackgroundRole)

    def getCurrentShipType(self):
        return self.shipTypes[self.currentIndex()]
