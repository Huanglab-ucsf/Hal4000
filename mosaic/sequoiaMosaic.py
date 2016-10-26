#!/usr/bin/python
#
## @file
#
#
# RJM 8/14
#

import numpy



# mosaic control thread.
import mosaic
#
# Focus Lock Dialog Box specialized for STORM3
# with Phresh QPD and MCL objective Z positioner.
#
class AMosaic(mosaic.Mosaic):
    def __init__(self, hardware, parameters, parent = None):
        print "Initializing mosaic..."
        print "Parametes are: ", parameters
        mosaic.Mosaic.__init__(self,parameters,parent)


#class AFocusLockZ(focusLockZ.FocusLockZQPD:)
#    def __init__(self, parameters, tcp_control, parent = None):
#        qpd = phreshQPD.PhreshQPDSTORM3()
#        stage = mclController.MCLStage("c:/Program Files/Mad City Labs/NanoDrive/")
#        motor = prior.PriorFocus()
#        lock_fn = lambda (x): -1.75 * x
#        control_thread = stageOffsetControl.motorStageQPDThread(qpd,
#                                                                stage,
#                                                                motor,
#                                                                lock_fn,
#                                                                50.0,
#                                                                parameters.qpd_zcenter)
#        ir_laser = LDC210.LDC210("PCI-6722", 1)
#        focusLockZ.FocusLockZQPD.__init__(self,
#                                          parameters,
#                                          tcp_control,
#                                          control_thread,
#                                          ir_laser,
#                                          parent)


#
# The MIT License
#
# Copyright (c) 2012 Zhuang Lab, Harvard University
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
