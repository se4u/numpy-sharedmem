#!/usr/bin/env python
# this clearly compiles with VS 2008, probably would work with mingw32 gcc4.4 too
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import os, sys

## configuration
import numpy, os.path
numpy_basedir = os.path.dirname(numpy.__file__)

print "sys.platform:", sys.platform
if sys.platform == 'linux2':
    numpy_include = os.path.join(numpy_basedir, r"core/include")
    inc_dirs = [numpy_include]
    lib_dirs = [r'/usr/local/lib', r'.']
    libs = ['m']

    unixshared =  Extension("sharedmem.sharedmemory_sysv",
                            ["sharedmem/sharedmemory_sysv.pyx"],
                           include_dirs=inc_dirs,
                           library_dirs=lib_dirs,
                           libraries=libs)
    ext_modules = [unixshared]

    # notes:
    # on ubuntu 8.04
    # inc_dirs = [r"/usr/lib/python2.5/site-packages/numpy/core/include",
    # on ubuntu 9.04
    # inc_dirs = [r"/usr/lib/python2.6/dist-packages/numpy/core/include",

elif sys.platform == 'darwin':
    # tryin on os 10.6 with enthought python 6.01 + cython 12.1
    numpy_include = os.path.join(numpy_basedir, r"core/include")
    inc_dirs = [numpy_include]
    lib_dirs = [r'/usr/local/lib', r'.']
    libs = ['m']

    unixshared =  Extension("sharedmemory_sysv",
                            ["sharedmemory_sysv.c"], # [sharedmemory_sysv.pyx"],
                           include_dirs=inc_dirs,
                           library_dirs=lib_dirs,
                           libraries=libs)
    ext_modules = [unixshared]



elif sys.platform == 'win32':
    inc_dirs = [r'e:/Python26/Lib/site-packages/numpy/core/include', r'c:/Python26/Lib/site-packages/numpy/core/include', r'./']
    lib_dirs = [r'./', r'e:/Programs/NationaInstruments/NI-DAQ/DAQmx ANSI C Dev/lib/msvc', r'c:/Programs/NationaInstruments/NI-DAQ/DAQmx ANSI C Dev/lib/msvc']
    libs = [] # worked for MSVC 9, maybe mingw too
    # libs = ['nicaiu'] # worked for mingw


# on daq1 rig/winxp
#inc_dirs = [r'e:/Python26/Lib/site-packages/numpy/core/include', r'./']
#lib_dirs = [r'./', r'e:/Programs/NationaInstruments/NI-DAQ/DAQmx ANSI C Dev/lib/msvc']

winshared =  Extension("sharedmemory_win", ["sharedmemory_win.pyx", "ntqueryobject.c"],
                            include_dirs=inc_dirs,
                            library_dirs=lib_dirs,
                            libraries=libs)



ext_modules = [winshared]

setup(
    author="Sturla Molden",
    name="numpy-sharedmem",
    version="2009-02-12",
    description="numpy-sharedmem  easy to use shared memory implementation for numpy to make it easy to share memory in an array across processes and threads.",
    url='https://cleemesser@bitbucket.org/cleemesser/numpy-sharedmem/',
    classifiers=[
        "Development Status :: 3 - alpha, research",
        "Intended Audience :: Scientific programmers",
        "License :: scipy",
        "Operating System :: unix, windows"],
    # packages=["sharedmem"],
    # package_dir= {"sharedmem" : ""},
    cmdclass = {'build_ext': build_ext},
    ext_modules = ext_modules,

)
