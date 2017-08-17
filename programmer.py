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
import serial
import sys
import argparse
from camino_api import Camino

parser = argparse.ArgumentParser(description='Program the AMEC Camino 108 AIS Transponder.')
parser.add_argument('-r', '--reset-mmsi', dest='reset_mmsi', action='store_true',
                    default=False, help='Reset the MMSI number in order to reprogram it')
parser.add_argument('-d', '--device-info', dest='device_info', action='store_true',
                    default=False, help='Read the device information')
parser.add_argument('-s', '--short-info', dest='device_short_info', action='store_true',
                    default=False, help='Read short device information')
parser.add_argument('-a', '--additional-info', dest='device_additional_info', action='store_true',
                    default=False, help='Read additional device information')
parser.add_argument('-m', '--mmsi', metavar="MMSI", dest='mmsi', type=int,
                    default=0, help='Program the MMSI number')
parser.add_argument('-p', '--program', dest='program', action='store_true',
                    default=False, help='Program the ship data')

args = parser.parse_args()

#################
#     MAIN      #
#################

camino = Camino('/dev/ttyACM0')

# Program data:
if args.program:
    camino.configureAISData('ELIO DEL MARE', 'EDM4321')

# Reset MMSI
if args.reset_mmsi:
    camino.bruteForceResetMMSI()
# Print device info
if args.device_info:
    camino.getDeviceInfo()
elif args.device_short_info:
    camino.getShortDeviceInfo()
elif args.device_additional_info:
    camino.getAdditionalDeviceInfo()

# program MMSI
if args.mmsi != 0:
    camino.serialDevice.flush()
    camino.configureMMSI(args.mmsi)
    # camino.readData()
