# -*- coding: utf-8 -*-
# Installation script for PROG
#
# R.F. Smith <rsmith@xs4all.nl>
# Time-stamp: <>

from distutils.core import setup

with open('README.txt') as file:
    ld = file.read()


setup(name='PROG',
      version='VERSION',
      license='BSD',
      description='Missing!',
      author='Roland Smith', author_email='rsmith@xs4all.nl',
      url='http://www.xs4all.nl/~rsmith/software/',
      scripts=['PROG.py'],
      provides='PROG', py_modules=['FOO','BAR'],
      classifiers=['Development Status :: 5 - Production/Stable',
                   'Environment :: Console',
                   'Intended Audience :: End Users/Desktop',
                   'Intended Audience :: Manufacturing',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python :: 2.7',
                   'Topic :: Scientific/Engineering'
                   ],
      long_description = ld
      )
