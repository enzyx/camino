#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# This file is part of Camino.
# Copyright (C) 2017 Manuel Luitz <manuel.luitz@gmail.com>
#
# Camino is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Camino is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Camino. If not, see <http://www.gnu.org/licenses/>.
#
from PyQt4 import QtCore, QtGui
from math import cos, sin, pi

class GPSSatellitePlot(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        # Margins
        self.bottomMargin = 18
        self.topMargin = 18
        self.leftMargin = 18
        self.rightMargin = 18

        # Axes
        self.axesColor = QtGui.QColor(50,50,50,255)
        self.axesInnerLineColor = QtGui.QColor(200,200,200,255)
        self.axesLineWidth = 2
        self.axesInnerLineWidth = 1
        self.ticksLengthScale = 0.98

        # Background color
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QtCore.Qt.white)
        self.setPalette(palette)

        # Satellite drawing style
        self.satelliteRadiusScale = 0.06
        self.satelliteBorderColor = QtGui.QColor(50,50,50,255)
        self.satelliteLineWidth = 1
        self.satelliteColor  = QtGui.QColor(0, 153, 0, 255)
        self.satelliteLabelOffset = 6

        self.data = []

    def x(self, r, phi):
        return self.center.x() + r * cos(phi * pi/180.)

    def y(self, r, phi):
        return self.center.y() + r * sin(phi * pi/180.)

    def updateData(self, gpgsvMessage):
        self.data = gpgsvMessage
        self.update()

    def resetData(self):
        self.data = []
        self.update()

    def drawCircles(self, painter):
        # set color and width of line drawing pen
        painter.setPen(QtGui.QPen(self.axesColor, self.axesLineWidth))
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        # draw three circles
        painter.drawEllipse(self.center, self.radius, self.radius)
        painter.setPen(QtGui.QPen(self.axesInnerLineColor, self.axesInnerLineWidth))
        painter.drawEllipse(self.center, self.radius * 2./3., self.radius * 2./3.)
        painter.drawEllipse(self.center, self.radius * 1./3., self.radius * 1./3.)

    def drawAxes(self, painter):
        # set color and width of line drawing pen
        painter.setPen(QtGui.QPen(self.axesColor, self.axesLineWidth))

        # Cross
        painter.drawLine(self.center.x() - self.radius, self.center.y(),
                         self.center.x() + self.radius, self.center.y())
        painter.drawLine(self.center.x(), self.center.y() - self.radius,
                         self.center.x(), self.center.y() + self.radius)

        # Draw tics
        for angle in [22.5, 45.0, 67.5]:
            for offset in [0, 90, 180, 270]:
                phi = angle + offset
                x1 = self.x(self.radius, phi)
                y1 = self.y(self.radius, phi)
                x2 = self.x(self.radius * self.ticksLengthScale, phi)
                y2 = self.y(self.radius * self.ticksLengthScale, phi)
                painter.drawLine(x1,y1,x2,y2)

        # Draw tics labels
        for label in [[0,"O"],  [45,"SO"], [90,"S"], [135,"SW"],
                      [180,"W"],[225,"NW"],[270,"N"],[315,"NO"]]:
            phi = label[0]
            x1 = self.x(self.radius, phi)
            y1 = self.y(self.radius, phi)
            painter.save()
            painter.translate(x1, y1)
            painter.rotate(phi+90)
            painter.drawText(-5*len(label[1]), -5, label[1])
            painter.restore()

    def drawSatellite(self, painter, satellite):
        # Check if tracking else return
        if not satellite.isTracking(): return
        painter.save()
        # Painter settings
        painter.setBrush(self.satelliteColor)
        painter.setPen(QtGui.QPen(self.satelliteBorderColor, self.satelliteLineWidth))

        r   = (1.-satellite.getElevation()/90.) * self.radius
        phi = satellite.getAzimuth()-90
        location =  QtCore.QPoint(self.x(r,phi),self.y(r,phi))
        satelliteRadius = self.radius * self.satelliteRadiusScale
        painter.drawEllipse(location, satelliteRadius, satelliteRadius)
        painter.drawText(location.x() + self.satelliteLabelOffset,
                         location.y() - self.satelliteLabelOffset, str(satellite.getPrnId()))
        painter.restore()

    def paintEvent(self, event):
        # Get dimensions
        self.w = self.frameGeometry().width()
        self.h = self.frameGeometry().height()

        # Center
        self.center = QtCore.QPoint((self.w - self.rightMargin + self.leftMargin)/2.,
                                    (self.h - self.topMargin + self.bottomMargin)/2. )

        # Radius
        self.radius = min((self.w - self.rightMargin - self.leftMargin)/2.,
                          (self.h - self.topMargin - self.bottomMargin)/2. )

        painter = QtGui.QPainter()
        painter.begin(self)

        # Circles
        self.drawCircles(painter)
        # Axes
        self.drawAxes(painter)
        # satellites
        for satellite in self.data:
            self.drawSatellite(painter, satellite)

        painter.end()
