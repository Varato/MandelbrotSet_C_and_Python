from distutils.core import setup, Extension

setup(name='Mand',
      ext_modules=[
        Extension('Mand',
                  ['pyAPI.c'],
                  )
        ]
)
