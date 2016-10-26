#!/usr/bin/python
#
# Coherent CUBE 405 laser control.
#
# Hazen 3/09
#

import halLib.RS232 as RS232
import time


class Cube405(RS232.RS232):
    def __init__(self, port = "COM5"):
        try:
            # open port
            RS232.RS232.__init__(self, port, None, 19200, "\r", 0.05)

            # see if the laser is connected
            assert not(self.commWithResp("?HID") == None)

            # finish setup
            self.pmin = 0.0
            self.pmax = 5.0
            [self.pmin, self.pmax] = self.getPowerRange()
            self.setExtControl(0)
#            self.on = 0
#            self.setLaserOnOff(1)
        except:
            self.live = 0
            print "Failed to connect to 405 Laser. Perhaps it is turned off"
            print "or the Keyspan COM ports have been scrambled?"

    def respToFloat(self, resp, start):
        return float(resp[start:-1])

    def getExtControl(self):
        self.sendCommand("?EXT")
        response = self.waitResponse()
        if response.find("=1") == -1:
            return 0
        else:
            return 1

    def getLaserOnOff(self):
        self.sendCommand("?L")
        return self.waitResponse()

    def getPowerRange(self):
        self.sendCommand("?MINLP")
        pmin = self.respToFloat(self.waitResponse(), 6)
        self.sendCommand("?MAXLP")
        pmax = self.respToFloat(self.waitResponse(), 6)
        return [pmin, pmax]

    def getPower(self):
        self.sendCommand("?SP")
        power_string = self.waitResponse()
        return float(power_string[3:-1])

    def setExtControl(self, mode):
        if mode:
            self.sendCommand("EXT=1")
        else:
            self.sendCommand("EXT=0")
        self.waitResponse()

    def setLaserOnOff(self, on):
        if on and (not self.on):
            self.sendCommand("L=1")
            self.waitResponse()
            self.on = 1
        if (not on) and self.on:
            self.sendCommand("L=0")
            self.waitResponse()
            self.on = 0

    def setPower(self, power_in_mw):
#        if power_in_mw < self.pmin:
#            power_in_mw = self.pmin
#            self.setLaserOnOff(0)
#        else:
#            self.setLaserOnOff(1)
        if power_in_mw > self.pmax:
            power_in_mw = self.pmax
        self.sendCommand("P=" + str(power_in_mw))
        self.waitResponse()

#
# Testing
#

if __name__ == "__main__":
    cube = Cube405()
    if cube.getStatus():
        print cube.getPowerRange()
        print cube.getLaserOnOff()
        power = 2.0
        while power < 3.0:
            cube.setPower(power)
            time.sleep(0.5)
            print cube.getPower()
            power += 0.1


#
# The MIT License
#
# Copyright (c) 2009 Zhuang Lab, Harvard University
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

