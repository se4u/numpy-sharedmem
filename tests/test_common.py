# def test():
#    setup_test()
#    try:
#       do_test()
#       make_test_assertions()
#    finally:
#       cleanup_after_test()
import sharedmem, os
import numpy as np
numtypes = [np.float64, np.int32, np.float32, np.uint8, np.complex]

def test_shared_ones():
    for typestr in numtypes:
        shape = (10,)
        a = sharedmem.ones(shape,dtype=typestr)
        t = (a == np.ones(shape))
        assert t.all()
