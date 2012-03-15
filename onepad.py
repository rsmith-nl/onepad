#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright © 2012 R.F. Smith <rsmith@xs4all.nl>. All rights reserved.
# Time-stamp: <2012-03-15 23:43:13 rsmith>
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

class Key(object):

    def __init__(self, name=None, size=None):
        self.data = bytearray()
        if name:
            self.read(name)
            if len(self.data):
                return
        if size == None:
            raise ValueError('No size given when creating a Key.')
        if size < 0:
            raise ValueError("Negative size given when creating a Key.")
        self.data += os.urandom(size)

    def __len__(self):
        return len(self.data)

    def read(self, name):
        f = open(name, 'r') # Can raise IOError.
        buf = f.read().translate(None, ' \t\n').decode('base64')
        f.close()
        if len(self.data):
            del self.data
        self.data = bytearray(buf)
        del buf

    def write(self, name):
        dl = len(self.data)
        if dl == 0:
            raise IOError('Key is empty, nothing to write.')
        f = open(name, 'w+')
        segsz = 57
        for i in range(0, dl, segsz):
            f.write(str(self.data[i:i+segsz]).encode('base64'))
        f.close()

    def use(self, message):
        a = len(message)
        rv = bytearray([p^q for p,q in zip(bytearray(message),self.data)])
        if len(self.data) > a:
            self.data = self.data[a:]
        else:
            self.data = bytearray()
        return rv

# Built-in test.
if __name__ == '__main__':
    pass
