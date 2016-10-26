#!/usr/bin/python
#
# Qt Widget for handling the display of camera data.
#
# Hazen 11/09
#

from PyQt4 import QtCore, QtGui
import sys

# Camera widget
class QCameraWidget(QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.buffer = QtGui.QPixmap(512, 512)
        self.image = 0
        self.image_min = 0
        self.image_max = 1
        self.live = 0
        self.show_grid = 0
        self.show_info = 1
        self.show_target = 0
        self.x = 0
        self.x_final = 512
        self.x_size = 0
        self.y = 0
        self.y_final = 512
        self.y_size = 0

    def blank(self):
        painter = QtGui.QPainter(self.buffer)
        color = QtGui.QColor(0, 0, 0)
        painter.setPen(color)
        painter.setBrush(color)
        painter.drawRect(0, 0, 512, 512)

    def getAutoScale(self):
        margin = int(0.1 * float(self.image_max - self.image_min))
        return [self.image_min - margin, self.image_max + margin]

    def mousePressEvent(self, event):
        self.x = event.x()
        self.y = event.y()

    def newColorTable(self, colortable):
        self.setColorTable(colortable)
        self.update()

    def newParameters(self, parameters, colortable, display_range):
        print "qtCamWidg parameters (x_pixels): ", parameters.x_pixels
        print "qtCamWidg parameters (y_pixels): ", parameters.y_pixels
        print "qtCamWidg parameters (x_bin): ", parameters.x_bin
        self.live = 1
        self.x_size = parameters.x_pixels/parameters.x_bin
        self.y_size = parameters.y_pixels/parameters.y_bin
        self.x_final = 512
        self.y_final = 512
        if self.x_size > self.y_size:
            self.y_final = 512 * self.y_size / self.x_size
        if self.x_size < self.y_size:
            self.x_final = 512 * self.x_size / self.y_size
        self.display_range = display_range
        self.image = QtGui.QImage(self.x_size, self.y_size, QtGui.QImage.Format_Indexed8)
        print "self.image width: ", self.image.width()
        if colortable:
            self.setColorTable(colortable)
        else:
            for i in range(256):
                self.image.setColor(i,QtGui.qRgb(i,i,i))
        self.blank()

    def newRange(self, range):
        self.display_range = range

    def paintEvent(self, Event):
        if self.live:
            painter = QtGui.QPainter(self.buffer)
            painter.drawImage(0, 0, self.image.scaled(self.x_final, self.y_final))
            painter = QtGui.QPainter(self)
            painter.drawPixmap(0, 0, self.buffer)
            
            if self.show_grid:
                painter.setPen(QtGui.QColor(255, 255, 255))
                for i in range(7):
                    painter.drawLine((i+1)*64, 0, (i+1)*64, 512)
                    painter.drawLine(0, (i+1)*64, 512, (i+1)*64)

            if self.show_target:
                painter.setPen(QtGui.QColor(255, 255, 255))
                painter.drawEllipse(236, 236, 40, 40)
                
    def setColorTable(self, colortable):
        for i in range(256):
            self.image.setColor(i, QtGui.qRgb(colortable[i][0], 
                                              colortable[i][1], 
                                              colortable[i][2]))

    def setShowGrid(self, bool):
        if bool:
            self.show_grid = 1
        else:
            self.show_grid = 0

    def setShowInfo(self, bool):
        if bool:
            self.show_info = 1
        else:
            self.show_info = 0

    def setShowTarget(self, bool):
        if bool:
            self.show_target = 1
        else:
            self.show_target = 0

    def updateImageWithData(self, new_data):
        print "updateImageWIthData called."
        self.blank()
        self.update()
        if self.show_info:
            self.emit(QtCore.SIGNAL("intensityInfo(int, int, int)"), self.x, self.y, 0)

#
# Testing
#

if __name__ == "__main__":
    class Parameters:
        def __init__(self):
            self.x_pixels = 200
            self.y_pixels = 200

    parameters = Parameters()
    app = QtGui.QApplication(sys.argv)
    viewer = QCameraWidget(parameters, [200,400])
    viewer.show()

    sys.exit(app.exec_())


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
