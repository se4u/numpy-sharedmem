import numpy
import sharedmem as shm
import pickle


def modify_array(a):
    # a = pickle.loads(a)
    a[:,:3] = 1
    #print a.shape
    print "modified array in modify_array"
    #shm.cleanup()

from multiprocessing import Pool, Process


if __name__ == '__main__':
    a = shm.zeros((2,4))
    print "original process:", a
    p = Pool()
    job = p.apply_async(modify_array, (a, ))
    p.close()
    p.join()
    
    print "reprint a in original process:", a



