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
import serial, sys
from nmea_checksum import nmeaChecksum
# Full programming sample log (without MMSI)
# at_1 = '$ECSSD,[callsign],[shipname],15,0,0,4,1,AI*1D\r\n'
# at_2 = '$ECSSD,[callsign],[shipname],15,0,0,4,1,GP*02\r\n'
# at_3 = '$ECVSD,36,00.0,0,,,00,00,15,*44\r\n'
# at_4 = '$PTST,,,,,00016*18\r\n'
# at_5 = '$PAMC,Q,CFG,30,0,0,*0F\r\n'
# at_6 = '$PAMC,Q,CFG,108,3,0,*36\r\n'
# at_7 = '$AIAIQ,CEK*30\r\n'
# at_8 = '$PAMC,Q,CFG,183,0,0,*36\r\n'

class Camino(nmeaChecksum):
    def __init__(self, device):
        self.serialDevice = serial.Serial(device, 115200, timeout=5)
        #self.serialDevice = serial_for_url('socket://192.168.10.22:10110')

    def send(self, cmd):
        # print cmd
        self.serialDevice.write(cmd)

    def sendWithChecksum(self, cmd):
        cmdChecksum = self.addChecksum(cmd)
        self.send(cmdChecksum)

    def readData(self):
        while True:
            sys.stdout.write(self.serialDevice.readline())

    def parseData(self, msg):
        if msg in self.serialDevice.readline():
            return True
        else:
            return False

    def readLines(self,lines=2):
        ret = ""
        for i in range(lines):
            ret += self.serialDevice.readline()
        return ret

    def readUntilMessage(self, msg):
        ret = ""
        while msg not in ret:
            ret = self.readLines(1)
            sys.stdout.write(ret)

    def configureAISData(self, name, callsign, dim=[15,0,0,2]):
        '''
        Configure basic ship data: name, callsign, (TODO: Lenght(15), GPS_position(2,2))
        '''
        at_cmd1 = '$ECSSD,{callsign},{name},{dimA},{dimB},{dimC},{dimD},1,AI'.format(
            name=name, callsign=callsign, dimA=dim[0], dimB=dim[1], dimC=dim[2], dimD=dim[3])
        at_cmd2 = '$ECSSD,{callsign},{name},{dimA},{dimB},{dimC},{dimD},1,GP'.format(
            name=name, callsign=callsign, dimA=dim[0], dimB=dim[1], dimC=dim[2], dimD=dim[3])

        self.sendWithChecksum(at_cmd1)
        self.sendWithChecksum(at_cmd2)

    def configureShipType(self, shipType=36):
        ''' Ship type is a number (e.g. 36 = Vessel-Sailing) '''
        self.sendWithChecksum("$ECVSD,{:d},00.0,0,,,00,00,15,".format(shipType))

    def initFlashMode(self):
        '''
        Put the Camino in flash mode
            !!!DANGEROUS!!!
        '''
        at_cmd = "$PDBG,107,1,,,,,,"
        self.sendWithChecksum(at_cmd)

    def configureMMSI(self, mmsi):
        '''
        Configure MMSI when unconfigured
        '''
        at_cmd = '$PMID,{:09d},{:09d}'.format(mmsi, 000000000)
        self.sendWithChecksum(at_cmd)
        # self.readUntilMessage('$PMID,')

    def resetMMSI(self, passwd=00000000):
        '''
        First send the license key (8 int) derived from current MMSI
        Then reset the MMSI to 000000000
        '''
        at_cmd1 = '$PTPS,120,{passwd:08d}'.format(passwd=passwd)
        at_cmd2 = '$PMID,{:09d},'.format(000000000)
        self.sendWithChecksum(at_cmd1)
        self.sendWithChecksum(at_cmd2)

    def bruteForceResetMMSI(self, verbose=False):
        '''
        In cases where the license key to reset the MMSI is unknown
        it can easily brute forced.
        '''
        print "Resetting MMSI"
        for key in range(99999):
           self.resetMMSI(passwd=key)
           ret = self.readLines(2)
           if verbose:
               print ret
           elif key % 500 == 0:
               sys.stdout.write(".")
               sys.stdout.flush()
           if "$PTXT,MMSI programmable*0D" in ret:
               print "\nMMSI is now programmable"
               break

    def getDeviceInfo(self):
        ''' Read information from device '''
        self.sendWithChecksum('$PTST,,,,,00016')
        # self.readUntilMessage('[SYSTEM DATA END](21)')

    def getAdditionalDeviceInfo(self):
        ''' Read information from device '''
        for i in [0, 1, 30, 99, 108, 183, 600, 8117]:
            at_cmd = '$PAMC,Q,CFG,{:d},0,0,'.format(i)
            self.sendWithChecksum(at_cmd)
            self.readUntilMessage(at_cmd)

    def getShortDeviceInfo(self):
        self.sendWithChecksum('!AIAIQ,VER')
        self.readUntilMessage('$AIVER')
