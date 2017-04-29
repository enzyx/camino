#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
import sys,os
from PyQt4 import QtGui
from PyQt4 import QtCore
from serial import Serial

from input_parser import InputParser
import design_overlay
import settings_view
from camino_108 import Camino
from settings import Settings
import signal

class SerialListener(QtCore.QThread):
    new_data = QtCore.pyqtSignal(object)
    sig_disconnect = QtCore.pyqtSignal(object)

    def __init__(self, device):
        self.device = device
        QtCore.QThread.__init__(self)

    def run(self):
        self.request_stop = False
        while self.request_stop is False:
            try:
                line = self.device.readline()
                self.new_data.emit(line)
            except:
                self.sig_disconnect.emit(line)

    def quit(self):
        self.request_stop = True

class CaminoProgrammer(QtGui.QMainWindow, design_overlay.UiOverlayWindow):
    serialListener = None
    serialDevice = None
    def __init__(self, parent=None):
        super(CaminoProgrammer, self).__init__(parent)
        self.setupUi(self)
        self.actionExit.triggered.connect(QtGui.qApp.quit)
        self.actionConnect.triggered.connect(self.connectCamino)
        self.actionDisconnect.triggered.connect(self.disconnectCamino)
        self.pushButtonConfigureDevice.clicked.connect(self.programCamino)
        self.pushButtonReadDevice.clicked.connect(self.readCamino)

        self.inputParser = InputParser(self)

        # Instance of the settings device
        self.settings = Settings(self)
        self.actionSettings.triggered.connect(self.settings.show)

    def connectCamino(self):
        if self.serialDevice is None:
             self.serialDevice = Serial(self.settings.serial_port, 115200, timeout=5)

        if self.serialListener is None:
            self.serialListener = SerialListener(self.serialDevice)
            self.serialListener.new_data.connect(self.inputParser.update)
            self.serialListener.sig_disconnect.connect(self.disconnectCamino)
            self.serialListener.start()
            self.setStatusConnected(self.settings.serial_port)

    def disconnectCamino(self):
        self.setStatusDisconnected()
        if self.serialListener is not None:
            self.serialListener.quit()
            self.serialListener.wait()
            del(self.serialListener)

        if self.serialDevice is not None:
            del(self.serialDevice)

    def programCamino(self):
        print self.lineEditShipName.text()
        print self.lineEditCallSign.text()
        print self.lineEditMMSI.text()
        print int(self.comboBoxShipType.currentText().split('=')[0])
        print self.spinBoxDimA.text(), self.spinBoxDimB.text(), \
              self.spinBoxDimC.text(),self.spinBoxDimD.text()

    def readCamino(self):
        # self.camino.getDeviceInfo()
        if self.serialDevice is not None:
            self.serialDevice.write('$PTST,,,,,00016*18\r\n')
        else:
            msg = QtGui.QMessageBox()
            msg.setIcon(QtGui.QMessageBox.Information)
            msg.setText("Please connect the device!")
            msg.setWindowTitle("Device not connected")
            msg.setStandardButtons(QtGui.QMessageBox.Cancel)
            retval = msg.exec_()
            print "value of pressed message box button:", retval




def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QtGui.QApplication(sys.argv)
    form = CaminoProgrammer()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
