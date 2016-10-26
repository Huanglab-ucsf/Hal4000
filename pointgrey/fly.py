#!/usr/bin/python
#
# RJM 7/31/2012
#

import time
import numpy 
import scipy
import scipy.optimize
import os
import ctypes
import ctypes.util
import ctypes.wintypes
import cam_wrapper as cw

import sc_library.hdebug as hdebug

Handle = ctypes.wintypes.HANDLE

cam_wrapper = cw.API()

## fitAFunctionLS
#
# Does least squares fitting of a function.
#
# @param data The data to fit.
# @param params The initial values for the fit.
# @param fn The function to fit.
#
def fitAFunctionLS(data, params, fn):
    result = params
    errorfunction = lambda p: numpy.ravel(fn(*p)(*numpy.indices(data.shape)) - data)
    good = True
    [result, cov_x, infodict, mesg, success] = scipy.optimize.leastsq(errorfunction, params, full_output = 1, maxfev = 500)
    if (success < 1) or (success > 4):
        hdebug.logText("Fitting problem: " + mesg)
        #print "Fitting problem:", mesg
        good = False
    return [result, good]

def fitAFunctionLS1D(data, params, fn):
    result = params
    errorfunction = lambda p: numpy.ravel(fn(*p)(*numpy.indices(data.shape)) - data)
    good = True
    [result, cov_x, infodict, mesg, success] = scipy.optimize.leastsq(errorfunction, params, full_output = 1, maxfev = 500)
    if (success < 1) or (success > 4):
        hdebug.logText("Fitting problem: " + mesg)
        #print "Fitting problem:", mesg
        good = False
    return [result, good]


## symmetricGaussian
#
# Returns a function that will return the amplitude of a symmetric 2D-gaussian at a given x, y point.
#
# @param background The gaussian's background.
# @param height The gaussian's height.
# @param center_x The gaussian's center in x.
# @param center_y The gaussian's center in y.
# @param width The gaussian's width.
#
# @return A function.
#
def symmetricGaussian(background, height, center_x, center_y, width):
    return lambda x,y: background + height*numpy.exp(-(((center_x-x)/width)**2 + ((center_y-y)/width)**2) * 2)

def oneDGaussian(background, height, center_x, width):
    #background = params[0]
    #height = params[1]
    #center_x = params[2]
    #width = params[3]
    return lambda x: background + height*numpy.exp(-(((center_x-x)/width)**2  * 2))


## fixedEllipticalGaussian
#
# Returns a function that will return the amplitude of a elliptical gaussian (constrained to be oriented
# along the XY axis) at a given x, y point.
#
# @param background The gaussian's background.
# @param height The gaussian's height.
# @param center_x The gaussian's center in x.
# @param center_y The gaussian's center in y.
# @param width_x The gaussian's width in x.
# @param width_y The gaussian's width in y.
#
# @return A function.
#
def fixedEllipticalGaussian(background, height, center_x, center_y, width_x, width_y):
    return lambda x,y: background + height*numpy.exp(-(((center_x-x)/width_x)**2 + ((center_y-y)/width_y)**2) * 2)

## fitSymmetricGaussian
#
# Fits a symmetric gaussian to the data.
#
# @param data The data to fit.
# @param sigma An initial value for the sigma of the gaussian.
#
# @return [[fit results], good (True/False)]
#
def fitSymmetricGaussian(data, sigma):
    params = [numpy.min(data),
              numpy.max(data),
              0.5 * data.shape[0],
              0.5 * data.shape[1],
              2.0 * sigma]
    return fitAFunctionLS(data, params, symmetricGaussian)

def fit1DGaussian(data, sigma):
    params = [numpy.min(data),
              numpy.max(data),
              0.5*len(data),
              2.0*sigma]
    return fitAFunctionLS1D(data, params, oneDGaussian)


## fitFixedEllipticalGaussian
#
# Fits a fixed-axis elliptical gaussian to the data.
#
# @param data The data to fit.
# @param sigma An initial value for the sigma of the gaussian.
#
# @return [[fit results], good (True/False)]
#
def fitFixedEllipticalGaussian(data, sigma):
    params = [numpy.min(data),
              numpy.max(data),
              0.5 * data.shape[0],
              0.5 * data.shape[1],
              2.0 * sigma,
              2.0 * sigma]
    return fitAFunctionLS(data, params, fixedEllipticalGaussian)



class Camera(Handle):
    def __init__(self,camera_id,ini_file="None"):
        Handle.__init__(self, camera_id)

        '''
        self.exposureTime = settings['exposure_time']*10e-3
        self.xdim = settings['dimensions'][0]
        self.ydim = settings['dimensions'][1]
        self.x0 = settings['roi'][0]
        self.y0 = settings['roi'][1]
        '''
        self.x0=50
        self.y0=50
        self.xdim=400
        self.ydim=400

    def captureImage(self):
        im = cam_wrapper.getImage()
        #print "FLY: captureImage"
        return im[self.x0:self.x0+self.xdim, self.y0:self.y0+self.ydim]

    def capture(self):
        return self.captureImage()

    def getImage(self):
        im = cam_wrapper.getImage()
        image = im[self.x0:self.x0+self.xdim, self.y0:self.y0+self.ydim]
        return [image,0,0,0,0]

    def qpdScan(self, reps=4):
        power_total = 0.0
        offset_total = 0.0
        good_total = 0.0
        '''
        for i in range(reps):
            data = self.singleQpdScan()
            if (data[0] > 0):
                power_total += data[0]
                offset_total += data[1]
                good_total += 1.0
        if (good_total > 0):
            inv_good = 1.0/good_total
            return [power_total * inv_good, offset_total * inv_good, 0]
        else:
            return [0, 0, 0]
        '''
        return [0,0,0]

    def setExposureTime(self, time):
        cam_wrapper.setShutterTime(time)

    def shutDown(self):
        cam_wrapper.shutDown()

class CameraQPD():
    def __init__(self, camera_id = 1, fit_mutex = False):
        self.file_name = "cam_offsets_" + str(camera_id) + ".txt"
        self.fit_mode = 1
        self.fit_mutex = fit_mutex
        self.fit_size = 20 #was 12
        self.image = None
        self.x_off1 = 0.0
        self.y_off1 = 0.0
        self.x_off2 = 0.0
        self.y_off2 = 0.0
        self.zero_dist = 100.0

        # Open camera
        self.cam = Camera(camera_id)

        # Set timeout
        #self.cam.setTimeout(1)

        # Set camera AOI
        if (os.path.exists(self.file_name)):
            fp = open(self.file_name, "r")
            data = fp.readline().split(",")
            self.x_start = int(data[0])
            self.y_start = int(data[1])
            fp.close()
        else:
            self.x_start = 0
            self.y_start = 0

        self.x_width = 400
        self.y_width = 400
        #self.setAOI()

    def capture(self):
        self.image = self.cam.captureImage()
        return self.image

    def captureImage(self):
        im = cam_wrapper.getImage()
        print "FLY: captureImage"
        return im[self.x0:self.x0+self.xdim, self.y0:self.y0+self.ydim]

    def fitGaussian(self, data):
        if (numpy.max(data) < 25):
            return [False, False, False, False]
        x_width = data.shape[0]
        y_width = data.shape[1]
        max_i = data.argmax()
        max_x = int(max_i/y_width)
        max_y = int(max_i%y_width)
        #print "max x and y: %i,%i" % (max_x, max_y)
        if (max_x > (self.fit_size-1)) and (max_x < (x_width - self.fit_size)) and (max_y > (self.fit_size-1)) and (max_y < (y_width - self.fit_size)):
            if self.fit_mutex:
                self.fit_mutex.lock()
            #[params, status] = fitSymmetricGaussian(data[max_x-self.fit_size:max_x+self.fit_size,max_y-self.fit_size:max_y+self.fit_size], 8.0)
            [params, status] = fitFixedEllipticalGaussian(data[max_x-self.fit_size:max_x+self.fit_size,max_y-self.fit_size:max_y+self.fit_size], 8.0)
            #print "Fit with status: ", status
            #print "And params: ", params
            if self.fit_mutex:
                self.fit_mutex.unlock()
            params[2] = params[2] - self.fit_size/2
            params[3] = params[3] - self.fit_size/2
            return [max_x, max_y, params, status]
        else:
            return [False, False, False, False]

    def fitGaussianSumColumns(self, data):
        if (numpy.max(data) < 25):
            return [False, False, False, False]
        x_width = data.shape[0]
        y_width = data.shape[1]
        sumColumns = data.sum(axis=0)
        #if not(os.path.exists("flyData.npy")):
        #    numpy.save("flyData.npy",data)
        max_x = sumColumns.argmax()
        max_i = data.argmax()
        #max_x = int(max_i/y_width)
        max_y = int(max_i%y_width)
        #print "max x and y: %i,%i" % (max_x, max_y)
        if (max_x > (self.fit_size-1)) and (max_x < (x_width - self.fit_size)):
            if self.fit_mutex:
                self.fit_mutex.lock()
            #[params, status] = fitSymmetricGaussian(data[max_x-self.fit_size:max_x+self.fit_size,max_y-self.fit_size:max_y+self.fit_size], 8.0)
            [params, status] = fit1DGaussian(sumColumns[max_x-self.fit_size:max_x+self.fit_size], 8.0)
            #print "Fit with status: ", status
            #print "And params: ", params
            if self.fit_mutex:
                self.fit_mutex.unlock()
            params[2] -= self.fit_size/2
            return [max_x, max_y, params, status]
        else:
            return [False, False, False, False]

    def getImage(self):
        "CameraQPD getImage..."
        #self.image = self.cam.captureImage()
        return [self.image, self.x_off1, self.y_off1, self.x_off2, self.y_off2]

    ## singleQpdScan
    #
    # Perform a single measurement of the focus lock offset and camera sum signal.
    #
    # @return [sum, x-offset, y-offset].
    #
    def singleQpdScan(self):
        data = self.capture().copy()
        power = numpy.max(data)
        total_good=0

        if (power < 25):
            # This hack is because if you bombard the USB camera with 
            # update requests too frequently it will freeze. Or so I
            # believe, not sure if this is actually true.
            #
            # It still seems to freeze?
            time.sleep(0.02)
            return [0, 0, 0]

        if (self.fit_mode==1):
            total_good =0
            self.x_off1 = 0.0
            self.y_off1 = 0.0
            [max_x, max_y, params, status] = self.fitGaussian(data)
            if status:
                total_good += 1
                self.x_off1 = float(max_x) + params[2] 
                self.y_off1 = float(max_y) + params[3] 
                dist1 = abs(self.y_off1)

        elif (self.fit_mode==2):
            #This will sum over columns
            total_good =0
            self.x_off1 = 0.0
            self.y_off1 = 0.0
            [max_x, max_y, params, status] = self.fitGaussianSumColumns(data)
            if status:
                total_good += 1
                self.y_off1 = float(max_x) + params[2]
                self.x_off1 = float(max_y)
                dist1 = abs(self.y_off1)
            

        if total_good==0:
            offset=0
        else:
            offset = self.y_off1
        return [power, offset, 0]

    def qpdScan(self, reps = 4):
        power_total = 0.0
        offset_total = 0.0
        good_total = 0.0
        for i in range(reps):
            data = self.singleQpdScan()
            if (data[0] > 0):
                power_total += data[0]
                offset_total += data[1]
                good_total += 1.0
        if (good_total > 0):
            inv_good = 1.0/good_total
            return [power_total * inv_good, offset_total * inv_good, 0]
        else:
            return [0, 0, 0]

    def adjustCamera(self,dx,dy):
        print "FocusLock camera adjust..."

    def adjustOffset(self, offset):
        print "FocusLock offset adjust..."

    def adjustZeroDist(self, inc):
        print "Adjust zero dist..."

    def adjustAOI(self,dx,dy):
        print "FocusLock camera adjust AOI... Not implemented"

    def changeFitMode(self, mode):
        #self.fit_mode = mode
        if self.fit_mode == 1:
            self.fit_mode = 2
        else:
            self.fit_mode = 1
        print "FocusLock change fit mode to %i" % self.fit_mode

    def returnExposureTime(self):
        etime = cam_wrapper.getExposureTime()
        #print "Fly Camera Exposure time: ", etime
        return etime

    def setExposureTime(self, updown):
        current_exp_time = self.returnExposureTime()
        cam_wrapper.setShutterTime(current_exp_time - (updown*0.5))
        
        
        
    def shutDown(self):
        cam_wrapper.shutDown()
