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
import mosaic.mosaicDisplay as mosaicDisplay

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
        QtGui.QDialog.__init__(self, parent)
        halModule.HalModule.__init__(self)

        if parent:
            self.have_parent = True
        else:
            self.have_parent = False

        # general
        self.offset_file = 0
        self.parameters = parameters
        self.jumpsize = 0.0

    ## cleanup
    #
    @hdebug.debug
    def cleanup(self):
        self.lock_display1.quit()
        self.closeOffsetFile()

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

    ## closeOffsetFile
    #
    # Closes the offset file. This is called at the end of filming.
    #
    @hdebug.debug
    def closeOffsetFile(self):
        if self.offset_file:
            self.offset_file.close()
            self.offset_file = False

    ## configureUI
    #
    # This sets up the UI, connects the signals, etc.
    #
    @hdebug.debug
    def configureUI(self):
        parameters = self.parameters

        # UI setup
        self.setWindowTitle(parameters.setup_name + " MOSAIC")
        self.setWindowIcon(qtAppIcon.QAppIcon())
        self.ui.lockLabel.setStyleSheet("QLabel { color: green }")
        self.toggleLockButtonDisplay(self.lock_display1.shouldDisplayLockButton())
        self.toggleLockLabelDisplay(self.lock_display1.shouldDisplayLockLabel())

        # Setup mode radio buttons.
        vbox_layout = QtGui.QVBoxLayout(self.ui.modeWidget)
        self.ui.modeWidget.setLayout(vbox_layout)
        lock_modes = self.lock_display1.getLockModes()
        self.buttons = []
        for i, mode in enumerate(lock_modes):
            button = QtGui.QRadioButton(mode.getName(), self.ui.modeWidget)
            vbox_layout.addWidget(button)
            self.buttons.append(button)

        self.buttons[parameters.qpd_mode].setChecked(True)

        for button in self.buttons:
            button.clicked.connect(self.handleRadioButtons)

        # Connect signals
        if self.have_parent:
            self.ui.okButton.setText("Close")
            self.ui.okButton.clicked.connect(self.handleOk)
        else:
            self.ui.okButton.setText("Quit")
            self.ui.okButton.clicked.connect(self.handleQuit)

        self.ui.lockButton.clicked.connect(self.handleLockButton)
        self.ui.jumpPButton.clicked.connect(self.handleJumpPButton)
        self.ui.jumpNButton.clicked.connect(self.handleJumpNButton)
        self.ui.jumpSpinBox.valueChanged.connect(self.handleJumpSpinBox)

        # set modeless
        self.setModal(False)

    ## connectSignals
    #
    # @param signals An array of signals that we might be interested in connecting to.
    #
    @hdebug.debug
    def connectSignals(self, signals):
        for signal in signals:
            if (signal[1] == "commMessage"):
                signal[2].connect(self.handleCommMessage)

            if (signal[1] == "lockJump"):
                signal[2].connect(self.jump)

    ## getLockTarget
    #
    # @return The current lock target.
    #
    @hdebug.debug
    def getLockTarget(self):
        return self.lock_display1.getLockTarget()

    ## getSignals
    #
    # @return The signals this module provides.
    #
    @hdebug.debug
    def getSignals(self):
        return [[self.hal_type, "tcpComplete", self.tcpComplete],
                [self.hal_type, "focusLockStatus", self.lock_display1.lockStatus],
                [self.hal_type, "focusLockDisplay", self.lock_display1.lockDisplay]]

    ## handleCommMessage
    #
    # Handles all the message from tcpControl.
    #
    # @param message A tcpControl.TCPMessage object.
    #
    @hdebug.debug
    def handleCommMessage(self, message):

        m_type = message.getType()
        m_data = message.getData()

        if (m_type == "findSum"):
            self.tcpHandleFindSum()

        elif (m_type == "optimizeSum"):
            self.tcpHandleOptimizeSum()

        elif (m_type == "recenterPiezo"):
            self.tcpHandleRecenterPiezo

        elif (m_type == "setLockTarget"):
            self.tcpHandleSetLockTarget(m_data[0])

    ## handleFoundOptimal
    #
    # Notify external program (via TCP/IP) that the optimal sum signal has been found.
    #
    # @param lock_sum The lock sum signal.
    #
    @hdebug.debug
    def handleFoundOptimal(self, lock_sum):
        self.tcpComplete.emit(str(lock_sum))

    ## handleFoundSum
    #
    # Notify external program (via TCP/IP) that the sum signal has been found.
    #
    # @param lock_sum The lock sum signal.
    #
    @hdebug.debug
    def handleFoundSum(self, lock_sum):
        self.tcpComplete.emit(str(lock_sum))

    ## handleJumpPButton
    #
    # Handles the jump+ button.
    #
    # @param boolean Dummy parameter.
    #
    @hdebug.debug
    def handleJumpPButton(self, boolean):
        self.lock_display1.jump(self.jumpsize)

    ## handleJumpNButton
    #
    # Handles the jump- button.
    #
    # @param boolean Dummy parameter.
    #
    @hdebug.debug
    def handleJumpNButton(self, boolean):
        self.lock_display1.jump(-self.jumpsize)

    ## handleJumpSpinBox
    #
    # Handles the jump spin box.
    #
    @hdebug.debug                    
    def handleJumpSpinBox(self, jumpsize):
        self.jumpsize = jumpsize

    ## handleLockButton
    #
    # Handles the lock button.
    #
    # @param boolean Dummy parameter.
    #
    @hdebug.debug
    def handleLockButton(self, boolean):
        self.lock_display1.lockButtonToggle()
        self.toggleLockButtonText(self.lock_display1.amLocked())
        self.toggleLockLabelDisplay(self.lock_display1.shouldDisplayLockLabel())

    ## handleOk
    #
    # Handles the close button.
    #
    # @param boolean Dummy parameter.
    #
    @hdebug.debug
    def handleOk(self, boolean):
        self.hide()

    ## handleRadioButtons.
    #
    # Handles the lock mode radio buttons.
    #
    # @param boolean Dummy parameter.
    #
    @hdebug.debug
    def handleRadioButtons(self, boolean):
        for i in range(len(self.buttons)):
            if self.buttons[i].isChecked():
                if self.lock_display1.changeLockMode(i):
                    self.toggleLockButtonDisplay(self.lock_display1.shouldDisplayLockButton())
                    self.toggleLockButtonText(self.lock_display1.amLocked())
                    self.toggleLockLabelDisplay(self.lock_display1.shouldDisplayLockLabel())

    ## handleRecenteredPiezo
    #
    # Notify external program (via TCP/IP) that the piezo has been recentered.
    #
    @hdebug.debug
    def handleRecenteredPiezo(self):
        self.tcpComplete.emit("NA")

    ## handleQuit
    #
    # Handles the quit button.
    #
    # @param boolean Dummy parameter.
    #
    @hdebug.debug
    def handleQuit(self, boolean):
        self.close()

    ## jump
    #
    # Handles jump requests (these usually come from the joystick).
    #
    @hdebug.debug
    def jump(self, step_size):
        self.lock_display1.jump(step_size)

    ## newFrame
    #
    # Handles a new frame of data from the camera. If we are filming
    # this writes the current offset information into the offset file.
    #
    # @param frame A frame object.
    # @param filming True/False if we are currently filming.
    #
    def newFrame(self, frame, filming):
        if filming and frame.master:
            if self.offset_file:
                [offset, power, stage_z] = self.lock_display1.getOffsetPowerStage()
                self.offset_file.write("{0:d} {1:.6f} {2:.6f} {3:.6f}\n".format(frame.number, offset, power, stage_z))
            self.lock_display1.newFrame(frame)

    ## newParameters
    #
    # Handles new parameters.
    #
    # @param parameters A parameters object.
    #
    @hdebug.debug
    def newParameters(self, parameters):
        self.parameters = parameters
        self.lock_display1.newParameters(self.parameters)

    ## openOffsetFile
    #
    # Open a file to save the offset data in during filming.
    #
    # @param filename The name of the offset file.
    #
    @hdebug.debug
    def openOffsetFile(self, filename):
        self.offset_file = open(filename + ".off", "w")
        self.offset_file.write("frame offset power stage-z\n")

    ## startFilm
    #
    # Start the focus lock. This is called at the start of an acquisition.
    # If filename is not False then a file of the same name is opened
    # to store the offset data in during filming.
    #
    # @param filename The name of the file to save the offset data in.
    # @param run_shutters True/False the shutters should be run or not.
    #
    @hdebug.debug
    def startFilm(self, filename, run_shutters):
        self.counter = 0
        self.error = 0.0
        self.error_counts = 0
        if filename:
            self.openOffsetFile(filename)
        self.lock_display1.startLock(filename)
        self.toggleLockButtonText(self.lock_display1.amLocked())
        self.toggleLockLabelDisplay(self.lock_display1.shouldDisplayLockLabel())

    ## stopFilm
    #
    # Stop the focus lock and close the offset file (if it is open).
    #
    # @param film_writer A film writer object.
    #
    @hdebug.debug
    def stopFilm(self, film_writer):
        self.lock_display1.stopLock()
        self.toggleLockButtonText(self.lock_display1.amLocked())
        self.toggleLockLabelDisplay(self.lock_display1.shouldDisplayLockLabel())
        self.closeOffsetFile()
        if film_writer:
            film_writer.setLockTarget(self.lock_display1.getLockTarget())

    ## tcpHandleFindSum
    #
    # Handle find sum requests that come via TCP/IP.
    #
    @hdebug.debug
    def tcpHandleFindSum(self):
        self.lock_display1.tcpHandleFindSum()

    ## tcpHandleOptimizeSum
    #
    # Handle optimize sum requests that come via TCP/IP.
    #
    @hdebug.debug
    def tcpHandleOptimizeSum(self):
        self.lock_display1.tcpHandleOptimizeSum()

    ## tcpHandleRecenterPiezo
    #
    # Handle piezo recentering requests that come via TCP/IP.
    #
    @hdebug.debug
    def tcpHandleRecenterPiezo(self):
        self.lock_display1.tcpHandleRecenterPiezo()

    ## tcpHandleSetLockTarget
    #
    # Handle lock target setting requests that come via TCP/IP.
    #
    # @param target The desired lock target.
    #
    @hdebug.debug
    def tcpHandleSetLockTarget(self, target):
        self.lock_display1.tcpHandleSetLockTarget(target)


    ## toggleLockButtonDisplay
    #
    # Show/hide the lock button depending on the show parameter.
    #
    # @param show True/False show/hide the lock button.
    #
    @hdebug.debug
    def toggleLockButtonDisplay(self, show):
        if show:
            self.ui.lockButton.show()
        else:
            self.ui.lockButton.hide()

    ## toggleLockLabelDisplay
    #
    # Show/hide the lock label depending on the show parameter.
    #
    # @param show True/False show/hide the lock label.
    #
    @hdebug.debug
    def toggleLockLabelDisplay(self, show):
        if show:
            self.ui.lockLabel.show()
        else:
            self.ui.lockLabel.hide()

    ## toggleLockButtonText
    #
    # Change the lock button text depending on the locked parameter.
    #
    # @param locked True/False is the focus locked.
    #
    @hdebug.debug
    def toggleLockButtonText(self, locked):
        if locked:
            self.ui.lockButton.setText("Unlock")
            self.ui.lockButton.setStyleSheet("QPushButton { color: green}")
        else:
            self.ui.lockButton.setText("Lock")
            self.ui.lockButton.setStyleSheet("QPushButton { color: black}")


#
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
