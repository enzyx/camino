from PyQt4 import QtCore, QtGui
import gpgsv

class GPSBarPlot(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        # Bars
        self.barWidth = 15
        self.barLineWidth = 2
        self.barDistance = 10
        self.barTextDistance = 3
        self.xBarOffset = 5

        # Margins
        self.bottomMargin = 40
        self.topMargin = 10
        self.leftMargin = 40
        self.rightMargin = 10

        # Axes
        self.axesColor = QtGui.QColor(50,50,50,255)
        self.axesLineWidth = 2

        self.range = [0,60]
        self.yticsFreq = 10
        self.yticsDist = 25
        self.xticsDist = 18

        # grid
        self.grid = True
        self.gridLineWidth = 1
        self.gridColor = QtGui.QColor(200,200,200,255)

        # Bar Colors
        self.labelColor = QtCore.Qt.black
        self.barBorderColor  = QtGui.QColor(60, 60, 60, 255)
        self.barColor1 = QtGui.QColor(0, 153, 0, 255)
        self.barColor2  = QtGui.QColor(0,  76, 153, 255)

        # Background color
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QtCore.Qt.white)
        self.setPalette(palette)

        self.data = []

    def updateData(self, gpgsvMessage):
        self.data = gpgsvMessage
        self.update()

    def resetData(self):
        self.data = []
        self.update()

    def drawAxes(self, painter):
        # set color and width of line drawing pen
        painter.setPen(QtGui.QPen(self.axesColor, self.axesLineWidth))
        # axis: drawLine(x1, y1, x2, y2) from point (x1,y1) to (x2,y2)
        # x-axis
        painter.drawLine(self.leftMargin, self.h-self.bottomMargin, self.w-self.rightMargin, self.h-self.bottomMargin)
        # y-axis
        painter.drawLine(self.leftMargin, self.topMargin, self.leftMargin, self.h - self.bottomMargin)

        # draw y-ticks
        for i in range(0, self.range[1], self.yticsFreq):
            y = self.h - self.bottomMargin - self.yscale * i
            painter.drawLine(self.leftMargin, y, self.leftMargin-4, y)
            s = "{: >3d}".format(i)
            painter.drawText(self.leftMargin - self.yticsDist, y+4, s)

        # draw x-ticks
        for x in range(self.leftMargin + self.barDistance + self.xBarOffset + self.barWidth/2, self.w-self.rightMargin, self.barWidth + self.barDistance):
            painter.drawLine(x, self.h - self.bottomMargin, x, self.h-self.bottomMargin + 4)


        painter.rotate(-90)
        painter.drawText(-(self.h+self.bottomMargin)/2.-20, 13, "SNR (dB-Hz)")
        painter.rotate(90)

        painter.drawText((self.leftMargin + self.w)/2. - 25, self.h-3, "Satellite ID")

    def drawGrid(self, painter):
        painter.setPen(QtGui.QPen(self.gridColor, self.gridLineWidth))

        # draw y grid
        for i in range(0, self.range[1], self.yticsFreq):
            y = self.h - self.bottomMargin - self.yscale * i
            painter.drawLine(self.leftMargin, y, self.w-self.rightMargin, y)


    def paintEvent(self, event):
        # Get dimensions
        self.w = self.frameGeometry().width()
        self.h = self.frameGeometry().height()
        self.yspace = self.h - self.bottomMargin - self.topMargin
        self.yscale = float(self.yspace)/self.range[1]

        painter = QtGui.QPainter()
        painter.begin(self)

        # Grid
        if self.grid: self.drawGrid(painter)
        # Axes
        self.drawAxes(painter)

        # set up color and width of the bars
        delta = self.barWidth + self.barDistance
        x = self.barDistance + self.xBarOffset  + self.leftMargin
        for satellite in self.data:
            if satellite.isTracking():
                painter.setBrush(self.barColor1)
            else:
                painter.setBrush(self.barColor2)

            # correct for width
            y = self.h  - self.bottomMargin - ( satellite.getSnr() * self.yscale ) - (self.axesLineWidth )/2.
            barHeight = satellite.getSnr() * self.yscale
            # draw each bar
            painter.setPen(QtGui.QPen(self.barBorderColor, self.barLineWidth))
            painter.drawRect(x, y, self.barWidth, barHeight)

            # Draw labels
            painter.setPen(QtGui.QPen(self.labelColor, self.barLineWidth))
            s = "{: >2d}".format(satellite.getSnr())
            painter.drawText(x, y-self.barTextDistance, s)
            s = "{: >2d}".format(satellite.getPrnId())
            painter.drawText(x, self.h - self.bottomMargin + self.xticsDist, s)
            x += delta
        painter.end()
