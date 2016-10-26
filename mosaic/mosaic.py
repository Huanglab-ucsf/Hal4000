#!/usr/bin/python
#
## @file
#
# Mosaic
#
# RJM 8/14
#

import numpy
from PyQt4 import QtCore, QtGui

import qtWidgets.qtAppIcon as qtAppIcon

import halLib.halModule as halModule

# Debugging
import sc_library.hdebug as hdebug

# Widgets
import mosaicDisplay

import qtdesigner.mosaicdisplay_ui as mosaicdisplayUi

## FocusLockZ
#
# This class controls the focus lock GUI.
#
class Mosaic(QtGui.QDialog, halModule.HalModule):
    tcpComplete = QtCore.pyqtSignal(object)

    ## __init__
    #
    # Create the focus lock object. This does not create the UI.
    #
    # @param parameters A parameters object.
    # @param parent The PyQt parent of this object.
    #
    @hdebug.debug
    def __init__(self, parameters, parent):
        #QtGui.QDialog.__init__(self, parent)
        QtGui.QMainWindow.__init__(self, parent)
        halModule.HalModule.__init__(self)

        if parent:
            self.have_parent = True
        else:
            self.have_parent = False

        # general
        self.stepSize=0.121*200

        #self.display = mosaicDisplay.MosaicDisplay(parameters,parent)

        #self.configureUI()

        self.ui = mosaicdisplayUi.Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle(parameters.setup_name + " Mosaic")
        self.setWindowIcon(qtAppIcon.QAppIcon())

        


    def configureUI(self):
        print "Config UI..."

    def connectSignals(self, signals):
        print "CONNECTING MOSAIC SIGNALS>>>"
        print signals
        for signal in signals:
            if signal[1]=="newData":
                signal[2].connect(self.doSomething)
            elif signal[1]=="reachedMaxFrames":
                signal[2].connect(self.reachedMax)

    def doSomething(self, frame, key):
        print "Got frame"

    def reachedMax(self):
        print "Reached max frames"

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
