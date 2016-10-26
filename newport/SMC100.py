#!/usr/bin/python
#
# Communicates with the Newport SMC100 motor controller on COM1.
#
# Hazen 4/09
#

import time

import halLib.RS232 as RS232

class SMC100(RS232.RS232):
    def __init__(self, port = "COM4", timeout = None, baudrate = 57600):
        RS232.RS232.__init__(self, port, timeout, baudrate, "\r\n", 0.1)
        try:
            # check if we are referenced
            if self.amNotReferenced():
                print "SMC100 homing."
                # reference
                self.commWithResp("1OR")
                # wait until homed
                while self.amHoming():
                    time.sleep(1)
        except:
            print "SMC100 controller is not responding."
            print "Perhaps it is not turned on, or the Keyspan COM ports have been scrambled."
            self.live = 0

    def _command(self, command):
        if self.live:
            self.sendCommand(command)
            return self.waitResponse()[:-2]

    def amHoming(self):
        self.state = self._command("1TS")
        if self.state == "1TS00001E":
            return 1
        else:
            return 0

    def amMoving(self):
        self.state = self._command("1TS")
        if self.state == "1TS000028":
            return 1
        else:
            return 0

    def amNotReferenced(self):
        self.state = self._command("1TS")
        assert len(self.state) == len("1TS00000A"), "SMC100 controller not responding."
        if self.state == "1TS00000A":
            return 1
        else:
            return 0

    def getPosition(self):
        try:
            return float(self._command("1TP")[3:])
        except:
            return -1.0

    def moveTo(self, position):
        self.position = position
        self.commWithResp("1PA"+str(self.position))
        error = self._command("1TE")
        if not (error == "1TE@"):
            print "SMC100 motion error:", error
        self.position = float(self._command("1TP")[3:])

    def stopMove(self):
        if self.amMoving():
            self.sendCommand("1ST")

#
# Testing
# 

if __name__ == "__main__":
    smc100 = SMC100()
    pos = smc100.getPosition()
    print pos
    print smc100._command("1TE")
    print smc100._command("1TS")
    smc100.moveTo(pos+0.1)

#
#    Copyright (C) 2009  Hazen Babcock
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
