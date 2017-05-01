#!/usr/bin/env python2
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
