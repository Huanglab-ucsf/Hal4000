#!/usr/bin/python
#
# Interfaces with a phresh photonics QPD via a National Instruments card.
#
# Hazen 4/09
#

import ctypes
import os
import sys

try:
    import nationalInstruments.nicontrol as nicontrol
except:
    sys.path.append("..")
    import nationalInstruments.nicontrol as nicontrol

if os.path.exists("averager.dll"):
    averager = ctypes.cdll.LoadLibrary("averager")
else:
    averager = ctypes.cdll.LoadLibrary("phreshPhotonics/averager")


#
# PhreshQPD interface class.
#
class PhreshQPD:
    def __init__(self, samples = 5000, sample_rate_Hz = 100000):
        self.samples = samples

    def collectData(self):
        # Collect the data.
        self.qpd_task.startTask()
        data = self.qpd_task.getData()
        self.qpd_task.stopTask()

        return data

    def shutDown(self):
        self.qpd_task.clearTask()


#
# STORM3 QPD Class
#
# PCI-MIO-16E board:
#  Sum    - AI channel 0
#  X diff - AI channel 1
#  Y diff - AI channel 2
#
class PhreshQPDSTORM3(PhreshQPD):
    def __init__(self, samples = 5000, sample_rate_Hz = 100000):
        PhreshQPD.__init__(self, samples = samples, sample_rate_Hz = sample_rate_Hz)
        self.qpd_task = nicontrol.AnalogInput("PCI-MIO-16E-4", 0)
        self.qpd_task.addChannel(1)
        self.qpd_task.addChannel(2)
        self.qpd_task.configureAcquisition(samples, sample_rate_Hz)

    def qpdScan(self):
        data = self.collectData()

        # Compute the average using C helper library (for speed purposes).
        average_type = ctypes.c_double * 3
        average = average_type()
        averager.averager(ctypes.byref(data), 
                          ctypes.byref(average), 
                          ctypes.c_int(self.samples),
                          ctypes.c_int(3))
        return [1000.0 * average[0], 1000.0 * average[1], 1000.0 * average[2]]


#
# PRISM2 QPD Class
#
# PCI-MIO-16E board:
#  Sum    - AI channel 0
#  X diff - AI channel 1
#
class PhreshQPDPRISM2(PhreshQPD):
    def __init__(self, samples = 5000, sample_rate_Hz = 100000):
        PhreshQPD.__init__(self, samples = samples, sample_rate_Hz = sample_rate_Hz)
#        self.qpd_task = nicontrol.AnalogInput("PCI-MIO-16E-4", 0)
        self.qpd_task = nicontrol.AnalogInput("PCIe-6321", 0)
        self.qpd_task.addChannel(1)
        self.qpd_task.configureAcquisition(samples, sample_rate_Hz)

    def qpdScan(self):
        data = self.collectData()

        # Compute the average using C helper library (for speed purposes).
        average_type = ctypes.c_double * 2
        average = average_type()
        averager.averager(ctypes.byref(data), 
                          ctypes.byref(average), 
                          ctypes.c_int(self.samples),
#                          ctypes.c_int(1))
                          ctypes.c_int(2))
        return [1000.0 * average[0] - 25.4, 1000.0 * average[1] - 40.8, 0.0]
#        return [1000.0 * average[0], 0.0, 0.0]


# testing
if __name__ == "__main__":
    qpd = PhreshQPDSTORM3()
    for i in range(10):
        print qpd.qpdScan()
    qpd.shutDown()


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
