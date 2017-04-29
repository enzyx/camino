#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
        self.setCurrentIndex(7)

    def setShipTypeByNumber(self, shipNumber):
        for index, shipType in enumerate(self.shipTypes):
            if shipType.getNumber() == shipNumber:
                self.setCurrentIndex(index)
                self.setItemData(index, QtGui.QColor("#FFFF3D"), QtCore.Qt.BackgroundRole)

    def getCurrentShipType(self):
        return self.shipTypes[self.currentIndex()]
