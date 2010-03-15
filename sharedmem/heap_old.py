from __future__ import with_statement


# Almost all of this is taken from multiprocessing/heap.py
# Copyright (c) 2007-2008, R Oudkerk --- see COPYING.txt


import bisect
import tempfile
import os
import sys
import threading
import itertools
import Queue
import time


import multiprocessing

if sys.version_info < (2, 5):
    import multiprocessing._mmap25 as mmap
else:
    import mmap


from multiprocessing.util import Finalize, info
from multiprocessing.forking import assert_spawning

__all__ = ['BufferWrapper']


if sys.platform == 'win32':
    from sharedmemory_win import SharedMemoryBuffer 
else:
    from sharedmemory_sysv import SharedMemoryBuffer 


class Arena(object):

    def __init__(self, size):
        self.buffer = SharedMemoryBuffer(size)
        self.size = size
        self.name = None

            
class Heap(object):

    _alignment = 8

    def __init__(self, size=mmap.PAGESIZE):
        self._lastpid = os.getpid()
        self._lock = threading.Lock()
        self._size = size
        self._lengths = []
        self._len_to_seq = {}
        self._start_to_block = {}
        self._stop_to_block = {}
        self._allocated_blocks = set()
        #self._arenas = []

    @staticmethod
    def _roundup(n, alignment):
        # alignment must be a power of 2
        mask = alignment - 1
        return (n + mask) & ~mask

    def _malloc(self, size):
        # returns a large enough block -- it might be much larger
        i = bisect.bisect_left(self._lengths, size)
        if i == len(self._lengths):
            length = self._roundup(max(self._size, size), mmap.PAGESIZE)
            self._size *= 2
            info('allocating a new mmap of length %d', length)
            arena = Arena(length)
            #self._arenas.append(arena)
            return (arena, 0, length)
        else:
            length = self._lengths[i]
            seq = self._len_to_seq[length]
            block = seq.pop()
            if not seq:
                del self._len_to_seq[length], self._lengths[i]

        (arena, start, stop) = block
        del self._start_to_block[(arena, start)]
        del self._stop_to_block[(arena, stop)]
        return block

    def _free(self, block):
        # free location and try to merge with neighbours
        (arena, start, stop) = block

        try:
            prev_block = self._stop_to_block[(arena, start)]
        except KeyError:
            pass
        else:
            start, _ = self._absorb(prev_block)

        try:
            next_block = self._start_to_block[(arena, stop)]
        except KeyError:
            pass
        else:
            _, stop = self._absorb(next_block)

        block = (arena, start, stop)
        length = stop - start

        try:
            self._len_to_seq[length].append(block)
        except KeyError:
            self._len_to_seq[length] = [block]
            bisect.insort(self._lengths, length)

        self._start_to_block[(arena, start)] = block
        self._stop_to_block[(arena, stop)] = block

    def _absorb(self, block):
        # deregister this block so it can be merged with a neighbour
        (arena, start, stop) = block
        del self._start_to_block[(arena, start)]
        del self._stop_to_block[(arena, stop)]

        length = stop - start
        seq = self._len_to_seq[length]
        seq.remove(block)
        if not seq:
            del self._len_to_seq[length]
            self._lengths.remove(length)

        return start, stop

    def free(self, block):
        # free a block returned by malloc()
        assert os.getpid() == self._lastpid
        self._lock.acquire()
        try:
            self._allocated_blocks.remove(block)
            self._free(block)
        finally:
            self._lock.release()

    def malloc(self, size):
        # return a block of right size (possibly rounded up)
        assert 0 <= size < sys.maxint
        if os.getpid() != self._lastpid:
            self.__init__()                     # reinitialize after fork
        self._lock.acquire()
        try:
            size = self._roundup(max(size,1), self._alignment)
            (arena, start, stop) = self._malloc(size)
            new_stop = start + size
            if new_stop < stop:
                self._free((arena, new_stop, stop))
            block = (arena, start, new_stop)
            self._allocated_blocks.add(block)
            return block
        finally:
            self._lock.release()

#
# Class representing a chunk of an mmap -- can be inherited
#

# Garbage collector for small arrays 
# A block cannot be collected before the following conditions
# are met:
#    - the SharedMemoryBuffer's refcount is 1 (nobody else is using it)
#    - the refcount in this process for the block is 0. 
#


gc_monitor_queue = Queue.Queue(0)
gc_queue = Queue.Queue(0) 


def __gc_thread_monitor_proc():
    # this thread monitors blocks that could be used by other
    # processes and releases them when possible
    while 1:
        niter = gc_monitor_queue.qsize()
        if niter:
            for n in range(niter):
                block = gc_monitor_queue.get()
                (arena, start, stop) = block
                if arena.buffer.gethandlecount() == 1:
                    _heap.free(block) # thread-safe call
                else:
                    gc_monitor_queue.put(block)
            # Sleep for some time to let the queue repopulate;
            # we also don't want to immediately scan those blocks we
            # put back.
            time.sleep(gc_monitor_interval)
                
        else:
            # this will make the thread sleep until
            # something is put on the queue
            block = gc_monitor_queue.get()
            (arena, start, stop) = block
            if arena.buffer.gethandlecount() == 1:
                _heap.free(block) # thread-safe call
            else:
                gc_monitor_queue.put(block)


def __gc_thread_proc():
    # this thread frees unused blocks, except those
    # whos buffer are still used by other processes
    while 1:
        block = gc_queue.get()
        (arena, start, stop) = block
        
        if arena.buffer.gethandlecount() == 1:
            _heap.free(block) # thread-safe call
            print 'deallocated block'
        else:
            gc_monitor_queue.put(block)


# increase or decrease refcount
# make sure you hold __gc_lock before calling
# these functions

def gc_inc(block):
    try:
        cnt =  gc_dict[block]
    except KeyError:
        cnt = 0
    gc_dict[block] = cnt + 1 

def gc_dec(block):
    cnt = gc_dict[block]
    if cnt == 1:
        del gc_dict[block]
        gc_queue.put(block)
    else:
        gc_dict[block] = cnt - 1


gc_monitor_interval = 5.0 # sleep for 5 seconds
gc_dict = dict()
gc_lock = threading.Lock()

gc_thread = threading.Thread(target=__gc_thread_proc)
gc_thread.setDaemon(True)
gc_thread.start()

gc_thread_monitor = threading.Thread(target=__gc_thread_monitor_proc)
gc_thread_monitor.setDaemon(True)
gc_thread_monitor.start()

_heap = Heap()

class BufferWrapper(object):

    def __init__(self, size):
        assert 0 <= size < sys.maxint
        if size > mmap.PAGESIZE:
            arena = Arena(size)
            _, length = arena.buffer.getbuffer()
            self._state = (arena, 0, length), size
            self.gc = False
        else:
            with gc_lock:
                block = _heap.malloc(size)
                self._state = (block, size)
                self.gc = True
                # increase refcount
                gc_inc(block)
            
    def __del__(self):
        block, size = self._state
        if self.gc:
            with gc_lock:
                gc_dec(block)

    def __setstate__(self, _state):

        state, pid, gc = _state
        
        with gc_lock:
            self._state = state
            block, size = state
            if not gc:
                self.gc = False
                return
            if pid != os.getpid():
                self.gc = False
                return
            if (size > mmap.PAGESIZE):
                self.gc = False
            else:
                gc_inc(block)
                self.gc = True
            

                
                    
    def __getstate__(self):
        return self._state, os.getpid(), self.gc
        
    def get_address(self):
        (arena, start, stop), size = self._state
        address, length = arena.buffer.getbuffer()
        assert size <= length
        return address + start

    def get_size(self):
        return self._state[1]






















