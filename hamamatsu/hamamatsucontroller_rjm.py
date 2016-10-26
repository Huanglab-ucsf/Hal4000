#!/usr/bin/python


from ctypes import *
from ctypes import wintypes
from ctypes.wintypes import WORD, DWORD, BYTE, LONG, SHORT, DOUBLE
import numpy as np
import sys
import Queue
import threading
import time

#Hamamatsu Constants:
bitsperchannel = 4325680
triggersource = 1048848
triggermode = 1049104
triggeractive = 1048864
triggerpolarity = 1049120
triggerconnector = 1049136
triggertimes = 1049152
triggerdelay = 1049184
exposturetime = 2031888
defectcorrectmode = 4653072
binning = 4198672
subarrayhpos = 4202768
subarrayhsize = 4202784
subarrayvpos = 4202800
subarrayvsize = 4202816
subarraymode = 4202832  #(1==Not used, 2==used)
timingreadouttime = 4206608
timingcyclictriggerperiod = 4206624
timingmintriggerblanking = 4206640
timingmintriggerinterval = 4206672
timingexposure = 4206688
timinginvalidexposureperiod = 4206704
internalframerate = 4208656
internalframeinterval = 4208672
imagewidth = 4325904
imageheight = 4325920
imagerowbytes = 4325936
imageframebytes = 4325952
imagetopoffsetbytes = 4325968
imagepixelformat = 4326000
bufferrowbytes = 4326192
bufferframebytes = 4326208
buffertopoffsetbytes = 4326224
bufferpixeltype = 4326240
numberofoutputtriggerconnector = 1835024
outputtriggerpolarity = 1835296
outputtriggeractive = 1835312
outputtriggerdelay = 1835328
outputtriggerperiod = 1835344
outputtriggerkind = 1835360

cam_status = {4: "Unstable",
              3: "Stable",
              2: "Ready",
              1: "Busy"}

class DCAM_SIZE(Structure):
    _fields_ = [("cx", LONG),
                ("cy", LONG)]

class DCAM_PARAM_PROPERTYATTR(Structure):
    _fields_ = [("cbSize", LONG),        #Size of this structure
               ("iProp", LONG),         # DCAM ID PROPERTY
               ("option", LONG),        # DAM PROP OPTION
               ("iReserved1", LONG),    #must be 0

               ("attribute", LONG),     #DCAMPROPATTRIBUTE
               ("iGroup", LONG),        #0 (DCAMIDGROUP)
               ("iUnit", LONG),         # DCAMPROPUNIT
               ("attribute2", LONG),    #DCAMPROPATTRIBUTE2
               ("valuemin", DOUBLE),    # minimum value
               ("valuemax", DOUBLE),    # maximum value
               ("valuestep", DOUBLE),   # minimum stepping value
               ("valuedefault", DOUBLE),#default
               ("nMaxChannel", LONG),   #max channel if supports
               ("iReserved3", LONG),    #0
               ("nMaxView", LONG),      #max view if supports
               ("iProp_NumberOfElement", LONG),
               ("iProp_ArrayBase", LONG),
               ("iPropStep_Element", LONG)]

hamamatsu = 0
def loadHamamatsuDLL(dcam_path):
    global hamamatsu
    if (hamamatsu==0):
        hamamatsu = windll.LoadLibrary(dcam_path+"dcamapi")

def _getStatus_():
    status = DWORD()
    f_getstatus = hamamatsu.__getattr__('dcam_getstatus')
    err = self.f_getstatus(hamamatsu, byref(status))
    return status.value

#DCAM_PATH = self.dcam_path = "D:\\Programs\\DCAM-SDK (1112)\\bin\\win32\\"

instantiated = 0
class HamamatsuCamera:
    '''
    A ctypes based Python wrapper of the Software Development Kit for Hamamatsu
    ORCA Flash4.0

    '''

    def __init__(self, dcam_path):
        global instantiated
        assert instantiated == 0, "Attempt to instantiate two camera controller instances."

        self.pixels = 0
        self._props_ = {}

        loadHamamatsuDLL(dcam_path)

        self.allocatedBuffers = 20
        
        #self.dcam_path = "D:\\Programs\\DCAM-SDK (1112)\\bin\\win32\\"
        #self.dcam = windll.LoadLibrary(self.dcam_path+"dcamapi")

        res1 = c_void_p(0)
        count = c_int(0)
        f_init = hamamatsu.__getattr__('dcam_init')
        err = f_init(res1, byref(count), wintypes.LPCSTR(0))
        print "Result of initializing Hamamatsu camera: ", err

        self.f_getmodelinfo = hamamatsu.__getattr__('dcam_getmodelinfo')
        self.f_open = hamamatsu.__getattr__('dcam_open')
        self.f_close = hamamatsu.__getattr__('dcam_close')
        self.f_uninit = hamamatsu.__getattr__('dcam_uninit')
        self.f_getstring = hamamatsu.__getattr__('dcam_getstring')
        self.f_getcapability = hamamatsu.__getattr__('dcam_getcapability')
        self.f_getdatatype = hamamatsu.__getattr__('dcam_getdatatype')
        self.f_getbitstype = hamamatsu.__getattr__('dcam_getbitstype')
        self.f_setdatatype = hamamatsu.__getattr__('dcam_setdatatype')
        self.f_setbitstype = hamamatsu.__getattr__('dcam_setbitstype')
        self.f_getdatasize = hamamatsu.__getattr__('dcam_getdatasize')
        self.f_getbitssize = hamamatsu.__getattr__('dcam_getbitssize')
        self.f_queryupdate = hamamatsu.__getattr__('dcam_queryupdate')
        self.f_getbinning = hamamatsu.__getattr__('dcam_getbinning')
        self.f_getexposuretime = hamamatsu.__getattr__('dcam_getexposuretime')
        self.f_gettriggermode = hamamatsu.__getattr__('dcam_gettriggermode')
        self.f_gettriggerpolarity = hamamatsu.__getattr__('dcam_gettriggerpolarity')
        self.f_setbinning = hamamatsu.__getattr__('dcam_setbinning')
        self.f_setexposuretime = hamamatsu.__getattr__('dcam_setexposuretime')
        self.f_settriggermode = hamamatsu.__getattr__('dcam_settriggermode')
        self.f_settriggerpolarity = hamamatsu.__getattr__('dcam_settriggerpolarity')
        self.f_precapture = hamamatsu.__getattr__('dcam_precapture')
        self.f_getdatarange = hamamatsu.__getattr__('dcam_getdatarange')
        self.f_getdataframebytes = hamamatsu.__getattr__('dcam_getdataframebytes')
        self.f_allocframe = hamamatsu.__getattr__('dcam_allocframe')
        self.f_getframecount = hamamatsu.__getattr__('dcam_getframecount')
        self.f_capture = hamamatsu.__getattr__('dcam_capture')
        self.f_firetrigger = hamamatsu.__getattr__('dcam_firetrigger')
        self.f_idle = hamamatsu.__getattr__('dcam_idle')
        self.f_wait = hamamatsu.__getattr__('dcam_wait')
        self.f_getstatus = hamamatsu.__getattr__('dcam_getstatus')
        self.f_gettransferinfo = hamamatsu.__getattr__('dcam_gettransferinfo')
        self.f_freeframe = hamamatsu.__getattr__('dcam_freeframe')
        self.f_attachbuffer = hamamatsu.__getattr__('dcam_attachbuffer')
        self.f_releasebuffer = hamamatsu.__getattr__('dcam_releasebuffer')
        self.f_lockdata = hamamatsu.__getattr__('dcam_lockdata')
        self.f_lockbits = hamamatsu.__getattr__('dcam_lockbits')
        self.f_unlockdata = hamamatsu.__getattr__('dcam_unlockdata')
        self.f_unlockbits = hamamatsu.__getattr__('dcam_unlockbits')
        self.f_setbitsinputlutrange = hamamatsu.__getattr__('dcam_setbitsinputlutrange')
        self.f_setbitsoutputlutrange = hamamatsu.__getattr__('dcam_setbitsoutputlutrange')
        self.f_extended = hamamatsu.__getattr__('dcam_extended')
        self.f_getlasterror = hamamatsu.__getattr__('dcam_getlasterror')
        self.f_getnextpropertyid = hamamatsu.__getattr__('dcam_getnextpropertyid')
        self.f_getpropertyname = hamamatsu.__getattr__('dcam_getpropertyname')
        self.f_getpropertyvalue = hamamatsu.__getattr__('dcam_getpropertyvalue')
        self.f_setpropertyvalue = hamamatsu.__getattr__('dcam_setpropertyvalue')
        
        
        err = self.openCamera()
        print "Result of opening Hamamatsu camera: ", err

        xsize,ysize = self.getDataSize()
        self._props_['XPixels'] = xsize
        self._props_['YPixels'] = ysize
        self._props_['Camera'] = self.getString(0x04000104)
        self._props_['Version'] = self.getString(0x04000105)
        self._props_['API_Version'] = self.getString(0x04000108)
        

        #self.debugCheck()

        err = self.preCapture(1)
        print "PreCapture result: ", err
        status = self.getStatus()
        print "Status after precapture: ", status
        

    def openCamera(self):
        self.hcam = wintypes.HANDLE()
        res = wintypes.LPCSTR(0)
        return self.f_open(byref(self.hcam), c_int(0), res)

    def closeCamera(self):
        return self.f_close(self.hcam)

    def debugCheck(self):
        status = self.getStatus()
        print "Status: ", status

        print "self._props_: ", self.getProperties()

        

        self.setROIAndBinning([768,768+511,768,768+511],1)
        time.sleep(0.05)

        

        xsize,ysize = self.getDataSize()
        print "Data size: (%i,%i)" % (xsize,ysize)

        
        err = self.preCapture(1)
        print "PreCapture result: ", err
        status = self.getStatus()
        print "Status after precapture: ", status
        err = self.allocFrame(10)
        print "AllocFrame result: ", err
        status = self.getStatus()
        print "Status after allocFrame: ", status
        err = self.capture()
        print "Capture result: ", err
        status = self.getStatus()
        print "Status after capture: ", status

    def getProperties(self):
        return self._props_
        

    def getString(self, ID):
        '''
        Model (product name): 0x04000104
        CameraID: 0x04000102
        Camera Version: 0x04000105
        Driver Version: 0x04000106
        Module Version: 0x04000107
        DCAM-API Version: 0x04000108
        '''
        size_string_buffer = 64
        modelinfo = create_string_buffer(size_string_buffer)
        err = self.f_getstring(self.hcam, c_int(ID),
                               byref(modelinfo), DWORD(size_string_buffer))
        return modelinfo.value

    def setROIAndBinning(self, ROI, binning):
        if (ROI[0] > ROI[1]):
            raise AssertionError, "Invalid x range."
        if (ROI[2] > ROI[3]):
            raise AssertionError, "Invalid y range."
        self.setPropertyValue(4202832,2) #Allows use of ROI
        time.sleep(0.05)
        self.setPropertyValue(4202768, ROI[0]) #Sets x0
        time.sleep(0.05)
        self.setPropertyValue(4202800, ROI[2]) #Sets y0
        time.sleep(0.05)
        self.setPropertyValue(4202784, ROI[1]-ROI[0]+1) #Sets xsize
        time.sleep(0.05)
        self.setPropertyValue(4202816, ROI[3]-ROI[2]+1) #Sets ysize
        time.sleep(0.05)
        x0 = self.getPropertyValue(4202768)
        y0 = self.getPropertyValue(4202800)
        xsize,ysize = self.getDataSize()
        self.ROI = [x0+1,x0+xsize,y0+1,y0+ysize]
        self.pixels = xsize*ysize
        print "Asked for xsize: ", ROI[1]-ROI[0]+1
        print "Resulting xsize: ", xsize
        

    def uninit(self):
        res1 = c_void_p()
        res2 = c_char()
        return self.f_uninit(res1, byref(res2))

    def getDataType(self):
        dataType = c_int()
        err = self.f_getdatatype(self.hcam, byref(dataType))
        return dataType.value

    def getDataSize(self):
        size = DCAM_SIZE()
        err = self.f_getdatasize(self.hcam, byref(size))
        return size.cx, size.cy

    def getStatus(self):
        #0=Error; 1=Busy; 2=Ready; 3=Stable; 4=Unstable
        status = DWORD()
        err = self.f_getstatus(self.hcam, byref(status))
        return status.value

    def getTriggerMode(self):
        pMode = c_int()
        err = self.f_gettriggermode(self.hcam, byref(pMode))
        return pMode.value

    def setTriggerMode(self, value):
        pMode = c_int(value)
        err = self.f_settriggermode(self.hcam, pMode)
        return err

    def getInternalFrameRate(self):
        return self.getPropertyValue(4208656)

    def getExposureTime(self):
        expTime = c_double()
        err = self.f_getexposuretime(self.hcam, byref(expTime))
        return expTime.value

    def setExposureTime(self, expTime):
        return self.f_setexposuretime(self.hcam, DOUBLE(expTime))
        

    def getTransferInfo(self):
        pNewestFrame = c_int()
        pFrameCount = c_int()
        err = self.f_gettransferinfo(self.hcam, byref(pNewestFrame),
                                     byref(pFrameCount))
        return pNewestFrame.value, pFrameCount.value

    def preCapture(self, capturemode):
        #0: Snap; 1: Sequence
        return self.f_precapture(self.hcam, c_int(capturemode))

    def allocFrame(self, framecount):
        return self.f_allocframe(self.hcam, c_int(framecount))

    def getFrameCount(self):
        count = c_int()
        err = self.f_getframecount(self.hcam, byref(count))
        return count.value

    def capture(self):
        return self.f_capture(self.hcam)

    def freeFrame(self):
        return self.f_freeframe(self.hcam)

    def getDataFrameBytes(self):
        size = DWORD()
        err = self.f_getdataframebytes(self.hcam, byref(size))
        return size.value

    def lockData(self, frame, size, raw=False):
        #Use frame=-1 for last captured frame
        image_temp = np.zeros((size), dtype=np.uint16)
        strBuffer = create_string_buffer(size*2)
        pTop = c_void_p()
        pRowbytes = c_int()
        err = self.f_lockdata(self.hcam, byref(pTop), byref(pRowbytes), c_int(frame))
        if err!=0:
            #memmove(image_temp.ctypes.data, pTop, size*2)
            memmove(strBuffer, pTop, size*2)
            if raw:
                return [strBuffer]
            else:
                image = np.frombuffer(image_temp, dtype=np.uint16)
                return image
        else:
            print "Error in lockData: ", err
            return None

    def lockBits(self, frame, size, raw=False):
        image_temp = np.zeros((size), dtype=np.uint8)
        pTop = c_void_p()
        pRowbytes = c_int()
        err = self.f_lockbits(self.hcam, byref(pTop), byref(pRowbytes), c_int(frame))
        memmove(image_temp.ctypes.data, pTop, size)
        if raw:
            return image_temp.ctypes.data
        else:
            image = np.frombuffer(image_temp, dtype=np.uint8)
            return image

    def unlockData(self):
        return self.f_unlockdata(self.hcam)

    def unlockBits(self):
        return self.f_unlockbits(self.hcam)

    def attachBuffer(self, frameSize, numFrames):
        one_frame = np.zeros((frameSize),dtype=np.uint16)
        frames = np.zeros((frameSize*numFrames), dtype=np.uint16)
        dSize = DWORD(frameSize*numFrames*2)
        err = self.f_attachbuffer(self.hcam,
                                  addressof(c_void_p(frames.ctypes.data)),
                                  dSize)
        return (err, frames)

    def attachBuffer2(self, frameSize, numFrames):
        frames = create_string_buffer(frameSize*numFrames*2)
        dSize = DWORD(4*numFrames)
        err = self.f_attachbuffer(self.hcam, byref(frames), dSize)
        return (err, frames)

    def attachBuffer3(self, frameSize, numFrames):
        oneframe = (c_uint16*frameSize)
        frames = oneframe(numFrames)
        #frames = c_void_p(frameSize*numFrames*2)
        dSize = DWORD(numFrames*4)
        err = self.f_attachbuffer(self.hcam, byref(frames), dSize)
        return (err, frames)

    def attachBuffer4(self, frameSize, numFrames):
        self.image_temp = np.zeros((numFrames*frameSize), dtype=np.uint16)
        pTop = c_void_p()
        dSize = DWORD(numFrames*4)
        #memset(byref(pTop), 0, 2*frameSize*numFrames)
        err = self.f_attachbuffer(self.hcam, byref(self.image_temp.ctypes.data_as(c_void_p)), dSize)
        #memmove(image_temp.ctypes.data, pTop, frameSize*numFrames*2)
        return (err,self.image_temp.reshape(numFrames,frameSize))

    def attachBuffer5(self, frameSize, numFrames):
        image_temp = np.zeros((frameSize*numFrames), dtype=np.uint16)
        pTop = (c_void_p * numFrames)()
        memset(byref(pTop), 0, 2*frameSize*numFrames)
        dSize = DWORD(frameSize*numFrames*2)
        err = self.f_attachbuffer(self.hcam, byref(pTop), dSize)
        memmove(image_temp.ctypes.data, pTop, frameSize*numFrames*2)
        return (err, image_temp)
                                  

    def releaseBuffer(self):
        return self.f_releasebuffer(self.hcam)
        
    def idle(self):
        return self.f_idle(self.hcam)

    def wait(self, waitCode, waitTime):
        '''
        waitCode:
        1 = frame start
        2 = frame end
        4 = cycle end
        8 = exposure end
        16 = capture end
        '''
        pCode = DWORD(waitCode)
        dwTime = DWORD(waitTime)
        hdCamSig = wintypes.HANDLE(0)
        return self.f_wait(self.hcam, byref(pCode), dwTime, hdCamSig)

    def getLastError(self):
        size_string_buffer = 64
        errBuff = create_string_buffer(size_string_buffer)
        err = self.f_getlasterror(self.hcam,
                                  byref(errBuff),
                                  DWORD(size_string_buffer))
        return errBuff.value

    def getNextPropertyID(self, iPropNum):
        iProp = c_int(iPropNum)
        err = self.f_getnextpropertyid(self.hcam, byref(iProp), c_int(0))
        return iProp.value

    def getPropertyName(self, iProp):
        size_string_buffer = 64
        propname = create_string_buffer(size_string_buffer)
        err = self.f_getpropertyname(self.hcam, c_int(iProp),
                                     byref(propname), c_int(size_string_buffer))
        return propname.value

    def getPropertyValue(self, iProp):
        pValue = DOUBLE()
        err = self.f_getpropertyvalue(self.hcam, c_int(iProp),
                                      byref(pValue))
        return pValue.value

    def setPropertyValue(self, iProp, value):
        return self.f_setpropertyvalue(self.hcam, c_int(iProp), DOUBLE(value))
        
    def setACQMode(self, mode, number_frames = "undef"):
        print "Set to mode: ", mode
        if mode == "single_frame":
            self.preCaptMode = 0
        else:
            self.preCaptMode = 1
        self.acqmode = mode

    def setFrameTransferMode(self, mode):
        print "Set frame transfer mode: ", mode

    def getAcquisitionTimings(self):
        exposure_time = self.getExposureTime()
        readoutTime = self.getPropertyValue(timingreadouttime)
        intFrameRate = self.getPropertyValue(internalframerate)
        print "Exposure time: ", exposure_time
        print "Timing readout time: ", readoutTime
        print "Internal frame rate: ", intFrameRate
        return [exposure_time,1.0,1.0]

    def getTemperature(self):
        return [-50, "stable"]

    def startAcquisition(self):
        print "Starting acquisition..."
        self.allocFrame(self.allocatedBuffers)
        self.capture()

    def stopAcquisition(self):
        print "Stopping acquisistion..."
        self.idle()
        self.freeFrame()

    def shutdown(self):
        self.closeCamera()
        

    


if __name__ == '__main__':
    cam_api = HamamatsuCamera("D:\\Programs\\DCAM-SDK (1112)\\bin\\win32\\")
    #cam_api.openCamera()
    print "Camera: ", cam_api.getString(0x04000104)
    print "Version: ", cam_api.getString(0x04000105)
    print "DCAM-API Version: ", cam_api.getString(0x04000108)
    cam_api.setPropertyValue(4202768, 768)
    cam_api.setPropertyValue(4202784, 256)
    cam_api.setPropertyValue(4202800, 768)
    cam_api.setPropertyValue(4202816, 256)
    cam_api.setPropertyValue(4202832, 2)
    cam_api.setExposureTime(0.0005)
    data_type = cam_api.getDataType()
    xsize,ysize = cam_api.getDataSize()
    print "DataType: ", data_type
    print "x,y size: ", xsize, ysize
    print "Trigger mode: ", cam_api.getTriggerMode()
    print "Exposure time: ", cam_api.getExposureTime()
    cam_api.preCapture(1)
    numFrames = 20
    cam_api.allocFrame(numFrames)
    cam_api.allocFrame(numFrames)
    ims = np.zeros((numFrames,xsize*ysize),dtype=np.uint16)
    print "Frame count for allocFrame: ", cam_api.getFrameCount()
    bytesize = cam_api.getDataFrameBytes()
    print "ByteSize: ", bytesize
    cam_api.capture()
    t1 = time.clock()
    print "Transfer info: ", cam_api.getTransferInfo()
    cam_api.wait(4, 0x80000000)
    print "Transfer info: ", cam_api.getTransferInfo()
    t2 = time.clock()
    for i in range(0, numFrames):
        ims[i] = cam_api.lockData(i, xsize*ysize, raw=True)
    cam_api.unlockData()
    np.save("ims_test.npy", ims)
    print "Transfer info: ", cam_api.getTransferInfo()
    t3 = time.clock()
    cam_api.freeFrame()
    #cam_api.preCapture(0)
    
    '''
    err, im2 = cam_api.attachBuffer4(xsize*ysize,8)
    print "AttachBuffer error: ", cam_api.getLastError()
    print "Frame count for attachFrame: ", cam_api.getFrameCount()
    stat = cam_api.getStatus()
    print "Status: ", stat
    
    cam_api.capture()
    stat = cam_api.getStatus()
    print "Status: ", stat
    cam_api.wait(4, 0x80000000)

    time.sleep(1)

    
    #cam_api.wait(16, 0x80000000)
    '''
    #cam_api.wait(16, 0x80000000)
    #time.sleep(2.0)
    #print "Frame count for attachFrame: ", cam_api.getFrameCount()
    #stat = cam_api.getStatus()
    #print "Status: ", stat
    #errRelease = cam_api.releaseBuffer()
    #print "ReleaseBuffer error: ", cam_api.getLastError()
    print "Frame count for attachFrame: ", cam_api.getFrameCount()
    print "Transfer info: ", cam_api.getTransferInfo()
    
    cam_api.idle()

    #errRelease = cam_api.releaseBuffer()
    #print "ReleaseBuffer error: ", cam_api.getLastError()
    
    propID = 0
    for i in range(0,50):
        propID = cam_api.getNextPropertyID(propID)
        propName = cam_api.getPropertyName(propID)
        propVal = cam_api.getPropertyValue(propID)
        print "ID: ", propID
        print "Name: ", propName
        print "Value: ", propVal
    
    #cam_api.freeFrame()
    cam_api.closeCamera()
    cam_api.uninit()
