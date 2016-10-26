import numpy as _np
import struct as _struct
from scipy import misc as _misc
import os as _os
from matplotlib import pyplot as _pyplot
import Image
import sys as _sys
import re as _re

def _check_file_extension(name, extension):
    if _os.path.splitext(name)[1] != '.' + extension:
        name += '.' + extension
    return name


class BinaryFileMap(object):

    def __init__(self, filename, dtype, shape):
    
        self._file = open(filename, 'rb')
        self._dtype = _np.dtype(dtype)
        self._shape = shape
        self._ndim = len(shape)
        self._item_shape = shape[::-1][0:2]
        self._item_size = _np.prod(self._item_shape)

    @property
    def dtype(self):
        return self._dtype

    @property
    def ndim(self):
        return self._ndim
    
    @property
    def shape(self):
        return self._shape

    def __del__(self):
        try:
            self.close()
        except:
            pass

    def __getitem__(self, item):
        
        if isinstance(item, int):
            if item < self._shape[0]:
                return self._get_item(item)
            else:
                raise IndexError
        
        elif isinstance(item, tuple):
            root = self._get_item(item[0])
            return root[item[1:]]
        
        elif isinstance(item, slice):
            indices = item.indices(self._shape[0])
            data = _np.zeros((len(indices),) + self._item_shape)
            for i in indices:
                data[i] = self._get_item(i)

    def _get_item(self, index):
        
        self._file.seek(self._dtype.itemsize * index * self._item_size)
        data = _np.fromfile(self._file, self._dtype, self._item_size)
        return _np.reshape(data, self._item_shape)

    def close(self):
        self._file.close()




class DAX(BinaryFileMap):

    def __init__(self, filename):

        daxfile = _check_file_extension(filename, 'dax')
	inffile = _os.path.splitext(daxfile)[0] + '.inf'

	inf = open(inffile, 'r')

	bits=16

        for line in inf:

            matchObj = _re.match('(.*) = (.*)', line)
            
            if matchObj:
                node = matchObj.group(1)
                value = matchObj.group(2).rstrip()

                if node == 'frame dimensions':
                    matchObj = _re.match('(\d*) x (\d*)', value)
                    dimensions = (int(matchObj.group(1)), int(matchObj.group(2)))

                elif node == 'number of frames':
                    n_frames = int(value)

                elif node == 'data type':
                    if value == '16 bit integers (binary, big endian)':
                        endianness = '>'
                        bits = 16
                    elif value == '16 bit integers (binary, little endian)':
                        endianness = '<'
                        bits = 16
                    elif value == '8 bit integers (binary, big endian)':
                        endianness = '>'
                        bits = 8
                    elif value == '8 bit integers (binary, little endian)':
                        endianness = '<'
                        bits = 8
                    else:
                        raise Exception('Data type not understood.')
	
        inf.close()

        if bits==16:
            dataType = endianness+'i2'
        elif bits==8:
            dataType = endianness+'i1'

        BinaryFileMap.__init__(self, daxfile, dataType, (n_frames,)+dimensions)


def _read_binary(handle, dtype, position=None, number=1):
   
    if dtype in 'xcbB?':
        size = 1
    elif dtype in 'hH':
        size = 2
    elif dtype in 'iIlLf':
        size = 4
    elif dtype in 'qQd':
        size = 8
    else:
        raise ValueError('Unknown dtype {}'.format(dtype))

    if position:
        handle.seek(position)
 
    re = _struct.unpack(number*dtype, handle.read(number*size))

    if number == 1:
        return re[0]
    return re


def _write_binary(handle, data=None, dtype=None, position=None, **kwargs):

    if position:
        handle.seek(position)

    if data != None:
        if isinstance(data, _np.ndarray):
            handle.write(data.tostring())
        else:
            handle.write(_struct.pack(dtype, data))
    else:
        handle.write(_struct.pack(kwargs['number']*'x'))


def loadSPE(filename):

    filename = _check_file_extension(filename, 'spe')

    handle = open(filename, 'rb')
    
    x_dim = _read_binary(handle, 'I', 42)
    dtype = _read_binary(handle, 'i', 108)
    y_dim = _read_binary(handle, 'I', 656)
    z_dim = _read_binary(handle, 'q', 1446)

    if dtype == 0:
        dtype = 'f'
    elif dtype == 1:
        dtype = 'q'
    elif dtype == 2:
        dtype = 'i'
    elif dtype == 3:
        dtype = 'I'
    elif dtype == 5:
        dtype = 'd'
    elif dtype == 6:
        dtype == 'H'
    elif dtype == 8:
        dtype == 'Q'
    else:
        raise Exception('Unsupported SPE data type {}'.format(dtype))

    data = _read_binary(handle, dtype, 4100, x_dim*y_dim*z_dim)
    handle.close()

    return _np.reshape(_np.array(data), (z_dim, x_dim, y_dim))


def saveSPE(filename, data):

    filename = _check_file_extension(filename, 'spe')

    if data.dtype == _np.float32:
        dtype = 0
    elif data.dtype == _np.int32:
        dtype = 1
    elif data.dtype == _np.int16:
        dtype = 2
    elif data.dtype == _np.uint16:
        dtype = 3
    elif data.dtype == _np.float64:
        dtype = 5
    elif data.dtype == _np.uint8:
        dtype = 6
    elif data.dtype == _np.uint32:
        dtype = 8
    else:
        raise TypeError('Data type not suported by SPE file format.')
    
    z_dim, x_dim, y_dim = data.shape

    handle = open(filename, 'wb')

    _write_binary(handle, number=4100)
    _write_binary(handle, x_dim, 'I', 42)
    _write_binary(handle, dtype, 'i', 108)
    _write_binary(handle, y_dim, 'I', 656)
    _write_binary(handle, z_dim, 'q', 1446)
    _write_binary(handle, data, position=4100)

    handle.close()


def loadMBinList(filename):

    if _os.path.splitext(filename)[1] != '.bin':
        filename += '.bin'

    handle = open(filename, 'rb')

    # Reading out some info
    version, = _struct.unpack('4s', handle.read(4))
    n_frames, = _struct.unpack('i', handle.read(4))
    type, = _struct.unpack('i', handle.read(4))

    # Get molecules from master list
    n_molecules, = _struct.unpack('i',handle.read(4))
    
    molecules = []

    for i in xrange(n_molecules):

        m = Molecule()
        
        m.x,m.y,m.xc,m.yc,m.h,m.a,m.w,m.phi,m.ax,m.b,m.i \
            = _struct.unpack('11f',handle.read(11*4))
        m.c,m.val_fit_den,m.frame,m.length,m.link \
            = _struct.unpack('5i',handle.read(5*4))
        m.z,m.zc = _struct.unpack('2f',handle.read(2*4))

        molecules.append(m)

    mlist = MList(molecules, n_frames)

    # Get the index for each molecule in the frame lists.
    for i in xrange(n_frames):
        
        n_molecules_frame, = _struct.unpack('i',handle.read(4))

        for j in xrange(n_molecules_frame):

            handle.seek(16 + 72*n_molecules + 4*i + 72*j)
            # This assumes that the order in the frame list is the same as
            # in the master list.
            mlist[i+1,j].index = _struct.unpack('i', handle.read(4))

    handle.close()

    return mlist


class MList(object):

    def __init__(self, molecules=[], n_frames=None):

        if not n_frames:
            n_frames = 0
            for molecule in molecules:
                if molecule.frame > n_frames: n_frames = molecule.frame

        self._molecules = molecules
        self.n_frames = n_frames


    def __getattr__(self, name):
        return _np.array([getattr(_, name) for _ in self._molecules])


    def __getitem__(self, item):
               
        if isinstance(item, int):
            # The user wants a list of molecules in frame <item>
            return MList(self._get_molecules_from_frame(item))

        elif isinstance(item, slice):
            # The user wants a list of molecules in the provided slice
            indices = item.indices(self.max_frame+1)
            mols = []
            for i in range(*indices):
                mols += self._get_molecules_from_frame(i)
            return MList(mols)
        
        elif isinstance(item, tuple):

            if isinstance(item[0], int):
                # The user wants something from a specific frame.
                mols = self._get_molecules_from_frame(item[0])

            elif isinstance(item[0], slice):
                # The user wants something from the sliced frames.
                indices = item[0].indices(self.max_frame+1)
                mols = []
                for i in range(*indices):
                    mols += self._get_molecules_from_frame(i)

            if isinstance(item[1], int):
                # The user wants a specific molecule
                return mols[item[1]]
            elif isinstance(item[1], slice):
                # The user wants a slice of the molecules in the frame(s).
                return MList(mols[item[1]])

        elif isinstance(item, _np.ndarray):
            
            if item.ndim == 1:
                
                indices, = _np.where(item)
                mols = [self._molecules[i] for i in indices]
            
            return MList(mols)

        
        # We could not figure out what the user wants.
        raise Exception(
                'MList instance could not be sliced with provided expression.')


    def __iter__(self):

        for mol in self._molecules:
            yield mol


    def _get_molecules_from_frame(self, frame):
        return [_ for _ in self._molecules if _.frame == frame]



    @property
    def max_frame(self):
        
        max_frame = 0
        for molecule in self._molecules:
            if molecule.frame > max_frame: max_frame = molecule.frame
        return max_frame


    @property
    def n_molecules(self):
        return len(self._molecules)


    @property
    def type(self):
        return 6


    @property
    def version(self):
        return 'M425'


    def _write_to_file(self, handle, frame):

        if frame == 'master':
            molecules = self._molecules
        else:
            molecules = [_ for _ in self._molecules if _.frame == frame]

        handle.write(_struct.pack('i', len(molecules)))

        for molecule in molecules:
            
            handle.write(_struct.pack('11f', molecule.x, molecule.y,
                molecule.xc, molecule.yc, molecule.h, molecule.a,
                molecule.w, molecule.phi, molecule.ax, molecule.b,
                molecule.i))

            handle.write(_struct.pack('3i', molecule.c, molecule.val_fit_den,
                molecule.frame))

            if frame == 'master':
                handle.write(_struct.pack('i', molecule.length))
            else:
                handle.write(_struct.pack('i', molecule.index))

            handle.write(_struct.pack('i', molecule.link))
            handle.write(_struct.pack('2f', molecule.z, molecule.zc))


    def add(self, molecule):
        self._molecules.append(molecule)

    
    def remove(self, molecule):
        self._molecules.remove(molecule)

    
    def save(self, filename):

        if _os.path.splitext(filename)[1] != '.bin':
            filename += '.bin'
        
        handle = open(filename, 'wb')
        
        handle.write(self.version)
        handle.write(_struct.pack('i', self.n_frames))
        handle.write(_struct.pack('i', self.type))

        self._write_to_file(handle, 'master')

        for i in xrange(self.n_frames):
            self._write_to_file(handle, i)

        handle.close()



class Molecule(object):

    def __init__(self, **kwargs):
            
        self.__dict__.update({'x':0,'y':0,'xc':0,'yc':0,'h':0,'a':0,'w':0,
            'phi':0,'ax':0,'b':0,'i':0,'c':0,'val_fit_den':0,'frame':0,
                'length':0,'index':0,'link':-2,'z':0,'zc':0})
        self.__dict__.update(kwargs)



def npy2tif(path):

    data = _np.load(path)
    filebase = _os.path.splitext(path)[0]
    print 'File base name:', filebase
    if data.dtype is not _np.float32:
        data = _np.array(data, dtype=_np.float32)
    if data.ndim == 2:
        saveto = filebase + '.tif'
        print 'Creating file', saveto
        image = Image.fromarray(data, mode='F')
        image.save(saveto)
    else:
        try:
            _os.mkdir(filebase)
        except WindowsError as e:
            if e.errno != 17:
                raise
        except:
            raise
        n_digits = len(str(data.shape[0]))
        min = data.min()
        max = data.max()
        for i in xrange(data.shape[0]):
            formatstr = '0' + str(n_digits) + 'd'
            filename = '{0:' + formatstr + '}.tif'
            filepath = _os.path.join(filebase, filename.format(i))
            image = Image.fromarray(data[i], mode='F')
            image.save(filepath)



def npydir2tif(path):

    for dirpath, dirnames, filenames in _os.walk(path):
        for f in filenames:
            base, ext = _os.path.splitext(f)
            if ext == '.npy':
                fpath = _os.path.join(dirpath, f)
                npy2tif(fpath)
