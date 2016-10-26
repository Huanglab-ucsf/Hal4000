import numpy as _np
from scipy.misc import factorial as _factorial
from scipy import optimize as _optimize

nm = [(0,0),
            (1,1),
            (1,-1),
            (2,0),
            (2,-2),
            (2,2),
            (3,-1),
            (3,1),
            (3,-3),
            (3,3),
            (4,0),
            (4,2),
            (4,-2),
            (4,4),
            (4,-4),
            (5,1),
            (5,-1),
            (5,3),
            (5,-3),
            (5,5),
            (5,-5),
            (6,0),
            (6,-2),
            (6,2),
            (6,-4),
            (6,4)]


def radial((n,m),rho):
    """
    Computes the radial part of the Zernike polynomials.

    Parameters
    ----------
    (n,m) : tuple of ints
        Indices n and m
    rho: float
        Radial distance 

    Returns
    -------

    """
    
    if n<0 or m<0:
        print 'Error: n,m have to be >0.'
        return 0

    summation = _np.zeros_like(rho)

    #If n-m is odd, value is 0
    if _np.mod((n-m),2):
        print "For n-m odd Zernike polynomials are zero."
        return summation
   
    if n == 0:
        return _np.ones_like(rho)
    elif n == 1:
        return rho
    elif n == 2:
        if m == 0:
            return 2*rho**2-1
        elif m == 2:
            return rho**2
    elif n == 3:
        if m == 1:
            return 3*rho**2-2*rho
        elif m == 3:
            return rho**3
    elif n == 4:
        if m == 0:
            return 6*rho**4-6*rho**2+1
        elif m == 2:
            return 4*rho**4-3*rho**2
        elif m == 4:
            return rho**4
    
    for k in range(0, ((n-m)/2)+1):
        temp_top = ((-1)**k) * _factorial(n-k)
        temp_bot = _factorial(k) * _factorial((n+m)/2. - k) * _factorial((n-m)/2. - k)
        rho_term = pow(rho, n - (2*k))
        summation = summation + (rho_term * (temp_top/temp_bot))

        return summation


def zernike((n,m),rho,phi):
    """
    Computes the Zernike polynomials.

    Parameters
    ----------
    (n,m) : tuple of ints
        Zernike indices n and m
    rho: float
        Radial distance
    phi: float
        Azimuthal angle (in radians)

    Returns
    -------

    """
    if n < abs(m):
        print 'Error: n has to be >= abs(m)!'
        return 0

    rad_part = _np.sqrt(n+1)*radial((n,abs(m)),rho)
    
    if m == 0:
        return rad_part
    elif m>0:
        return _np.sqrt(2) * rad_part * _np.cos(m*phi)
    elif m<0:
        return _np.sqrt(2) * rad_part * _np.sin(m*phi)


def basic_set(p,r,theta):
    return  p[0]*zernike(nm[0],r,theta) + \
            p[1]*zernike(nm[1],r,theta) + \
            p[2]*zernike(nm[2],r,theta) + \
            p[3]*zernike(nm[3],r,theta) + \
            p[4]*zernike(nm[4],r,theta) + \
            p[5]*zernike(nm[5],r,theta) + \
            p[6]*zernike(nm[6],r,theta) + \
            p[7]*zernike(nm[7],r,theta) + \
            p[8]*zernike(nm[8],r,theta) + \
            p[9]*zernike(nm[9],r,theta) + \
            p[10]*zernike(nm[10],r,theta) + \
            p[11]*zernike(nm[11],r,theta) + \
            p[12]*zernike(nm[12],r,theta) + \
            p[13]*zernike(nm[13],r,theta) + \
            p[14]*zernike(nm[14],r,theta)

def decompose(data,r,theta):
    basis = [zernike((0,0),r,theta),
             zernike((1,-1),r,theta),
             zernike((1,1),r,theta),
             zernike((2,0),r,theta),
             zernike((2,-2),r,theta),
             zernike((2,2),r,theta),
             zernike((3,-1),r,theta),
             zernike((3,1),r,theta),
             zernike((3,-3),r,theta),
             zernike((3,3),r,theta),
             zernike((4,0),r,theta),
             zernike((4,-2),r,theta),
             zernike((4,2),r,theta),
             zernike((4,-4),r,theta),
             zernike((4,4),r,theta)]
    cov_mat = _np.array([[_np.sum(zi*zj) for zi in basis] for zj in basis])
    cov_mat_inv = _np.linalg.pinv(cov_mat)
    inner_products = _np.array([_np.sum(data*zi) for zi in basis])
    return _np.dot(cov_mat_inv,inner_products)


def fit_to_basic_set(image,p0,r,theta,weight=None,**kwargs):
    data = _np.copy(image)
    data[r>1] = 0
    sumsquares = []
    count = [0]
    def fitfunction(p):
        Z = basic_set(p,r,theta)
        Z[r>1] = 0
        return Z
    def errorfunction(p):
        print 'Iteration', count[0]
        errormap = fitfunction(p)-data
        if weight != None:
            errormap *= weight
        error = _np.ravel(errormap)
        sumsquares.append(_np.sum(error**2))
        print 'Sum of squares:',sumsquares[-1]
        count[0] += 1
        return error
    p,success = _optimize.leastsq(errorfunction,p0,**kwargs)
    return p,success,sumsquares
