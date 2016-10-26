#!/usr/bin/python
#
## @file
#
# ctypes interace to a Mad City Labs piezo stage.
#
# Hazen 3/09
#

from ctypes import *
import time
#import pi_api

pi_path = "C:\\Users\\Public\\Documents\\PI\\E-709\\Samples\\C++\\First_steps\\"
pi_sn = "0113002170"

## ProductInformation
#
# The Mad City Labs product information structure.
#
class ProductInformation(Structure):
    _fields_ = [("axis_bitmap", c_ubyte),
                ("ADC_resolution", c_short),
                ("DAC_resolution", c_short),
                ("Product_id", c_short),
                ("FirmwareVersion", c_short),
                ("FirmwareProfile", c_short)]

parameterIDS = {"Number of System Axes": 0x0e000b02,
                "Stage Type": 0x0f000100,
                "Hardware Name": 0x0d000700,
                "Stage Serial Number": 0x0f000200,
                "Unique Firmware Name": 0xffff0006,
                "Version of Firmware": 0xffff0008,
                "Description of Firmware": 0xffff000d,
                "Length of Firmware": 0xffff0010,
                "Logical Device": 0xffff000c,
                "CRC-32 of Firmware Program Code": 0xffff0002,
                "DAC Bit Width": 0x0a000100,
                "ADC Bit Width": 0x04000b00}


## load PI DLL
#
# Handles loading the library (only once)
#
piPiezo = False
def loadPIDLL(pi_path):
    global piPiezo
    if(piPiezo == False):
        piPiezo = windll.LoadLibrary(pi_path + "PI_GCS2_DLL.dll")


## MCLStage
#
# The Mad City Labs piezo stage control class.
#
class PIControl:

    # Class instance variables
    dll_loaded = False
    handles_grabbed = False

    ## __init__
    #
    # Initializes the object by initializing the DLL, opening
    # a connection to requested stage, or the first the stage
    # if none is specified. The stage is then queried to
    # determine its various properties.
    #
    # @param mcl_path The path to the Mad City Labs stage control DLL.
    # @param serial_number (Optional) The serial number of the stage to control. If False then the first available stage is chosen.
    #
    def __init__(self, pi_path):

        # load DLL is necessary
        if not PIControl.dll_loaded:
            loadPIDLL(pi_path)
            PIControl.dll_loaded = True

        # stage properties storage
        self._props_ = {}

        # define the return types of some the functions
        #mcl.MCL_GetCalibration.restype = c_double
        #mcl.MCL_SingleReadN.restype = c_double

        #
        # Get a stage handle.
        #
        # If the stage serial number is not specified we assume that there
        # is only stage connected (or at least powered on).
        #
        self.handle = -1

        self.handle = piPiezo.PI_ConnectUSB(pi_sn)
        PIControl.handles_grabbed = True

        self.axis = create_string_buffer('1\n')

        if self.handle < 0:
            PIControl.handles_grabbed = False
            print "Failed to connect to the PI objective piezo. Perhaps it is turned off?"

        # get the stage information
        if not(self.handle):
            self._props_['DAC_resolution'] = self._getParam("DAC Bit Width", number=True)
            self._props_['ADC_resolution'] = self._getParam("ADC Bit Width", number=True)
            self._props_['Hardware'] = self._getParam("Hardware Name", number=False)
            self._props_['StageType'] = self._getParam("Stage Type", number=False)
            
        
        '''
        caps = ProductInformation(0, 0, 0, 0, 0, 0)
        if self.handle:
            assert mcl.MCL_GetProductInfo(byref(caps), self.handle) == 0, "MCL_GetProductInfo failed."
            self._props_['axis_bitmap'] = caps.axis_bitmap
            self._props_['ADC_resolution'] = caps.ADC_resolution
            self._props_['DAC_resolution'] = caps.DAC_resolution
            self._props_['Product_id'] = caps.Product_id
            self._props_['FirmwareVersion'] = caps.FirmwareVersion
            self._props_['FirmwareProfile'] = caps.FirmwareProfile
            self._props_['SerialNumber'] = mcl.MCL_GetSerialNumber(self.handle)
        '''

        # store which axises are valid
        #
        # Note that the axises are 1 indexed, i.e.:
        #   axis X = 1
        #   axis Y = 2
        #   axis Z = 3
        self.valid_axises = [0, 0, 0, 1]

        # store axises ranges
        self.axis_range = [0, 
                           0,
                           0,
                           self._getZRange()]


        print "PI objective piezo loaded with range of ", self.axis_range[3]
        servoState = self._getServoState()
        if not servoState:
            self._setServoState(True)

    ## _getCalibration
    #
    # (Internal)
    #
    # @param axis The axis to get the calibration from.
    #
    # @return The calibration information for the specified axis.
    #
    '''
    def _getCalibration(self, axis):
        if self.handle and self.valid_axises[axis]:
            return mcl.MCL_GetCalibration(c_ulong(axis), self.handle)
        else:
            return 0
    '''

    def _getParam(self, parameter_string, number=True):
        parameterID = parameterIDS[parameter_string]
        paramArray = (c_int*1)()
        paramArray[0] = parameterID
        pdValues = (c_double*1)()
        szStrings = create_string_buffer(2048)
        err = piPiezo.PI_qSEP(self.handle, self.axis, paramArray,
                              pdValues, szStrings, c_int(2048))
        if not err:
            print "Error getting parameter..."
        #print "getFirmwaveVersion...", err
        #print "getFirmwareVersion string...", szStrings.value
        if number:
            return pdValues[0]
        else:
            return szStrings.value

    def _getZRange(self):
        if self.handle>=0:
            minPos = (c_double*1)()
            err1 = piPiezo.PI_qTMN(self.handle, self.axis, minPos)
            maxPos = (c_double*1)()
            err2 = piPiezo.PI_qTMX(self.handle, self.axis, maxPos)
            if err1<=1 and err2<=1:
                return [minPos[0], maxPos[0]]
            else:
                print "Error getting PI z-range...", (err1,err2)
                return [0,0]
        else:
            return [0,0]

    def _getServoState(self):
        servoValue = (c_bool*1)()
        err = piPiezo.PI_qSVO(self.handle, self.axis, servoValue)
        if err==1:
            return servoValue[0]
        else:
            print "Error getting PI servo state..."

    def _setServoState(self, state):
        servoValue = (c_bool*1)()
        servoValue[0] = state
        err = piPiezo.PI_SVO(self.handle, self.axis, servoValue)
        if err!=1:
            print "Error setting PI to closed-loop servo state."
        

    ## getAxisRange
    #
    # @param axis (integer) The axis to get the range of.
    #
    # @return The axis range
    #
    def getAxisRange(self, axis):
        if self.handle and self.valid_axises[axis]:
            return self.axis_range[axis]
        else:
            return 0

    ## getPosition
    #
    # @param axis (integer) The axis to get the position of.
    #
    # @return The position of the axis.
    #
    '''
    def getPosition(self, axis):
        if not(self.valid_axises[axis]):
            print "getPosition: invalid axis", axis
        if self.handle:
            return mcl.MCL_SingleReadN(c_ulong(axis), self.handle)
    '''
    def getPosition(self, axis):
        if not(self.valid_axises[axis]):
            print "getPosition: invalid axis", axis
        if self.handle>=0:
            position = (c_double*1)()
            err = piPiezo.PI_qPOS(self.handle, self.axis, position)
            if err<=1:
                return position[0]
            else:
                print "getPosition: PI Error"
                return err
        else:
            return 0

    ## getProperties
    #
    # @return The stage properties.
    #
    def getProperties(self):
        return self._props_

    ## moveTo
    #
    # @param axis (integer) The axis to move.
    # @param position The position to move to.
    #
    def moveTo(self, axis, position):
#        assert self.valid_axises[axis], "moveTo: invalid axis " + str(axis)
#        assert position >= 0.0, "moveTo: position too small " + str(position)
#        assert position <= self.axis_range[axis], "moveTo: position too large " + str(position)
        if not(self.valid_axises[axis]):
            print "moveTo: invalid axis", axis
        elif not(position >= self.axis_range[axis][0]):
            print "moveTo: position too small", position
        elif not(position <= self.axis_range[axis][1]):
            print "moveTo: position too large", position
        elif self.handle>=0:
            pos = (c_double*1)()
            pos[0] = position
            err = piPiezo.PI_MOV(self.handle, self.axis, pos)
            if not(err<=1):
                print "moveTo: PI Error"

    ## printDeviceInfo
    #
    # Print information about this device.
    #
    def printDeviceInfo(self):
        if self.handle>=0:
            print "device info..."
            #mcl.MCL_PrintDeviceInfo(self.handle)

    def getParameters(self):
        if self.handle>=0:
            szBuffer = create_string_buffer(10000)
            err = piPiezo.PI_qHPA(self.handle, szBuffer, c_int(10000))
            return szBuffer.value

    def getHelp(self):
        if self.handle>=0:
            szBuffer = create_string_buffer(10000)
            err = piPiezo.PI_qHLP(self.handle, szBuffer, c_int(10000))
            print "getHelp error: ", err
            return szBuffer.value

    ## readWaveForm
    #
    # Read the (position) wave form from an axis. Reading (I think) occurs at a 500us rate.
    #
    # @param axis (integer) The axis to read.
    # @param points The number of points to acquire.
    #
    # @return The waveform data as a python array.
    #
    '''
    def readWaveForm(self, axis, points):
        if self.handle:
            if points < 1000:
                wave_form_data_type = c_double * points
                wave_form_data = wave_form_data_type()
                mcl.MCL_ReadWaveFormN(c_ulong(axis), c_ulong(points), c_double(4.0), wave_form_data, self.handle)
                return wave_form_data
            else:
                print "MCL stage can only acquire a maximum of 999 points"
    '''
    ## shutDown
    #
    # Move the stage axises back to their zero positions and close the connection to the stage.
    #
    def shutDown(self):
        for i in range(4):
            if self.valid_axises[i]:
                self.moveTo(i, 0.0)
        if self.handle>=0:
            piPiezo.PI_CloseConnection(self.handle)

    ## zMoveTo
    #
    # Move the z axis to the specified position.
    #
    # @param position The new stage z axis position.
    #
    def zMoveTo(self, position):
        self.moveTo(3, position)


#
# Testing section.
#

if __name__ == "__main__":

    def printDict(dict):
        keys = dict.keys()
        keys.sort()
        for key in keys:
            print key, '\t', dict[key]

    print "Initializing Stage"
    #stage = MCLStage("c:\\Program Files\\Mad City Labs\\NanoDrive\\")
    stage = PIControl(pi_path)
    #print stage.getParameters()
    #print stage.getHelp()
    #print "Firmware version: ", stage._getFirmwareVersion()
    printDict(stage._props_)
    stage.shutDown()
    

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
