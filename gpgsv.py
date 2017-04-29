#!/usr/bin/env python
# -*- coding: utf-8 -*-

class GPGSVSatellite(object):
    def __init__(self, prn, elevation, azimuth, snr):
        # Satellite ID
        self.prn_id = prn
        # Elevation, in degrees, 90° maximum
        self.elevation = elevation
        # Azimuth, degrees from True North, 000° through 359°
        self.azimuth = azimuth
        # Signal to Noise Ratio, 00 through 99 dB (null when not tracking)
        self.snr = snr

    def isTracking(self):
        return self.elevation != 0 and self.azimuth != 0 and self.snr != 0

    def getPrnId(self):
        return self.prn_id

    def getElevation(self):
        return self.elevation

    def getAzimuth(self):
        return self.azimuth

    def getSnr(self):
        return self.snr

class GPGSVMessage(object):
    def __init__(self):
        self.current = -1
        self.numberOfMessages = 0
        self.satellites = []

    def __iter__(self):
        return self

    def next(self):
        self.current += 1
        if self.current >= len(self.satellites):
            self.current = -1
            raise StopIteration
        else:
            return self.satellites[self.current]

    def reset(self):
        self.satellites = []

    def newSatellite(self, prn, elevation, azimuth, srn):
        gpgsvSatellite = GPGSVSatellite(prn, elevation, azimuth, srn)
        self.satellites.append(gpgsvSatellite)

class GPGSVCollector(object):
    def __init__(self):
        self.messages = []

    def cleanMessages(self):
        self.messages = []

    def addMessage(self, msg):
        self.messages.append(msg)

    def isComplete(self):
        if len(self.messages) == 0:
            return False
        expectedMessages = self._getNumberExpectedMessages(self.messages[0])
        if len(self.messages) >= expectedMessages:
            return True

    def getGPGSVMessage(self):
        gpgsvMessage = GPGSVMessage()
        for msg in self.messages:
            msg = msg.split('*')[0]
            sat = []
            for dat in msg.split(',')[4:]:
                try:
                    sat.append(int(dat))
                except ValueError:
                    sat.append(0)
                if len(sat) == 4:
                    gpgsvMessage.newSatellite(sat[0], sat[1], sat[2], sat[3])
                    sat = []

        self.cleanMessages()
        return gpgsvMessage

    def _getNumberExpectedMessages(self, msg):
        return int(msg.split(',')[1])
