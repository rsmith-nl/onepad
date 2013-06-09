# -*- coding: utf-8 -*-
# Installation script for onepad.
# R.F. Smith <rsmith@xs4all.nl>
# $Date$

from distutils.core import setup

with open('README.rst') as f:
    ld = f.read()

name = 'onepad'
setup(name=name,
      version='$Revision$'[11:-2],
      description='Program for one-time pad ecnryption',
      author='Roland Smith',
      author_email='rsmith@xs4all.nl',
      url='http://www.xs4all.nl/~rsmith/software/',
      scripts=['onepad.py', 'genpad.py'],
      provides=[name],
      classifiers=['Development Status :: 4 - Beta',
                   'Environment :: Console',
                   'Natural Language :: English',
                   'Intended Audience :: Other Audience',
                   'License :: Public Domain',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python :: 3.3',
                   'Topic :: Security :: Cryptography'
                   ],
      long_description = ld
      )
