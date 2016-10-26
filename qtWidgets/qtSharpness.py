#!/usr/bin/python
#
## @file
#
# Qt Thread for finding sharpness
# defined as second moment of FT of image
#
# RJM 2/2015
#

from PyQt4 import QtCore, QtGui
from halLib import signalForAO

import pyfftw

## QObjectCounterThread
#
# The thread class, which does all the actual object counting.
#
class QSharpnessThread(QtCore.QThread):
    imageProcessed = QtCore.pyqtSignal(int, object, int, float)

    ## __init__
    #
    # @param parameters A parameters object.
    # @param index The index of the thread (an integer).
    # @param parent (Optional) The PyQt parent of this object.
    #
    def __init__(self, parameters, index, parent = None):
        QtCore.QThread.__init__(self, parent)

        self.frame = False
        self.mutex = QtCore.QMutex()
        self.running = True
        self.thread_index = index
        self.threshold = parameters.threshold

        self.pixelSize = 143
        self.diffLimit = 350

    ## newImage
    #
    # A new image for this thread to analyze.
    #
    # @param frame A frame object.
    #
    def newImage(self, frame):
        self.mutex.lock()
        self.frame = frame
        self.mutex.unlock()

    ## newParameters
    #
    # @param parameters A parameters object.
    #
    def newParameters(self, parameters):
        self.mutex.lock()
        self.threshold = parameters.threshold
        self.mutex.unlock()

    ## run
    #
    # The thread loop.
    #
    def run(self):
         while (self.running):
             self.mutex.lock()
             if self.frame:
                 npdata = self.frame.getData()
                 xdim = self.frame.image_x
                 ydim = self.frame.image_y
                 npdata = npdata.reshape(xdim,ydim)
                 #print "npdata size: ", npdata.shape
                 sharpness = signalForAO.secondMoment(npdata, self.pixelSize, self.diffLimit)
                 self.imageProcessed.emit(self.thread_index,
                                          self.frame.which_camera,
                                          self.frame.number,
                                          sharpness)
                 self.frame = False
                     
             self.mutex.unlock()
             self.usleep(50)

    ## stopThread
    #
    # Tells the thread loop to stop running.
    #
    def stopThread(self):
        self.running = False


## QObjectCounter
#
# The front end.
#
class QSharpness(QtGui.QWidget):
    imageProcessed = QtCore.pyqtSignal(object, int, float)

    ## __init__
    #
    # @param parameters A parameters object.
    # @param number_threads The number of object finding threads to start.
    # @param parent (Optional) The PyQt parent of this object.
    #
    def __init__(self, parameters, number_threads = 16, parent = None):
        QtGui.QWidget.__init__(self, parent)

        self.dropped = 0
        self.number_threads = number_threads
        self.total = 0

        # Initialize threads.
        self.idle = []
        self.threads = []
        for i in range(self.number_threads):
            self.threads.append(QSharpnessThread(parameters, i))
            self.idle.append(True)
            
        for thread in self.threads:
            thread.start(QtCore.QThread.NormalPriority)
            thread.imageProcessed.connect(self.returnResults)

    ## newImageToCount
    #
    # Assigns a new image to be analyzed to the first available thread. If
    # no threads are available then the image is considered to have been dropped.
    #
    # @param frame A frame object.
    #
    def newImageToFT(self, frame):
        self.total += 1
        if frame:
            i = 0
            not_found = True
            while (i < self.number_threads) and not_found:
                if self.idle[i]:
                    self.threads[i].newImage(frame)
                    self.idle[i] = False
                    not_found = False
                i += 1
            if not_found:
                self.dropped += 1

    ## newParameters
    #
    # @param parameters A parameters object.
    #
    def newParameters(self, parameters):
        for thread in self.threads:
            thread.newParameters(parameters)

    ## returnResults
    #
    # When a thread completes it emits a image processed signal, which this gets. This then
    # marks the thread as not busy and emits a imageProcessed signal.
    #
    # @param thread_index The index of the thread that did the processing.
    # @param which_camera The camera that the image that was processed came from.
    # @param frame_number The frame number of the image that was processed.
    # @param x_locs A Python array of localization x positions.
    # @param y_locs A Python array of localization y positions.
    # @param spots The number of spots in the x_locs, y_locs arrays.
    #
    def returnResults(self, thread_index, which_camera, frame_number, sharpness):
        self.idle[thread_index] = True
        self.imageProcessed.emit(which_camera,
                                 frame_number,
                                 sharpness)

    ## shutDown
    #
    # Call the cleanup function of the object finder C code.
    # Stop all the threads.
    # Print how many images were analyzed and how many were dropped.
    #
    def shutDown(self):

        # Thread cleanup.
        for thread in self.threads:
            thread.stopThread()
            thread.wait()
        print "Sharpess detector dropped", self.dropped, "images out of", self.total, "total images"


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

