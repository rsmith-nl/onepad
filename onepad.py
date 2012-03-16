#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright © 2012 R.F. Smith <rsmith@xs4all.nl>. All rights reserved.
# Time-stamp: <2012-03-16 23:12:17 rsmith>
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY AUTHOR AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

"Module for handling one-time-pad keys"

import os

def readb64(name):
    '''Read data from the base64 encoded text file 'name'.'''
    f = open(name, 'r') # Can raise IOError.
    buf = f.read().translate(None, ' \t\n').decode('base64')
    f.close()
    return bytearray(buf)

def writeb64(name, data):
    '''Write 'data' to the file 'name' in base64 encoded text.'''
    dl = len(data)
    if dl == 0:
        raise IOError('Nothing to write.')
    f = open(name, 'w+')
    segsz = 57
    for i in range(0, dl, segsz):
        f.write(str(data[i:i+segsz]).encode('base64'))
    f.close()
    

class Key(object):

    def __init__(self, name=None, size=None):
        '''Read a key from a file 'name', or create a new one from os.urandom
        that is 'size' bytes long.'''
        self.data = bytearray()
        if name:
            self.date = readb64(name)
            if len(self.data):
                return
        if size == None:
            raise ValueError('No size given when creating a Key.')
        if size < 0:
            raise ValueError("Negative size given when creating a Key.")
        self.data += os.urandom(size)

    def __len__(self):
        return len(self.data)

    def write(self, name):
        '''Write the key to a file 'name' in base64 encoding.'''
        writeb64(name, self.data)

    def crypt(self, message):
        '''Encrypt or decrypt 'message'.'''
        a = len(message)
        rv = bytearray([p^q for p,q in zip(bytearray(message),self.data)])
        if len(self.data) > a:
            self.data = self.data[a:]
        else:
            self.data = bytearray()
        return rv


# Built-in test.
if __name__ == '__main__':
    from copy import deepcopy
    k = Key(None, 1024)
    p = deepcopy(k)
    test = 'This is a test.'
    ciphertext = k.crypt(test)
    copy  =  str(p.crypt(ciphertext))
    if copy == test:
        print "It works!"
    else:
        print 'original: "{}"'.format(test)
        print 'crypted: "{}"'.format(copy)

