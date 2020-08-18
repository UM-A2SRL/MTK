#===============================================================================
#
#     Modal Tool Kit (MTK)
#
#     Copyright 2017-2020 Christopher A. Lupp
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
#
#===============================================================================

import os
from subprocess import check_output
import sys
import eigency
import numpy

from setuptools import setup, find_packages
from setuptools.extension import Extension
from Cython.Build import cythonize


# Convert from local to absolute directories
#-------------------------------------------
def GlobalDirectory(files):
    root_dir = os.path.abspath(os.path.dirname(__file__))
    new = []
    for f in files:
        new.append(os.path.join(root_dir, f))
    return new


def ReadConfigFile(fname):
    """Reads a config file and sets the include directories
    """
    f = open(fname, 'r')
    list = []
    for line in f:
        if line[0] == "#":
            # treat as a commented line
            pass
        elif len(line.rstrip()) == 0:
            # skip empty lines
            pass
        else:
            list += [line.rstrip(),]
    return list


# find the eigen root directory and add it to the include path
try:
    inc_dirs = [os.environ['EIGEN3_ROOT']]
except KeyError:
    print("""
    It looks like you don't have Eigen installed in your system.
    Please clone it with
        git clone --branch 3.3.4 --depth 1 https://github.com/eigenteam/eigen-git-mirror.git
    And set an environment variable pointing to it
        export EIGEN3_ROOT=$PWD/eigen-git-mirror
    Consider adding that variable to your .bashrc, e.g. with
        echo "export EIGEN3_ROOT=$PWD/eigen-git-mirror" >> ~/.bashrc
    """)
    raise

# Relative paths for the include/library directories
rel_inc_dirs = ['MTK/include/']

# Convert from relative to absolute directories
inc_dirs.extend(GlobalDirectory(rel_inc_dirs))

exts = [Extension('MTK.MTK', sources=['MTK/MTK.pyx'],
            include_dirs=inc_dirs + eigency.get_includes())
    ]

for e in exts:
    e.cython_directives = {"embedsignature": True, "binding":True}
    
setup(name='modaltoolkit',
    version='3.0.0',
    description='Modal Tool Kit',
    author='Christopher A. Lupp',
    author_email='clupp@umich.edu',
    include_package_data=True,
    packages = find_packages(),
    package_data = {"MTK": ['*.pxd','include/*']},
    ext_modules=cythonize(exts),
    setup_requires=['setuptools','numpy','eigency','Cython'],
    install_requires = ['numpy','h5py','eigency','sphinx', 'matplotlib']
    )
