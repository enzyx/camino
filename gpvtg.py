#!/usr/bin/env python
# -*- coding: utf-8 -*-

# $GPVTG,054.7,T,034.4,M,005.5,N,010.2,K*48

class GPVTGMessage(object):
    def __init__(self):
        # hhmmss.ss = UTC of position
        self.track_made_good = "0.0"
        self.degrees_true = "T"
        self.track_magnetic = "0.0"
        self.degrees_magnetic = "M"
        self.speed_over_ground_knots = "0.0"
        self.speed_over_ground_knots_unit = "N"
        # Fixed text "K" (knots)
        self.speed_over_ground_kmh = "0.0"
        # Fixed text "K" (km/h)
        self.speed_over_ground_kmh_unit = "K"

    def parseGPVTGMessage(self, msg):
        msg = msg.split('*')[0].split(',')
        self.track_made_good = msg[1]
        self.degrees_true = msg[2]
        self.track_magnetic = msg[3]
        self.degrees_magnetic = msg[4]
        self.speed_over_ground_knots = msg[5]
        self.speed_over_ground_knots_unit = msg[6]
        self.speed_over_ground_kmh = msg[7]
        self.speed_over_ground_kmh_unit = msg[8]

    def formatSpeedOverGroundKmh(self):
        return u"{sog:} km/h".format(sog=float(self.speed_over_ground_kmh))

    def formatSpeedOverGroundKnots(self):
        return u"{sog:} knots".format(sog=float(self.speed_over_ground_knots))

    def getSpeedOverGroundStringMetric(self):
        return self.formatSpeedOverGroundKmh()

    def getSpeedOverGroundStringImperial(self):
        return self.formatSpeedOverGroundKnots()
