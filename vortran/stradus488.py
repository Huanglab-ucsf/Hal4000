#!/usr/bin/python
#
# Vortran Stradus 488 laser control.
#
# Hazen 3/09
# Bryant 2/10

import halLib.RS232 as RS232  # 2/24/10 changed lib.RS232 to halLib.RS232
import time


class Stradus488(RS232.RS232):
    def __init__(self, port = "COM6"):
        try:
            # open port
            print "488: opening COM6"
            RS232.RS232.__init__(self, port, None, 19200, "\r", 0.7)
            print "488: port open"

            # see if the laser is connected
            print "488: getting response"
            assert not(self.commWithResp("?LI") == None)
            print "488: got response"

            # finish setup
            self.pmin = 0.0
            self.pmax = 5.0
            print "488: getting power range"
            [self.pmin, self.pmax] = self.getPowerRange()
            print "488: got power range"
            #print "488: setting ext control"
            #self.setExtControl(0)
            #print "488: ext control is off"
            self.on = 0
            self.setLaserOnOff(1)
            self.pulsemode = 1
            self.setPulseMode(1)
        except:
            self.live = 0
            print "Failed to connect to 488 Laser. Perhaps it is turned off"
            print "or the Keyspan COM ports have been scrambled?"

    def respToFloat(self, resp, start):
        return float(resp[start:-13])

    def getExtControl(self):
        self.sendCommand("?EPC")
        time.sleep(0.2)
        response = self.waitResponse()
        if response.find("=1") == -1:
            return 0
        else:
            return 1

    def getLaserOnOff(self):
        self.sendCommand("?LE")
        time.sleep(0.2)
        onoff = self.waitResponse()
        return float(onoff[10:-13])

    def getPowerRange(self):
        #self.sendCommand("?MINLP")                         # Vortran Stradus lasers do not have min power command
        #pmin = self.respToFloat(self.waitResponse(), 6)
        #self.sendCommand("?MAXP")
        #time.sleep(0.2)                                     # time delay guarantees that "waitResponse" receives full return
        #pmax = self.respToFloat(self.waitResponse(), 14)    # the laser gives horribly inconsistent returns
        pmin = 1                                            # this is probably due to timing issues
        pmax = 50
        return [pmin, pmax]

    def getPower(self):
        self.sendCommand("?LP")
        time.sleep(0.2)
        power_string = self.waitResponse()
        return float(power_string[10:-13])

    def setExtControl(self, mode):
        if mode:
            self.sendCommand("EPC=1")
        else:
            self.sendCommand("EPC=0")
        self.waitResponse()

    def setPulseMode(self, mode):
        if mode:
            print "setting pulse mode on 488"
            self.sendCommand("PUL=1")
            self.pulsemode = 1
            #print "pulse mode on 488"
        else:
            print "setting pulse mode off 488"
            self.sendCommand("PUL=0")
            self.pulsemode = 0
            #print "pulse mode off 488"
        self.waitResponse()

    def setLaserOnOff(self, on):
        if on and (not self.on):
            self.sendCommand("LE=1")
            self.waitResponse()
            self.on = 1
        if (not on) and self.on:
            self.sendCommand("LE=0")
            self.waitResponse()
            self.on = 0

    def setPower(self, power_in_mw):
        if power_in_mw < self.pmin:
            power_in_mw = self.pmin
            self.setLaserOnOff(0)
        else:
            self.setLaserOnOff(1)
        if power_in_mw > self.pmax:
            power_in_mw = self.pmax
        if self.pulsemode == 1:
            print "setting PP 488"
            self.sendCommand("PP=" + str(power_in_mw))
            print "PP set 488"
            print "getting PP response 488"
            self.waitResponse()
            print "got PP response 488"
        elif self.pulsemode == 0:
            print "setting LP 488"
            self.sendCommand("LP=" + str(power_in_mw))
            print "LP set 488"
            print "getting LP response 488"
            self.waitResponse()
            print "got LP response 488"

#
# Testing
#

if __name__ == "__main__":
    cube = Stradus488()
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

