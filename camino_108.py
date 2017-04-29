#!/usr/bin/env python
import serial, sys

# Full programming sample log (without MMSI)
# at_1 = '$ECSSD,[callsign],[shipname],15,0,0,4,1,AI*1D\r\n'
# at_2 = '$ECSSD,[callsign],[shipname],15,0,0,4,1,GP*02\r\n'
# at_3 = '$ECVSD,36,00.0,0,,,00,00,15,*44\r\n'
# at_4 = '$PTST,,,,,00016*18\r\n'
# at_5 = '$PAMC,Q,CFG,30,0,0,*0F\r\n'
# at_6 = '$PAMC,Q,CFG,108,3,0,*36\r\n'
# at_7 = '$AIAIQ,CEK*30\r\n'
# at_8 = '$PAMC,Q,CFG,183,0,0,*36\r\n'

class Camino():
    def __init__(self, device):
        self.serial = serial.Serial(device, 115200, timeout=5)

    def calculateChecksum(self, data):
        """
        Take a NMEA 0183 string and compute the checksum.
        @param data: NMEA message.  Leading ?/! and training checksum are optional
        @type data: str
        @return: hexidecimal value
        @rtype: str

        Checksum is calculated by xor'ing everything between ? or ! and the *

        >>> checksumStr("!AIVDM,1,1,,B,35MsUdPOh8JwI:0HUwquiIFH21>i,0*09")
        '09'
        >>> checksumStr("AIVDM,1,1,,B,35MsUdPOh8JwI:0HUwquiIFH21>i,0")
        '09'
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

    def send(self, cmd):
        # print cmd
        self.serial.write(cmd)

    def sendWithChecksum(self, cmd):
        cmdChecksum = self.addChecksum(cmd)
        self.send(cmdChecksum)

    def readData(self):
        while True:
            sys.stdout.write(self.serial.readline())

    def parseData(self, msg):
        if msg in self.serial.readline():
            return True
        else:
            return False

    def readLines(self,lines=2):
        ret = ""
        for i in range(lines):
            ret += self.serial.readline()
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
        at_cmd1 = '$ECSSD,{callsign},{name},15,0,0,2,1,AI'.format(name=name, callsign=callsign)
        at_cmd2 = '$ECSSD,{callsign},{name},15,0,0,2,1,GP'.format(name=name, callsign=callsign)

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
        self.readUntilMessage('[SYSTEM DATA END](21)')

    def getAdditionalDeviceInfo(self):
        ''' Read information from device '''
        for i in [0, 1, 30, 99, 108, 183, 600, 8117]:
            at_cmd = '$PAMC,Q,CFG,{:d},0,0,'.format(i)
            self.sendWithChecksum(at_cmd)
            self.readUntilMessage(at_cmd)

    def getShortDeviceInfo(self):
        self.sendWithChecksum('!AIAIQ,VER')
        self.readUntilMessage('$AIVER')
