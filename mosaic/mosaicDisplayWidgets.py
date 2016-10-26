#!/usr/bin/python
#
## @file
#

# RJM 8/14
#

import numpy
from PyQt4 import QtCore, QtGui

# Debugging
import sc_library.hdebug as hdebug

class MosaicFieldDisplay(QtGui.QWidget):

    @hdebug.debug
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.background = QtGui.QColor(0,0,0)



    def newImage(self, data):
        print "got new data"



'''
    ## shouldDisplayLockButton
    #
    # @return True/False depending on whether the lock button should be shown for the current lock mode.
    #
    @hdebug.debug
    def shouldDisplayLockButton(self):
        return self.current_mode.shouldDisplayLockButton()

    ## shouldDisplayLockLabel
    #
    # @return True/False depending on whether the lock label should be shown for the current lock mode.
    #
    @hdebug.debug
    def shouldDisplayLockLabel(self):
        return self.current_mode.shouldDisplayLockLabel()

    ## startLock
    #
    # Start the focus lock. The filename parameter is ignored.
    #
    # @param filename This is not used.
    #
    @hdebug.debug
    def startLock(self, filename):
        self.current_mode.startLock()

    ## stopLock
    #
    # Stop the focus lock.
    #
    @hdebug.debug
    def stopLock(self):
        self.current_mode.stopLock()

    ## tcpHandleFindSum
    #
    # Tell the control thread to execute the find sum signal procedure.
    #
    def tcpHandleFindSum(self):
        self.control_thread.findSumSignal()

    ## tcpHandleOptimizeSum
    #
    # Adjust the laser power until the sum signal is in the range 0.5 - 0.9.
    #
    def tcpHandleOptimizeSum(self):
        if self.ir_laser and self.ir_laser.havePowerControl():
            self.optimizing_sum = True
        else:
            self.foundOptimal.emit(self.power)

    ## tcpHandleRecenterPiezo
    #
    # Tell the control thread to recenter the piezo.
    #
    @hdebug.debug
    def tcpHandleRecenterPiezo(self):
        self.control_thread.recenterPiezo()

    ## tcpHandleSetLockTarget
    #
    # Tell the control thread to set its lock target to target.
    #
    # @param target The desired lock target.
    #
    @hdebug.debug
    def tcpHandleSetLockTarget(self, target):
        self.current_mode.setLockTarget(target/self.scale)

'''
#
# The MIT License
#
# Copyright (c) 2012 Zhuang Lab, Harvard University
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
