from PyQt4 import QtGui,QtCore
import settings_view

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


class Settings(QtGui.QMainWindow, settings_view.Ui_MainWindow):
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
