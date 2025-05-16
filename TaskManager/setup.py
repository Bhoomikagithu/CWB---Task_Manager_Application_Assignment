from setuptools import setup, Extension
import pybind11
import sys

# Define compiler args based on platform
extra_compile_args = []
if sys.platform == 'win32':
    extra_compile_args = ['/std:c++14']  # MSVC flag for C++14
else:
    extra_compile_args = ['-std=c++11']  # GCC/Clang flag

# Define the extension module
cpp_ext = Extension(
    'task_structures',
    sources=['task_structures.cpp'],
    include_dirs=[pybind11.get_include()],
    language='c++',
    extra_compile_args=extra_compile_args,
)

# Setup the module
setup(
    name='task_structures',
    version='0.1',
    ext_modules=[cpp_ext],
    install_requires=['pybind11>=2.6.0'],
) 