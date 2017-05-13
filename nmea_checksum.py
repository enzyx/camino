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
class nmeaChecksum(object):
  def calculateChecksum(self, data):
      """
      Take a NMEA 0183 string and compute the checksum.
      @param data: NMEA message.  Leading ?/! and training checksum are optional
      @type data: str
      @return: hexidecimal value
      @rtype: str
      """
      if data[0]=='!' or data[0]=='?' or data[0]=='$': data = data[1:]
      if data[-1]=='*': data = data[:-1]
      if data[-3]=='*': data = data[:-3]
      data = data.strip()
      # FIX: rename sum to not shadown builting function
      chksum=0
      for c in data: chksum = chksum ^ ord(c)
      sumHex = "{:02X}".format(chksum)
      return sumHex

  def addChecksum(self, msg):
      chk = self.calculateChecksum(msg)
      return msg + '*' + chk + '\r\n'
