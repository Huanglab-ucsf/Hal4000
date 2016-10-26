#!/usr/bin/python
#
# Communicates with the Prior stage, typically on com2.
#
# Hazen 3/09
#

import halLib.RS232 as RS232
import time

class Prior(RS232.RS232):
    def __init__(self, port = "COM2", timeout = None, baudrate = 9600):
        self.unit_to_um = 1.0
        self.um_to_unit = 1.0/self.unit_to_um

        # RS232 stuff
        RS232.RS232.__init__(self, port, timeout, baudrate, "\r", 0.02)
        test = self.commWithResp("?")
        if not test:
            print "Prior Stage is not connected? Stage is not on?"
            self.live = 0

#        else:
#            # Get the current position
#            self.x = 0
#            self.y = 0
#            self.z = 0
#            self.getPosition()

    def _command(self, command):
        response = self.commWithResp(command)
        return response.split("\r")

    def active(self):
        state = self.state()
        try:
            state.index("busy")
            return 1
        except:
            return 0
        
    def backlashOnOff(self, on):
        if on:
            self._command("BLSH 1")
        else:
            self._command("BLSH 0")

    def goAbsolute(self, x, y):
        self.sendCommand("G " + str(x * self.um_to_unit) + "," + str(y * self.um_to_unit))
        self.waitResponse()

    def goRelative(self, dx, dy):
        self.sendCommand("GR " + str(dx * self.um_to_unit) + "," + str(dy * self.um_to_unit))
        self.waitResponse()
            
    def info(self):
        return self._command("?")

    def joystickOnOff(self, on):
        if on:
            self._command("J")
        else:
            self._command("H")
        
    def position(self):
        try:
            response = self._command("P")[0]
            [self.x, self.y, self.z] = map(int, response.split(","))
        except:
            print "  Bad position from Prior stage."
        return [self.x * self.unit_to_um, 
                self.y * self.unit_to_um, 
                self.z * self.unit_to_um]

    def setEncoderWindow(self, axis, window):
        assert window >= 0, "setEncoderWindow window is too smale " + str(window)
        assert window <= 4, "setEncoderWindow window is too large " + str(window)
        if axis == "X":
            self._command("ENCW X," + str(window))
        if axis == "Y":
            self._command("ENCW Y," + str(window))

    def state(self):
        response = self._command("#")[0]
        state = []
        for i in range(len(response)):
            if response[i] == "1":
                state.append("busy")
            else:
                state.append("idle")
        return state
        
    def zero(self):
        self._command("P 0,0,0")


#
# Testing
# 

if __name__ == "__main__":
    stage = Prior()
    for info in stage.info():
        print info
    stage.zero()
    print stage.position()
    stage.goAbsolute(500, 500)
    print stage.position()
    stage.goAbsolute(0, 0)
    print stage.position()
    stage.goRelative(-500, -5000)
    print stage.position()
    stage.goAbsolute(0, 0)
    print stage.position()


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
