#!/usr/bin/env python

# Can use this file via setup.py build_ext --inplace
# during development
#from setuptools import setup  # problems with cython, see setupegg.py

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import os, sys

## configuration
# what's the standard way to find where numpy is. This seems awkward. Is it automatic with cython's build_ext?
import numpy, os.path
numpy_basedir = os.path.dirname(numpy.__file__)

print "sys.platform:", sys.platform

if sys.platform == 'win32':
    numpy_include = os.path.join(numpy_basedir, r"core\include")
    inc_dirs = [numpy_include, r'./']
    lib_dirs = [r'.']
    libs = [] 


    winshared =  Extension("sharedmem.sharedmemory_win", ["sharedmem/sharedmemory_win.pyx", "sharedmem/ntqueryobject.c"],
                           include_dirs=inc_dirs,
                           library_dirs=lib_dirs,
                           libraries=libs)



    ext_modules = [winshared]

else: #if sys.platform == 'linux2' 'linux3' or 'darwin'
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


setup(
    author="Sturla Molden",
    name="numpy-sharedmem",
    version="2009-03-15",
    license='scipy license (http://scipy.org)', 
    description="numpy-sharedmem  easy to use shared memory implementation for numpy to make it easy to share memory in an array across processes and threads.",
    url='https://cleemesser@bitbucket.org/cleemesser/numpy-sharedmem/',
    classifiers=[
        "Development Status :: 3 - alpha, research",
        "Intended Audience :: Scientific programmers",
        "License :: scipy",
        "Operating System :: unix, windows"],
    packages=["sharedmem"],
#    zip_safe=False, # because of ext module
    cmdclass = {'build_ext': build_ext},
    ext_modules = ext_modules,
    py_modules=['shmarray'],
)

