#!/usr/bin/env python3
from setuptools import setup

setup(name='cmdtool',
      version='0.2',
      description='A very basic framework for writing command line tools',
      url='https://github.com/ConnorDillon/cmdtool',
      author='Connor Dillon',
      author_email='connor@cdillon.nl',
      license='GPLv3',
      packages=['cmdtool'],
      test_suite='cmdtool.tests',
      zip_safe=False)