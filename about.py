from PyQt4 import QtGui
import about_window

class About(QtGui.QMainWindow, about_window.Ui_AboutWindow):
    def __init__(self, parent=None):
        super(About, self).__init__(parent)
        self.setupUi(self)
