import gpgsv, gpgga

class InputParser(object):
    def __init__(self, QMainWindow):
        self.QMainWindow = QMainWindow
        self.gpgsvCollector = gpgsv.GPGSVCollector()
        self.gpgsvMessage = gpgsv.GPGSVMessage()
        self.gpggaMessage = gpgga.GPGGAMessage()

    def update(self, data):
        self.QMainWindow.textEditLog.appendPlainText(data.strip())
        if "(01) MMSI:(" in data:
            self.QMainWindow.lineEditMMSI.setText(data[10:20])
        if "(03) Name:(" in data:
            self.QMainWindow.lineEditShipName.setText(data.strip()[11:-1])
        if "(04) Call Sign:(" in data:
            self.QMainWindow.lineEditCallSign.setText(data.strip()[16:-1])
        if "(05) Ship Cargo Type:(" in data:
            shipType = data.split('(')[2].split(')')[0]
            self.QMainWindow.spinBoxDimA.setValue(int(data.split('(')[3].split(')')[0]))
            self.QMainWindow.spinBoxDimB.setValue(int(data.split('(')[4].split(')')[0]))
            self.QMainWindow.spinBoxDimC.setValue(int(data.split('(')[5].split(')')[0]))
            self.QMainWindow.spinBoxDimD.setValue(int(data.split('(')[6].split(')')[0]))

        if "$GPGSV," in data:
            self.gpgsvCollector.addMessage(data)
            if self.gpgsvCollector.isComplete():
                self.gpgsvMessage = self.gpgsvCollector.getGPGSVMessage()
                self.QMainWindow.gpsBarPlot.updateData(self.gpgsvMessage)
                self.QMainWindow.gpsSatellitePlot.updateData(self.gpgsvMessage)

        if "$GPGGA," in data:
            self.gpggaMessage.parseGPGGAMessage(data)
            print self.gpggaMessage.getPositionString()
            print self.gpggaMessage.getAltitudeString()
