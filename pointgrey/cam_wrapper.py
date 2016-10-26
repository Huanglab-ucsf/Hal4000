__all__ = [ ]

import os
import platform
import sys
import textwrap
import numpy as np
from numpy import ctypeslib
import ctypes
import ctypes.util
import ctypes.wintypes
from ctypes.wintypes import UINT, INT, BYTE, BOOLEAN, LPVOID
from ctypes import *
import warnings

#sys.path.append("ptgrey//pyflycapture2-0.1//build//lib.win32-2.7")
import flycapture2

from ctypes.wintypes import WORD
from ctypes.wintypes import DWORD
HCAM = ctypes.wintypes.HANDLE
from ctypes.wintypes import HDC
from ctypes.wintypes import HWND
c_char = ctypes.c_byte
c_char_p = ctypes.POINTER(ctypes.c_byte)
c_int_p = ctypes.POINTER(ctypes.c_int)
c_double_p = ctypes.POINTER(ctypes.c_double)
from ctypes import c_int, c_uint, c_double, c_bool, c_long, c_ulong, c_float
from ctypes import byref



class fc2Config(Structure):
    _fields_ = [("numBuffers", UINT),
                ("numImageNotifications", UINT),
                ("minNumImageNotifications", UINT),
                ("grabTimeout", INT),
                ("grabMode", UINT),
                ("isochBusSpeed", UINT),
                ("asyncBusSpeed", UINT),
                ("bandwidthAllocation", UINT),
                ("registerTimeoutRetries", UINT),
                ("registerTimeout", UINT),
                ("reserved[16]", 16*UINT)]

class fc2Image(Structure):
    _fields_ = [("rows", UINT),
                ("cols", UINT),
                ("stride", UINT),
                ("pData", c_char_p),
                ("dataSize", UINT),
                ("receivedDataSize", UINT),
                ("format", UINT),
                ("bayerFormat", UINT),
                ("imageImpl", LPVOID)]
                
'''
dll_name = 'tisgrabber.dll'
cam = ctypes.windll.LoadLibrary(dll_name)

serialNum = ctypes.create_string_buffer(20)
serialNum = "ISB3200016679"

filenm = ctypes.create_string_buffer("test.bmp")

initLib = cam.__getattr__('IC_InitLibrary')
closeLib = cam.__getattr__('IC_CloseLibrary')
createGrabber = cam.__getattr__('IC_CreateGrabber')
releaseGrabber = cam.__getattr__('IC_ReleaseGrabber')
getDeviceName = cam.__getattr__('IC_GetDeviceName')
getDevice = cam.__getattr__('IC_GetDevice')
getDeviceCount = cam.__getattr__('IC_GetDeviceCount')
openDevice = cam.__getattr__('IC_OpenVideoCaptureDevice')
getSerialNumber = cam.__getattr__('IC_GetSerialNumber')
getUniqueNameFromList = cam.__getattr__('IC_GetUniqueNamefromList')
getFrameRate = cam.__getattr__('IC_GetFrameRate')
startLive = cam.__getattr__('IC_StartLive')
prepareLive = cam.__getattr__('IC_PrepareLive')
suspendLive = cam.__getattr__('IC_SuspendLive')
stopLive = cam.__getattr__('IC_StopLive')
snapImage = cam.__getattr__('IC_SnapImage')
saveImage = cam.__getattr__('IC_SaveImage') #0 = jpeg; 1 = bitmap
getImagePtr = cam.__getattr__('IC_GetImagePtr')
getExpRegVal = cam.__getattr__('IC_GetExpRegVal')
getExpRegValRange = cam.__getattr__('IC_GetExpRegValRange')
getExpAbsValRange = cam.__getattr__('IC_GetExpAbsValRange')
getExpAbsVal = cam.__getattr__('IC_GetExpAbsVal')
setExpAbsVal = cam.__getattr__('IC_SetExpAbsVal')
getVideoProperty = cam.__getattr__('IC_GetVideoProperty')
getAutoVideoProperty = cam.__getattr__('IC_GetAutoVideoProperty')
getImageDescription = cam.__getattr__('IC_GetImageDescription')
enableAutoVideoProperty = cam.__getattr__('IC_EnableAutoVideoProperty')
#continuousMode not available in live mode
setContinuousMode = cam.__getattr__('IC_SetContinuousMode') #params: hGrabber (handle), cont (0=continuous snap, 1=not)
setFrameReadyCallback = cam.__getattr__('IC_SetFrameReadyCallback')
'''

class API():
    def __init__(self):
        self.fly = flycapture2.Context()
        a = self.fly.get_camera_from_index(0)
        b = self.fly.connect(a[0],a[1],a[2],a[3])

        self.videomodes = {'640x480_8bit': flycapture2.VIDEOMODE_640x480Y8, #5
                           '640x480_16bit': flycapture2.VIDEOMODE_640x480Y16, #6
                           '160x120YUV444': flycapture2.VIDEOMODE_160x120YUV444, #0
                           '800x600Y8': flycapture2.VIDEOMODE_800x600Y8, #9
                           '1024x768Y8': flycapture2.VIDEOMODE_1024x768Y8, #13
                           'format7': flycapture2.VIDEOMODE_FORMAT7}  

        self.framerates = {'7.5': flycapture2.FRAMERATE_7_5, #2
                           '15': flycapture2.FRAMERATE_15, #3
                           '30': flycapture2.FRAMERATE_30, #4
                           '60': flycapture2.FRAMERATE_60, #5
                           '120': flycapture2.FRAMERATE_120, #6
                           '240': flycapture2.FRAMERATE_240} #7

        self.fly.set_video_mode_and_frame_rate(5,5)


        self.use16bit=True

    def setVideoModeAndFrameRate(self, video_mode, frame_rate):
        vMode=5
        fRate=5
        if video_mode == '8bit':
            vMode = 5
        elif video_mode == '16bit':
            vMode = 6
        elif video_mode == 'format7':
            vMode = 23
        if frame_rate == 7.5:
            fRate = 2
        elif frame_rate == 15:
            fRate = 3
        elif frame_rate == 30:
            fRate = 4
        elif frame_rate == 50:
            fRate = 5
        self.fly.set_video_mode_and_frame_rate(vMode,fRate)

    def getImage(self):
        self.fly.start_capture()
        im = self.fly.retrieve_buffer()
        self.fly.stop_capture()
        image = im.__array__()
        if image.shape[-1]==2:
            im2 = image.astype(np.uint16)
            newimage = im2[:,:,1]<<8 + im2[:,:,0]
            return newimage
        elif image.shape[-1]==1:
            return image[:,:,0]

    def getShutterProp(self):
        self.shutterPropDict = self.fly.get_property(flycapture2.SHUTTER)

    def getExposureTime(self):
        self.getShutterProp()
        return self.shutterPropDict['abs_value']

    def setShutterTime(self, time):
        self.getShutterProp()
        self.shutterPropDict['abs_value'] = time
        self.shutterPropDict['abs_control'] = True
        self.shutterPropDict['auto_manual_mode'] = False
        self.fly.set_property(self.shutterPropDict['type'], self.shutterPropDict['present'],
                              self.shutterPropDict['on_off'], self.shutterPropDict['auto_manual_mode'],
                              self.shutterPropDict['abs_control'], self.shutterPropDict['one_push'],
                              self.shutterPropDict['abs_value'], self.shutterPropDict['value_a'],
                              self.shutterPropDict['value_b'])
                              
                                                

    def close(self):
        self.fly.disconnect()

    def shutDown(self):
        self.close()
        
        
        
        
