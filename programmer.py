#!/usr/bin/env python
import serial
import sys
import argparse
import camino_108

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
    camino.serial.flush()
    camino.configureMMSI(args.mmsi)
    # camino.readData()
