from PyQt4 import QtGui
import settings_view

class Settings(QtGui.QMainWindow, settings_view.Ui_MainWindow):
    serial_port = '/dev/ttyACM0'
    def __init__(self, parent=None):
        super(Settings, self).__init__(parent)
        self.setupUi(self)
        self.pushButtonApply.clicked.connect(self.applySettings)

    def applySettings(self):
        self.serial_port = self.lineEditSerialDevice.text()

    def show(self):
        super(Settings, self).show()
        self.lineEditSerialDevice.setText(self.serial_port)
