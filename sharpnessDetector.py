#!/usr/bin/python
#
## @file
#
# Spot counter. This performs real time analysis of the frames from
# camera. It uses a fairly simple object finder. It's purpose is to
# provide the user with a rough idea of the quality of the data
# that they are taking.
#
# Hazen 08/13
#

import sys
from PyQt4 import QtCore, QtGui
import sip

import qtWidgets.qtAppIcon as qtAppIcon

import halLib.halModule as halModule
import sc_library.parameters as params

# Debugging.
import sc_library.hdebug as hdebug

# The module that actually does the analysis.
import qtWidgets.qtSharpness as qtSharpness

## Counter
#
# Widget for keeping the various count displays up to date.
#
class Sharpness():

    ## __init__
    #
    # Initialize the counter object. This keeps track of the total
    # number of counts. One label is on the spot graph and the 
    # other label is on the image.
    #
    # @param q_label1 The first QLabel UI element.
    # @param q_label2 The second QLabel UI element.
    #
    def __init__(self, q_label1, q_label2):
        self.num = 0
        self.sharpness = 0
        self.q_label1 = q_label1
        self.q_label2 = q_label2
        self.updateSharpness(0)

    ## getCounts
    #
    # Returns the total number of counts.
    #
    # @return Returns the total number of counts.
    #
    def getSharpness(self):
        return self.sharpness

    ## reset
    #
    # Reset the counts to zero & update the labels.
    #
    def reset(self):
        self.num = 0
        self.sharpness = 0
        self.updateSharpness(0)

    ## updateCounts
    #
    # Increments the number of counts by the number of objects
    # found in the most recent frame. Updates the labels accordingly.
    #
    # @param counts The number of objects in the frame that was analyzed.
    #
    def updateSharpness(self, sharpness):
        #print "Got sharpness: ", sharpness
        self.num += 1
        self.sharpness = self.sharpness + ((sharpness - self.sharpness)/(self.num+1.0)) #cumulative average
        self.q_label1.setText(str(sharpness))
        self.q_label2.setText(str(self.sharpness))



## QSpotGraph
#
# Spot Count Graphing Widget.
#
class QSharpnessGraph(QtGui.QWidget):

    ## __init__
    #
    # Create a spot graph object.
    #
    # @param x_size The x size (in pixels) of this widget.
    # @param y_size The y size (in pixels) of this widget.
    # @param y_min The graph's minimum value.
    # @param y_max The graph's maximum value.
    # @param parent (Optional) The PyQt parent of this object.
    #
    def __init__(self, x_size, y_size, y_min, y_max, scale, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.range = y_max - y_min
        self.scale = scale
        self.x_size = x_size
        self.y_size = y_size
        self.y_min = float(y_min)
        self.y_max = float(y_max)

        self.colors = [False]
        self.points_per_cycle = len(self.colors)
        self.x_points = 100

        self.x_scale = float(self.x_size)/float(self.x_points)
        self.y_scale = float(y_size)/5.0
        self.cycle = 0
        if self.points_per_cycle > 1:
            self.cycle = self.x_scale * float(self.points_per_cycle)

        self.data = []
        for i in range(self.x_points):
            self.data.append(0)

    ## changeYRange
    #
    # @param y_min (Optional) The new y minimum of the graph.
    # @param y_max (Optional) The new y maximum of the graph.
    #
    def changeYRange(self, y_min = None, y_max = None, scale = None):
        if y_min:
            self.y_min = y_min
        if y_max:
            self.y_max = y_max
        if scale:
            self.scale = scale
        self.range = self.y_max - self.y_min

    ## newColors
    #
    # @param colors The colors to use for the points in the graph. This is based on the values specified in the shutter file.
    # @param total_points The total number of points in x.
    #
    def newColors(self, colors, total_points):
        self.colors = colors
        self.points_per_cycle = len(colors)
        self.x_points = total_points

        self.x_scale = float(self.x_size)/float(self.x_points)
        self.cycle = 0
        if self.points_per_cycle > 1:
            self.cycle = self.x_scale * float(self.points_per_cycle)

        self.data = []
        for i in range(self.x_points):
            self.data.append(0)

        self.update()

    ## paintEvent
    #
    # Redraw the graph.
    #
    # @param event A PyQt event object.
    #
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)

        # Background
        color = QtGui.QColor(255, 255, 255)
        painter.setPen(color)
        painter.setBrush(color)
        painter.drawRect(0, 0, self.x_size, self.y_size)

        # Draw lines in y to denote the start of each cycle, but only
        # if we have at least 2 points per cycle.
        #
        # Draw grid lines in x.
        if self.cycle:
            painter.setPen(QtGui.QColor(200, 200, 200))
            x = 0.0
            while x < float(self.x_size):
                ix = int(x)
                painter.drawLine(ix, 0, ix, self.y_size)
                x += self.cycle

            y = 0.0
            while y < float(self.y_size):
                iy = int(y)
                painter.drawLine(0, iy, self.x_size, iy)
                y += self.y_scale

        if (len(self.data)>0):
            # Lines
            painter.setPen(QtGui.QColor(0, 0, 0))
            x1 = int(self.x_scale * float(0))
            y1 = self.y_size - int((self.data[0]*self.scale - self.y_min)/self.range * float(self.y_size))
            for i in range(len(self.data)-1):
                x2 = int(self.x_scale * float(i+1))
                y2 = self.y_size - int((self.data[i+1]*self.scale - self.y_min)/self.range * float(self.y_size))
                painter.drawLine(x1, y1, x2, y2)
                x1 = x2
                y1 = y2

            # Points
            for i in range(len(self.data)):
                color = self.colors[i % self.points_per_cycle]
                qtcolor = 0
                if color:
                    qtcolor = QtGui.QColor(color[0], color[1], color[2])
                else:
                    qtcolor = QtGui.QColor(0, 0, 0)
                painter.setPen(QtGui.QColor(0, 0, 0))
#                painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0),0))
                painter.setBrush(qtcolor)

                x = int(self.x_scale * float(i))
                y = self.y_size - int((self.data[i]*self.scale - self.y_min)/self.range * float(self.y_size))
                if y < 0:
                    y = 0
                if y > self.y_size:
                    y = self.y_size
                painter.drawEllipse(x - 2, y - 2, 4, 4)

    ## updateGraph
    #
    # Updates the graph given a frame number and the number of spots in the frame.
    #
    # @param frame_index The frame number.
    # @param spots The number of spots in the frame.
    #
    def updateGraph(self, frame_index, sharpness):
        self.data[frame_index % self.x_points] = sharpness
        self.update()



## SpotCounter
#
# Spot Counter Dialog Box
#
class SharpnessDetector(QtGui.QDialog, halModule.HalModule):
    imageProcessed = QtCore.pyqtSignal()

    ## __init__
    #
    # Create the spot counter dialog box.
    #
    # @param parameters The initial parameters.
    # @param parent The PyQt parent of this dialog box.
    #
    @hdebug.debug
    def __init__(self, parameters, parent = None):
        QtGui.QMainWindow.__init__(self, parent)
        halModule.HalModule.__init__(self)

        self.counters = [False, False]
        self.filming = 0
        self.filenames = [False, False]
        self.number_cameras = 1
        self.parameters = parameters
        self.sharpness_detector = False
        self.spot_graphs = [False, False]

        if parent:
            self.have_parent = True
        else:
            self.have_parent = False

        # UI setup.
        self.ui.setupUi(self)
        self.setWindowTitle(parameters.setup_name + " Sharpness Detector")
        self.setWindowIcon(qtAppIcon.QAppIcon())

        # Setup Sharpness objects.
        if (self.number_cameras == 1):
            self.counters = [Sharpness(self.ui.countsLabel1, self.ui.countsLabel2)]
        else:
            self.counters = [Sharpness(self.ui.countsLabel1, self.ui.countsLabel2),
                             Sharpness(self.ui.countsLabel3, self.ui.countsLabel4)]

        # Setup sharpness detector
        self.sharpness_detector = qtSharpness.QSharpness(parameters)
        self.sharpness_detector.imageProcessed.connect(self.updateCounts)

        # Setup spot counts graph(s).
        if (self.number_cameras == 1):
            parents = [self.ui.graphFrame]
        else:
            parents = [self.ui.graphFrame, self.ui.graphFrame2]

        for i in range(self.number_cameras):
            graph_w = parents[i].width() - 4
            graph_h = parents[i].height() - 4
            self.spot_graphs[i] = QSharpnessGraph(graph_w,
                                                  graph_h,
                                                  parameters.min_sharp,
                                                  parameters.max_sharp,
                                                  parameters.scale_sharp,
                                                  parent = parents[i])
            self.spot_graphs[i].setGeometry(2, 2, graph_w, graph_h)
            self.spot_graphs[i].show()

        

        # Connect signals.
        if self.have_parent:
            self.ui.okButton.setText("Close")
            self.ui.okButton.clicked.connect(self.handleOk)
        else:
            self.ui.okButton.setText("Quit")
            self.ui.okButton.clicked.connect(self.handleQuit)
        self.ui.maxSpinBox.valueChanged.connect(self.handleMaxChange)
        self.ui.minSpinBox.valueChanged.connect(self.handleMinChange)
        self.ui.scale_lineEdit.returnPressed.connect(self.handleScaleChange)

        # Set modeless.
        self.setModal(False)

        
    ## cleanup
    #
    @hdebug.debug
    def cleanup(self):
        self.sharpness_detector.shutDown()

    ## closeEvent
    #
    # Handle close events. The event is ignored and the dialog box is simply
    # hidden if the dialog box has a parent.
    #
    # @param event A QEvent object.
    #
    @hdebug.debug
    def closeEvent(self, event):
        if self.have_parent:
            event.ignore()
            self.hide()

    ## connectSignals
    #
    # @param signals An array of signals that we might be interested in connecting to.
    #
    @hdebug.debug
    def connectSignals(self, signals):
        for signal in signals:

            if (signal[1] == "newColors"):
                signal[2].connect(self.newColors)

    ## getCounts
    #
    # Returns the number of objects detected. If the movie is requested
    # by TCP/IP this number is passed back to the calling program.
    #
    #@hdebug.debug
    #def getCounts(self):
    #    return self.counters[0].getCounts()

    ## handleMaxChange
    #
    # Handles changing the maximum of the spot graph.
    #
    # @param new_max The new maximum.
    #
    @hdebug.debug
    def handleMaxChange(self, new_max):
        for i in range(self.number_cameras):
            self.spot_graphs[i].changeYRange(y_max = new_max)
        self.ui.minSpinBox.setMaximum(new_max - 1)
        self.parameters.max_sharp = new_max

    ## handleMinChange
    #
    # Handles changing the minimum of the spot graph.
    #
    # @param new_min The new minimum.
    #
    @hdebug.debug
    def handleMinChange(self, new_min):
        for i in range(self.number_cameras):
            self.spot_graphs[i].changeYRange(y_min = new_min)
        self.ui.maxSpinBox.setMinimum(new_min + 1)
        self.parameters.min_sharp = new_min

    @hdebug.debug
    def handleScaleChange(self):
        scale = float(self.ui.scale_lineEdit.text())
        for i in range(self.number_cameras):
            self.spot_graphs[i].changeYRange(scale = scale)
        self.parameters.scale_sharp = scale

    ## handleOk
    #
    # Handles the close button, hides the dialog box.
    #
    # @param bool Dummy parameter.
    #
    @hdebug.debug
    def handleOk(self, bool):
        self.hide()

    ## handleQuit
    #
    # Handles the quit button, closes the dialog box.
    #
    # @param bool Dummy parameter.
    #
    @hdebug.debug
    def handleQuit(self, bool):
        self.close()

    ## newColors
    #
    # Called when the spot colors need to be changed, as for example
    # when a new shutters file is selected.
    #
    # @param colors A colors array.
    #
    def newColors(self, colors):

        # If colors is an empty array then we use the default color (white).
        if (len(colors) == 0):
            colors = [[255, 255, 255]]
        points_per_cycle = len(colors)
        total_points = points_per_cycle
        while total_points < 100:
            total_points += points_per_cycle

        for i in range(self.number_cameras):
            self.spot_graphs[i].newColors(colors, total_points)

    ## newFrame
    #
    # Called when there is a new frame from the camera.
    #
    # @param frame A frame object.
    # @param filming True/False if we are currently filming.
    #
    def newFrame(self, frame, filming):
        if self.sharpness_detector:
            self.sharpness_detector.newImageToFT(frame)

    ## newParameters
    #
    # Called when the parameters are changed. Updates the spot graphs
    # and image display with the new parameters.
    #
    # @param parameters A parameters object.
    #
    @hdebug.debug
    def newParameters(self, parameters):
        self.parameters = parameters

        self.sharpness_detector.newParameters(parameters)

        # Update counters, count graph(s) & STORM image(s).
        for i in range(self.number_cameras):
            self.counters[i].reset()

        # UI update.
        self.ui.maxSpinBox.setValue(parameters.max_sharp)
        self.ui.minSpinBox.setValue(parameters.min_sharp)
        self.ui.scale_lineEdit.setText(str(parameters.scale_sharp))

    ## updateCounts
    #
    # Called when the objects in a frame have been localized.
    #
    # @param which_camera This is one of "camera1" or "camera2"
    # @param frame_number The frame number of the frame that was analyzed.
    # @param x_locs The x locations of the objects that were found.
    # @param y_locs The y locations of the objects that were found.
    # @param spots The total number of spots that were found.
    #
    def updateCounts(self, which_camera, frame_number, sharpness):
        if (which_camera == "camera1"):
            self.spot_graphs[0].updateGraph(frame_number, sharpness)
            if self.filming or True:
                self.counters[0].updateSharpness(sharpness)
        elif (which_camera == "camera2"):
            self.spot_graphs[1].updateGraph(frame_number, sharpness)
            if self.filming:
                self.counters[1].updateSharpness(sharpness)
        else:
            print "spotCounter.update Unknown camera:", which_camera
        self.imageProcessed.emit()

    ## startCounter
    #
    # Called at the start of filming to reset the spot graphs and the
    # images. If name is not False then this is assumed to be root
    # filename to save the spot counter images in when filming is finished.
    #
    # @param film_name The name of the film without any extensions, or False if the film is not being saved.
    # @param run_shutters True/False the shutters should be run or not.
    #
    @hdebug.debug
    def startFilm(self, film_name, run_shutters):
        for i in range(self.number_cameras):
            self.counters[i].reset()
        self.filming = True
        self.filenames = [False, False]

    ## stopFilm
    #
    # Called at the end of filming.
    #
    # @param film_writer The film writer object.
    #
    @hdebug.debug
    def stopFilm(self, film_writer):
        self.filming = False
        if film_writer:
            film_writer.setSharpness(self.counters[0].getSharpness())


## SingleSpotCounter
#
# Spot counter dialog box for a single camera.
#
class SingleSharpnessDetector(SharpnessDetector):

    ## __init__
    #
    # @param hardware A hardware parameters object.
    # @param parameters A parameters object.
    # @param parent (Optional) The PyQt parent of this dialog box.
    #
    def __init__(self, hardware, parameters, parent = None):
        self.cameras = 1
        
        import qtdesigner.sharpnessdetector_ui as sharpnessDetectorUi
        self.ui = sharpnessDetectorUi.Ui_Dialog()
        
        SharpnessDetector.__init__(self, parameters, parent)

## DualSpotCounter
#
# Spot counter dialog box for a two camera setup.
#
class DualSpotCounter(SharpnessDetector):

    ## __init__
    #
    # @param hardware A hardware parameters object.
    # @param parameters A parameters object.
    # @param parent (Optional) The PyQt parent of this dialog box.
    #
    def __init__(self, hardware, parameters, parent = None):
        self.cameras = 2
        
        import qtdesigner.sharpnessdetector_ui as sharpnessDetectorUi
        self.ui = sharpnessDetectorUi.Ui_Dialog()
        
        SharpnessDetector.__init__(self, parameters, parent)


# Testing.
#
#   Load a movie file, analyze it & save the result.
#
if __name__ == "__main__":

    import numpy

    import camera.frame as frame

    # This file is available in the ZhuangLab storm-analysis project on github.
    import sa_library.datareader as datareader

    if (len(sys.argv) != 4):
        print "usage: <settings> <movie_in> <png_out>"
        exit()

    # Open movie & get size.
    data_file = datareader.inferReader(sys.argv[2])
    [width, height, length] = data_file.filmSize()

    # Start spotCounter as a stand-alone application.
    app = QtGui.QApplication(sys.argv)
    parameters = params.Parameters(sys.argv[1], is_HAL = True)
    parameters.setup_name = "offline"
    
    parameters.x_pixels = width
    parameters.y_pixels = height
    parameters.x_bin = 1
    parameters.y_bin = 1

    spotCounter = SingleSpotCounter(parameters)
    spotCounter.newParameters(parameters, [[255,255,255]])

    # Start driver.
    driver = OfflineDriver(spotCounter, data_file, sys.argv[3])

    # Show window & start application.
    spotCounter.show()
    app.exec_()


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

