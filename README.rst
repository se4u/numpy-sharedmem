---------------
numpy-sharedmem
---------------

A shared memory module for numpy by Sturla Molden and G. Varoquaux, adapted from Robert Kern. Code found posted on scipy list at http://folk.uio.no/sturlamo/python/sharedmem-feb13-2009.zip  See also Sturla's tutorial: 

Packaging by Chris Lee-Messer
License: scipy license (2009)

url:  http://cleemesser@bitbucket.org/cleemesser/numpy-sharedmem/

You might want to check Sturla's sourceforge project
http://sharedmemoryarr.sourceforge.net/ thought it didn't have any
content as of March 2010.

Features/Documentation
----------------------
see test.py to see how to pickle the shared array and send it to another process
See also http://folk.uio.no/sturlamo/python/multiprocessing-tutorial.pdf
which shows examples of using ctypes and multiprocessing to create shared memory.

I also have a copy of a C-types based code from Nadav Horesh adapted from other code in docs to look at.


Requirements:
-------------

It's suppose to work on unix and windows, at least in 32bit for not
too big arrays. I've only done basic tests on winxp so far using
ming32 (Pythonxy 2.6 distribution) numpy 1.3 and cython 12.1

The tests require multiprocessing, which is available for python 2.5 and is part of the standard library in python 2.6 and above


Installation:
-------------
on windows, need to use mingw and assuming you are using mercurial. 
Using the command line::
  $ hg clone https://cleemesser@bitbucket.org/cleemesser/numpy-sharedmem/
  $ cd numpy-sharedmem
  $ copy setup.cfg.template to setup.cfg  # to set mingw as the compiler
  $ python setup.py install

I have also started putting binary distributions in the dist/ directory in case I don't have a compiler handy.

To do
-----
 - test under linux
   [x] basic smoke tests done on 32bit linux (ubuntu 8.04)

 - test larger files: Nadav Horesh mentions that it doesn't work on
   "large" memory regions (but still under 1GB)

 - see if packaging is ok. trying out setuptools to use for development
   -> problem: cython build_ext doesn't seem to work with setuptools
 
 - decide if this is the right namespace--it requires numpy so perhaps it should be added to that namespace: e.g. "import numpy.sharedmem"

 - add doc on how to find allocated shared memory seg under linux and
   makesure they aren't leaking. e.g. ipcrm 
   
 - contact Sturla to see if he is working on this



Related Links
-------------
The python wiki on this http://wiki.python.org/moin/ParallelProcessing


References and issues:
----------------------
The oringal comment::
    http://old.nabble.com/Re:-Multiprocessing-and-shared-memory-p25949201.html

    Ga�l Varoquaux and I did some work on that some months ago. It's not as 
    trivial as it seems, but we have a working solution. 

    http://folk.uio.no/sturlamo/python/sharedmem-feb13-2009.zip

    Basically it uses named shared memory (Sys V IPC on Unix) as buffer. The 
    ndarray is pickled by its kernel name, the buffer is not copied. Thus 
    you can quickly communicate shared memory ndarrays between processes 
    (using multiprocessing.Queue). 

    Note that there is a pesky memory we could get rid of on Unix: It stems 
    from multiprocessing using os._exit instead of sys.exit to terminate 
    worker processes, preventing any clean-up code from executing. The bug 
    is in multiprocessing, not our code. Windows refcounts shared memory 
    segments in the kernel and is not affected. Change any occurrence of 
    os._exit in multiprocessing to sys.exit and it will work just fine. 

    Well, it's not quite up to date for all 64 bits systems. I'll fix that 
    some day. 


    Sturla Molden 


Nadav comments:: 
  http://permalink.gmane.org/gmane.comp.python.numeric.general/36749

  Extended module that I used for some useful work.
  Comments:
    1. Sturla's module is better designed, but did not work with very large (although sub GB) arrays
    2. Tested on 64 bit linux (amd64) + python-2.6.4 + numpy-1.4.0

Long discussion thread on scipy-user::
  http://old.nabble.com/Multiprocessing-and-shared-memory-td25949044.html




