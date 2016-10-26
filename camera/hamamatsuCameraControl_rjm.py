#!/usr/bin/python
#
# Camera control specialized for a Andor camera.
#
# Hazen 11/09
#

from PyQt4 import QtCore
import os

# Debugging
import halLib.hdebug as hdebug

import camera.cameraControl as cameraControl
import hamamatsu.hamamatsucontroller as hamamatsu

class ACameraControl(cameraControl.CameraControl):
    @hdebug.debug
    def __init__(self, parameters, parent = None):
        cameraControl.CameraControl.__init__(self, parameters, parent)

        self.currentBufferIndex = -1

    ''' No Shutter on sCMOS
    @hdebug.debug
    def closeShutter(self):
        self.shutter = 0
        self.stopAcq()
        if self.got_camera:
            if self.reversed_shutter:
                self.camera.openShutter()
            else:
                self.camera.closeShutter()
    '''

    @hdebug.debug
    def getAcquisitionTimings(self):
        self.stopAcq()
        if self.got_camera:
            return self.camera.getAcquisitionTimings()
        else:
            return [1.0, 1.0, 1.0]

    @hdebug.debug
    def getTemperature(self):
        self.stopAcq()
        if self.got_camera:
            return self.camera.getTemperature()
        else:
            return [50, "unstable"]

    @hdebug.debug
    def initCamera(self):
        if not self.camera:
            if hdebug.getDebug():
                print " Initializing Andor Camera"
            if os.path.exists("D:\\Programs\\DCAM-SDK (1112)\\bin\\win32\\"):
                self.camera = hamamatsu.HamamatsuCamera("D:\\Programs\\DCAM-SDK (1112)\\bin\\win32\\")
            #else:
            #   self.camera = andor.AndorCamera("c:/Program Files/Andor SOLIS/")

    @hdebug.debug
    def newFilmSettings(self, parameters, filming = 0):
        self.stopAcq()
        self.mutex.lock()
        self.parameters = parameters
        p = parameters
        if self.got_camera:
            if filming:
                self.camera.setACQMode(p.acq_mode, number_frames = p.frames)
            else:
                self.camera.setACQMode("run_till_abort")
            # Due to what I can only assume is a bug in some of the
            # older Andor software you need to reset the frame
            # transfer mode after setting the aquisition mode.
            self.camera.setFrameTransferMode(p.frame_transfer_mode)
            # Set camera fan to low. This is overriden by the off option
            if p.low_during_filming:
                if filming:
                    self.camera.setFanMode(1) # fan on low
                else:
                    self.camera.setFanMode(0) # fan on full
            # This is for testing whether the camera fan is shaking the
            # the camera, adding noise to the images.
            if p.off_during_filming:
                if filming:
                    self.camera.setFanMode(2) # fan off
                else:
                    self.camera.setFanMode(0) # fan on full
        self.frames = []
        self.filming = filming
        self.mutex.unlock()

    @hdebug.debug
    def newParameters(self, parameters):
        self.initCamera()
        p = parameters
        self.reversed_shutter = p.reversed_shutter
        try:
            if hdebug.getDebug():
                print "  Setting Exposure Time"
            self.camera.setExposureTime(p.exposure_time)
            if hdebug.getDebug():
                print "  Setting ROI and Binning"
            self.camera.setROIAndBinning(p.ROI, p.binning)
            self.camera.setROIAndBinning(p.ROI, p.binning)
            '''
            if hdebug.getDebug():
                print "  Setting Read Mode"
            self.camera.setReadMode(4)
            if hdebug.getDebug():
                print "  Setting Temperature"
            self.camera.setTemperature(p.temperature)
            if hdebug.getDebug():
                print "  Setting Trigger Mode"
            self.camera.setTriggerMode(0)
            if hdebug.getDebug():
                print "  Setting ADChannel"
            self.camera.setADChannel(p.adchannel)
            if hdebug.getDebug():
                print "  Setting ROI and Binning"
            self.camera.setROIAndBinning(p.ROI, p.binning)
            if hdebug.getDebug():
                print "  Setting Horizontal Shift Speed"
            self.camera.setHSSpeed(p.hsspeed)
            if hdebug.getDebug():
                print "  Setting Vertical Shift Amplitude"
            self.camera.setVSAmplitude(p.vsamplitude)
            if hdebug.getDebug():
                print "  Setting Vertical Shift Speed"
            self.camera.setVSSpeed(p.vsspeed)
            if hdebug.getDebug():
                print "  Setting EM Gain Mode"
            self.camera.setEMGainMode(p.emgainmode)
            if hdebug.getDebug():
                print "  Setting EM Gain"
            self.camera.setEMCCDGain(p.emccd_gain)
            if hdebug.getDebug():
                print "  Setting Baseline Clamp"
            self.camera.setBaselineClamp(p.baselineclamp)
            if hdebug.getDebug():
                print "  Setting Preamp Gain"
            self.camera.setPreAmpGain(p.preampgain)
            if hdebug.getDebug():
                print "  Setting Acquisition Mode"
            self.camera.setACQMode("run_till_abort")
            if hdebug.getDebug():
                print "  Setting Frame Transfer Mode"
            self.camera.setFrameTransferMode(p.frame_transfer_mode)
            if hdebug.getDebug():
                print "  Setting Exposure Time"
            self.camera.setExposureTime(p.exposure_time)
            if hdebug.getDebug():
                print "  Setting Kinetic Cycle Time"
            self.camera.setKineticCycleTime(p.kinetic_cycle_time)
            p.head_model = self.camera.getHeadModel()
            if hdebug.getDebug():
                print " Camera Initialized
            '''
            print "Got camera!\n"
            self.got_camera = 1
        except:
            if hdebug.getDebug():
                print "QCameraThread: Bad camera settings"
            self.got_camera = 0
        self.newFilmSettings(parameters)

    @hdebug.debug
    def openShutter(self):
        self.shutter = 1
        self.stopAcq()
        if self.got_camera:
            if self.reversed_shutter:
                self.camera.closeShutter()
            else:
                self.camera.openShutter()

    @hdebug.debug
    def quit(self):
        self.stopThread()
        self.wait()
        if self.got_camera:
            self.camera.shutdown()

    def run(self):
        while(self.running):
            self.mutex.lock()
            #print "Should acquire? ", self.should_acquire
            #print "Got camera? ", self.got_camera
            xres,yres = self.camera.getDataSize()
            if self.should_acquire and self.got_camera:
                previousFrame = self.currentBufferIndex
                frames = []
                newestFrames, frameCount = self.camera.getTransferInfo()
                #print "Newest frames and frame count: %i,%i " % (newestFrames,frameCount)
                if newestFrames>0:
                    if previousFrame==-1:
                        numFrames = newestFrames
                    else:
                        numFrames = newestFrames - previousFrame
                    if numFrames<0:
                        numFrames = newestFrames + (self.camera.allocatedBuffers - previousFrame)
                    for i in range(0,numFrames):
                        frameToGet = i + previousFrame + 1
                        if frameToGet >= self.camera.allocatedBuffers:
                            frameToGet = frameToGet - self.camera.allocatedBuffers
                        frames.extend(self.camera.lockData(frameToGet, xres*yres, raw=True))
                    self.currentBufferIndex = newestFrames
                    #print "Length of frames: ", len(frames)
                #[frames, state] = self.camera.getImages16()
                #if state == "acquiring":
                if True:
                    if len(frames) > 0:

                        # If we get behind, dummy out the frame storage array
                        # so that the display does not get out of phase with
                        # the camera. Downstream code needs to check that it 
                        # got a frame and not just a zero.
                        if len(self.frames) > 0:
                            for i in range(len(frames)):
                                self.frames.extend([0])
                        else:
                            self.frames = frames

                        self.emit(QtCore.SIGNAL("newData(int)"), self.key)
                        #print "Signal newData(int) emitted."
                        if self.filming:
                            for frame in frames:
                                self.daxfile.saveFrame(frame)
                        self.camera.unlockData()
                elif state == "idle":
                    if not(self.forced_idle):
                        self.emit(QtCore.SIGNAL("idleCamera()"))
                else:
                    print " run " + state
            else:
                self.frames = []
                self.have_paused = 1
            self.mutex.unlock()
            self.msleep(5)

    @hdebug.debug
    def setEMCCDGain(self, gain):
        self.stopAcq()
        if self.got_camera:
            self.camera.setEMCCDGain(gain)

    @hdebug.debug        
    def startAcq(self, key):
        if self.have_paused:
            self.mutex.lock()
            self.key = key
            self.forced_idle = 0
            self.should_acquire = 1
            self.have_paused = 0
            if self.got_camera:
                self.currentBufferIndex = -1
                self.camera.startAcquisition()
            self.mutex.unlock()

    @hdebug.debug
    def stopAcq(self):
        if self.should_acquire:
            self.mutex.lock()
            self.forced_idle = 1
            if self.got_camera:
                self.camera.stopAcquisition()
            self.should_acquire = 0
            self.mutex.unlock()
            while not self.have_paused:
                self.usleep(50)

        
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

