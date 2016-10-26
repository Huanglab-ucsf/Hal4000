#!/usr/bin/python
#
# Illumination control specialized for STORM3.
#
# Hazen 6/09
#

from PyQt4 import QtCore

import illumination.channelWidgets as channelWidgets
import illumination.commandQueues as commandQueues
import illumination.illuminationControl as illuminationControl

#
# Illumination power control specialized for STORM3.
#
class STORM3QIlluminationControlWidget(illuminationControl.QIlluminationControlWidget):
    def __init__(self, settings_file_name, parameters, parent = None):
        # setup the AOTF communication thread
        self.aotf_queue = commandQueues.QAOTFThread()
        self.aotf_queue.start(QtCore.QThread.NormalPriority)

        # setup the Cube communication thread
        self.cube_queue = commandQueues.QCubeThread()
        self.cube_queue.start(QtCore.QThread.NormalPriority)

        illuminationControl.QIlluminationControlWidget.__init__(self, settings_file_name, parameters, parent)

    def autoControl(self, channels):
        self.aotf_queue.analogModulationOn()
        self.cube_queue.analogModulationOn()
        illuminationControl.QIlluminationControlWidget.autoControl(self, channels)

    def manualControl(self):
        self.aotf_queue.analogModulationOff()
        self.cube_queue.analogModulationOff()
        illuminationControl.QIlluminationControlWidget.manualControl(self)

    def newParameters(self, parameters):
        illuminationControl.QIlluminationControlWidget.newParameters(self, parameters)

        # Layout the widget
        dx = 50
        width = self.number_channels * dx

        # The height is based on how many buttons there are per channel,
        # so first we figure out the number of buttons per channel.
        max_buttons = 0
        for i in range(self.number_channels):
            n_buttons = len(parameters.power_buttons[i])
            if n_buttons > max_buttons:
                max_buttons = n_buttons
        height = 204 + max_buttons * 22

        # Set the size based on the number of channels and buttons
        self.resize(width, height)
        self.setMinimumSize(QtCore.QSize(width, height))
        self.setMaximumSize(QtCore.QSize(width, height))

        # Create the individual channels
        x = 0
        for i in range(self.number_channels):
            n = self.settings[i].channel
            if hasattr(self.settings[i], 'use_aotf'):
                channel = channelWidgets.QAOTFChannel(self,
                                                      self.settings[i],
                                                      parameters.default_power[n],
                                                      parameters.on_off_state[n],
                                                      parameters.power_buttons[n],
                                                      x,
                                                      dx,
                                                      height)
                channel.setCmdQueue(self.aotf_queue)
                self.channels.append(channel)
            elif hasattr(self.settings[i], 'use_cube405'):
                channel = channelWidgets.QCube405Channel(self,
                                                         self.settings[i],
                                                         parameters.default_power[n],
                                                         parameters.on_off_state[n],
                                                         parameters.power_buttons[n],
                                                         x,
                                                         dx,
                                                         height)
                channel.setCmdQueue(self.cube_queue)
                self.channels.append(channel)
            x += dx

        # Update the channels to reflect there current ui settings.
        for channel in self.channels:
            channel.uiUpdate()
                            
        # Save access to the previous parameters file so that
        # we can save the settings when the parameters are changed.
        self.last_parameters = parameters

    def shutDown(self):
        illuminationControl.QIlluminationControlWidget.shutDown(self)
        self.aotf_queue.stopThread()
        self.aotf_queue.wait()
        self.cube_queue.stopThread()
        self.cube_queue.wait()


#
# Illumination power control dialog box specialized for STORM3.
#
class AIlluminationControl(illuminationControl.IlluminationControl):
    def __init__(self, parameters, parent = None):
        illuminationControl.IlluminationControl.__init__(self, parameters, parent)
        self.power_control = STORM3QIlluminationControlWidget("illumination/storm3_illumination_control_settings.xml",
                                                              parameters,
                                                              parent = self.ui.laserBox)
        self.updateSize()

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
