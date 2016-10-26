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

import herkulex2 as herk

import qtWidgets.qtAppIcon as qtAppIcon

import halLib.halModule as halModule

# Debugging
import sc_library.hdebug as hdebug

import camera.frame as frame

# Widgets
#import mosaicDisplay

import qtdesigner.odFilters_ui as odFiltersUi


#
# This class controls the OD filters
#
class ods(QtGui.QDialog, halModule.HalModule):
    changeFilter = QtCore.pyqtSignal(int, int)

    ## __init__
    #
    # Create the focus lock object. This does not create the UI.
    #
    # @param parameters A parameters object.
    # @param parent The PyQt parent of this object.
    #
    @hdebug.debug
    def __init__(self, hardware, parameters, parent):
        #QtGui.QDialog.__init__(self, parent)
        QtGui.QMainWindow.__init__(self, parent)
        halModule.HalModule.__init__(self)

        if parent:
            self.have_parent = True
        else:
            self.have_parent = False

        self.ui = odFiltersUi.Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle(parameters.setup_name + " OD Filters")
        self.setWindowIcon(qtAppIcon.QAppIcon())

        self.configAngles()

        self.servoids = [int(hardware.servo_id1),
                         int(hardware.servo_id2),
                         int(hardware.servo_id3),
                         int(hardware.servo_id4)]

        print "Got servo IDS: ", self.servoids

        self.servos = []

        self.connectServos("COM18", self.servoids)

        self.configureUI()

    def configAngles(self):
        self.angles561 = [-10,-70,-130,150,100,40]
        self.angles642 = [80,125,-150,-100,-45,15]
        self.angles488 = [-75,-25,35,95,150,-135]
        #self.angles405 = [-150,-110,-50,10,70,125]
        self.angles405 = [130,-150,-105,-50,5,55,60]
        

    @hdebug.debug
    def configureUI(self):
        print "Config UI..."

        self.ui.radioButton_405_0.clicked.connect(partial(self.changeFilter,[0,0]))
        self.ui.radioButton_405_05.clicked.connect(partial(self.changeFilter,[0,0.5]))
        self.ui.radioButton_405_1.clicked.connect(partial(self.changeFilter,[0,1]))
        self.ui.radioButton_405_2.clicked.connect(partial(self.changeFilter,[0,2]))
        self.ui.radioButton_405_3.clicked.connect(partial(self.changeFilter,[0,3]))
        self.ui.radioButton_405_4.clicked.connect(partial(self.changeFilter,[0,4]))

        self.ui.radioButton_488_0.clicked.connect(partial(self.changeFilter,[1,0]))
        self.ui.radioButton_488_05.clicked.connect(partial(self.changeFilter,[1,0.5]))
        self.ui.radioButton_488_1.clicked.connect(partial(self.changeFilter,[1,1]))
        self.ui.radioButton_488_2.clicked.connect(partial(self.changeFilter,[1,2]))
        self.ui.radioButton_488_3.clicked.connect(partial(self.changeFilter,[1,3]))
        self.ui.radioButton_488_4.clicked.connect(partial(self.changeFilter,[1,4]))

        self.ui.radioButton_561_0.clicked.connect(partial(self.changeFilter,[2,0]))
        self.ui.radioButton_561_05.clicked.connect(partial(self.changeFilter,[2,0.5]))
        self.ui.radioButton_561_1.clicked.connect(partial(self.changeFilter,[2,1]))
        self.ui.radioButton_561_2.clicked.connect(partial(self.changeFilter,[2,2]))
        self.ui.radioButton_561_3.clicked.connect(partial(self.changeFilter,[2,3]))
        self.ui.radioButton_561_4.clicked.connect(partial(self.changeFilter,[2,4]))

        self.ui.radioButton_642_0.clicked.connect(partial(self.changeFilter,[3,0]))
        self.ui.radioButton_642_05.clicked.connect(partial(self.changeFilter,[3,0.5]))
        self.ui.radioButton_642_1.clicked.connect(partial(self.changeFilter,[3,1]))
        self.ui.radioButton_642_2.clicked.connect(partial(self.changeFilter,[3,2]))
        self.ui.radioButton_642_3.clicked.connect(partial(self.changeFilter,[3,3]))
        self.ui.radioButton_642_4.clicked.connect(partial(self.changeFilter,[3,4]))

        self.ui.groupBox405.setStyleSheet("background-color: rgb(149,0,255);")
        self.ui.groupBox488.setStyleSheet("background-color: rgb(0,245,255);")
        self.ui.groupBox561.setStyleSheet("background-color: rgb(186,255,0);")
        self.ui.groupBox642.setStyleSheet("background-color: rgb(255,0,0);")

        
    @hdebug.debug
    def connectSignals(self, signals):
        print "CONNECTING odFilter SIGNALS>>>"
        #print signals
        '''
        for signal in signals:
            if signal[1]=="newData":
                signal[2].connect(self.doSomething)
            elif signal[1]=="reachedMaxFrames":
                signal[2].connect(self.reachedMax)
            elif signal[1]=="reportPosition":
                signal[2].connect(self.getPosition)
        '''

    def getSignals(self):
        return [[self.hal_type, "changeFilter", self.changeFilter]]

    def connectServos(self, port, ids):
        herk.connect(port, 115200)
        for servoID in ids:
            self.servos.append(herk.servo(servoID))

    def changeFilter(self, params):
        laser = params[0]
        od_position = params[1]
        if od_position>0:
            od_position = int(round(od_position+0.6))
        if laser==2:
            self.servos[0].torque_on()
            self.servos[0].set_servo_angle(self.angles561[od_position],1,0)
            #self.servos[0].torque_off()
        if laser==3:
            self.servos[1].torque_on()
            self.servos[1].set_servo_angle(self.angles642[od_position],1,0)
        if laser==1:
            self.servos[2].torque_on()
            self.servos[2].set_servo_angle(self.angles488[od_position],1,0)
        if laser==0:
            self.servos[3].torque_on()
            self.servos[3].set_servo_angle(self.angles405[od_position],1,0)
        herk.clear_errors()


    def newParameters(self,p):
        self.params = p
        print "odFilter got new parameters..."
        

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
        herk.close()
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
