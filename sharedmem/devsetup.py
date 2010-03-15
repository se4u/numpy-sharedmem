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
import numpy
numpy_basedir = os.path.dirname(numpy.__file__)
print "numpy_basedir:", numpy_basedir
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



elif sys.platform == 'win32':
    numpy_include = os.path.join(numpy_basedir, r"core\include")
    inc_dirs = [numpy_include, r'./']
    lib_dirs = [r'.']
    libs = [] 


    winshared =  Extension("sharedmem.sharedmemory_win", ["sharedmem/sharedmemory_win.pyx", "sharedmem/ntqueryobject.c"],
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
