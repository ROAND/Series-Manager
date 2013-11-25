#!/usr/bin/env python
import os
from distutils.core import setup

setup(name='SeMaRD',
      version='0.1',
      description='Anime downloading as easy as it gets.',
      author='Ronnie Andrew',
      author_email='ronnieandrew92@gmail.com',
      url='http://www.roandigital.com/applications/semard',
      packages=['views'],
      data_files=[('images', ['images'])]
      )
