from PyQt4 import QtGui
import about_view

class About(QtGui.QMainWindow, about_view.Ui_AboutWindow):
    def __init__(self, parent=None):
        super(About, self).__init__(parent)
        self.setupUi(self)
