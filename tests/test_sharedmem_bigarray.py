# test template
# def test():
#    setup_test()
#    try:
#       do_test()
#       make_test_assertions()
#    finally:
#       cleanup_after_test()


from __future__ import with_statement
import numpy as np
import sharedmem

# how big can the arrays be?

def test_sharedmem_bigarray_2_26_uint64():
    """test_sharedmem_bigarray test allocation of array 2**26 * np.uint64 size"""
    # sharedmem.empty(1644902724, dtype=np.uint64) # too big for my machine
    # sharedmem.empty(2**29, dtype=np.uint64) # too big for my machine
    arr = sharedmem.empty(2**26, dtype=np.uint64)
        
        
