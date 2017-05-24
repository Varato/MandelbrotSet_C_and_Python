from distutils.core import setup, Extension

setup(name='Mandelbrot',
      ext_modules=[Extension('Mandelbrot', ['Mand.c'])])
