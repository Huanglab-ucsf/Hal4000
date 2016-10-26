#!/usr/bin/python
#
## @file
#
# Mosaic
#
# RJM 8/14
#

import numpy
import time
from functools import partial
from PyQt4 import QtCore, QtGui

#import datareader
#import QExtensions as qext

import qtWidgets.qtAppIcon as qtAppIcon

import halLib.halModule as halModule
#import halLib.imagewriters as writers

# Debugging
import sc_library.hdebug as hdebug

import camera.frame as frame

# Widgets
#import mosaicDisplay

import qtdesigner.zscan_ui as zscanUi

## FocusLockZ
#
# This class controls the focus lock GUI.
#
class ZScan(QtGui.QDialog, halModule.HalModule):
    tcpComplete = QtCore.pyqtSignal(object)
    stepZ = QtCore.pyqtSignal(float)
    speedZ = QtCore.pyqtSignal(float)
    haltSig = QtCore.pyqtSignal()
    ttlSig = QtCore.pyqtSignal(float, int, int)
    #snapImage = QtCore.pyqtSignal()
    #captureDone = QtCore.pyqtSignal()

    ## __init__
    #
    # Create the focus lock object. This does not create the UI.
    #
    # @param parameters A parameters object.
    # @param parent The PyQt parent of this object.
    #
    @hdebug.debug
    def __init__(self, hardware, parameters, parent, stage = None):
        #QtGui.QDialog.__init__(self, parent)
        QtGui.QMainWindow.__init__(self, parent)
        halModule.HalModule.__init__(self)

        self.stage = stage

        if parent:
            self.have_parent = True
        else:
            self.have_parent = False

        # general
        self.stepSize=0.121*200
        self.files = [] #filenames of movies

        #self.display = mosaicDisplay.MosaicDisplay(parameters,parent)

        

        self.ui = zscanUi.Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle(parameters.setup_name + " ZScan")
        self.setWindowIcon(qtAppIcon.QAppIcon())
        
        self.params = None

        self.currentFrame = 0 #current frame of combined file to display

        self.counter = 0
        self.current_z = None
        self.name = "Z Scan"
        self.z_start = None
        self.z_step = None
        self.z_frames_to_pause = None
        self.z_stop = None

        self.readyForTTL = False

        self.dZ = 1
        self.n = 20

        self.configureUI()
        

    @hdebug.debug
    def configureUI(self):
        print "Config UI..."

        self.ui.downButton.clicked.connect(partial(self.oneStep, "-1"))
        self.ui.upButton.clicked.connect(partial(self.oneStep, "1"))
        self.ui.stepSize_lineEdit.setText("1")
        self.ui.frames_lineEdit.setText("1")
        self.ui.zRange_lineEdit.setText("60")
        self.ui.zSpeedSet_pushButton.clicked.connect(self.setZSpeed)
        self.ui.halt_pushButton.clicked.connect(self.halt)
        self.ui.ttl_pushButton.clicked.connect(self.ready_ttlZ)

        self.ui.readyButton.clicked.connect(self.ready)
        
    @hdebug.debug
    def connectSignals(self, signals):
        print "CONNECTING MOSAIC SIGNALS>>>"
        print signals
        for signal in signals:
            if signal[1]=="newData":
                signal[2].connect(self.doSomething)
            elif signal[1]=="reachedMaxFrames":
                signal[2].connect(self.reachedMax)
            elif signal[1]=="reportPosition":
                signal[2].connect(self.getPosition)

    def getSignals(self):
        return [[self.hal_type, "stepZ", self.stepZ],
                [self.hal_type, "speedZ", self.speedZ],
                [self.hal_type, "haltSig", self.haltSig],
                [self.hal_type, "ttlSig", self.ttlSig]]


    def newParameters(self,p):
        self.params = p
        print "ZScan got new parameters..."

    def ready_ttlZ(self):
        stepSize = float(self.ui.stepSize_lineEdit.text())
        self.dZ = stepSize*10.0
        zrange = float(self.ui.zRange_lineEdit.text())
        self.n = int(zrange/stepSize)
        self.readyForTTL = True

    '''
    def newFrame(self, frame, filming):
        if filming and self.readyForTTL:
            self.ttlZ()
            
            if abs(self.current_z - self.z_stop) > self.z_step:
                if self.counter == self.z_frames_to_pause:
                    self.counter = 0
                    self.current_z += self.z_step
                    self.stepZ.emit(self.z_step)
                    #self.stage.stepZ(self.z_step)
                self.counter += 1
            
    '''

    def startFilm(self, film_name, shutters):
        if self.readyForTTL:
            self.ttlZ()

    def stopFilm(self, writer):
        self.readyForTTL = False
        print "File saved to: ", writer.filenames[0]


    def doSomething(self, frame, key):
        print "Got frame"

    def reachedMax(self):
        print "Reached max frames"

    def ready(self):
        self.counter = 0
        self.z_range = float(self.ui.zRange_lineEdit.text())
        self.z_step = float(self.ui.stepSize_lineEdit.text())
        self.z_frames_to_pause = int(self.ui.frames_lineEdit.text())
        self.current_z = 0
        self.z_stop = self.z_range/2.0
        self.current_z = -1.0*self.z_stop
        self.stepZ.emit(self.current_z)
        #self.stage.stepZ(self.current_z)
        print "Current z: ", self.current_z
        print "Stop z: ", self.z_stop

    def setZSpeed(self):
        zspeed = float(self.ui.zSpeed_lineEdit.text())
        self.speedZ.emit(zspeed)

    def oneStep(self, direction):
        self.z_step = float(self.ui.stepSize_lineEdit.text())
        self.stepZ.emit(self.z_step*int(direction))
        #self.stage.stepZ(self.z_step*int(direction))

    def halt(self):
        self.haltSig.emit()

    def ttlZ(self):
        mode = 0
        #mode = int(self.ui.mode_lineEdit.text())
        self.ttlSig.emit(self.dZ, self.n, mode)

   
    ## cleanup
    #
    @hdebug.debug
    def cleanup(self):
        print "Clean up..."

    ## closeEvent
    #
    # Handles user clicking on the X in the upper right hand corner.
    # If the dialog has a parent it just gets hidden rather than
    # actually getting closed.
    #
    # @param event A PyQt window close event.
    #
    @hdebug.debug    
    def closeEvent(self, event):
        if self.have_parent:
            event.ignore()
            self.hide()

    @hdebug.debug
    def handleQuit(self, boolean):
        self.close()



# The MIT License
#
# Copyright (c) 2013 Zhuang Lab, Harvard University
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
