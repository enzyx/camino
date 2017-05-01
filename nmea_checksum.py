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
