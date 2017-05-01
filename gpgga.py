#!/usr/bin/env python
# -*- coding: utf-8 -*-

# $GPGGA,214551.00,4810.28564,N,01138.16720,E,1,06,5.16,537.4,M,46.2,M,,*52

class GPGGAMessage(object):
    def __init__(self):
        # hhmmss.ss = UTC of position
        self.utc = "000000.00"
        self.latitude = "0000.00000"
        self.latitudeDirection = "N"
        self.longitude = "00000.00000"
        self.longitudeDirection = "W"
        # GPS Quality indicator (0=no fix, 1=GPS fix, 2=Dif. GPS fix)
        self.fixQuality = 0
        self.numberOfSatellites = 0
        # Horizontal Dilution of Precision (HDOP)
        self.hdop = 0.0
        # Altitude
        self.altitude = 0.0
        self.altitudeUnit = "M"
        # Height of geoid above WGS84 ellipsoid
        self.geoidSeparation = 0.0
        self.geoidUnit = "M"
        # Age of Differential GPS data (seconds)
        self.dgpsAge = 0
        # Differential reference station ID
        self.dgpsRefStationId = 0

    def parseGPGGAMessage(self, msg):
        msg = msg.split('*')[0].split(',')
        self.utc = msg[1]
        self.latitude = msg[2]
        self.latitudeDirection = msg[3]
        self.longitude = msg[4]
        self.longitudeDirection = msg[5]
        self.fixQuality = int(msg[6])
        self.numberOfSatellites = int(msg[7])
        self.hdop = float(msg[8])
        self.altitude = msg[9]
        self.altitudeUnit = msg[10]
        self.geoidSeparation = msg[11]
        self.geoidUnit = msg[12]
        self.dgpsAge = msg[13]
        self.dgpsRefStationId = msg[14]

    def hasFix(self):
        return self.fixQuality == 1 or self.fixQuality == 2

    def formatLatLong(self, degree, minute, direction):
        try:
            return u"{degree:}°{minute:}'{second:}''{direction:s}".format(degree=int(degree),
                                                           minute=int(float(minute)),
                                                           second=int(round(float(minute) % 1 * 60)),
                                                           direction=direction)
        except:
            return ''

    def getLongitudeString(self):
        return self.formatLatLong(self.longitude[0:3],
                                  self.longitude[3:],
                                  self.longitudeDirection)

    def getLatitudeString(self):
        return self.formatLatLong(self.latitude[0:2],
                                  self.latitude[2:],
                                  self.latitudeDirection)

    def getPositionString(self):
        return self.getLatitudeString() + " " + self.getLongitudeString()

    def getAltitudeString(self):
        return str(self.altitude) + str(self.altitudeUnit)
