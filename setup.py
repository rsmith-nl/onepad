# file: setup.py
# vim:fileencoding=utf-8:ft=python
# Installation script for onepad.
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# Created: 2015-05-17 01:44:59 +0200
# Last modified: 2015-05-17 12:07:05 +0200

from setuptools import setup
import os

with open('README.rst') as f:
    ld = f.read()

# Remove the extensions from the scripts for UNIX-like systems.
_scripts = ['onepad.py', 'genpad.py']
outnames = [s[:-3] for s in _scripts]
if os.name is 'posix':
    try:
        for old, new in zip(_scripts, outnames):
            os.link(old, new)
    except OSError:
        pass
    _scripts = outnames

name = 'onepad'
setup(
    name=name,
    version='1.0',
    description='Program for one-time pad encryption',
    author='Roland Smith',
    author_email='rsmith@xs4all.nl',
    url='http://www.xs4all.nl/~rsmith/software/',
    scripts=_scripts,
    provides=[name],
    classifiers=[
        'Development Status :: 4 - Beta', 'Environment :: Console', 'Natural Language :: English',
        'License :: OSI Approved :: BSD License', 'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4', 'Topic :: Security :: Cryptography'
    ],
    long_description=ld
)

if os.name is 'posix':
    for nm in outnames:
        os.remove(nm)
