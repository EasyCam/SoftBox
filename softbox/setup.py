#!/usr/bin/env python

version="1.2"
import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


here = os.path.abspath(os.path.dirname(__file__))

README = open(os.path.join(here, 'README.md')).read()

setup(name='softbox',
      version=version,
      description='a tool for photographer to use Screen as SoftBox.',
      author='cycleuser',
      author_email='cycleuser@cycleuser.org',
      url='http://blog.cycleuser.org',
      packages=['softbox'],
      install_requires=[ 
                        "pandas",
                        "xlrd",
                        "matplotlib",
                        "pyside6",
                        "toga"
                         ],
     )
