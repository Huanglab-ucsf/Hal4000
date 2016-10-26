#!/usr/bin/python
#
# Vortran Stradus 405 laser control.
#
# Hazen 3/09
# Bryant 2/10
# Joerg 9/11

import halLib.RS232 as RS232
import time

class Stradus(RS232.RS232):
    def __init__(self, port = ""):
        try:
            # open port
            print "opening port " + str(port)
            RS232.RS232.__init__(self, port, None, 19200, "\r", 0.05)

            # see if the laser is connected
            print "getting response " + str(port)
            assert not(self.commWithResp("?LI") == None)

            # finish setup
            self.pmin = 0.0
            self.pmax = 5.0
            print "getting power range " + str(port)
            [self.pmin, self.pmax] = self.getPowerRange(port)
            #print "405: setting ext control"
            #self.setExtControl(0)
            self.waitResponse()
            #self.pulsemode = 1
            #self.setPulseMode(1)
            self.on = 0
            self.setLaserOnOff(1)
            onoff = self.waitResponse()
            print onoff
            
        except:
            self.live = 0
            print "Failed to connect to 488 Laser. Perhaps it is turned off"
            print "or the Keyspan COM ports have been scrambled?"

    def respToFloat(self, resp, start):
        print "!!! respToFloat called"
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
        print "!!! getLaserOnOff called"
        self.sendCommand("?LE")
        time.sleep(0.2)
        onoff = self.waitResponse()
        return float(onoff[10:-13])

    def getPowerRange(self, port):
        #self.sendCommand("?MINLP")                         # Vortran Stradus lasers do not have min power command
        #pmin = self.respToFloat(self.waitResponse(), 6)
        #self.sendCommand("?MAXP")
        #time.sleep(0.2)                                     # time delay guarantees that "waitResponse" receives full return
        #pmax = self.respToFloat(self.waitResponse(), 14)    # the laser gives horribly inconsistent returns
        pmin = 0                                            # this is probably due to timing issues
        #pmax = 40
        if port == "COM6":
            pmax = 50
        elif port == "COM8":
            pmax = 110
        elif port == "COM9":
            pmax = 100
        else:
            print "laser is not stradus"
        return [pmin, pmax]

    def getPower(self):
        print "!!! getPower Called"
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
            print "setting pulse mode on"
            self.sendCommand("PUL=1")
            self.pulsemode = 1
        else:
            print "setting pulse mode off"
            self.sendCommand("PUL=0")
            self.pulsemode = 0
        pulse = self.waitResponse()
        print pulse

    def setLaserOnOff(self, on):
        print "setLaserOnOff "
        if on and (not self.on):
            print "turning on Vortran laser"
            self.sendCommand("LE=1")
            emiss = self.waitResponse()
            print emiss
            self.on = 1
        if (not on) and self.on:
            print "turning off Vortran laser"
            self.sendCommand("LE=0")
            emiss = self.waitResponse()
            print emiss
            self.on = 0
        else:
            print "neither condition for on/off met"

    def setLaserOff(self):
        print "setLaserOff"
        self.sendCommand("LE=0")
        emiss = self.waitResponse()
        print emiss
        self.on = 0

    def setLaserOn(self):
        print "setLaserOn"
        self.sendCommand("LE=1")
        emiss = self.waitResponse()
        print emiss
        self.on = 1

    def setPower(self, power_in_mw):
        print "setPower called "
        print str(power_in_mw)
        
        if power_in_mw <= self.pmin:
            print "power = pmin"
            power_in_mw = self.pmin
            if self.on:
                self.setLaserOff()
        if power_in_mw > self.pmin:
            print "power > pmin"
            if (not self.on):
                self.setLaserOn()
        if power_in_mw > self.pmax:
            print "power > pmax"
            power_in_mw = self.pmax
            if (not self.on):
                self.setLaserOn()

        print "setting LP = " + str(power_in_mw)
        self.sendCommand("LP=" + str(power_in_mw))
        print "getting LP response"
        test = self.waitResponse()
        print test
        
##        if self.pulsemode == 1:
##            print "setting PP"
##            self.sendCommand("PP=" + str(power_in_mw))
##            #self.sendCommand("PP=30")
##            print "getting PP response"
##            test = self.waitResponse()
##            print test
##        else:
##            print "setting LP"
##            self.sendCommand("LP=" + str(power_in_mw))
##            #self.sendCommand("LP=30")
##            print "getting LP response"
##            test = self.waitResponse()
##            print test

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

