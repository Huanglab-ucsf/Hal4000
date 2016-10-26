#!/usr/bin/python
#
# Acadia shutter control.
#
# Hazen 11/09
#

import nationalInstruments.nicontrol as nicontrol

import illumination.shutterControl as shutterControl

class AShutterControl(shutterControl.ShutterControl):
    def __init__(self, powerToVoltage):
        self.ct_task = 0
        self.wv_task = 0
        self.board = "PCIe-6353"
        self.oversampling = 100
        self.number_channels = 5                                       # channel 6 is LED, added 8/02/10
        shutterControl.ShutterControl.__init__(self, powerToVoltage)

    def cleanup(self):
        if self.ct_task:
            self.ct_task.clearTask()
            self.wv_task.clearTask()
            self.ct_task = 0
            self.wv_task = 0

    def setup(self): #Before, had kinetic_cycle_time as argument
        assert self.ct_task == 0, "Attempt to call setup without first calling cleanup."
        #
        # the counter runs slightly faster than the camera so that it is ready
        # to catch the next camera "fire" immediately after the end of the cycle.
        #
        frequency = (1.001/self.kinetic_value) * float(self.oversampling)

        # set up the analog channels
        #self.wv_task = nicontrol.WaveformOutput(self.board, 0)
        #for i in range(self.number_channels - 1):
        #    self.wv_task.addChannel(i + 1)

        # set up the digital channels
        self.wv_task = nicontrol.DigWaveformOutput(self.board, 0)
        for i in range(self.number_channels - 1):
            self.wv_task.addDigChannel(i + 1)
        
        # set up the waveform
        self.wv_task.setDigWaveform(self.waveforms, frequency)

        # set up the counter
        self.ct_task = nicontrol.CounterOutput(self.board, 0, frequency, 0.5)
        self.ct_task.setCounter(self.waveform_len)
        self.ct_task.setTrigger(0)

    def startFilm(self):
        self.wv_task.startTask()
        self.ct_task.startTask()

    def stopFilm(self):
        # stop the tasks
        if self.ct_task:
            self.ct_task.stopTask()
            self.wv_task.stopTask()
            self.ct_task.clearTask()
            self.wv_task.clearTask()
            self.ct_task = 0
            self.wv_task = 0

        # reset all the analog signals.
        #for i in range(self.number_channels):
        #    ao_task = nicontrol.VoltageOutput(self.board, i)
        #    ao_task.outputVoltage(self.powerToVoltage(i, 0.0))
        #    ao_task.startTask()
        #    ao_task.stopTask()
        #    ao_task.clearTask()

        # reset all the digital signals.
        for i in range(self.number_channels): #we have exactly 1 channel at all times
            do_task = nicontrol.DigitalOutput(self.board, i)
            do_task.output(0)
            do_task.startTask()
            do_task.stopTask()
            do_task.clearTask()

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

