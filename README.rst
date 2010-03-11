---------------
numpy-sharedmem
---------------

A shared memory module for numpy by Sturla Molden and perhaps by G. Varaqueux Co
de found posted on scipy list at http://folk.uio.no/sturlamo/python/sharedmem-feb13-2009.zip

Packaging by Chris Lee-Messer
License: scipy license (2009)

url:  http://cleemesser@bitbucket.org/cleemesser/numpy-sharedmem/

Requirements:
-------------

It's suppose to work on unix and windows, at least in 32bit for not
too big arrays. I've only done basic tests on winxp so far using
ming32 (Pythonxy 2.6 distribution) numpy 1.3 and cython 12.1


Installation:
-------------
on windows, need to use mingw and assuming you are using mercurial. 
Using the command line::
  $ hg clone https://cleemesser@bitbucket.org/cleemesser/numpy-sharedmem/
  $ cd numpy-sharedmem
  $ copy setup.cfg.template to setup.cfg  # to set mingw as the compiler
  $ python setup.py install


References and issues:
---------------------
The oringal comment::
    http://old.nabble.com/Re:-Multiprocessing-and-shared-memory-p25949201.html

    Gaël Varoquaux and I did some work on that some months ago. It's not as 
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




