#    "Using Python, multiprocessing and NumPy/SciPy for parallel numerical computing"
# Modified and corrected by Nadav Horesh, Mar 2010
# No rights reserved
# http://www.scipy.org/Cookbook/multiprocessing
# posted to scipy-users

import numpy as N
import ctypes

_ctypes_to_numpy = {
    ctypes.c_char   : N.uint8,
    ctypes.c_wchar  : N.int16,
    ctypes.c_byte   : N.int8,
    ctypes.c_ubyte  : N.uint8,
    ctypes.c_short  : N.int16,
    ctypes.c_ushort : N.uint16,
    ctypes.c_int    : N.int32,
    ctypes.c_uint   : N.uint32,
    ctypes.c_long   : N.int64,
    ctypes.c_ulong  : N.uint64,
    ctypes.c_float  : N.float32,
    ctypes.c_double : N.float64}


def shmem_as_ndarray(raw_array, shape=None ):

    address = raw_array._obj._wrapper.get_address()
    size = len(raw_array)
    if (shape is None) or (N.asarray(shape).prod() != size):
        shape = (size,)
    elif type(shape) is int:
        shape = (shape,)
    else:
        shape = tuple(shape)
        
    dtype = _ctypes_to_numpy[raw_array._obj._type_]
    class Dummy(object): pass
    d = Dummy()
    d.__array_interface__ = {
        'data' : (address, False),
        'typestr' : N.dtype(dtype).str,
        'descr' : N.dtype(dtype).descr,
        'shape' : shape,
        'strides' : None,
        'version' : 3}
    return N.asarray(d).view( dtype=dtype )
