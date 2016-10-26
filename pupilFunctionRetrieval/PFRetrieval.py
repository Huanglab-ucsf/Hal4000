#!/usr/bin/python
#
## @file
#
# Mosaic
#
# RJM 8/14
#

import numpy as np
import time
from functools import partial
from PyQt4 import QtCore, QtGui

#import datareader
import QExtensions as qext

import qtWidgets.qtAppIcon as qtAppIcon

import halLib.halModule as halModule
import halLib.imagewriters as writers

#For reading in DAX file
import IO

#For getting PF
import pupil

# Debugging
import sc_library.hdebug as hdebug

import camera.frame as frame

# Widgets
#import mosaicDisplay

import qtdesigner.pf_ui as pfUi

## FocusLockZ
#
# This class controls the focus lock GUI.
#
class PFRetrieval(QtGui.QDialog, halModule.HalModule):
    tcpComplete = QtCore.pyqtSignal(object)
    hasPSF = QtCore.pyqtSignal()
    hasPF = QtCore.pyqtSignal()


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

        

        self.ui = pfUi.Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle(parameters.setup_name + " Pupil Function Retrieval")
        self.setWindowIcon(qtAppIcon.QAppIcon())
        
        self.params = None

        self.currentFrame = 0 #current frame of combined file to display


        self.dZ = 20
        self.startFrame = 0
        self.stopFrame = 100
        self.centerX = 128
        self.centerY = 128
        self.centerZ = 50

        self.npdata = None

        self.dx = 0.160
        self.wavelength = 0.705
        self.nInterations = 20

        self.configureUI()
        

    @hdebug.debug
    def configureUI(self):
        print "Config UI..."

        self.ui.stepSize_lineEdit.setText("20")
        self.ui.startFrame_lineEdit.setText("0")
        self.ui.stopFrame_lineEdit.setText("100")
        self.ui.centerX_lineEdit.setText("128")
        self.ui.centerY_lineEdit.setText("128")

        self.ui.setParams_pushButton.clicked.connect(self.setParams)
        
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
        return [[self.hal_type, "hasPSF", self.hasPSF],
                [self.hal_type, "hasPF", self.hasPF]]


    def newParameters(self,p):
        self.params = p
        print "ZScan got new parameters..."


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

    #def startFilm(self, film_name, shutters):
    #    if self.readyForTTL:
    #        self.ttlZ()

    def stopFilm(self, writer):
        if self.ui.recordPSF_checkBox.isChecked():
            print "File saved to: ", writer.filenames[0]
            time.sleep(30)
            self.daxFilename = writer.filenames[0]
            self.createNumpyArray(self.daxFilename)

    def createNumpyArray(self, filename):
        daxFile = IO.DAX(filename)
        self.npdata = np.zeros(daxFile.shape, dtype=np.uint16)
        for i in range(daxFile.shape[0]):
            self.npdata[i] = daxFile[i]

    def cropArray(self, x, y):
        if self.npdata is not None:
            numFrames, nx, ny = self.npdata.shape
            diffx = x-(nx/2)
            diffy = y-(ny/2)
            if abs(diffx)>abs(diffy):
                new_n = nx-abs(diffx)
            else:
                new_n = ny-abs(diffy)
            newData = self.npdata[:,x-(new_n/2):x+(new_n/2),y-(new_n/2):y+(new_n/2)]
            self.npdata = newData.copy()

    def getXZandYZ(self, x, y):
        if self.npdata is not None:
            return (self.npdata[:,:,y], self.npdata[:,x,:])

    def setParams(self):
        self.dZ = int(self.ui.stepSize_lineEdit.text())
        self.startFrame = int(self.ui.startFrame_lineEdit.text())
        self.stopFrame = int(self.ui.stopFrame_lineEdit.text())
        self.centerX = int(self.ui.centerX_lineEdit.text())
        self.centerY = int(self.ui.centerY_lineEdit.text())
        self.centerZ = (self.stopFrame-self.startFrame)/2

        if self.npdata is not None:
            nFrames, nx, ny = self.npdata.shape
            if (self.centerX != nx/2) or (self.centerY != ny/2):
                self.cropArray(self.centerX, self.centerY)

        xySlice = self.npdata[self.centerZ]
        nFrames,nx,ny = self.npdata.shape
        xz,yz = self.getXZandYZ(nx/2,ny/2)
        self.display(xySlice, xz)

    def display(self, im, z_im):
        vmin = im.min()
        vmax = im.max()
        qtImage = qext.numpy_to_qimage8(im, vmin, vmax, None, color=False)
        self._pixmap = QtGui.QPixmap.fromImage(qtImage)
        self._pixmap = self._pixmap.scaled(256,256,QtCore.Qt.KeepAspectRatio)
        self.ui.labelDisplay.setPixmap(self._pixmap)

        qtImage = qext.numpy_to_qimage8(z_im, vmin, vmax, None, color=False)
        self._pixmap2 = QtGui.QPixmap.fromImage(qtImage)
        self._pixmap2 = self._pixmap2.scaled(256,100,QtCore.Qt.KeepAspectRatio)
        self.ui.labelDisplay_2.setPixmap(self._pixmap2)

   
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
