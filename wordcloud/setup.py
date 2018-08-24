from distutils.core import setup
from Cython.Build import cythonize
setup(ext_modules=cythonize('query_integral_image.pyx'))