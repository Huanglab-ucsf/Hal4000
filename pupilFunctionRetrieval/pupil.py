#!/usr/bin/python

import numpy as _np
from numpy.lib.scimath import sqrt as _msqrt
from scipy import fftpack as _fftpack
from scipy import ndimage
import tempfile as _tempfile
#import zernike as _zernike
import halLib.imagewriters as imagewriters

def downSampleImage(image, newpixel,gaussfilt=False, filtSize=0):
    xshape,yshape = image.shape
    newxshape = xshape/newpixel
    newyshape = yshape/newpixel
    newimage = _np.zeros((newxshape,newyshape))
    ii = -1
    jj = -1
    if gaussfilt:
        if filtSize==0:
            filtSize = newpixel/2
        image = ndimage.gaussian_filter(image,filtSize)
    for i in range(0,xshape,newpixel):
        ii=ii+1
        for j in range(0,yshape,newpixel):
            jj=jj+1
            newimage[ii,jj] = image[i:i+newpixel,j:j+newpixel].mean()
        jj=-1
    return newimage


class _Pupil(object):

    def __init__(self, l, ni, ns, NA, f):

        self.l = float(l)
        self.ni = float(ni)
        self.ns = float(ns)
        self.NA = float(NA)
        self.f = float(f)
        self.s_max = f*NA
        self.k_max = NA/l


    def _unit_disk_to_spatial_radial_coordinate(self, unit_disk):

        return self.s_max * unit_disk


    def _unit_disk_to_optical_angles(self, unit_disk):

        beta = _np.arcsin(self.NA*unit_disk/self.ni)
        alpha = _np.arcsin(self.NA*unit_disk/self.ns)
        m = 1.0/_np.tan(beta)
        return alpha, beta, m


    def get_pupil_function(self, z, n_photons=3000, dcf=0):

        '''
        Computes the complex pupil function of single point source.

        Parameters
        ----------
        z: float
            Axial coordinate of the point source in um, where the origin of the
            coordinate system is at focus. Positive values are towards the
            objective.
	n_photons: int
	    The number of collected photons in the pupil plane.
	dcf: float
            Distance between focal plane and sample-side coverslip surfance in um.
            

        Returns
        -------
        PF: 2D array or list of 2D arrays
            If parameter *z* was a single number, a 2D array of the complex
            pupil function is returned. If *z* was an iterable of floats, a list
            of 2D pupil functions is returned.
        '''

        z = float(z)
        n_photons = float(n_photons)
        dcf = float(dcf)
        f = self.f
        m = self.m
        l = self.l
        ni = self.ni
        ns = self.ns
        alpha = self.alpha
        beta = self.beta
        m = self.m

        def compute_pupil_function(z):
            if dcf - z == 0:
                # The emitter is on the coverslip
                g0 = dcf
                PQ = 0
                QR = (_np.sqrt((1+m**2)*f**2-dcf**2)-m*dcf) / ((1+m**2)*_np.sin(beta))
            else:
                g0 = m*(z-dcf)*_np.tan(alpha) + dcf
                PQ = (dcf-z)/_np.cos(alpha)
                QR = (_np.sqrt((1+m**2)*f**2-g0**2)-m*g0) / ((1+m**2)*_np.sin(beta)) \
                        + (z-dcf)*_np.tan(alpha)/_np.sin(beta)
            Phi = 2*_np.pi*(ns*PQ + ni*QR)/l
            PF = _np.sqrt(n_photons/self.pupil_npxl)*_np.exp(1j*Phi)
            PF = _np.nan_to_num(PF)
	    return self.apply_NA_restriction(PF)

        if _np.ndim(z) == 0 or _np.ndim(z) == 2:
            return compute_pupil_function(z)

        elif _np.ndim(z) == 1:
            return _np.array([compute_pupil_function(_) for _ in z])


    def get_sli_pupil_function(self, z0, n_photons=6000, dcf=0, dmf=0, tilt=(0,0)):
        
        '''
        Computes the pupil function of a point source in front of a mirror.

        Parameters
        ----------
        z0: float or list/tuple of floats or array or list/tuple of arrays
            Distance between molecule and mirror.
	n_photons: int
	    The number of collected photons in the pupil plane.
	dcf: float
            Distance between focal plane and sample-side coverslip surfance in um.
        dmf: float
            Distance between focal plane and mirror surface.
            Positive direction is towards the objective.
        tilt: tuple of floats
            Coefficients of the Zernike modes (1,-1) and (1,1) to be added to
            the pupil function of the mirror image. This simulates the effect of
            a tilted mirror.

        Returns
        -------
        PF: 2D array or list of 2D arrays
            The 2D complex pupil function or a list of 2D complex pupil
            functions if z0 was an iterable.
        '''

        z0 = float(z0)
        n_photons = float(n_photons)
        dmf = float(dmf)
        tv, th = tilt
        tv = float(tv)
        th = float(th)
        
        if tv != 0:
            vertical_tilt = tv*_zernike.zernike((1,-1), self.r, self.theta)
        if th != 0:
            horizontal_tilt = th*_zernike.zernike((1,1), self.r, self.theta)

        def compute_sli_pupil_function(z1, z2):
            pf1 = self.get_pupil_function(z1, 0.5*n_photons, dcf)
            pf2 = self.get_pupil_function(z2, 0.5*n_photons, dcf)
            if tv != 0:
                pf2 *= _np.exp(1j*vertical_tilt)
            if th != 0:
                pf2 *= _np.exp(1j*horizontal_tilt)
            return pf1 - pf2
       
        if type(z0) in (list,tuple):
            z0 = _np.array(z0)

        z1 = z0 - dmf
        z2 = -(z0 + dmf)

        if _np.ndim(z0) in (0,2):
            return compute_sli_pupil_function(z1,z2)
        
        elif _np.ndim(z0) == 1:
            return _np.array([compute_sli_pupil_function(*_) for _ in zip(z1,z2)])

        
    def apply_NA_restriction(self, PF):

        '''
        Sets all values of a given pupil function to zero that are out of NA range.
        '''

	PF[self.r>1] = 0
	return PF

    
    def compute_Fisher_Information(self, PSF, poisson_noise, voxel_size,
            mask=None):

        '''
        Computes the Fisher information matrix as described in Ober et al.,
        Biophysical Journal, 2004, taking into account Poisson background noise.

        Parameters
        ----------
        PSF: array
            The 3D Point Spread Function, where the intensity values are the
	    number of photons.
        poisson_noise: float
            The poisson background noise per pixel in photons
        voxel_size: float
            The side length of the PSF voxel in micrometer.
        mask: 2D boolean numpy.array
            Optional: A two dimensional array of the same shape as one PSF
            slice. If mask is set, the Fisher Information is only calculated for
            regions where mask is True.
        '''

        poisson_noise = float(poisson_noise)

        dPSF = _np.gradient(PSF, voxel_size[0], voxel_size[1], voxel_size[2])
	if mask is not None:
	    dPSF = [_*mask for _ in dPSF]
        noisy = PSF + poisson_noise

        FI = [[0,0,0] for _ in xrange(3)]
        for i in xrange(3):
            for j in xrange(3):
                FI[i][j] = _np.sum(dPSF[i]*dPSF[j]/noisy,-1).sum(-1)

        return FI


    def compute_CRLB(self, PSF, poisson_noise, voxel_size, mask=None):

        '''
        Computes the CRLB as described in Ober et al.,
        Biophysical Journal, 2004, taking into account Poisson background noise.

        Parameters
        ----------
        PSF: array
            The 3D Point Spread Function, where the intensity values are the
	    number of photons.
        poisson_noise: float
            The poisson background noise per pixel in photons
        voxel_size: float
            The side length of the PSF voxel in micrometer.
        mask: 2D boolean numpy.array
            Optional: A two dimensional array of the same shape as one PSF
            slice. If mask is set, the CRLB is only calculated for
            regions where mask is True.
        '''

        FI = self.compute_Fisher_Information(PSF, poisson_noise, voxel_size,
                mask)
        return [_np.sqrt(1.0/FI[_][_]) for _ in xrange(3)]



class Geometry:

    '''
    A base class for pupil.Experiment which provides basic
    geometrical data of a microscope experiment.

    Parameters
    ----------
    size: tuple
        The pixel size of a device in the pupil plane of the
        microscope.
    cx: float
        The x coordinate of the pupil function center on the
        pupil plane device in pixels.
    cy: float
        The y coordinate (see cx).
    d: float
        The diameter of the pupil function on the pupil device
        in pixels.
    '''
    

    def __init__(self, size, cx, cy, d):

        self.cx = float(cx)
        self.cy = float(cy)
        self.d = float(d)
        self.size = size
        self.nx, self.ny = size
        self.x_pxl, self.y_pxl = _np.meshgrid(_np.arange(self.nx),_np.arange(self.ny))
        self.x_pxl -= cx
        self.y_pxl -= cy
        self.r_pxl = _msqrt(self.x_pxl**2+self.y_pxl**2)
        self.r = 2.0*self.r_pxl/d
        self.theta = _np.arctan2(self.y_pxl, self.x_pxl)
        self.x = 2.0*self.x_pxl/d
        self.y = 2.0*self.y_pxl/d

    

class Experiment(_Pupil):

    '''
    Provides computations for a microscope experiment base on
    Fourier optics.

    Parameters
    ----------

    geometry: pupil.Geometry
        A base object that provides basic geometric data of the
        microscope experiment.
    l: float
        The light wavelength in micrometer.
    ni: float
        The refractive index of the immersion medium.
    ns: float
        The refractive index of the sample medium.
    NA: float
        The numerical aperture of the microscope objective.
    f: float
        The objective focal length in micrometer.
    '''
    
    def __init__(self, geometry, l, n, NA, f):

        l = float(l)
        ni = float(ni)
        ns = float(ns)
        NA = float(NA)
        f = float(f)
        self.geometry = geometry
        self.nx = geometry.nx
        self.ny = geometry.ny
        self.theta = geometry.theta
        _Pupil.__init__(self, l, ni, ns, NA, f)

        self.s = self._unit_disk_to_spatial_radial_coordinate(geometry.r)
        self.alpha, self.beta, self.m = self._unit_disk_to_optical_angles(geometry.r)
        self.r = geometry.r
        self.size = geometry.size
        self.pupil_npxl = _np.sum(self.r<=1)


class Simulation(_Pupil):

    '''
    Simulates the behaviour of a microscope based on Fourier optics.

    Parameters
    ----------
    nx: int
        The side length of the pupil function or microscope image in pixels.
    dx: float
        The pixel size in the image plane.
    l: float
        Light wavelength in micrometer.
    ni: float
        The refractive index of the immersion medium.
    ns: float
        The refractive index of the sample medium
    NA: float
        The numerical aperture of the microscope objective.
    f: float
        The objective focal length in micrometers.
    ''' 

    def __init__(self, nx=256, dx=0.1, l=0.68, ni=1.33, ns=1.33, NA=1.27, f=3333.33, wavelengths=40):

        dx = float(dx)
        self.dx = dx
        l = float(l)
        ni = float(ni)
        ns = float(ns)
        NA = float(NA)
        f = float(f)
        self.nx = nx
        self.ny = nx

        self.numWavelengths = wavelengths

        self.tiltAv = False
        self.shift = 0.2
        
        _Pupil.__init__(self, l, ni, ns, NA, f)

        # Frequency sampling:
        dk = 1/(nx*dx)
        # Pupil function pixel grid:
        x,y = _np.mgrid[-nx/2.:nx/2.,-nx/2.:nx/2.]+0.5
	self.x_pxl = x
	self.y_pxl = y
	self.r_pxl = _np.sqrt(x**2+y**2)

        # Pupil function frequency space:
        kx = dk*x
        ky = dk*y
        self.k = _np.sqrt(kx**2+ky**2)
        
        # Axial Fourier space coordinate:
        self.kz = _msqrt((ni/l)**2-self.k**2)
        self.kzs = _np.zeros((self.numWavelengths,self.kz.shape[0],self.kz.shape[1]),dtype=self.kz.dtype)
        ls = _np.linspace(l-0.035,l+0.035,self.kzs.shape[0])
        for i in range(0,self.kzs.shape[0]):
            self.kzs[i] = _msqrt((ni/ls[i])**2-self.k**2)
    
        
        # Scaled pupil function radial coordinate:
        self.r = self.k/self.k_max

        self.s = self._unit_disk_to_spatial_radial_coordinate(self.r)
        self.alpha, self.beta, self.m = self._unit_disk_to_optical_angles(self.r)

        # The number of pixels in the pupil plane:
	self.pupil_npxl = _np.sum(self.r<=1)
	
        # A plane wave with 3000 collected photons
        phase = _np.zeros((nx,nx))
        n_photons = 3000.0
        self.plane = _np.sqrt(n_photons/self.pupil_npxl)*_np.exp(1j*phase)
	self.plane = self.apply_NA_restriction(self.plane)

        self.kx = kx
        self.theta = _np.arctan2(y,x)

    def amplitudeAdjust(self, dcf):

        sinTheta1 = (self.l/self.ni)*self.k
        sinTheta2 = (self.ni/self.ns)*sinTheta1
        theta1 = _np.arcsin(sinTheta1)
        theta2 = _np.arcsin(sinTheta2)
        amp_trans = (sinTheta1 * _np.cos(theta2) / _np.sin(theta1+theta2))*(1 + (1.0/_np.cos(theta2-theta1)))
        amp_comp = (self.ni*_np.tan(theta2))/(self.ns*_np.tan(theta1))

        newPhase = _np.pi*2.0*dcf*(self.ns*_np.cos(theta2) - self.ni*_np.cos(theta1))*(1./self.l)
        
        return amp_trans*amp_comp, newPhase


    def pf2psf(self, PF, zs, intensity=True, verbose=False, downSampleFactor=1, scalingFactor=None):
        
        """
        Computes the point spread function for a given pupil function.

        Parameters
        ----------
        PF: array
            The complex pupil function.
        zs: number or iterable
            The axial position or a list of axial positions which should be
            computed. Focus is at z=0.
        intensity: bool
            Specifies if the intensity or the complex field should be returned.

        Returns
        -------
        PSF: array or memmap
            The complex PSF. If the memory is to small, a memmap will be
            returned instead of an array.
        """

        if downSampleFactor==1:
            downSample=False
        else:
            downSample=True

        nx = self.nx
        
        if _np.isscalar(zs):
            zs = [zs]
        nz = len(zs)
        kz = self.kz

	# The normalization for ifft2:
	N = _np.sqrt(nx*self.ny)

        # Preallocating memory for PSF:
        try:
            if intensity:
                PSF = _np.zeros((nz,nx,nx))
            else:
                PSF = _np.zeros((nz,nx,nx))+1j*_np.zeros((nz,nx,nx))
        except MemoryError:
            print 'Not enough memory for PSF, \
                    using memory map in a temporary file.'
            temp_file = _tempfile.TemporaryFile()
            if intensity:
                temp_type = float
            else:
                temp_type = complex
            PSF = _np.memmap(temp_file, dtype=temp_type, mode='w+',
                shape=(nz,nx,nx))

        for i in xrange(nz):
            if verbose: print 'Calculating PSF slice for z={0}um.'.format(zs[i])
            U = N*_fftpack.ifft2(_np.exp(2*_np.pi*1j*kz*zs[i])*PF)
            for j in range(0,self.kzs.shape[0]):
                U = U + N*_fftpack.ifft2(_np.exp(2*_np.pi*1j*self.kzs[j]*zs[i])*PF)
            U = U/(1+self.kzs.shape[0])
            _slice_ = _fftpack.ifftshift(U)
            #_slice_ = U
            if intensity:
                #_slice_ = _np.abs(_slice_)**2
                _slice_ = _np.abs(_slice_ * _np.conj(_slice_))
            if self.tiltAv:
                #print "doing shift..."
                shiftx = [0,0,-1,1,1,-1,1,-1]
                shifty = [-1,1,0,0,1,1,-1,-1]
                for u in range(len(shiftx)):
                    pf_new = PF*_np.exp(1j*shiftx[u]*self.shift * _zernike.zernike((1,1),self.r,self.theta)) * _np.exp(1j * shifty[u]*self.shift * _zernike.zernike((1,-1),self.r,self.theta))
                    U = N*_fftpack.ifft2(_np.exp(2*_np.pi*1j*kz*zs[i])*pf_new)
                    for j in range(0,self.kzs.shape[0]):
                        U = U + N*_fftpack.ifft2(_np.exp(2*_np.pi*1j*self.kzs[j]*zs[i])*pf_new)
                    U = U/(1+self.kzs.shape[0])    
                    _slice2_ = _fftpack.ifftshift(U)
                    if intensity:
                        _slice2_ = _np.abs(_slice2_ * _np.conj(_slice2_))
                    _slice_ = _slice_ + _slice2_
                _slice_ = _slice_ / (len(shiftx)+1)
            if intensity:
                if scalingFactor is not None:
                    fftPSF = _np.fft.fftshift(_np.fft.fft2(_slice_))
                    fftPSFScaled = fftPSF*scalingFactor
                    _slice_ = abs(_np.fft.ifft2(fftPSFScaled))
            PSF[i] = _slice_

        if nz == 1:
            PSF = PSF[0]
        
        return PSF

    def pf2psf2DAX(self, PF, zs, daxFilename, intensity=True, verbose=False,
                   avg_background=1, read_noise_scale = 0.5,
                   baseline=100, maxVal=0,
                   downSampleFactor=1, gaussFilt=True,
                   vary_param=None, dcf=0,
                   filtSize=0,
                   scalingFactor=None):
        
        """
        Computes the point spread function for a given pupil function.

        Parameters
        ----------
        PF: array
            The complex pupil function.
        zs: number or iterable
            The axial position or a list of axial positions which should be
            computed. Focus is at z=0.
        daxFileName: string
                     Filename of DAX file to create
        intensity: bool
            Specifies if the intensity or the complex field should be returned.

        """
        if downSampleFactor==1:
            downSample=False
        else:
            downSample=True
        PSF = self.pf2psf(PF, zs, intensity=True, verbose=False)
        if maxVal>0:
            PSF = PSF * (maxVal/PSF.max())
        daxParams = {"exposure_time": 0,
                     "dimensions": [PSF.shape[1], PSF.shape[2]],
                     "x_start": 0,
                     "y_start": 0,
                     "NA": self.NA,
                     "ns": self.ns,
                     "ni": self.ni,
                     "wavelength": self.l,
                     "avg_background": avg_background,
                     "maxVal": maxVal}
        if vary_param is not None:
            daxParams["vary_param"] = vary_param
        if vary_param == "ns":
            daxParams["vary_param_value"] = self.ns
        elif vary_param == "ni":
            daxParams["vary_param_value"] = self.ni
        elif vary_param == "wavelength":
            daxParams["vary_param_value"] = self.l
        elif vary_param == "dcf":
            daxParams["vary_param_value"] = dcf
        elif vary_param == "maxVal":
            daxParams["maxVal"] = maxVal
        if downSample:
            daxParams["dimensions"] = [PSF.shape[1]/downSampleFactor,
                                       PSF.shape[2]/downSampleFactor]
        newDaxFile = imagewriters.DaxFile(daxFilename, daxParams)
        for i in range(0,PSF.shape[0]):
            if downSample:
                frame = downSampleImage(PSF[i],downSampleFactor,gaussfilt=gaussFilt,filtSize=filtSize)
            else:
                if scalingFactor is not None:
                    fftPSF = _np.fft.fftshift(_np.fft.fft2(PSF[i]))
                    fftPSFScaled = fftPSF*scalingFactor
                    frame = abs(_np.fft.ifft2(fftPSFScaled))
                else:
                    frame = PSF[i]
            frame = frame + _np.ones(frame.shape)*avg_background
            if i==0:
                read_noise = _np.random.normal(scale=read_noise_scale,
                                              size=frame.shape)
            frame = _np.random.poisson(frame) + read_noise + baseline
            newDaxFile.saveFrames(frame.astype(_np.dtype('>H')).tostring(),1)
        newDaxFile.closeFile([0,0,0],0)
        return PSF


    def pf2psf_old(self, PF, zs, intensity=True, verbose=False):
        
        """
        Computes the point spread function for a given pupil function.

        Parameters
        ----------
        PF: array
            The complex pupil function.
        zs: number or iterable
            The axial position or a list of axial positions which should be
            computed. Focus is at z=0.
        intensity: bool
            Specifies if the intensity or the complex field should be returned.

        Returns
        -------
        PSF: array or memmap
            The complex PSF. If the memory is to small, a memmap will be
            returned instead of an array.
        """

        nx = self.nx
        
        if _np.isscalar(zs):
            zs = [zs]
        nz = len(zs)
        kz = self.kz

	# The normalization for ifft2:
	N = _np.sqrt(nx*self.ny)

        # Preallocating memory for PSF:
        try:
            if intensity:
                PSF = _np.zeros((nz,nx,nx))
            else:
                PSF = _np.zeros((nz,nx,nx))+1j*_np.zeros((nz,nx,nx))
        except MemoryError:
            print 'Not enough memory for PSF, \
                    using memory map in a temporary file.'
            temp_file = _tempfile.TemporaryFile()
            if intensity:
                temp_type = float
            else:
                temp_type = complex
            PSF = _np.memmap(temp_file, dtype=temp_type, mode='w+',
                shape=(nz,nx,nx))

        for i in xrange(nz):
            if verbose: print 'Calculating PSF slice for z={0}um.'.format(zs[i])
            U = N*_fftpack.ifft2(_np.exp(2*_np.pi*1j*kz*zs[i])*PF)
            for j in range(0,self.kzs.shape[0]):
                U = U + N*_fftpack.ifft2(_np.exp(2*_np.pi*1j*self.kzs[j]*zs[i])*PF)
            U = U/(1+self.kzs.shape[0])
            _slice_ = _fftpack.ifftshift(U)
            #_slice_ = U
            if intensity:
                #_slice_ = _np.abs(_slice_)**2
                _slice_ = _np.abs(_slice_ * _np.conj(_slice_))
            PSF[i] = _slice_

        if nz == 1:
            PSF = PSF[0]
        
        return PSF

    def psf2pf(self, PSF, dz, mu, A, nIterations=20, z_offset=0):

        '''
        Retrieves the complex pupil function from an intensity-only
        PSF stack by relative entropy minimization. The algorithm is
        based on Kner et al., 2010, doi:10.1117/12.840943, which in turn
        is based on Deming, 2007, J Opt Soc Am A, Vol 24, No 11, p.3666.

        Parameters
        ---------
        PSF: 3D numpy.array
            An intensity PSF stack. PSF.shape has to be
            (nz, Simulation.nx, Simulation.nx), where nz is the arbitrary
            number of z slices.
        dz: float
            The distance between two PSF slices.
        mu: float
            The background level of the PSF.
        A: 2D numpy.array
            The initial guess for the complex pupil function with shape
            (Simulation.nx, Simulation.nx).
        nIterations: int
            The number of minimization steps.
        z_offset: float
            If the provided is not perfectly focussed, the offset can be
            given here in um.
        '''
        
        dz = float(dz)
        mu = float(mu)
        z_offset = float(z_offset)

        # Number of z slices:
        nz = PSF.shape[0]     
        
        kz = self.kz
        k = self.k
        k_max = self.k_max

        # Z position of slices:
        upper = 0.5*(nz-1)*dz
        zs = _np.linspace(-upper,upper,nz) - z_offset

	# Normalization for fft2:
	N = _np.sqrt(self.nx*self.ny)

        for i in xrange(nIterations):
            
            print 'Iteration',i+1        
            # Calculate PSF field from given PF:
            U = self.pf2psf(A, zs, intensity=False)
            # Calculated PSF intensity with background:
            #Ic = _np.abs(U)**2 + mu
            Ic = mu + (U * _np.conj(U))
            
            minFunc = _np.mean(PSF*_np.log(PSF/Ic))
            print 'Relative entropy per pixel:', minFunc
            redChiSq = _np.mean((PSF-Ic)**2)
            print 'Reduced Chi square:', redChiSq

            # Comparing measured with calculated PSF by entropy minimization:
            Ue = (PSF/Ic)*U
            # New PF guess:
            A = _np.zeros_like(Ue) + 1j*_np.zeros_like(Ue)
            for i in xrange(len(zs)):
                Ue[i] = _fftpack.fftshift(Ue[i])
                A[i] = _fftpack.fft2(Ue[i])/_np.exp(2*_np.pi*1j*kz*zs[i])/N
                for j in range(0,self.kzs.shape[0]):
                    A[i] = A[i] + _fftpack.fft2(Ue[i])/_np.exp(2*_np.pi*1j*self.kzs[j]*zs[i])/N
                A[i] = A[i]/(1+self.kzs.shape[0])
            A = _np.mean(A,axis=0)

            # Limit the aperture and distribute the amplitude equally:         
            A = self.apply_NA_restriction(A)
            counts = _np.sum(_np.abs(A))/self.pupil_npxl
            A = counts*_np.exp(1j*_np.angle(A))
            A = self.apply_NA_restriction(A)

        return A
    

    def modulation2slipsf(self, modulation, zs, n_photons, dcf=0, dmf=0,
                          tilt=(0,0), intensity=True, verbose=False):

        '''
        Calculates the interference PSF for a given SLI modulation.
        '''

        nz = len(zs)
        sliPSF = _np.zeros((nz,self.nx,self.nx))

        for i in xrange(nz):
            if verbose: print 'Calculating PSF slice for z={0}um.'.format(zs[i])

            modPF = self.get_sli_pupil_function(zs[i], n_photons, dcf, dmf, tilt) * \
                    _np.exp(1j*modulation)
            sliPSF[i] = self.pf2psf(modPF, 0, intensity=intensity, verbose=False)

        return sliPSF
