#!/usr/bin/env python

from distutils.core import setup

setup(name='softbox',
      version='0.0.1',
      description='a tool for photographer to use Screen as SoftBox.',
      author='cycleuser',
      author_email='cycleuser@cycleuser.org',
      url='http://blog.cycleuser.org',
      packages=['softbox'],
      install_requires=[ "cython",
                         "numpy",
                         "pandas",
                         "xlrd",
                         "matplotlib",
                         ],
     )
