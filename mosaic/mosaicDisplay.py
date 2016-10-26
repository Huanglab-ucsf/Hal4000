#!/usr/bin/python
#
## @file
#

# RJM 8/14
#

import numpy
from PyQt4 import QtCore, QtGui

import qtWidgets.qtAppIcon as qtAppIcon

# Debugging
import sc_library.hdebug as hdebug

# UIs.
import qtdesigner.mosaicdisplay_ui as mosaicdisplayUi

# Widgets
import mosaicDisplayWidgets
## MosaicDisplay
#
# The mosaic display UI and lock control base class.
#
class MosaicDisplay(QtGui.QDialog):
    #foundOptimal = QtCore.pyqtSignal(float)
    #foundSum = QtCore.pyqtSignal(float)
    #lockDisplay = QtCore.pyqtSignal(object)
    #lockStatus = QtCore.pyqtSignal(float, float)
    #recenteredPiezo = QtCore.pyqtSignal()

    ## __init__
    #
    # Create the LockDisplay class and setup the UI.
    #
    # ir_laser is a class with the following methods:
    #
    # on(power)
    #   Turn on the IR laser. Power is a value from 1 to 100.
    #
    # off()
    #   Turn off the IR laser
    #
    # @param parameters A parameters object.
    # @param control_thread A TCP control object.
    # @param ir_laser A ir laser control object as described above.
    # @param parent The PyQt parent of this object.
    #
    @hdebug.debug
    def __init__(self, parameters, parent):
        QtGui.QMainWindow.__init__(self, parent)
        self.newParameters(parameters)


        # UI setup
        self.ui = mosaicdisplayUi.Ui_Dialog()
        self.ui.setupUi(self)

        self.configureUI()


        # start the qpd monitoring thread & stage control thread
        #self.control_thread = control_thread
        #self.control_thread.start(QtCore.QThread.NormalPriority)
        #self.control_thread.controlUpdate.connect(self.controlUpdate)
        #self.control_thread.foundSum.connect(self.handleFoundSum)
        #self.control_thread.recenteredPiezo.connect(self.handleRecenteredPiezo)



        

    def configureUI(self):
        #parameters = self.parameters
        #self.setWindowTitle(parameters.setup_name + " Mosaic")
        #self.setWindowIcon(qtAppIcon.QAppIcon())
        self.setWindowTitle(" Mosaic")
        self.setModal(False)


    #
    # Handles new frame data from the camera.
    #
    # @param frame A frame data object.
    #
    #def newFrame(self, frame):
    #    self.current_mode.newFrame(frame, self.offset, self.power, self.stage_z)

    ## newParameters
    #
    # Handles a change in parameters.
    #
    # @param parameters A parameters object.
    #
    @hdebug.debug
    def newParameters(self, parameters):
        self.parameters = parameters
        p = parameters


    ## quit
    #
    # Stops the control thread and cleans things up prior to shutting down.
    #
    @hdebug.debug
    def quit(self):
        self.control_thread.stopThread()
        self.control_thread.wait()
        self.control_thread.cleanUp()

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
