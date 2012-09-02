#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright © 2012 R.F. Smith <rsmith@xs4all.nl>. All rights reserved.
# Time-stamp: <2012-08-25 15:47:18 rsmith>
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

def _readb64(name):
    '''Read data from the base64 encoded text file.

    Arguments:
    name -- name of the file to read the key from.
    '''
    with open(name, 'r') as f:
        buf = f.read().translate(None, ' \t\n').decode('base64')
    return bytearray(buf)

def _writeb64(name, data):
    '''Write data to the file name in base64 encoded text.

    Arguments:
    name -- name of the file to open
    data -- string of data to write.
    '''
    dl = len(data)
    if dl == 0:
        raise ValueError('Nothing to write.')
    segsz = 57
    with open(name, 'w+') as f:
        for i in range(0, dl, segsz):
            f.write(str(data[i:i+segsz]).encode('base64'))

class Key(object):

    def __init__(self, arg):
        '''Create a key. Key creation can happen in three ways.
        (1) Create a random key by giving an integer argument.
        (2) Read a key from a file by using a string argument.
        (3) Copy an existing key by using an existing key argument.

        Arguments:
        arg -- integer size in bytes of the random key to create
            -- or name of the file to read the file from
            -- or existing key to copy
        '''
        if isinstance(arg, int):
            if arg < 0:
                raise ValueError("Negative size given when creating a Key.")
            self.data = bytearray(os.urandom(arg))
            return
        if isinstance(arg, str):
            self.data = _readb64(arg)
            return
        if isinstance(arg, Key):
            self.data = arg.data[:]
        else:
            raise ValueError('The object to copy is not a Key.')

    def __len__(self):
        return len(self.data)

    def write(self, name):
        '''Write the key to a file in base64 encoding.

        Arguments:
        name -- name of the file to create
        '''
        _writeb64(name, self.data)

    def crypt(self, message):
        '''Encrypt or decrypt a message.

        Arguments:
        message -- string to encrypt or decrypt.
        '''
        a = len(message)
        if len(self.data) > a:
            rv = bytearray([p^q for p,q in zip(bytearray(message),
                                               self.data)])
            self.data = self.data[a:]
            return rv
        else:
            raise ValueError('Not enough key length to crypt the message.')

# Built-in test.
if __name__ == '__main__':
#    from copy import deepcopy
    k = Key(1024)
    p = Key(k)
    test = 'This is a test.'
    print 'plaintext "{}"'.format(test)
    ciphertext = k.crypt(test)
    pc = str(ciphertext).encode('base64')[:-1]
    print 'ciphertext (base64) "{}"'.format(pc)
    copy  =  str(p.crypt(ciphertext))
    if copy == test:
        print "It works!"
    else:
        print 'original: "{}"'.format(test)
        print 'crypted: "{}"'.format(copy)

