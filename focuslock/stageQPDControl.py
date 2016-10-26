#!/usr/bin/python
#
# Stage and QPD Control Thread Class
#
# This is a PyQt thread for controlling the z stage position
# and getting the current position reading from the QPD.
#
# stage is a class with the following methods:
#
#   moveTo(z)
#      Move the stage to position z in um.
#
#   shutDown()
#      Perform whatever cleanup is necessary to stop the stage cleanly
#
#
# qpd is a class with the following methods:
#
#   qpdScan()
#      Return the current reading from the QPD in a list
#      [power, x_offset, y_offset]
#
#   shutDown()
#      Perform whatever cleanup is necessary to stop the qpd cleanly
#
#
# lock_fn is a function that takes a single number (the QPD error signal)
#   and returns the appropriate response (in um) by the stage.
#
#
# Hazen 6/09
#

from PyQt4 import QtCore

# Debugging
import halLib.hdebug as hdebug

#
# QPD monitoring and stage control thread.
#
class QControlThread(QtCore.QThread):
    @hdebug.debug
    def __init__(self, qpd, stage, lock_fn, min_sum, z_center, parent = None):
        QtCore.QThread.__init__(self, parent)
        self.qpd = qpd
        self.stage = stage
        self.lock_fn = lock_fn
        self.sum_min = min_sum

        self.debug = 1
        self.target = 0
        self.unacknowledged = 1
        self.locked = 0
        self.running = 1
        self.offset = 0
        self.qpd_mutex = QtCore.QMutex()
        self.stage_mutex = QtCore.QMutex()
        self.stage_z = z_center - 1.0
        self.target = None
        self.z_center = z_center

        # center the stage
        # self.newZCenter(z_center)

    @hdebug.debug
    def cleanUp(self):
        self.qpd.shutDown()
        self.stage.shutDown()

    @hdebug.debug
    def getLockTarget(self):
        self.qpd_mutex.lock()
        target = self.target
        self.qpd_mutex.unlock()
        return target

    @hdebug.debug
    def getOffset(self):
        self.qpd_mutex.lock()
        temp = self.offset
        self.qpd_mutex.unlock()
        return temp

    def moveStageAbs(self, new_z):
        self.stage_mutex.lock()
        if new_z != self.stage_z:
            self.stage_z = new_z
            self.stage.moveTo(3, self.stage_z)
        self.stage_mutex.unlock()

    def moveStageRel(self, dz):
        new_z = self.stage_z + dz
        self.moveStageAbs(new_z)

    def newZCenter(self, z_center):
        self.z_center = z_center

    def recenter(self):
        self.moveStageAbs(self.z_center)
            
    def run(self):
        while(self.running):
            [power, x_offset, y_offset] = self.qpd.qpdScan()

            self.qpd_mutex.lock()
            if (power > 0):
                self.offset = x_offset / power
            self.unacknowledged = 0
            if self.locked and (power > self.sum_min):
                self.moveStageRel(self.lock_fn(self.offset - self.target))

            self.emit(QtCore.SIGNAL("controlUpdate(float, float, float, float)"), x_offset, y_offset, power, self.stage_z)
            self.qpd_mutex.unlock()
            self.msleep(1)

    def setStage(self, stage):
        self.qpd_mutex.lock()
        self.stage = stage
        self.qpd_mutex.unlock()

    @hdebug.debug
    def setTarget(self, target):
        self.qpd_mutex.lock()
        self.target = target
        self.qpd_mutex.unlock()

    @hdebug.debug
    def startLock(self):
        self.qpd_mutex.lock()
        self.unacknowledged = 1
        self.locked = 1
        if self.target == None:
            self.target = self.offset
        self.qpd_mutex.unlock()
        self.waitForAcknowledgement()

    @hdebug.debug
    def stopLock(self):
        self.qpd_mutex.lock()
        self.unacknowledged = 1
        self.locked = 0
        self.target = None
        self.qpd_mutex.unlock()
        self.waitForAcknowledgement()

    @hdebug.debug
    def stopThread(self):
        self.running = 0

    @hdebug.debug
    def waitForAcknowledgement(self):
        while(self.unacknowledged):
            self.msleep(20)


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
