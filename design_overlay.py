# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

import design
from gps_bar_plot import GPSBarPlot
from gps_satellite_plot import GPSSatellitePlot

from about import About

class UiOverlayWindow(design.Ui_MainWindow):
    def __init__(self, parent=None):
        super(UiOverlayWindow, self).__init__(parent)

    def setupUi(self, MainWindow):
        super(UiOverlayWindow, self).setupUi(MainWindow)

        # Tab layout
        # layout = QtGui.QHBoxLayout()
        # self.widgetGPSBarPlot.setLayout(layout)

        # layout.addWidget(self.widgetGPSData)
        # Add the custom GPS widget
        layout = QtGui.QVBoxLayout()
        self.widgetGPSBarPlot.setLayout(layout)
        self.gpsBarPlot = GPSBarPlot(self.widgetGPSBarPlot)
        layout.addWidget(self.gpsBarPlot)
        # self.gpsBarPlot.setGeometry(QtCore.QRect(10, 10, 500, 200))

        # Add the custom GPS satellites widget
        layout = QtGui.QVBoxLayout()
        self.widgetGPSSatellitePlot.setLayout(layout)
        self.gpsSatellitePlot = GPSSatellitePlot(self.widgetGPSSatellitePlot)
        layout.addWidget(self.gpsSatellitePlot)


        # Add the connection status label to statusbar
        self.label_connection_status = QtGui.QLabel()
        self.label_connection_status_led = QtGui.QLabel()
        self.statusbar.addPermanentWidget(self.label_connection_status)
        self.statusbar.addPermanentWidget(self.label_connection_status_led)
        self.setStatusDisconnected()

        # About Dialog
        self.aboutWindow = About(self)
        self.actionAbout.triggered.connect(self.aboutWindow.show)

    def setStatusConnected(self, device=None):
        pixmap = QtGui.QPixmap('res/led-on.svg')
        # pixmap = pixmap.scaled(self.statusbar.size()*0.4, QtCore.Qt.KeepAspectRatio)
        self.label_connection_status_led.setPixmap(pixmap)
        label = "Connected"
        if device is not None:
            label = "Connected to " + device
        self.label_connection_status.setText(label)

    def setStatusDisconnected(self):
        pixmap = QtGui.QPixmap('res/led-off.svg')
        # pixmap = pixmap.scaled(self.statusbar.size()*0.4, QtCore.Qt.KeepAspectRatio)
        self.label_connection_status_led.setPixmap(pixmap)
        self.label_connection_status.setText("Disonnected")
        self.gpsBarPlot.resetData()
        self.gpsSatellitePlot.resetData()

    def updateGPSData(self, gpggaMessage):
        self.lineEditLatitude.setText(gpggaMessage.getLatitudeString())
        self.lineEditLongitude.setText(gpggaMessage.getLongitudeString())
        self.lineEditAltitude.setText(gpggaMessage.getAltitudeString())
